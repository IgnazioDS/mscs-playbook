"""Hardened ingestion and operator API for the mini platform."""

from __future__ import annotations

import json
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Annotated, Any, Literal
from uuid import uuid4

import psycopg2
from fastapi import Depends, FastAPI, HTTPException, Query, Request, Security
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from kafka import KafkaProducer
from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

from app.config import IngestAPISettings
from app.logging_utils import configure_json_logger
from mini_platform.auth import APIKeyRecord
from mini_platform.contracts import OrderCreatedV1, supported_contracts
from mini_platform.release import ReleaseMetadata


NonEmptyText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
_API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)
_API_KEY_ID_HEADER = APIKeyHeader(name="X-API-Key-Id", auto_error=False)


class IngestEvent(OrderCreatedV1):
    """Current supported ingest contract."""


class IngestAccepted(BaseModel):
    event_id: str
    status: Literal["accepted"]


class DependencyCheck(BaseModel):
    status: Literal["ok", "error"]
    detail: str | None = None


class HealthResponse(BaseModel):
    status: Literal["ok", "degraded"]
    checks: dict[str, DependencyCheck]


class IngestCounters(BaseModel):
    accepted_count: int
    rejected_count: int


class WorkerCounters(BaseModel):
    completed_count: int
    failed_count: int
    in_progress_count: int
    dlq_count: int


class ReleaseView(BaseModel):
    version: str
    build_sha: str
    build_time: str


class TelemetryResponse(BaseModel):
    ingest: IngestCounters
    worker: WorkerCounters
    release: ReleaseView


class ReplayCounters(BaseModel):
    requested_count: int
    running_count: int
    completed_count: int
    failed_count: int
    cancelled_count: int
    timed_out_count: int


class DurableWorkerCounters(BaseModel):
    completed_total: int
    failed_total: int
    in_progress_count: int
    dlq_total: int
    dlq_backlog_count: int


class DurableIngestCounters(BaseModel):
    accepted_total: int
    rejected_total: int


class ContractSupport(BaseModel):
    event_type: str
    schema_version: int
    model: str


class DurableTelemetryResponse(BaseModel):
    ingest: DurableIngestCounters
    worker: DurableWorkerCounters
    replay: ReplayCounters
    contracts: list[ContractSupport]
    release: ReleaseView


class ProcessingStateView(BaseModel):
    event_id: str
    status: str
    claimed_at: datetime | None
    lease_expires_at: datetime | None
    heartbeat_at: datetime | None
    updated_at: datetime
    storage_written_at: datetime | None
    analytics_written_at: datetime | None
    completed_at: datetime | None
    failed_at: datetime | None
    last_error: str | None
    attempt_count: int
    owner_token: str | None
    lease_generation: int


class ReplayJobEventView(BaseModel):
    event_id: str
    source_type: str
    source_row_id: int | None
    status: str
    published_at: datetime | None
    completed_at: datetime | None
    failed_at: datetime | None
    updated_at: datetime
    last_error: str | None
    last_observed_processing_status: str | None


class ReplayJobSummary(BaseModel):
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
    total_events: int
    published_events: int
    completed_events: int
    failed_events: int
    skipped_events: int
    lease_expires_at: datetime | None
    heartbeat_at: datetime | None
    cancel_requested_at: datetime | None
    cancelled_at: datetime | None
    deadline_at: datetime | None
    timed_out_at: datetime | None
    terminal_reason: str | None
    terminal_detail: str | None
    last_error: str | None
    attempt_count: int
    lease_generation: int


class AuditEntry(BaseModel):
    audit_id: int
    action: str
    actor: str
    target_type: str
    target_id: str
    metadata: dict[str, Any]
    created_at: datetime


class ReplayJobDetailResponse(BaseModel):
    replay_job: ReplayJobSummary
    events: list[ReplayJobEventView]
    audit: list[AuditEntry]


class ReplayJobCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    selector_type: Literal["event_id", "time_range"]
    event_id: NonEmptyText | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None

    @model_validator(mode="after")
    def _validate_selector(self) -> "ReplayJobCreateRequest":
        if self.selector_type == "event_id":
            if self.event_id is None:
                raise ValueError("event_id is required for selector_type=event_id")
            if self.start_time is not None or self.end_time is not None:
                raise ValueError("time range fields are not valid for selector_type=event_id")
            return self

        if self.start_time is None or self.end_time is None:
            raise ValueError("start_time and end_time are required for selector_type=time_range")
        if self.event_id is not None:
            raise ValueError("event_id is not valid for selector_type=time_range")
        if self.start_time.tzinfo is None or self.end_time.tzinfo is None:
            raise ValueError("start_time and end_time must include timezone offsets")
        if self.start_time >= self.end_time:
            raise ValueError("start_time must be before end_time")
        self.start_time = self.start_time.astimezone(timezone.utc)
        self.end_time = self.end_time.astimezone(timezone.utc)
        return self

    def selector_payload(self) -> dict[str, Any]:
        if self.selector_type == "event_id":
            return {"event_id": self.event_id}
        return {
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
        }


