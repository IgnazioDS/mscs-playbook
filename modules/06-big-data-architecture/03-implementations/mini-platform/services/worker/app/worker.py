"""Worker that consumes events with resumable state tracking."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from io import BytesIO
from typing import Any, Dict, Literal

import psycopg2
from clickhouse_driver import Client as ClickHouseClient
from kafka import KafkaConsumer, KafkaProducer
from minio import Minio
from minio.error import S3Error

from app.config import WorkerSettings
from app.logging_utils import configure_json_logger


ProcessingResult = Literal["processed", "skipped"]
IN_PROGRESS_STATES = ("claimed", "storage_written", "analytics_written")


@dataclass(frozen=True)
class ProcessingState:
    event_id: str
    status: str
    claimed_at: datetime | None
    lease_expires_at: datetime | None
    updated_at: datetime
    storage_written_at: datetime | None
    analytics_written_at: datetime | None
    completed_at: datetime | None
    failed_at: datetime | None
    last_error: str | None
    attempt_count: int


@dataclass(frozen=True)
class ClaimResult:
    acquired: bool
    state: ProcessingState | None


def _parse_time(value: str) -> datetime:
    if value.endswith("Z"):
        value = value.replace("Z", "+00:00")
    return datetime.fromisoformat(value)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _connect_postgres(dsn: str) -> psycopg2.extensions.connection:
    conn = psycopg2.connect(dsn)
    conn.autocommit = True
    return conn


def _ensure_bucket(client: Minio, bucket: str) -> None:
    if not client.bucket_exists(bucket):
        client.make_bucket(bucket)


def _write_minio(client: Minio, bucket: str, object_name: str, payload: bytes) -> None:
    client.put_object(
        bucket,
        object_name,
        data=BytesIO(payload),
        length=len(payload),
        content_type="application/json",
    )


def _storage_object_exists(client: Minio, bucket: str, object_name: str) -> bool:
    try:
        client.stat_object(bucket, object_name)
        return True
    except S3Error as exc:
        if exc.code in {"NoSuchKey", "NoSuchObject", "NoSuchBucket"}:
            return False
        raise


def _insert_clickhouse(client: ClickHouseClient, database: str, row: Dict[str, Any]) -> None:
    client.execute(
        f"INSERT INTO {database}.events (event_date, event_time, received_at, event_id, event_type, schema_version, payload) VALUES",
        [
            (
                row["event_date"],
                row["event_time"],
                row["received_at"],
                row["event_id"],
                row["event_type"],
                row["schema_version"],
                row["payload"],
            )
        ],
    )


def _clickhouse_event_exists(client: ClickHouseClient, database: str, event_id: str) -> bool:
    rows = client.execute(
        f"SELECT count() FROM {database}.events WHERE event_id = %(event_id)s",
        {"event_id": event_id},
    )
    return rows[0][0] > 0


def _with_retries(func, max_retries: int = 3, base_sleep: float = 0.5) -> None:
    for attempt in range(max_retries):
        try:
            func()
            return
        except Exception:
            if attempt == max_retries - 1:
                raise
            time.sleep(base_sleep * (2 ** attempt))


def _row_to_state(row: tuple | None) -> ProcessingState | None:
    if row is None:
        return None
    return ProcessingState(
        event_id=row[0],
        status=row[1],
        claimed_at=row[2],
        lease_expires_at=row[3],
        updated_at=row[4],
        storage_written_at=row[5],
        analytics_written_at=row[6],
        completed_at=row[7],
        failed_at=row[8],
        last_error=row[9],
        attempt_count=row[10],
    )


def _claim_or_resume_event(
    pg_conn: psycopg2.extensions.connection,
    event_id: str,
    now: datetime,
    lease_timeout: timedelta,
) -> ClaimResult:
    lease_expires_at = now + lease_timeout
    with pg_conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO event_processing (
                event_id,
                status,
                claimed_at,
                lease_expires_at,
                updated_at,
                attempt_count
            )
            VALUES (%s, 'claimed', %s, %s, %s, 1)
            ON CONFLICT DO NOTHING
            RETURNING
                event_id,
                status,
                claimed_at,
                lease_expires_at,
                updated_at,
                storage_written_at,
                analytics_written_at,
                completed_at,
                failed_at,
                last_error,
                attempt_count
            """,
            (event_id, now, lease_expires_at, now),
        )
        row = cur.fetchone()
        if row is not None:
            return ClaimResult(acquired=True, state=_row_to_state(row))

        cur.execute(
            """
            UPDATE event_processing
            SET status = 'claimed',
                claimed_at = %s,
                lease_expires_at = %s,
                updated_at = %s,
                failed_at = NULL,
                last_error = NULL,
                attempt_count = attempt_count + 1
            WHERE event_id = %s
              AND (
                  status = 'failed'
                  OR (status IN ('claimed', 'storage_written', 'analytics_written') AND lease_expires_at < %s)
              )
            RETURNING
                event_id,
                status,
                claimed_at,
                lease_expires_at,
                updated_at,
                storage_written_at,
                analytics_written_at,
                completed_at,
                failed_at,
                last_error,
                attempt_count
            """,
            (now, lease_expires_at, now, event_id, now),
        )
        row = cur.fetchone()
        if row is not None:
            return ClaimResult(acquired=True, state=_row_to_state(row))

        cur.execute(
            """
            SELECT
                event_id,
                status,
                claimed_at,
                lease_expires_at,
                updated_at,
                storage_written_at,
                analytics_written_at,
                completed_at,
                failed_at,
                last_error,
                attempt_count
            FROM event_processing
            WHERE event_id = %s
            """,
            (event_id,),
        )
        return ClaimResult(acquired=False, state=_row_to_state(cur.fetchone()))


