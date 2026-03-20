#!/usr/bin/env python3
"""Applies executable retention policies for the mini-platform."""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import psycopg2
from clickhouse_driver import Client as ClickHouseClient
from minio import Minio

MINI_PLATFORM_ROOT = Path(__file__).resolve().parents[1]
SHARED_ROOT = MINI_PLATFORM_ROOT / "shared"
if str(SHARED_ROOT) not in sys.path:
    sys.path.insert(0, str(SHARED_ROOT))

from mini_platform.ops import RetentionCutoffs, filter_expired_minio_objects


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    return int(raw) if raw is not None else default


def build_cutoffs(now: datetime) -> RetentionCutoffs:
    return RetentionCutoffs(
        ingest_log_before=now - timedelta(days=_env_int("RETENTION_INGEST_LOG_DAYS", 30)),
        event_processing_before=now - timedelta(days=_env_int("RETENTION_EVENT_PROCESSING_DAYS", 30)),
        dlq_before=now - timedelta(days=_env_int("RETENTION_DLQ_DAYS", 30)),
        replay_before=now - timedelta(days=_env_int("RETENTION_REPLAY_JOBS_DAYS", 30)),
        audit_before=now - timedelta(days=_env_int("RETENTION_AUDIT_LOG_DAYS", 90)),
        ingest_rejections_before=now - timedelta(days=_env_int("RETENTION_INGEST_REJECTIONS_DAYS", 30)),
        minio_before=(now - timedelta(days=_env_int("RETENTION_MINIO_RAW_DAYS", 30))).date(),
        clickhouse_before=(now - timedelta(days=_env_int("RETENTION_CLICKHOUSE_DAYS", 30))).date(),
    )


def apply_postgres_retention(pg_conn, cutoffs: RetentionCutoffs, now: datetime) -> dict[str, int]:
    summary: dict[str, int] = {}
    with pg_conn.cursor() as cur:
        cur.execute(
            """
            SELECT event_id
            FROM event_processing
            WHERE status IN ('claimed', 'storage_written', 'analytics_written')
            """
        )
        active_event_ids = [row[0] for row in cur.fetchall()]

        cur.execute(
            """
            DELETE FROM ingest_log
            WHERE received_at < %s
              AND NOT (event_id = ANY(%s))
            """,
            (cutoffs.ingest_log_before, active_event_ids),
        )
        summary["ingest_log_deleted"] = cur.rowcount

        cur.execute(
            """
            DELETE FROM event_processing
            WHERE updated_at < %s
              AND status NOT IN ('claimed', 'storage_written', 'analytics_written')
            """,
            (cutoffs.event_processing_before,),
        )
        summary["event_processing_deleted"] = cur.rowcount

        cur.execute("DELETE FROM dlq_events WHERE failed_at < %s", (cutoffs.dlq_before,))
        summary["dlq_deleted"] = cur.rowcount

        cur.execute(
            """
            DELETE FROM replay_job_events
            WHERE replay_job_id IN (
                SELECT replay_job_id
                FROM replay_jobs
                WHERE updated_at < %s
                  AND status IN ('completed', 'failed', 'cancelled', 'timed_out')
            )
            """,
            (cutoffs.replay_before,),
        )
        summary["replay_job_events_deleted"] = cur.rowcount

        cur.execute(
            """
            DELETE FROM replay_jobs
            WHERE updated_at < %s
              AND status IN ('completed', 'failed', 'cancelled', 'timed_out')
            """,
            (cutoffs.replay_before,),
        )
        summary["replay_jobs_deleted"] = cur.rowcount

        cur.execute("DELETE FROM operator_audit_log WHERE created_at < %s", (cutoffs.audit_before,))
        summary["audit_log_deleted"] = cur.rowcount

        cur.execute("DELETE FROM ingest_rejections WHERE rejected_at < %s", (cutoffs.ingest_rejections_before,))
        summary["ingest_rejections_deleted"] = cur.rowcount

        cur.execute(
            """
            INSERT INTO operator_audit_log (action, actor, target_type, target_id, metadata, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                "retention_applied",
                "retention-script",
                "retention",
                now.isoformat(),
                json.dumps(
                    {
                        "cutoffs": {
                            "ingest_log_before": cutoffs.ingest_log_before.isoformat(),
                            "event_processing_before": cutoffs.event_processing_before.isoformat(),
                            "dlq_before": cutoffs.dlq_before.isoformat(),
                            "replay_before": cutoffs.replay_before.isoformat(),
                            "audit_before": cutoffs.audit_before.isoformat(),
                            "ingest_rejections_before": cutoffs.ingest_rejections_before.isoformat(),
                            "minio_before": cutoffs.minio_before.isoformat(),
                            "clickhouse_before": cutoffs.clickhouse_before.isoformat(),
                        },
                        "summary": summary,
                    }
                ),
                now,
            ),
        )
    return summary


def apply_minio_retention(minio_client: Minio, bucket: str, cutoffs: RetentionCutoffs) -> dict[str, int]:
    object_names = [item.object_name for item in minio_client.list_objects(bucket, recursive=True)]
    expired = filter_expired_minio_objects(object_names, cutoffs.minio_before)
    for object_name in expired:
        minio_client.remove_object(bucket, object_name)
    return {"minio_objects_deleted": len(expired)}


def apply_clickhouse_retention(client: ClickHouseClient, database: str, cutoffs: RetentionCutoffs) -> dict[str, str]:
    client.execute(
        f"ALTER TABLE {database}.events DELETE WHERE event_date < %(cutoff)s",
        {"cutoff": cutoffs.clickhouse_before.isoformat()},
    )
    return {"clickhouse_delete_before": cutoffs.clickhouse_before.isoformat()}


def main() -> None:
    now = _utc_now()
    cutoffs = build_cutoffs(now)

    pg_conn = psycopg2.connect(os.environ["POSTGRES_DSN"])
    pg_conn.autocommit = True
    minio_client = Minio(
        os.environ["MINIO_ENDPOINT"],
        access_key=os.environ["MINIO_ACCESS_KEY"],
        secret_key=os.environ["MINIO_SECRET_KEY"],
        secure=os.getenv("MINIO_SECURE", "false").lower() == "true",
    )
    clickhouse = ClickHouseClient(
        host=os.environ["CLICKHOUSE_HOST"],
        port=int(os.getenv("CLICKHOUSE_PORT", "9000")),
    )

    summary = {"applied_at": now.isoformat()}
    summary.update(apply_postgres_retention(pg_conn, cutoffs, now))
    summary.update(apply_minio_retention(minio_client, os.getenv("MINIO_BUCKET", "events"), cutoffs))
    summary.update(apply_clickhouse_retention(clickhouse, os.getenv("CLICKHOUSE_DATABASE", "analytics"), cutoffs))
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