class ReplayJobAccepted(BaseModel):
    replay_job_id: str
    status: Literal["requested"]


class ReplayJobControlResponse(BaseModel):
    replay_job_id: str
    status: str


class ReplayJobCancelRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reason: str | None = None


class ReplayAttemptView(BaseModel):
    replay_job_id: str
    job_type: str
    status: str
    selector_type: str
    source_type: str
    published_at: datetime | None
    completed_at: datetime | None
    failed_at: datetime | None
    last_error: str | None
    last_observed_processing_status: str | None
    terminal_reason: str | None
    terminal_detail: str | None


class DLQEventSummary(BaseModel):
    dlq_id: int
    event_id: str | None
    error: str
    failed_at: datetime
    current_processing_status: str | None
    latest_replay_status: str | None


class DLQEventDetail(BaseModel):
    dlq_id: int
    event_id: str | None
    error: str
    payload: dict[str, Any]
    failed_at: datetime
    processing_state: ProcessingStateView | None
    replay_attempts: list[ReplayAttemptView]
    audit: list[AuditEntry]


class EventLifecycleResponse(BaseModel):
    event_id: str
    ingest: dict[str, Any] | None
    processing_state: ProcessingStateView | None
    processed_at: datetime | None
    dlq_events: list[dict[str, Any]]
    replay_attempts: list[ReplayAttemptView]
    audit: list[AuditEntry]


@dataclass(frozen=True)
class AuthenticatedActor:
    scope: Literal["ingest", "operator"]
    key_id: str

    @property
    def actor_name(self) -> str:
        return f"{self.scope}-key:{self.key_id}"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _normalize_json(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return value
    return json.loads(value)


def _json_dumps(value: Any) -> str:
    return json.dumps(value, default=str)


def _connect_postgres(dsn: str) -> psycopg2.extensions.connection:
    conn = psycopg2.connect(dsn)
    conn.autocommit = True
    return conn


def _make_producer(bootstrap_servers: str) -> KafkaProducer:
    return KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )


def _postgres_check(pg_conn: psycopg2.extensions.connection | None) -> DependencyCheck:
    if pg_conn is None:
        return DependencyCheck(status="error", detail="connection not initialized")

    try:
        with pg_conn.cursor() as cur:
            cur.execute("SELECT 1")
            cur.fetchone()
    except Exception as exc:
        return DependencyCheck(status="error", detail=f"query failed: {exc}")

    return DependencyCheck(status="ok")


def _kafka_check(producer: KafkaProducer | None) -> DependencyCheck:
    if producer is None:
        return DependencyCheck(status="error", detail="producer not initialized")

    try:
        if not producer.bootstrap_connected():
            return DependencyCheck(status="error", detail="bootstrap connection unavailable")
    except Exception as exc:
        return DependencyCheck(status="error", detail=f"producer check failed: {exc}")

    return DependencyCheck(status="ok")


def _health_response(app: FastAPI) -> JSONResponse:
    startup_complete = bool(getattr(app.state, "startup_complete", False))
    checks = {
        "startup": DependencyCheck(
            status="ok" if startup_complete else "error",
            detail=None if startup_complete else "startup not complete",
        ),
        "postgres": _postgres_check(getattr(app.state, "pg_conn", None)),
        "kafka": _kafka_check(getattr(app.state, "producer", None)),
    }

    overall_ok = all(check.status == "ok" for check in checks.values())
    payload = HealthResponse(status="ok" if overall_ok else "degraded", checks=checks)
    return JSONResponse(status_code=200 if overall_ok else 503, content=payload.model_dump(mode="json"))


def _row_to_processing_state(row: tuple | None) -> ProcessingStateView | None:
    if row is None:
        return None
    return ProcessingStateView(
        event_id=row[0],
        status=row[1],
        claimed_at=row[2],
        lease_expires_at=row[3],
        heartbeat_at=row[4],
        updated_at=row[5],
        storage_written_at=row[6],
        analytics_written_at=row[7],
        completed_at=row[8],
        failed_at=row[9],
        last_error=row[10],
        attempt_count=row[11],
        owner_token=row[12],
        lease_generation=row[13],
    )


def _load_processing_state(
    pg_conn: psycopg2.extensions.connection,
    event_id: str,
) -> ProcessingStateView | None:
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
        return _row_to_processing_state(cur.fetchone())


def _release_view(metadata: ReleaseMetadata) -> ReleaseView:
    return ReleaseView(**metadata.as_dict())