def _mark_storage_written(
    pg_conn: psycopg2.extensions.connection,
    event_id: str,
    now: datetime,
    lease_timeout: timedelta,
) -> ProcessingState:
    with pg_conn.cursor() as cur:
        cur.execute(
            """
            UPDATE event_processing
            SET status = 'storage_written',
                storage_written_at = COALESCE(storage_written_at, %s),
                updated_at = %s,
                lease_expires_at = %s,
                failed_at = NULL,
                last_error = NULL
            WHERE event_id = %s
            RETURNING
                event_id,
                status,
                claimed_at,
                lease_expires_at,
                updated_at,
                storage_written_at,
                analytics_written_at,
                completed_at,
                failed_at,
                last_error,
                attempt_count
            """,
            (now, now, now + lease_timeout, event_id),
        )
        return _row_to_state(cur.fetchone())


def _mark_analytics_written(
    pg_conn: psycopg2.extensions.connection,
    event_id: str,
    now: datetime,
    lease_timeout: timedelta,
) -> ProcessingState:
    with pg_conn.cursor() as cur:
        cur.execute(
            """
            UPDATE event_processing
            SET status = 'analytics_written',
                analytics_written_at = COALESCE(analytics_written_at, %s),
                updated_at = %s,
                lease_expires_at = %s,
                failed_at = NULL,
                last_error = NULL
            WHERE event_id = %s
            RETURNING
                event_id,
                status,
                claimed_at,
                lease_expires_at,
                updated_at,
                storage_written_at,
                analytics_written_at,
                completed_at,
                failed_at,
                last_error,
                attempt_count
            """,
            (now, now, now + lease_timeout, event_id),
        )
        return _row_to_state(cur.fetchone())


