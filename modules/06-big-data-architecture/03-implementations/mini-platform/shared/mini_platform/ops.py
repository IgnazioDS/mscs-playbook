"""Shared operational helpers for Phase 4 productization flows."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from statistics import mean
from typing import Any


IN_PROGRESS_EVENT_STATUSES = {"claimed", "storage_written", "analytics_written"}
TERMINAL_REPLAY_STATUSES = {"completed", "failed", "cancelled", "timed_out"}
CONTROL_PLANE_TABLES = (
    "ingest_log",
    "event_processing",
    "processed_events",
    "dlq_events",
    "ingest_rejections",
    "replay_jobs",
    "replay_job_events",
    "operator_audit_log",
)


@dataclass(frozen=True)
class RetentionCutoffs:
    ingest_log_before: datetime
    event_processing_before: datetime
    dlq_before: datetime
    replay_before: datetime
    audit_before: datetime
    ingest_rejections_before: datetime
    minio_before: date
    clickhouse_before: date


def should_delete_event_processing(row: dict[str, Any], cutoff: datetime) -> bool:
    return row["status"] not in IN_PROGRESS_EVENT_STATUSES and row["updated_at"] < cutoff


def should_delete_replay_job(row: dict[str, Any], cutoff: datetime) -> bool:
    return row["status"] in TERMINAL_REPLAY_STATUSES and row["updated_at"] < cutoff


def should_delete_ingest_log(
    row: dict[str, Any],
    cutoff: datetime,
    active_event_ids: set[str],
) -> bool:
    return row["received_at"] < cutoff and row["event_id"] not in active_event_ids


def should_delete_rejection(row: dict[str, Any], cutoff: datetime) -> bool:
    return row["rejected_at"] < cutoff


def should_delete_audit_entry(row: dict[str, Any], cutoff: datetime) -> bool:
    return row["created_at"] < cutoff


def extract_minio_event_date(object_name: str) -> date | None:
    parts = object_name.split("/")
    if len(parts) < 3 or parts[0] != "raw":
        return None
    try:
        return date.fromisoformat(parts[1])
    except ValueError:
        return None


def filter_expired_minio_objects(object_names: list[str], cutoff: date) -> list[str]:
    return sorted(
        object_name
        for object_name in object_names
        if (event_date := extract_minio_event_date(object_name)) is not None and event_date < cutoff
    )


def restore_insert_order() -> tuple[str, ...]:
    return (
        "ingest_log",
        "event_processing",
        "processed_events",
        "dlq_events",
        "ingest_rejections",
        "replay_jobs",
        "replay_job_events",
        "operator_audit_log",
    )


def restore_truncate_order() -> tuple[str, ...]:
    return tuple(reversed(restore_insert_order()))


def snapshot_manifest(*, version: str, build_sha: str, created_at: str) -> dict[str, Any]:
    return {
        "format_version": 1,
        "app_version": version,
        "build_sha": build_sha,
        "created_at": created_at,
        "tables": list(CONTROL_PLANE_TABLES),
    }


def render_scoped_key_env(entries: list[tuple[str, str]]) -> str:
    return ",".join(f"{key_id}:{secret}" for key_id, secret in entries)


def rotate_keys(
    current_entries: list[tuple[str, str]],
    *,
    add_entries: list[tuple[str, str]],
    retire_key_ids: set[str] | None = None,
) -> list[tuple[str, str]]:
    retire_key_ids = retire_key_ids or set()
    merged: dict[str, str] = {
        key_id: secret
        for key_id, secret in current_entries
        if key_id not in retire_key_ids
    }
    for key_id, secret in add_entries:
        merged[key_id] = secret
    return sorted(merged.items())


def percentile(sorted_values: list[float], target: float) -> float:
    if not sorted_values:
        return 0.0
    index = int(round((len(sorted_values) - 1) * target))
    return float(sorted_values[index])


def summarize_capacity_run(
    *,
    ingest_latencies_ms: list[float],
    processing_latencies_ms: list[float],
    replay_completion_rates_per_minute: list[float],
    accepted: int,
    completed: int,
    failed: int,
) -> dict[str, Any]:
    ingest_sorted = sorted(ingest_latencies_ms)
    processing_sorted = sorted(processing_latencies_ms)
    replay_sorted = sorted(replay_completion_rates_per_minute)
    return {
        "accepted": accepted,
        "completed": completed,
        "failed": failed,
        "error_rate": round((failed / accepted), 4) if accepted else 0.0,
        "ingest_latency_ms": {
            "avg": round(mean(ingest_sorted), 2) if ingest_sorted else 0.0,
            "p95": round(percentile(ingest_sorted, 0.95), 2),
            "max": round(max(ingest_sorted), 2) if ingest_sorted else 0.0,
        },
        "processing_latency_ms": {
            "avg": round(mean(processing_sorted), 2) if processing_sorted else 0.0,
            "p95": round(percentile(processing_sorted, 0.95), 2),
            "max": round(max(processing_sorted), 2) if processing_sorted else 0.0,
        },
        "replay_completion_rate_per_minute": {
            "avg": round(mean(replay_sorted), 2) if replay_sorted else 0.0,
            "min": round(min(replay_sorted), 2) if replay_sorted else 0.0,
        },
    }


DEFAULT_SLO_THRESHOLDS = {
    "readiness_availability": 0.99,
    "max_ingest_to_complete_latency_ms": 30_000,
    "max_dlq_backlog": 5,
    "min_replay_completion_rate_per_minute": 10.0,
}


def evaluate_slo_report(
    telemetry: dict[str, Any],
    capacity_report: dict[str, Any],
    *,
    thresholds: dict[str, float] | None = None,
) -> list[dict[str, Any]]:
    thresholds = {**DEFAULT_SLO_THRESHOLDS, **(thresholds or {})}
    violations: list[dict[str, Any]] = []

    readiness = float(telemetry.get("readiness_availability", 1.0))
    if readiness < thresholds["readiness_availability"]:
        violations.append(
            {
                "slo": "readiness_availability",
                "expected": thresholds["readiness_availability"],
                "actual": readiness,
            }
        )

    processing_p95 = float(capacity_report.get("processing_latency_ms", {}).get("p95", 0.0))
    if processing_p95 > thresholds["max_ingest_to_complete_latency_ms"]:
        violations.append(
            {
                "slo": "max_ingest_to_complete_latency_ms",
                "expected": thresholds["max_ingest_to_complete_latency_ms"],
                "actual": processing_p95,
            }
        )

    dlq_backlog = int(telemetry.get("worker", {}).get("dlq_backlog_count", 0))
    if dlq_backlog > thresholds["max_dlq_backlog"]:
        violations.append(
            {
                "slo": "max_dlq_backlog",
                "expected": thresholds["max_dlq_backlog"],
                "actual": dlq_backlog,
            }
        )

    replay_rate = float(capacity_report.get("replay_completion_rate_per_minute", {}).get("avg", 0.0))
    if replay_rate < thresholds["min_replay_completion_rate_per_minute"]:
        violations.append(
            {
                "slo": "min_replay_completion_rate_per_minute",
                "expected": thresholds["min_replay_completion_rate_per_minute"],
                "actual": replay_rate,
            }
        )

    return violations