def _load_simple_telemetry(
    pg_conn: psycopg2.extensions.connection,
    release_metadata: ReleaseMetadata,
) -> TelemetryResponse:
    with pg_conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM ingest_log")
        accepted_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM ingest_rejections")
        rejected_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM processed_events")
        completed_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM dlq_events")
        failed_count = cur.fetchone()[0]
        cur.execute(
            """
            SELECT COUNT(*)
            FROM event_processing
            WHERE status IN ('claimed', 'storage_written', 'analytics_written')
            """
        )
        in_progress_count = cur.fetchone()[0]

    return TelemetryResponse(
        ingest=IngestCounters(
            accepted_count=accepted_count,
            rejected_count=rejected_count,
        ),
        worker=WorkerCounters(
            completed_count=completed_count,
            failed_count=failed_count,
            in_progress_count=in_progress_count,
            dlq_count=failed_count,
        ),
        release=_release_view(release_metadata),
    )


def _load_durable_telemetry(
    pg_conn: psycopg2.extensions.connection,
    release_metadata: ReleaseMetadata,
) -> DurableTelemetryResponse:
    with pg_conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM ingest_log")
        accepted_total = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM ingest_rejections")
        rejected_total = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM processed_events")
        completed_total = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM dlq_events")
        failed_total = cur.fetchone()[0]
        cur.execute(
            """
            SELECT COUNT(*)
            FROM event_processing
            WHERE status IN ('claimed', 'storage_written', 'analytics_written')
            """
        )
        in_progress_count = cur.fetchone()[0]
        cur.execute(
            """
            SELECT COUNT(*)
            FROM event_processing
            WHERE status = 'failed'
            """
        )
        dlq_backlog_count = cur.fetchone()[0]
        cur.execute(
            """
            SELECT
                COUNT(*) FILTER (WHERE status = 'requested'),
                COUNT(*) FILTER (WHERE status = 'running'),
                COUNT(*) FILTER (WHERE status = 'completed'),
                COUNT(*) FILTER (WHERE status = 'failed'),
                COUNT(*) FILTER (WHERE status = 'cancelled'),
                COUNT(*) FILTER (WHERE status = 'timed_out')
            FROM replay_jobs
            """
        )
        (
            requested_count,
            running_count,
            completed_count,
            replay_failed_count,
            cancelled_count,
            timed_out_count,
        ) = cur.fetchone()

    return DurableTelemetryResponse(
        ingest=DurableIngestCounters(
            accepted_total=accepted_total,
            rejected_total=rejected_total,
        ),
        worker=DurableWorkerCounters(
            completed_total=completed_total,
            failed_total=failed_total,
            in_progress_count=in_progress_count,
            dlq_total=failed_total,
            dlq_backlog_count=dlq_backlog_count,
        ),
        replay=ReplayCounters(
            requested_count=requested_count,
            running_count=running_count,
            completed_count=completed_count,
            failed_count=replay_failed_count,
            cancelled_count=cancelled_count,
            timed_out_count=timed_out_count,
        ),
        contracts=[ContractSupport(**entry) for entry in supported_contracts()],
        release=_release_view(release_metadata),
    )


def _record_ingest_rejection(
    pg_conn: psycopg2.extensions.connection | None,
    path: str,
    status_code: int,
    reason: str,
    detail: dict[str, Any],
    rejected_at: datetime,
) -> None:
    if pg_conn is None:
        return

    with pg_conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO ingest_rejections (path, status_code, reason, detail, rejected_at)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (path, status_code, reason, _json_dumps(detail), rejected_at),
        )


def _record_audit(
    pg_conn: psycopg2.extensions.connection,
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
            INSERT INTO operator_audit_log (
                action,
                actor,
                target_type,
                target_id,
                metadata,
                created_at
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (action, actor, target_type, target_id, _json_dumps(metadata), created_at),
        )


def _insert_ingest_log(
    pg_conn: psycopg2.extensions.connection,
    *,
    event_id: str,
    received_at: datetime,
    event: dict[str, Any],
) -> None:
    with pg_conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO ingest_log (
                event_id,
                received_at,
                event_type,
                schema_version,
                event_time,
                payload
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                event_id,
                received_at,
                event["event_type"],
                event["schema_version"],
                event["event_time"],
                _json_dumps(event),
            ),
        )


def _row_to_replay_job(row: tuple | None) -> ReplayJobSummary | None:
    if row is None:
        return None
    return ReplayJobSummary(
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
        total_events=row[12],
        published_events=row[13],
        completed_events=row[14],
        failed_events=row[15],
        skipped_events=row[16],
        lease_expires_at=row[17],
        heartbeat_at=row[18],
        cancel_requested_at=row[19],
        cancelled_at=row[20],
        deadline_at=row[21],
        timed_out_at=row[22],
        terminal_reason=row[23],
        terminal_detail=row[24],
        last_error=row[25],
        attempt_count=row[26],
        lease_generation=row[27],
    )