def _mark_event_completed(
    pg_conn: psycopg2.extensions.connection,
    event_id: str,
    now: datetime,
) -> ProcessingState:
    with pg_conn.cursor() as cur:
        cur.execute(
            """
            WITH updated AS (
                UPDATE event_processing
                SET status = 'completed',
                    updated_at = %s,
                    completed_at = COALESCE(completed_at, %s),
                    failed_at = NULL,
                    last_error = NULL
                WHERE event_id = %s
                RETURNING
                    event_id,
                    status,
                    claimed_at,
                    lease_expires_at,
                    updated_at,
                    storage_written_at,
                    analytics_written_at,
                    completed_at,
                    failed_at,
                    last_error,
                    attempt_count
            ),
            inserted AS (
                INSERT INTO processed_events (event_id, processed_at)
                SELECT event_id, %s FROM updated
                ON CONFLICT DO NOTHING
                RETURNING event_id
            )
            SELECT
                event_id,
                status,
                claimed_at,
                lease_expires_at,
                updated_at,
                storage_written_at,
                analytics_written_at,
                completed_at,
                failed_at,
                last_error,
                attempt_count
            FROM updated
            """,
            (now, now, event_id, now),
        )
        return _row_to_state(cur.fetchone())


def _mark_event_failed(
    pg_conn: psycopg2.extensions.connection,
    event_id: str,
    error: str,
    now: datetime,
) -> ProcessingState:
    with pg_conn.cursor() as cur:
        cur.execute(
            """
            UPDATE event_processing
            SET status = 'failed',
                updated_at = %s,
                failed_at = %s,
                lease_expires_at = %s,
                last_error = %s
            WHERE event_id = %s
            RETURNING
                event_id,
                status,
                claimed_at,
                lease_expires_at,
                updated_at,
                storage_written_at,
                analytics_written_at,
                completed_at,
                failed_at,
                last_error,
                attempt_count
            """,
            (now, now, now, error, event_id),
        )
        return _row_to_state(cur.fetchone())


def _count_stale_claims(pg_conn: psycopg2.extensions.connection, now: datetime) -> int:
    with pg_conn.cursor() as cur:
        cur.execute(
            """
            SELECT COUNT(*)
            FROM event_processing
            WHERE status IN ('claimed', 'storage_written', 'analytics_written')
              AND lease_expires_at < %s
            """,
            (now,),
        )
        return cur.fetchone()[0]


