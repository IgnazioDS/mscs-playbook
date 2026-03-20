from __future__ import annotations

from datetime import date, datetime, timedelta, timezone


def test_retention_helpers_respect_age_and_active_state(load_service_module) -> None:
    module = load_service_module("mini_platform_ops", "shared/mini_platform/ops.py")
    now = datetime(2026, 3, 14, 12, 0, tzinfo=timezone.utc)
    cutoff = now - timedelta(days=30)

    assert module.should_delete_event_processing({"status": "completed", "updated_at": cutoff - timedelta(seconds=1)}, cutoff)
    assert not module.should_delete_event_processing({"status": "claimed", "updated_at": cutoff - timedelta(days=1)}, cutoff)
    assert module.should_delete_ingest_log(
        {"event_id": "evt-1", "received_at": cutoff - timedelta(seconds=1)},
        cutoff,
        active_event_ids=set(),
    )
    assert not module.should_delete_ingest_log(
        {"event_id": "evt-1", "received_at": cutoff - timedelta(seconds=1)},
        cutoff,
        active_event_ids={"evt-1"},
    )


def test_minio_retention_and_rotation_helpers_are_deterministic(load_service_module) -> None:
    module = load_service_module("mini_platform_ops_rotation", "shared/mini_platform/ops.py")

    expired = module.filter_expired_minio_objects(
        [
            "raw/2026-01-01/evt-old.json",
            "raw/2026-02-20/evt-keep.json",
            "misc/not-an-event.txt",
        ],
        date(2026, 2, 1),
    )
    rotated = module.rotate_keys(
        [("ingest-a", "secret-a"), ("ingest-b", "secret-b")],
        add_entries=[("ingest-c", "secret-c")],
        retire_key_ids={"ingest-a"},
    )

    assert expired == ["raw/2026-01-01/evt-old.json"]
    assert module.render_scoped_key_env(rotated) == "ingest-b:secret-b,ingest-c:secret-c"


def test_backup_restore_order_and_manifest_are_stable(load_service_module) -> None:
    module = load_service_module("mini_platform_ops_backup", "shared/mini_platform/ops.py")

    manifest = module.snapshot_manifest(version="1.2.3", build_sha="abc1234", created_at="2026-03-14T00:00:00Z")

    assert manifest["format_version"] == 1
    assert module.restore_insert_order()[0] == "ingest_log"
    assert module.restore_insert_order()[-1] == "operator_audit_log"
    assert module.restore_truncate_order()[0] == "operator_audit_log"
    assert module.restore_truncate_order()[-1] == "ingest_log"


def test_capacity_summary_and_slo_evaluation_are_machine_checkable(load_service_module) -> None:
    module = load_service_module("mini_platform_ops_slo", "shared/mini_platform/ops.py")

    report = module.summarize_capacity_run(
        ingest_latencies_ms=[80.0, 100.0, 120.0],
        processing_latencies_ms=[5000.0, 5500.0, 6000.0],
        replay_completion_rates_per_minute=[12.0, 14.0],
        accepted=3,
        completed=3,
        failed=0,
    )
    violations = module.evaluate_slo_report(
        {"worker": {"dlq_backlog_count": 0}, "readiness_availability": 1.0},
        report,
    )
    bad_violations = module.evaluate_slo_report(
        {"worker": {"dlq_backlog_count": 10}, "readiness_availability": 0.9},
        {**report, "processing_latency_ms": {"p95": 60_000}, "replay_completion_rate_per_minute": {"avg": 1.0}},
    )

    assert report["ingest_latency_ms"]["p95"] >= 100.0
    assert violations == []
    assert {item["slo"] for item in bad_violations} == {
        "readiness_availability",
        "max_ingest_to_complete_latency_ms",
        "max_dlq_backlog",
        "min_replay_completion_rate_per_minute",
    }