def _load_replay_job(
    pg_conn: psycopg2.extensions.connection,
    replay_job_id: str,
) -> ReplayJobSummary | None:
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
                total_events,
                published_events,
                completed_events,
                failed_events,
                skipped_events,
                lease_expires_at,
                heartbeat_at,
                cancel_requested_at,
                cancelled_at,
                deadline_at,
                timed_out_at,
                terminal_reason,
                terminal_detail,
                last_error,
                attempt_count,
                lease_generation
            FROM replay_jobs
            WHERE replay_job_id = %s
            """,
            (replay_job_id,),
        )
        return _row_to_replay_job(cur.fetchone())


def _load_replay_job_events(
    pg_conn: psycopg2.extensions.connection,
    replay_job_id: str,
) -> list[ReplayJobEventView]:
    with pg_conn.cursor() as cur:
        cur.execute(
            """
            SELECT
                event_id,
                source_type,
                source_row_id,
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
        rows = cur.fetchall()

    return [
        ReplayJobEventView(
            event_id=row[0],
            source_type=row[1],
            source_row_id=row[2],
            status=row[3],
            published_at=row[4],
            completed_at=row[5],
            failed_at=row[6],
            updated_at=row[7],
            last_error=row[8],
            last_observed_processing_status=row[9],
        )
        for row in rows
    ]


def _load_audit_entries(
    pg_conn: psycopg2.extensions.connection,
    *,
    target_type: str,
    target_id: str,
) -> list[AuditEntry]:
    with pg_conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, action, actor, target_type, target_id, metadata, created_at
            FROM operator_audit_log
            WHERE target_type = %s
              AND target_id = %s
            ORDER BY created_at DESC
            """,
            (target_type, target_id),
        )
        rows = cur.fetchall()

    return [
        AuditEntry(
            audit_id=row[0],
            action=row[1],
            actor=row[2],
            target_type=row[3],
            target_id=row[4],
            metadata=_normalize_json(row[5]),
            created_at=row[6],
        )
        for row in rows
    ]


def _create_replay_job(
    pg_conn: psycopg2.extensions.connection,
    *,
    job_type: Literal["replay", "redrive"],
    selector_type: Literal["event_id", "time_range", "dlq_event"],
    selector: dict[str, Any],
    source_type: Literal["ingest_log", "dlq_events"],
    requested_by: str,
    requested_at: datetime,
    timeout_seconds: int,
) -> ReplayJobSummary:
    replay_job_id = str(uuid4())
    deadline_at = requested_at + timedelta(seconds=timeout_seconds)
    with pg_conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO replay_jobs (
                replay_job_id,
                job_type,
                selector_type,
                selector,
                source_type,
                status,
                requested_by,
                requested_at,
                updated_at,
                deadline_at
            )
            VALUES (%s, %s, %s, %s, %s, 'requested', %s, %s, %s, %s)
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
                total_events,
                published_events,
                completed_events,
                failed_events,
                skipped_events,
                lease_expires_at,
                heartbeat_at,
                cancel_requested_at,
                cancelled_at,
                deadline_at,
                timed_out_at,
                terminal_reason,
                terminal_detail,
                last_error,
                attempt_count,
                lease_generation
            """,
            (
                replay_job_id,
                job_type,
                selector_type,
                _json_dumps(selector),
                source_type,
                requested_by,
                requested_at,
                requested_at,
                deadline_at,
            ),
        )
        return _row_to_replay_job(cur.fetchone())


def _request_replay_job_cancellation(
    pg_conn: psycopg2.extensions.connection,
    *,
    replay_job_id: str,
    requested_at: datetime,
    reason: str | None,
) -> ReplayJobSummary | None:
    with pg_conn.cursor() as cur:
        cur.execute(
            """
            UPDATE replay_jobs
            SET
                status = CASE
                    WHEN status = 'requested' THEN 'cancelled'
                    ELSE status
                END,
                cancel_requested_at = COALESCE(cancel_requested_at, %s),
                cancelled_at = CASE
                    WHEN status = 'requested' THEN COALESCE(cancelled_at, %s)
                    ELSE cancelled_at
                END,
                updated_at = %s,
                terminal_reason = CASE
                    WHEN status = 'requested' THEN 'cancelled'
                    ELSE terminal_reason
                END,
                terminal_detail = CASE
                    WHEN status = 'requested' THEN COALESCE(%s, terminal_detail)
                    ELSE terminal_detail
                END
            WHERE replay_job_id = %s
              AND status IN ('requested', 'running')
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
                total_events,
                published_events,
                completed_events,
                failed_events,
                skipped_events,
                lease_expires_at,
                heartbeat_at,
                cancel_requested_at,
                cancelled_at,
                deadline_at,
                timed_out_at,
                terminal_reason,
                terminal_detail,
                last_error,
                attempt_count,
                lease_generation
            """,
            (
                requested_at,
                requested_at,
                requested_at,
                reason,
                replay_job_id,
            ),
        )
        return _row_to_replay_job(cur.fetchone())