def process_event(
    event: Dict[str, Any],
    settings: WorkerSettings,
    pg_conn: psycopg2.extensions.connection,
    minio_client: Minio,
    ch_client: ClickHouseClient,
    logger,
) -> ProcessingResult:
    event_id = str(event.get("event_id", ""))
    if not event_id:
        logger.warning(
            "event skipped because event_id is missing",
            extra={"component": "worker", "processing_state": "skipped"},
        )
        return "skipped"

    now = _utc_now()
    claim = _claim_or_resume_event(pg_conn, event_id, now, settings.lease_timeout)
    if claim.state is None:
        logger.warning(
            "event skipped because processing state is unavailable",
            extra={"component": "worker", "event_id": event_id, "processing_state": "skipped"},
        )
        return "skipped"

    state = claim.state
    if not claim.acquired:
        logger.info(
            "event skipped because another terminal or active state already exists",
            extra={
                "component": "worker",
                "event_id": event_id,
                "processing_state": state.status,
            },
        )
        return "skipped"

    logger.info(
        "event claimed for processing",
        extra={
            "component": "worker",
            "event_id": event_id,
            "processing_state": state.status,
            "lease_seconds": settings.lease_seconds,
        },
    )

    event_time_raw = event.get("event_time") or event.get("received_at")
    event_time = _parse_time(event_time_raw)
    received_at = _parse_time(event.get("received_at"))
    event_type = str(event.get("event_type", "unknown"))
    schema_version = int(event.get("schema_version", 1))
    payload = json.dumps(event).encode("utf-8")
    object_name = f"raw/{event_time.date().isoformat()}/{event_id}.json"
    clickhouse_row = {
        "event_date": event_time.date(),
        "event_time": event_time,
        "received_at": received_at,
        "event_id": event_id,
        "event_type": event_type,
        "schema_version": schema_version,
        "payload": payload.decode("utf-8"),
    }

    try:
        if state.storage_written_at is None:
            if _storage_object_exists(minio_client, settings.minio_bucket, object_name):
                state = _mark_storage_written(pg_conn, event_id, _utc_now(), settings.lease_timeout)
                logger.info(
                    "storage write recovered from existing object",
                    extra={
                        "component": "worker",
                        "event_id": event_id,
                        "processing_state": state.status,
                    },
                )
            else:
                _with_retries(
                    lambda: _write_minio(minio_client, settings.minio_bucket, object_name, payload)
                )
                state = _mark_storage_written(pg_conn, event_id, _utc_now(), settings.lease_timeout)
                logger.info(
                    "storage written",
                    extra={
                        "component": "worker",
                        "event_id": event_id,
                        "processing_state": state.status,
                    },
                )

        if state.analytics_written_at is None:
            if _clickhouse_event_exists(ch_client, settings.clickhouse_database, event_id):
                state = _mark_analytics_written(pg_conn, event_id, _utc_now(), settings.lease_timeout)
                logger.info(
                    "analytics write recovered from existing row",
                    extra={
                        "component": "worker",
                        "event_id": event_id,
                        "processing_state": state.status,
                    },
                )
            else:
                _insert_clickhouse(ch_client, settings.clickhouse_database, clickhouse_row)
                state = _mark_analytics_written(pg_conn, event_id, _utc_now(), settings.lease_timeout)
                logger.info(
                    "analytics written",
                    extra={
                        "component": "worker",
                        "event_id": event_id,
                        "processing_state": state.status,
                        "schema_version": schema_version,
                    },
                )

        state = _mark_event_completed(pg_conn, event_id, _utc_now())
        logger.info(
            "event processing completed",
            extra={
                "component": "worker",
                "event_id": event_id,
                "processing_state": state.status,
            },
        )
        return "processed"
    except Exception as exc:
        failed_state = _mark_event_failed(pg_conn, event_id, str(exc), _utc_now())
        logger.error(
            "event processing failed",
            extra={
                "component": "worker",
                "event_id": event_id,
                "processing_state": failed_state.status if failed_state else "failed",
                "detail": str(exc),
            },
            exc_info=True,
        )
        raise


def main() -> None:
    settings = WorkerSettings.from_env()
    logger = configure_json_logger(settings.service_name, settings.log_level)

    producer = KafkaProducer(
        bootstrap_servers=settings.kafka_bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    consumer = KafkaConsumer(
        settings.kafka_topic,
        bootstrap_servers=settings.kafka_bootstrap_servers,
        group_id=settings.kafka_group_id,
        enable_auto_commit=False,
        auto_offset_reset="earliest",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    )

    pg_conn = _connect_postgres(settings.postgres_dsn)
    minio_client = Minio(
        settings.minio_endpoint,
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        secure=settings.minio_secure,
    )
    _ensure_bucket(minio_client, settings.minio_bucket)
    ch_client = ClickHouseClient(host=settings.clickhouse_host, port=settings.clickhouse_port)

    logger.info(
        "worker startup complete",
        extra={
            "component": "worker",
            "processing_state": "startup",
            "lease_seconds": settings.lease_seconds,
            "detail": f"stale_claims={_count_stale_claims(pg_conn, _utc_now())}",
        },
    )

    for message in consumer:
        event = message.value
        event_id = str(event.get("event_id", ""))
        if not event_id:
            consumer.commit()
            continue

        try:
            process_event(event, settings, pg_conn, minio_client, ch_client, logger)
            consumer.commit()
        except Exception as exc:
            error_payload = {
                "event_id": event_id,
                "error": str(exc),
                "payload": event,
                "failed_at": _utc_now().isoformat(),
            }
            producer.send(settings.kafka_dlq_topic, error_payload)
            producer.flush(2)
            with pg_conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO dlq_events (event_id, error, payload, failed_at) VALUES (%s, %s, %s, %s)",
                    (event_id, str(exc), json.dumps(event), _utc_now()),
                )
            consumer.commit()


if __name__ == "__main__":
    main()
