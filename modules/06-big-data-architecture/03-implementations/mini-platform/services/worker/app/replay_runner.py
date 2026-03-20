"""Replay and redrive runner for durable operator jobs."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import uuid4

from kafka import KafkaProducer

from app.config import WorkerSettings
from app.logging_utils import configure_json_logger
from app.worker import ClaimLostError, IN_PROGRESS_STATES, _connect_postgres, _row_to_state, _utc_now


@dataclass(frozen=True)
class ReplayJob:
    replay_job_id: str
    job_type: str
    selector_type: str
    selector: dict[str, Any]
    source_type: str
    status: str
    requested_by: str
    requested_at: datetime
    started_at: datetime | None
    completed_at: datetime | None
    failed_at: datetime | None
    updated_at: datetime
    lease_expires_at: datetime | None
    heartbeat_at: datetime | None
    cancel_requested_at: datetime | None
    cancelled_at: datetime | None
    deadline_at: datetime | None
    timed_out_at: datetime | None
    terminal_reason: str | None
    terminal_detail: str | None
    attempt_count: int
    total_events: int
    published_events: int
    completed_events: int
    failed_events: int
    skipped_events: int
    last_error: str | None
    owner_token: str | None
    lease_generation: int


@dataclass(frozen=True)
class ReplayJobEvent:
    replay_job_id: str
    event_id: str
    source_type: str
    source_row_id: int | None
    event_payload: dict[str, Any]
    status: str
    published_at: datetime | None
    completed_at: datetime | None
    failed_at: datetime | None
    updated_at: datetime
    last_error: str | None
    last_observed_processing_status: str | None


def _normalize_json(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return value
    return json.loads(value)


def _make_producer(bootstrap_servers: str) -> KafkaProducer:
    return KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )


def _row_to_replay_job(row: tuple | None) -> ReplayJob | None:
    if row is None:
        return None
    return ReplayJob(
        replay_job_id=row[0],
        job_type=row[1],
        selector_type=row[2],
        selector=_normalize_json(row[3]),
        source_type=row[4],
        status=row[5],
        requested_by=row[6],
        requested_at=row[7],
        started_at=row[8],
        completed_at=row[9],
        failed_at=row[10],
        updated_at=row[11],
        lease_expires_at=row[12],
        heartbeat_at=row[13],
        cancel_requested_at=row[14],
        cancelled_at=row[15],
        deadline_at=row[16],
        timed_out_at=row[17],
        terminal_reason=row[18],
        terminal_detail=row[19],
        attempt_count=row[20],
        total_events=row[21],
        published_events=row[22],
        completed_events=row[23],
        failed_events=row[24],
        skipped_events=row[25],
        last_error=row[26],
        owner_token=row[27],
        lease_generation=row[28],
    )


def _row_to_replay_job_event(row: tuple) -> ReplayJobEvent:
    return ReplayJobEvent(
        replay_job_id=row[0],
        event_id=row[1],
        source_type=row[2],
        source_row_id=row[3],
        event_payload=_normalize_json(row[4]),
        status=row[5],
        published_at=row[6],
        completed_at=row[7],
        failed_at=row[8],
        updated_at=row[9],
        last_error=row[10],
        last_observed_processing_status=row[11],
    )


def _record_audit(
    pg_conn,
    *,
    action: str,
    actor: str,
    target_type: str,
    target_id: str,
    metadata: dict[str, Any],
    created_at: datetime,
) -> None:
    with pg_conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO operator_audit_log (action, actor, target_type, target_id, metadata, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (action, actor, target_type, target_id, json.dumps(metadata), created_at),
        )


def _claim_next_replay_job(
    pg_conn,
    now: datetime,
    lease_timeout,
    owner_token: str | None = None,
) -> ReplayJob | None:
    claim_owner_token = owner_token or f"replay-runner-{uuid4()}"
    with pg_conn.cursor() as cur:
        cur.execute(
            """
            SELECT replay_job_id
            FROM replay_jobs
            WHERE (
                (status = 'requested' AND cancel_requested_at IS NULL)
                OR (status = 'running' AND lease_expires_at < %s)
            )
              AND (deadline_at IS NULL OR deadline_at >= %s)
            ORDER BY requested_at
            LIMIT 1
            """,
            (now, now),
        )
        candidate = cur.fetchone()
        if candidate is None:
            return None

        cur.execute(
            """
            UPDATE replay_jobs
            SET status = 'running',
                started_at = COALESCE(started_at, %s),
                updated_at = %s,
                lease_expires_at = %s,
                heartbeat_at = %s,
                attempt_count = attempt_count + 1,
                failed_at = NULL,
                timed_out_at = NULL,
                cancelled_at = NULL,
                last_error = NULL,
                owner_token = %s,
                lease_generation = lease_generation + 1
            WHERE replay_job_id = %s
              AND (
                  (status = 'requested' AND cancel_requested_at IS NULL)
                  OR (status = 'running' AND lease_expires_at < %s)
              )
            RETURNING
                replay_job_id,
                job_type,
                selector_type,
                selector,
                source_type,
                status,
                requested_by,
                requested_at,
                started_at,
                completed_at,
                failed_at,
                updated_at,
                lease_expires_at,
                heartbeat_at,
                cancel_requested_at,
                cancelled_at,
                deadline_at,
                timed_out_at,
                terminal_reason,
                terminal_detail,
                attempt_count,
                total_events,
                published_events,
                completed_events,
                failed_events,
                skipped_events,
                last_error,
                owner_token,
                lease_generation
            """,
            (
                now,
                now,
                now + lease_timeout,
                now,
                claim_owner_token,
                candidate[0],
                now,
            ),
        )
        return _row_to_replay_job(cur.fetchone())


def _require_owned_job(job: ReplayJob | None, replay_job_id: str) -> ReplayJob:
    if job is None:
        raise ClaimLostError(f"claim lost for replay job {replay_job_id}")
    return job


def _load_processing_state(pg_conn, event_id: str):
    with pg_conn.cursor() as cur:
        cur.execute(
            """
            SELECT
                event_id,
                status,
                claimed_at,
                lease_expires_at,
                heartbeat_at,
                updated_at,
                storage_written_at,
                analytics_written_at,
                completed_at,
                failed_at,
                last_error,
                attempt_count,
                owner_token,
                lease_generation
            FROM event_processing
            WHERE event_id = %s
            """,
            (event_id,),
        )
        return _row_to_state(cur.fetchone())


def _load_replay_job_events(pg_conn, replay_job_id: str) -> list[ReplayJobEvent]:
    with pg_conn.cursor() as cur:
        cur.execute(
            """
            SELECT
                replay_job_id,
                event_id,
                source_type,
                source_row_id,
                event_payload,
                status,
                published_at,
                completed_at,
                failed_at,
                updated_at,
                last_error,
                last_observed_processing_status
            FROM replay_job_events
            WHERE replay_job_id = %s
            ORDER BY event_id
            """,
            (replay_job_id,),
        )
        return [_row_to_replay_job_event(row) for row in cur.fetchall()]


def _load_replay_job(pg_conn, replay_job_id: str) -> ReplayJob | None:
    with pg_conn.cursor() as cur:
        cur.execute(
            """
            SELECT
                replay_job_id,
                job_type,
                selector_type,
                selector,
                source_type,
                status,
                requested_by,
                requested_at,
                started_at,
                completed_at,
                failed_at,
                updated_at,
                lease_expires_at,
                heartbeat_at,
                cancel_requested_at,
                cancelled_at,
                deadline_at,
                timed_out_at,
                terminal_reason,
                terminal_detail,
                attempt_count,
                total_events,
                published_events,
                completed_events,
                failed_events,
                skipped_events,
                last_error,
                owner_token,
                lease_generation
            FROM replay_jobs
            WHERE replay_job_id = %s
            """,
            (replay_job_id,),
        )
        return _row_to_replay_job(cur.fetchone())


def _load_source_rows(pg_conn, job: ReplayJob) -> list[tuple[int, str, dict[str, Any], str]]:
    with pg_conn.cursor() as cur:
        if job.selector_type == "event_id":
            cur.execute(
                """
                SELECT id, event_id, payload
                FROM ingest_log
                WHERE event_id = %s
                """,
                (job.selector["event_id"],),
            )
            rows = cur.fetchall()
            return [(row[0], row[1], _normalize_json(row[2]), "ingest_log") for row in rows]

        if job.selector_type == "time_range":
            cur.execute(
                """
                SELECT id, event_id, payload
                FROM ingest_log
                WHERE event_time >= %s
                  AND event_time <= %s
                ORDER BY event_time, event_id
                """,
                (job.selector["start_time"], job.selector["end_time"]),
            )
            rows = cur.fetchall()
            return [(row[0], row[1], _normalize_json(row[2]), "ingest_log") for row in rows]

        cur.execute(
            """
            SELECT id, event_id, payload
            FROM dlq_events
            WHERE id = %s
            """,
            (job.selector["dlq_event_id"],),
        )
        rows = cur.fetchall()
        return [(row[0], row[1], _normalize_json(row[2]), "dlq_events") for row in rows]


def _materialize_replay_job_events(pg_conn, job: ReplayJob, now: datetime) -> list[ReplayJobEvent]:
    with pg_conn.cursor() as cur:
        cur.execute(
            """
            SELECT COUNT(*)
            FROM replay_job_events
            WHERE replay_job_id = %s
            """,
            (job.replay_job_id,),
        )
        existing_count = cur.fetchone()[0]

    if existing_count > 0:
        return _load_replay_job_events(pg_conn, job.replay_job_id)

    source_rows = _load_source_rows(pg_conn, job)
    if not source_rows:
        raise ValueError("replay selector did not match any source events")

    with pg_conn.cursor() as cur:
        for source_row_id, event_id, payload, source_type in source_rows:
            cur.execute(
                """
                INSERT INTO replay_job_events (
                    replay_job_id,
                    event_id,
                    source_type,
                    source_row_id,
                    event_payload,
                    status,
                    updated_at
                )
                VALUES (%s, %s, %s, %s, %s, 'pending', %s)
                ON CONFLICT DO NOTHING
                """,
                (
                    job.replay_job_id,
                    event_id,
                    source_type,
                    source_row_id,
                    json.dumps(payload),
                    now,
                ),
            )

    _update_replay_job_counts(pg_conn, job, now)
    return _load_replay_job_events(pg_conn, job.replay_job_id)


def _update_replay_job_event(
    pg_conn,
    *,
    job: ReplayJob,
    event_id: str,
    status: str,
    now: datetime,
    published_at: datetime | None = None,
    completed_at: datetime | None = None,
    failed_at: datetime | None = None,
    last_error: str | None = None,
    last_observed_processing_status: str | None = None,
) -> None:
    with pg_conn.cursor() as cur:
        cur.execute(
            """
            UPDATE replay_job_events
            SET status = %s,
                published_at = COALESCE(%s, published_at),
                completed_at = COALESCE(%s, completed_at),
                failed_at = COALESCE(%s, failed_at),
                updated_at = %s,
                last_error = %s,
                last_observed_processing_status = %s
            WHERE replay_job_id = %s
              AND event_id = %s
              AND EXISTS (
                  SELECT 1
                  FROM replay_jobs
                  WHERE replay_job_id = %s
                    AND owner_token = %s
                    AND lease_generation = %s
                    AND status = 'running'
              )
            """,
            (
                status,
                published_at,
                completed_at,
                failed_at,
                now,
                last_error,
                last_observed_processing_status,
                job.replay_job_id,
                event_id,
                job.replay_job_id,
                job.owner_token,
                job.lease_generation,
            ),
        )


def _update_replay_job_counts(pg_conn, job: ReplayJob, now: datetime) -> ReplayJob:
    with pg_conn.cursor() as cur:
        cur.execute(
            """
            SELECT
                COUNT(*),
                COUNT(*) FILTER (WHERE published_at IS NOT NULL),
                COUNT(*) FILTER (WHERE status = 'completed'),
                COUNT(*) FILTER (WHERE status = 'failed'),
                COUNT(*) FILTER (WHERE status = 'skipped')
            FROM replay_job_events
            WHERE replay_job_id = %s
            """,
            (job.replay_job_id,),
        )
        total_events, published_events, completed_events, failed_events, skipped_events = cur.fetchone()
        cur.execute(
            """
            UPDATE replay_jobs
            SET total_events = %s,
                published_events = %s,
                completed_events = %s,
                failed_events = %s,
                skipped_events = %s,
                updated_at = %s
            WHERE replay_job_id = %s
              AND owner_token = %s
              AND lease_generation = %s
              AND status = 'running'
            RETURNING
                replay_job_id,
                job_type,
                selector_type,
                selector,
                source_type,
                status,
                requested_by,
                requested_at,
                started_at,
                completed_at,
                failed_at,
                updated_at,
                lease_expires_at,
                heartbeat_at,
                cancel_requested_at,
                cancelled_at,
                deadline_at,
                timed_out_at,
                terminal_reason,
                terminal_detail,
                attempt_count,
                total_events,
                published_events,
                completed_events,
                failed_events,
                skipped_events,
                last_error,
                owner_token,
                lease_generation
            """,
            (
                total_events,
                published_events,
                completed_events,
                failed_events,
                skipped_events,
                now,
                job.replay_job_id,
                job.owner_token,
                job.lease_generation,
            ),
        )
        return _require_owned_job(_row_to_replay_job(cur.fetchone()), job.replay_job_id)


def _heartbeat_replay_job(pg_conn, job: ReplayJob, now: datetime, lease_timeout) -> ReplayJob:
    with pg_conn.cursor() as cur:
        cur.execute(
            """
            UPDATE replay_jobs
            SET updated_at = %s,
                heartbeat_at = %s,
                lease_expires_at = %s
            WHERE replay_job_id = %s
              AND owner_token = %s
              AND lease_generation = %s
              AND status = 'running'
            RETURNING
                replay_job_id,
                job_type,
                selector_type,
                selector,
                source_type,
                status,
                requested_by,
                requested_at,
                started_at,
                completed_at,
                failed_at,
                updated_at,
                lease_expires_at,
                heartbeat_at,
                cancel_requested_at,
                cancelled_at,
                deadline_at,
                timed_out_at,
                terminal_reason,
                terminal_detail,
                attempt_count,
                total_events,
                published_events,
                completed_events,
                failed_events,
                skipped_events,
                last_error,
                owner_token,
                lease_generation
            """,
            (
                now,
                now,
                now + lease_timeout,
                job.replay_job_id,
                job.owner_token,
                job.lease_generation,
            ),
        )
        return _require_owned_job(_row_to_replay_job(cur.fetchone()), job.replay_job_id)


def _finalize_replay_job(
    pg_conn,
    *,
    job: ReplayJob,
    status: str,
    now: datetime,
    last_error: str | None = None,
    terminal_reason: str | None = None,
    terminal_detail: str | None = None,
) -> ReplayJob:
    with pg_conn.cursor() as cur:
        cur.execute(
            """
            UPDATE replay_jobs
            SET status = %s,
                updated_at = %s,
                completed_at = CASE WHEN %s = 'completed' THEN COALESCE(completed_at, %s) ELSE completed_at END,
                failed_at = CASE WHEN %s = 'failed' THEN COALESCE(failed_at, %s) ELSE failed_at END,
                cancelled_at = CASE WHEN %s = 'cancelled' THEN COALESCE(cancelled_at, %s) ELSE cancelled_at END,
                timed_out_at = CASE WHEN %s = 'timed_out' THEN COALESCE(timed_out_at, %s) ELSE timed_out_at END,
                lease_expires_at = %s,
                heartbeat_at = %s,
                last_error = %s,
                terminal_reason = %s,
                terminal_detail = %s
            WHERE replay_job_id = %s
              AND owner_token = %s
              AND lease_generation = %s
            RETURNING
                replay_job_id,
                job_type,
                selector_type,
                selector,
                source_type,
                status,
                requested_by,
                requested_at,
                started_at,
                completed_at,
                failed_at,
                updated_at,
                lease_expires_at,
                heartbeat_at,
                cancel_requested_at,
                cancelled_at,
                deadline_at,
                timed_out_at,
                terminal_reason,
                terminal_detail,
                attempt_count,
                total_events,
                published_events,
                completed_events,
                failed_events,
                skipped_events,
                last_error,
                owner_token,
                lease_generation
            """,
            (
                status,
                now,
                status,
                now,
                status,
                now,
                status,
                now,
                status,
                now,
                now,
                now,
                last_error,
                terminal_reason,
                terminal_detail,
                job.replay_job_id,
                job.owner_token,
                job.lease_generation,
            ),
        )
        finalized = _require_owned_job(_row_to_replay_job(cur.fetchone()), job.replay_job_id)

    if status == "completed":
        action = f"{job.job_type}_completed"
    elif status == "failed":
        action = f"{job.job_type}_failed"
    elif status == "cancelled":
        action = f"{job.job_type}_cancelled"
    else:
        action = f"{job.job_type}_timed_out"
    _record_audit(
        pg_conn,
        action=action,
        actor="replay-runner",
        target_type="replay_job",
        target_id=job.replay_job_id,
        metadata={
            "job_type": job.job_type,
            "selector_type": job.selector_type,
            "total_events": finalized.total_events if finalized else job.total_events,
            "published_events": finalized.published_events if finalized else job.published_events,
            "completed_events": finalized.completed_events if finalized else job.completed_events,
            "failed_events": finalized.failed_events if finalized else job.failed_events,
            "skipped_events": finalized.skipped_events if finalized else job.skipped_events,
            "last_error": last_error,
            "terminal_reason": terminal_reason,
            "terminal_detail": terminal_detail,
        },
        created_at=now,
    )
    return finalized


def _sweep_replay_jobs(pg_conn, now: datetime) -> list[ReplayJob]:
    swept: list[ReplayJob] = []
    with pg_conn.cursor() as cur:
        cur.execute(
            """
            UPDATE replay_jobs
            SET status = 'cancelled',
                updated_at = %s,
                cancelled_at = COALESCE(cancelled_at, %s),
                terminal_reason = COALESCE(terminal_reason, 'cancelled'),
                terminal_detail = COALESCE(terminal_detail, 'cancellation requested before replay claim'),
                lease_expires_at = %s,
                heartbeat_at = %s
            WHERE status = 'requested'
              AND cancel_requested_at IS NOT NULL
            RETURNING
                replay_job_id,
                job_type,
                selector_type,
                selector,
                source_type,
                status,
                requested_by,
                requested_at,
                started_at,
                completed_at,
                failed_at,
                updated_at,
                lease_expires_at,
                heartbeat_at,
                cancel_requested_at,
                cancelled_at,
                deadline_at,
                timed_out_at,
                terminal_reason,
                terminal_detail,
                attempt_count,
                total_events,
                published_events,
                completed_events,
                failed_events,
                skipped_events,
                last_error,
                owner_token,
                lease_generation
            """,
            (now, now, now, now),
        )
        swept.extend(_row_to_replay_job(row) for row in cur.fetchall())

        cur.execute(
            """
            UPDATE replay_jobs
            SET status = 'cancelled',
                updated_at = %s,
                cancelled_at = COALESCE(cancelled_at, %s),
                terminal_reason = COALESCE(terminal_reason, 'cancelled'),
                terminal_detail = COALESCE(terminal_detail, 'cancelled after runner lease expiry'),
                lease_expires_at = %s,
                heartbeat_at = %s
            WHERE status = 'running'
              AND cancel_requested_at IS NOT NULL
              AND lease_expires_at < %s
            RETURNING
                replay_job_id,
                job_type,
                selector_type,
                selector,
                source_type,
                status,
                requested_by,
                requested_at,
                started_at,
                completed_at,
                failed_at,
                updated_at,
                lease_expires_at,
                heartbeat_at,
                cancel_requested_at,
                cancelled_at,
                deadline_at,
                timed_out_at,
                terminal_reason,
                terminal_detail,
                attempt_count,
                total_events,
                published_events,
                completed_events,
                failed_events,
                skipped_events,
                last_error,
                owner_token,
                lease_generation
            """,
            (now, now, now, now, now),
        )
        swept.extend(_row_to_replay_job(row) for row in cur.fetchall())

        cur.execute(
            """
            UPDATE replay_jobs
            SET status = 'timed_out',
                updated_at = %s,
                timed_out_at = COALESCE(timed_out_at, %s),
                terminal_reason = COALESCE(terminal_reason, 'deadline_exceeded'),
                terminal_detail = COALESCE(terminal_detail, 'replay job deadline exceeded'),
                lease_expires_at = %s,
                heartbeat_at = %s
            WHERE status IN ('requested', 'running')
              AND deadline_at IS NOT NULL
              AND deadline_at < %s
            RETURNING
                replay_job_id,
                job_type,
                selector_type,
                selector,
                source_type,
                status,
                requested_by,
                requested_at,
                started_at,
                completed_at,
                failed_at,
                updated_at,
                lease_expires_at,
                heartbeat_at,
                cancel_requested_at,
                cancelled_at,
                deadline_at,
                timed_out_at,
                terminal_reason,
                terminal_detail,
                attempt_count,
                total_events,
                published_events,
                completed_events,
                failed_events,
                skipped_events,
                last_error,
                owner_token,
                lease_generation
            """,
            (now, now, now, now, now),
        )
        swept.extend(_row_to_replay_job(row) for row in cur.fetchall())

    for job in [item for item in swept if item is not None]:
        action = f"{job.job_type}_{job.status}"
        _record_audit(
            pg_conn,
            action=action,
            actor="replay-sweeper",
            target_type="replay_job",
            target_id=job.replay_job_id,
            metadata={
                "status": job.status,
                "terminal_reason": job.terminal_reason,
                "terminal_detail": job.terminal_detail,
            },
            created_at=now,
        )

    return [item for item in swept if item is not None]


def _refresh_replay_event(
    pg_conn,
    *,
    job: ReplayJob,
    job_event: ReplayJobEvent,
    producer: KafkaProducer,
    settings: WorkerSettings,
    logger,
) -> None:
    now = _utc_now()
    processing_state = _load_processing_state(pg_conn, job_event.event_id)

    if job_event.status == "pending":
        if processing_state is not None and processing_state.status == "completed":
            _update_replay_job_event(
                pg_conn,
                job=job,
                event_id=job_event.event_id,
                status="skipped",
                now=now,
                last_error="event already completed before replay publication",
                last_observed_processing_status="completed",
            )
            return

        if (
            processing_state is not None
            and processing_state.status in IN_PROGRESS_STATES
            and processing_state.lease_expires_at is not None
            and processing_state.lease_expires_at > now
        ):
            _update_replay_job_event(
                pg_conn,
                job=job,
                event_id=job_event.event_id,
                status="pending",
                now=now,
                last_error=None,
                last_observed_processing_status=processing_state.status,
            )
            return

        producer.send(settings.kafka_topic, job_event.event_payload)
        producer.flush(2)
        _update_replay_job_event(
            pg_conn,
            job=job,
            event_id=job_event.event_id,
            status="published",
            now=now,
            published_at=now,
            last_error=None,
            last_observed_processing_status=processing_state.status if processing_state else None,
        )
        logger.info(
            "replay event published",
            extra={
                "component": "replay-runner",
                "event_id": job_event.event_id,
                "processing_state": "published",
                "replay_job_id": job.replay_job_id,
            },
        )
        return

    if job_event.status != "published":
        return

    if processing_state is None:
        _update_replay_job_event(
            pg_conn,
            job=job,
            event_id=job_event.event_id,
            status="published",
            now=now,
            last_error=None,
            last_observed_processing_status=None,
        )
        return

    if processing_state.status == "completed":
        _update_replay_job_event(
            pg_conn,
            job=job,
            event_id=job_event.event_id,
            status="completed",
            now=now,
            completed_at=now,
            last_error=None,
            last_observed_processing_status="completed",
        )
        return

    if processing_state.status == "failed":
        _update_replay_job_event(
            pg_conn,
            job=job,
            event_id=job_event.event_id,
            status="failed",
            now=now,
            failed_at=now,
            last_error=processing_state.last_error,
            last_observed_processing_status="failed",
        )
        return

    _update_replay_job_event(
        pg_conn,
        job=job,
        event_id=job_event.event_id,
        status="published",
        now=now,
        last_error=None,
        last_observed_processing_status=processing_state.status,
    )


def process_replay_job(
    job: ReplayJob,
    settings: WorkerSettings,
    pg_conn,
    producer: KafkaProducer,
    logger,
) -> ReplayJob:
    try:
        _materialize_replay_job_events(pg_conn, job, _utc_now())
        job = _update_replay_job_counts(pg_conn, job, _utc_now())
    except Exception as exc:
        logger.error(
            "replay job failed during materialization",
            extra={
                "component": "replay-runner",
                "processing_state": "failed",
                "replay_job_id": job.replay_job_id,
                "detail": str(exc),
            },
            exc_info=True,
        )
        return _finalize_replay_job(
            pg_conn,
            job=job,
            status="failed",
            now=_utc_now(),
            last_error=str(exc),
            terminal_reason="materialization_failed",
            terminal_detail=str(exc),
        )

    while True:
        now = _utc_now()
        try:
            job = _heartbeat_replay_job(pg_conn, job, now, settings.replay_lease_timeout)
            job = _update_replay_job_counts(pg_conn, job, now)
        except ClaimLostError as exc:
            logger.warning(
                "replay job claim lost",
                extra={
                    "component": "replay-runner",
                    "processing_state": "claim_lost",
                    "replay_job_id": job.replay_job_id,
                    "detail": str(exc),
                },
            )
            return _load_replay_job(pg_conn, job.replay_job_id) or job

        if job.cancel_requested_at is not None:
            return _finalize_replay_job(
                pg_conn,
                job=job,
                status="cancelled",
                now=now,
                terminal_reason="cancelled",
                terminal_detail="operator requested cancellation",
            )

        if job.deadline_at is not None and now >= job.deadline_at:
            return _finalize_replay_job(
                pg_conn,
                job=job,
                status="timed_out",
                now=now,
                last_error="replay deadline exceeded",
                terminal_reason="deadline_exceeded",
                terminal_detail="replay job exceeded configured timeout",
            )

        events = _load_replay_job_events(pg_conn, job.replay_job_id)
        try:
            for job_event in events:
                job = _heartbeat_replay_job(pg_conn, job, _utc_now(), settings.replay_lease_timeout)
                _refresh_replay_event(
                    pg_conn,
                    job=job,
                    job_event=job_event,
                    producer=producer,
                    settings=settings,
                    logger=logger,
                )
        except ClaimLostError as exc:
            logger.warning(
                "replay job claim lost while refreshing events",
                extra={
                    "component": "replay-runner",
                    "processing_state": "claim_lost",
                    "replay_job_id": job.replay_job_id,
                    "detail": str(exc),
                },
            )
            return _load_replay_job(pg_conn, job.replay_job_id) or job

        job = _update_replay_job_counts(pg_conn, job, _utc_now())
        events = _load_replay_job_events(pg_conn, job.replay_job_id)
        failed_events = [event for event in events if event.status == "failed"]
        active_events = [event for event in events if event.status in {"pending", "published"}]

        if failed_events:
            return _finalize_replay_job(
                pg_conn,
                job=job,
                status="failed",
                now=_utc_now(),
                last_error=failed_events[0].last_error or "one or more replayed events failed",
                terminal_reason="event_failed",
                terminal_detail=failed_events[0].last_error or "one or more replayed events failed",
            )

        if not active_events:
            return _finalize_replay_job(
                pg_conn,
                job=job,
                status="completed",
                now=_utc_now(),
                terminal_reason="completed",
                terminal_detail="all replay events reached terminal states",
            )

        time.sleep(settings.replay_poll_seconds)


def main() -> None:
    settings = WorkerSettings.from_env()
    logger = configure_json_logger(
        "replay-runner",
        settings.log_level,
        release_metadata=settings.release_metadata,
    )
    pg_conn = _connect_postgres(settings.postgres_dsn)
    producer = _make_producer(settings.kafka_bootstrap_servers)

    logger.info(
        "replay runner startup complete",
        extra={
            "component": "replay-runner",
            "processing_state": "startup",
            "detail": json.dumps(settings.release_metadata.as_dict(), sort_keys=True),
        },
    )

    try:
        while True:
            swept_jobs = _sweep_replay_jobs(pg_conn, _utc_now())
            for swept in swept_jobs:
                logger.info(
                    "replay job swept to terminal state",
                    extra={
                        "component": "replay-runner",
                        "processing_state": swept.status,
                        "replay_job_id": swept.replay_job_id,
                        "detail": swept.terminal_reason,
                    },
                )

            job = _claim_next_replay_job(
                pg_conn,
                _utc_now(),
                settings.replay_lease_timeout,
            )
            if job is None:
                time.sleep(settings.replay_poll_seconds)
                continue

            logger.info(
                "replay job claimed",
                extra={
                    "component": "replay-runner",
                    "processing_state": "running",
                    "replay_job_id": job.replay_job_id,
                    "detail": f"generation={job.lease_generation}",
                },
            )
            process_replay_job(job, settings, pg_conn, producer, logger)
    finally:
        producer.flush(2)
        producer.close()
        pg_conn.close()


if __name__ == "__main__":
    main()