def _load_dlq_row(
    pg_conn: psycopg2.extensions.connection,
    dlq_id: int,
) -> tuple[int, str | None, str, dict[str, Any], datetime] | None:
    with pg_conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, event_id, error, payload, failed_at
            FROM dlq_events
            WHERE id = %s
            """,
            (dlq_id,),
        )
        row = cur.fetchone()

    if row is None:
        return None
    return row[0], row[1], row[2], _normalize_json(row[3]), row[4]


def _load_replay_attempts_for_event(
    pg_conn: psycopg2.extensions.connection,
    event_id: str,
) -> list[ReplayAttemptView]:
    with pg_conn.cursor() as cur:
        cur.execute(
            """
            SELECT
                rje.replay_job_id,
                rj.job_type,
                rje.status,
                rj.selector_type,
                rje.source_type,
                rje.published_at,
                rje.completed_at,
                rje.failed_at,
                rje.last_error,
                rje.last_observed_processing_status,
                rj.terminal_reason,
                rj.terminal_detail
            FROM replay_job_events rje
            JOIN replay_jobs rj
              ON rj.replay_job_id = rje.replay_job_id
            WHERE rje.event_id = %s
            ORDER BY COALESCE(rje.published_at, rj.requested_at) DESC
            """,
            (event_id,),
        )
        rows = cur.fetchall()

    return [
        ReplayAttemptView(
            replay_job_id=row[0],
            job_type=row[1],
            status=row[2],
            selector_type=row[3],
            source_type=row[4],
            published_at=row[5],
            completed_at=row[6],
            failed_at=row[7],
            last_error=row[8],
            last_observed_processing_status=row[9],
            terminal_reason=row[10],
            terminal_detail=row[11],
        )
        for row in rows
    ]


def _load_dlq_summaries(
    pg_conn: psycopg2.extensions.connection,
    limit: int,
) -> list[DLQEventSummary]:
    with pg_conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, event_id, error, failed_at
            FROM dlq_events
            ORDER BY failed_at DESC
            LIMIT %s
            """,
            (limit,),
        )
        rows = cur.fetchall()

    summaries: list[DLQEventSummary] = []
    for dlq_id, event_id, error, failed_at in rows:
        processing_state = _load_processing_state(pg_conn, event_id) if event_id else None
        latest_attempt = None
        if event_id:
            attempts = _load_replay_attempts_for_event(pg_conn, event_id)
            latest_attempt = attempts[0].status if attempts else None
        summaries.append(
            DLQEventSummary(
                dlq_id=dlq_id,
                event_id=event_id,
                error=error,
                failed_at=failed_at,
                current_processing_status=processing_state.status if processing_state else None,
                latest_replay_status=latest_attempt,
            )
        )
    return summaries


def _load_event_lifecycle(
    pg_conn: psycopg2.extensions.connection,
    event_id: str,
) -> EventLifecycleResponse:
    with pg_conn.cursor() as cur:
        cur.execute(
            """
            SELECT event_id, received_at, event_type, schema_version, event_time, payload
            FROM ingest_log
            WHERE event_id = %s
            """,
            (event_id,),
        )
        ingest_row = cur.fetchone()
        cur.execute(
            """
            SELECT processed_at
            FROM processed_events
            WHERE event_id = %s
            """,
            (event_id,),
        )
        processed_row = cur.fetchone()
        cur.execute(
            """
            SELECT id, error, payload, failed_at
            FROM dlq_events
            WHERE event_id = %s
            ORDER BY failed_at DESC
            """,
            (event_id,),
        )
        dlq_rows = cur.fetchall()

    ingest = None
    if ingest_row is not None:
        ingest = {
            "event_id": ingest_row[0],
            "received_at": ingest_row[1],
            "event_type": ingest_row[2],
            "schema_version": ingest_row[3],
            "event_time": ingest_row[4],
            "payload": _normalize_json(ingest_row[5]),
        }

    audit = _load_audit_entries(pg_conn, target_type="event", target_id=event_id)
    audit.extend(_load_audit_entries(pg_conn, target_type="ingest_event", target_id=event_id))
    audit.sort(key=lambda entry: entry.created_at, reverse=True)

    return EventLifecycleResponse(
        event_id=event_id,
        ingest=ingest,
        processing_state=_load_processing_state(pg_conn, event_id),
        processed_at=processed_row[0] if processed_row else None,
        dlq_events=[
            {
                "dlq_id": row[0],
                "error": row[1],
                "payload": _normalize_json(row[2]),
                "failed_at": row[3],
            }
            for row in dlq_rows
        ],
        replay_attempts=_load_replay_attempts_for_event(pg_conn, event_id),
        audit=audit,
    )


def _authenticate_scoped_key(
    *,
    request: Request,
    scope: Literal["ingest", "operator"],
    api_key: str | None,
    key_id: str | None,
) -> AuthenticatedActor:
    settings: IngestAPISettings = request.app.state.settings
    if not settings.auth_enabled:
        return AuthenticatedActor(scope=scope, key_id="auth-disabled")

    if key_id is None:
        raise HTTPException(status_code=401, detail="Missing API key id")
    if api_key is None:
        raise HTTPException(status_code=401, detail="Missing API key")

    key_registry: dict[str, APIKeyRecord]
    if scope == "ingest":
        key_registry = settings.ingest_api_keys
    else:
        key_registry = settings.operator_api_keys

    record = key_registry.get(key_id)
    if record is None or record.secret != api_key:
        raise HTTPException(status_code=403, detail="Invalid API key")

    return AuthenticatedActor(scope=scope, key_id=record.key_id)


def require_ingest_api_key(
    request: Request,
    api_key: str | None = Security(_API_KEY_HEADER),
    key_id: str | None = Security(_API_KEY_ID_HEADER),
) -> AuthenticatedActor:
    return _authenticate_scoped_key(
        request=request,
        scope="ingest",
        api_key=api_key,
        key_id=key_id,
    )


def require_operator_api_key(
    request: Request,
    api_key: str | None = Security(_API_KEY_HEADER),
    key_id: str | None = Security(_API_KEY_ID_HEADER),
) -> AuthenticatedActor:
    return _authenticate_scoped_key(
        request=request,
        scope="operator",
        api_key=api_key,
        key_id=key_id,
    )


def create_app(settings: IngestAPISettings | None = None) -> FastAPI:
    settings = settings or IngestAPISettings.from_env()
    logger = configure_json_logger(
        settings.service_name,
        settings.log_level,
        release_metadata=settings.release_metadata,
    )
    docs_url = "/docs" if settings.docs_enabled else None
    openapi_url = "/openapi.json" if settings.docs_enabled else None
    redoc_url = "/redoc" if settings.docs_enabled else None

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.producer = _make_producer(settings.kafka_bootstrap_servers)
        app.state.pg_conn = _connect_postgres(settings.postgres_dsn)
        app.state.startup_complete = True
        logger.info(
            "ingest API startup complete",
            extra={
                "component": "lifespan",
                "processing_state": "startup",
                "detail": json.dumps(settings.release_metadata.as_dict(), sort_keys=True),
            },
        )

        try:
            yield
        finally:
            producer = getattr(app.state, "producer", None)
            if producer is not None:
                producer.flush(2)
                producer.close()

            pg_conn = getattr(app.state, "pg_conn", None)
            if pg_conn is not None:
                pg_conn.close()

            app.state.startup_complete = False
            logger.info(
                "ingest API shutdown complete",
                extra={"component": "lifespan", "processing_state": "shutdown"},
            )

    app = FastAPI(
        lifespan=lifespan,
        docs_url=docs_url,
        openapi_url=openapi_url,
        redoc_url=redoc_url,
    )
    app.state.settings = settings
    app.state.kafka_topic = settings.kafka_topic
    app.state.startup_complete = False
    app.state.logger = logger

    @app.middleware("http")
    async def enforce_request_size(request: Request, call_next):
        if request.url.path == "/ingest" and request.method == "POST":
            content_length = request.headers.get("content-length")
            if content_length is not None:
                try:
                    declared_size = int(content_length)
                except ValueError:
                    declared_size = settings.max_request_bytes + 1
                if declared_size > settings.max_request_bytes:
                    _record_ingest_rejection(
                        getattr(app.state, "pg_conn", None),
                        path=request.url.path,
                        status_code=413,
                        reason="request_too_large",
                        detail={"request_size": declared_size},
                        rejected_at=_utc_now(),
                    )
                    logger.warning(
                        "request rejected for size limit",
                        extra={
                            "component": "auth",
                            "path": request.url.path,
                            "status_code": 413,
                            "request_size": declared_size,
                        },
                    )
                    return JSONResponse(status_code=413, content={"detail": "Request body too large"})

            body = await request.body()
            if len(body) > settings.max_request_bytes:
                _record_ingest_rejection(
                    getattr(app.state, "pg_conn", None),
                    path=request.url.path,
                    status_code=413,
                    reason="request_too_large",
                    detail={"request_size": len(body)},
                    rejected_at=_utc_now(),
                )
                logger.warning(
                    "request rejected for size limit",
                    extra={
                        "component": "auth",
                        "path": request.url.path,
                        "status_code": 413,
                        "request_size": len(body),
                    },
                )
                return JSONResponse(status_code=413, content={"detail": "Request body too large"})

        return await call_next(request)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        if request.url.path == "/ingest":
            _record_ingest_rejection(
                getattr(app.state, "pg_conn", None),
                path=request.url.path,
                status_code=422,
                reason="validation_failed",
                detail={"errors": exc.errors()},
                rejected_at=_utc_now(),
            )
            logger.warning(
                "request validation failed",
                extra={
                    "component": "validation",
                    "path": request.url.path,
                    "status_code": 422,
                    "detail": str(exc.errors()[0] if exc.errors() else exc),
                },
            )
        return await request_validation_exception_handler(request, exc)

    @app.exception_handler(HTTPException)
    async def custom_http_exception_handler(request: Request, exc: HTTPException):
        if request.url.path == "/ingest" and exc.status_code in {401, 403, 413}:
            reason = "missing_api_key" if exc.status_code == 401 else "invalid_api_key"
            if exc.status_code == 413:
                reason = "request_too_large"
            elif str(exc.detail) == "Missing API key id":
                reason = "missing_api_key_id"
            _record_ingest_rejection(
                getattr(app.state, "pg_conn", None),
                path=request.url.path,
                status_code=exc.status_code,
                reason=reason,
                detail={"detail": exc.detail},
                rejected_at=_utc_now(),
            )
            logger.warning(
                "request rejected",
                extra={
                    "component": "auth",
                    "path": request.url.path,
                    "status_code": exc.status_code,
                    "detail": str(exc.detail),
                },
            )
        return await http_exception_handler(request, exc)

    @app.get("/health", response_model=HealthResponse)
    @app.get("/ready", response_model=HealthResponse)
    def health() -> JSONResponse:
        return _health_response(app)

    @app.get("/telemetry", response_model=TelemetryResponse)
    def telemetry() -> TelemetryResponse:
        return _load_simple_telemetry(app.state.pg_conn, settings.release_metadata)

    @app.get(
        "/ops/telemetry",
        response_model=DurableTelemetryResponse,
    )
    def ops_telemetry(_actor: AuthenticatedActor = Depends(require_operator_api_key)) -> DurableTelemetryResponse:
        return _load_durable_telemetry(app.state.pg_conn, settings.release_metadata)

    @app.post("/ingest", response_model=IngestAccepted, status_code=202)
    def ingest(
        payload: IngestEvent,
        actor: AuthenticatedActor = Depends(require_ingest_api_key),
    ) -> IngestAccepted:
        received_at = _utc_now()
        event = payload.model_dump(mode="json")
        event_id = str(uuid4())
        event["event_id"] = event_id
        event["received_at"] = received_at.isoformat()

        producer: KafkaProducer = app.state.producer
        producer.send(settings.kafka_topic, event)
        producer.flush(2)
        _insert_ingest_log(app.state.pg_conn, event_id=event_id, received_at=received_at, event=event)

        logger.info(
            "ingest accepted",
            extra={
                "component": "ingest",
                "event_id": event_id,
                "processing_state": "accepted",
                "path": "/ingest",
                "status_code": 202,
                "schema_version": event["schema_version"],
                "key_id": actor.key_id,
            },
        )

        return IngestAccepted(event_id=event_id, status="accepted")

    @app.post(
        "/ops/replays",
        response_model=ReplayJobAccepted,
        status_code=202,
    )
    def create_replay_job(
        request: ReplayJobCreateRequest,
        actor: AuthenticatedActor = Depends(require_operator_api_key),
    ) -> ReplayJobAccepted:
        now = _utc_now()
        replay_job = _create_replay_job(
            app.state.pg_conn,
            job_type="replay",
            selector_type=request.selector_type,
            selector=request.selector_payload(),
            source_type="ingest_log",
            requested_by=actor.actor_name,
            requested_at=now,
            timeout_seconds=settings.replay_job_timeout_seconds,
        )
        _record_audit(
            app.state.pg_conn,
            action="replay_requested",
            actor=actor.actor_name,
            target_type="replay_job",
            target_id=replay_job.replay_job_id,
            metadata={
                "job_type": replay_job.job_type,
                "selector_type": replay_job.selector_type,
                "selector": replay_job.selector,
                "requested_by_key_id": actor.key_id,
            },
            created_at=now,
        )
        logger.info(
            "replay job requested",
            extra={
                "component": "ops",
                "processing_state": "requested",
                "replay_job_id": replay_job.replay_job_id,
                "detail": _json_dumps(replay_job.selector),
                "key_id": actor.key_id,
            },
        )
        return ReplayJobAccepted(replay_job_id=replay_job.replay_job_id, status="requested")

    @app.get(
        "/ops/replays/{replay_job_id}",
        response_model=ReplayJobDetailResponse,
    )
    def get_replay_job(
        replay_job_id: str,
        _actor: AuthenticatedActor = Depends(require_operator_api_key),
    ) -> ReplayJobDetailResponse:
        replay_job = _load_replay_job(app.state.pg_conn, replay_job_id)
        if replay_job is None:
            raise HTTPException(status_code=404, detail="Replay job not found")
        return ReplayJobDetailResponse(
            replay_job=replay_job,
            events=_load_replay_job_events(app.state.pg_conn, replay_job_id),
            audit=_load_audit_entries(app.state.pg_conn, target_type="replay_job", target_id=replay_job_id),
        )

    @app.post(
        "/ops/replays/{replay_job_id}/cancel",
        response_model=ReplayJobControlResponse,
        status_code=202,
    )
    def cancel_replay_job(
        replay_job_id: str,
        request: ReplayJobCancelRequest,
        actor: AuthenticatedActor = Depends(require_operator_api_key),
    ) -> ReplayJobControlResponse:
        now = _utc_now()
        replay_job = _request_replay_job_cancellation(
            app.state.pg_conn,
            replay_job_id=replay_job_id,
            requested_at=now,
            reason=request.reason,
        )
        if replay_job is None:
            existing = _load_replay_job(app.state.pg_conn, replay_job_id)
            if existing is None:
                raise HTTPException(status_code=404, detail="Replay job not found")
            replay_job = existing
        _record_audit(
            app.state.pg_conn,
            action="replay_cancel_requested",
            actor=actor.actor_name,
            target_type="replay_job",
            target_id=replay_job_id,
            metadata={"reason": request.reason, "requested_by_key_id": actor.key_id},
            created_at=now,
        )
        logger.info(
            "replay job cancellation requested",
            extra={
                "component": "ops",
                "processing_state": replay_job.status,
                "replay_job_id": replay_job_id,
                "detail": request.reason,
                "key_id": actor.key_id,
            },
        )
        return ReplayJobControlResponse(replay_job_id=replay_job_id, status=replay_job.status)

    @app.get(
        "/ops/dlq",
        response_model=list[DLQEventSummary],
    )
    def list_dlq(
        limit: int = Query(default=20, ge=1, le=100),
        _actor: AuthenticatedActor = Depends(require_operator_api_key),
    ) -> list[DLQEventSummary]:
        return _load_dlq_summaries(app.state.pg_conn, limit)

    @app.get(
        "/ops/dlq/{dlq_id}",
        response_model=DLQEventDetail,
    )
    def get_dlq(
        dlq_id: int,
        _actor: AuthenticatedActor = Depends(require_operator_api_key),
    ) -> DLQEventDetail:
        row = _load_dlq_row(app.state.pg_conn, dlq_id)
        if row is None:
            raise HTTPException(status_code=404, detail="DLQ event not found")
        _, event_id, error, payload, failed_at = row
        return DLQEventDetail(
            dlq_id=dlq_id,
            event_id=event_id,
            error=error,
            payload=payload,
            failed_at=failed_at,
            processing_state=_load_processing_state(app.state.pg_conn, event_id) if event_id else None,
            replay_attempts=_load_replay_attempts_for_event(app.state.pg_conn, event_id) if event_id else [],
            audit=_load_audit_entries(app.state.pg_conn, target_type="dlq_event", target_id=str(dlq_id)),
        )

    @app.post(
        "/ops/dlq/{dlq_id}/redrive",
        response_model=ReplayJobAccepted,
        status_code=202,
    )
    def redrive_dlq(
        dlq_id: int,
        actor: AuthenticatedActor = Depends(require_operator_api_key),
    ) -> ReplayJobAccepted:
        row = _load_dlq_row(app.state.pg_conn, dlq_id)
        if row is None:
            raise HTTPException(status_code=404, detail="DLQ event not found")
        _, event_id, _error, _payload, _failed_at = row
        now = _utc_now()
        replay_job = _create_replay_job(
            app.state.pg_conn,
            job_type="redrive",
            selector_type="dlq_event",
            selector={"dlq_event_id": dlq_id, "event_id": event_id},
            source_type="dlq_events",
            requested_by=actor.actor_name,
            requested_at=now,
            timeout_seconds=settings.replay_job_timeout_seconds,
        )
        _record_audit(
            app.state.pg_conn,
            action="redrive_requested",
            actor=actor.actor_name,
            target_type="dlq_event",
            target_id=str(dlq_id),
            metadata={
                "replay_job_id": replay_job.replay_job_id,
                "event_id": event_id,
                "requested_by_key_id": actor.key_id,
            },
            created_at=now,
        )
        _record_audit(
            app.state.pg_conn,
            action="redrive_requested",
            actor=actor.actor_name,
            target_type="replay_job",
            target_id=replay_job.replay_job_id,
            metadata={"dlq_event_id": dlq_id, "event_id": event_id},
            created_at=now,
        )
        if event_id:
            _record_audit(
                app.state.pg_conn,
                action="redrive_requested",
                actor=actor.actor_name,
                target_type="event",
                target_id=event_id,
                metadata={"replay_job_id": replay_job.replay_job_id, "dlq_event_id": dlq_id},
                created_at=now,
            )
        logger.info(
            "DLQ redrive requested",
            extra={
                "component": "ops",
                "processing_state": "requested",
                "event_id": event_id,
                "replay_job_id": replay_job.replay_job_id,
                "key_id": actor.key_id,
            },
        )
        return ReplayJobAccepted(replay_job_id=replay_job.replay_job_id, status="requested")

    @app.get(
        "/ops/events/{event_id}",
        response_model=EventLifecycleResponse,
    )
    def get_event_lifecycle(
        event_id: str,
        _actor: AuthenticatedActor = Depends(require_operator_api_key),
    ) -> EventLifecycleResponse:
        lifecycle = _load_event_lifecycle(app.state.pg_conn, event_id)
        if lifecycle.ingest is None and lifecycle.processing_state is None and not lifecycle.dlq_events:
            raise HTTPException(status_code=404, detail="Event not found")
        return lifecycle

    return app


app = create_app()
