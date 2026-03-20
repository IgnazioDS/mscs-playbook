from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient

from .test_ingest_api import (
    INGEST_HEADERS,
    OPERATOR_HEADERS,
    VALID_PAYLOAD,
    _build_app as build_ingest_app,
    FakePostgresConnection as IngestConnection,
)
from .test_replay_runner import (
    EVENT as REPLAY_EVENT,
    FakeProducer as ReplayProducer,
    FakeReplayConnection,
    _make_settings as make_replay_settings,
)
from .test_worker import (
    EVENT as WORKER_EVENT,
    FakeClickHouseClient,
    FakeMinio,
    FakeS3Error,
    FakeWorkerConnection,
    _make_settings as make_worker_settings,
)


@pytest.fixture
def worker_module(load_service_module, monkeypatch):
    module = load_service_module("mini_platform_worker_eval", "services/worker/app/worker.py")
    monkeypatch.setattr(module.time, "sleep", lambda _seconds: None)
    monkeypatch.setattr(module, "S3Error", FakeS3Error)
    return module


@pytest.fixture
def replay_module(load_service_module, monkeypatch):
    module = load_service_module("mini_platform_replay_eval", "services/worker/app/replay_runner.py")
    monkeypatch.setattr(module.time, "sleep", lambda _seconds: None)
    return module


def test_eval_worker_normal_completion_and_stale_recovery(worker_module) -> None:
    pg_conn = FakeWorkerConnection()
    minio = FakeMinio()
    clickhouse = FakeClickHouseClient()
    settings = make_worker_settings(worker_module)

    first_event = dict(WORKER_EVENT)
    first_event["event_id"] = "evt-normal"
    result = worker_module.process_event(
        first_event,
        settings,
        pg_conn,
        minio,
        clickhouse,
        worker_module.configure_json_logger("worker-eval", "INFO"),
    )
    assert result == "processed"
    assert pg_conn.event_processing["evt-normal"]["status"] == "completed"

    now = datetime.now(timezone.utc)
    stale_event = dict(WORKER_EVENT)
    stale_event["event_id"] = "evt-stale"
    pg_conn.event_processing["evt-stale"] = pg_conn.make_row(
        event_id="evt-stale",
        status="claimed",
        claimed_at=now - timedelta(minutes=5),
        lease_expires_at=now - timedelta(minutes=4),
        updated_at=now - timedelta(minutes=5),
        storage_written_at=None,
        analytics_written_at=None,
        completed_at=None,
        failed_at=None,
        last_error=None,
        attempt_count=1,
    )
    stale_result = worker_module.process_event(
        stale_event,
        settings,
        pg_conn,
        minio,
        clickhouse,
        worker_module.configure_json_logger("worker-eval", "INFO"),
    )

    assert stale_result == "processed"
    assert pg_conn.event_processing["evt-stale"]["status"] == "completed"
    assert len(clickhouse.rows) == 2


def test_eval_replay_after_failure_and_replay_after_completion(replay_module) -> None:
    now = datetime.now(timezone.utc)

    failed_conn = FakeReplayConnection()
    failed_conn.ingest_log.append(
        {"id": 1, "event_id": "evt-failed", "event_time": now, "payload": {**REPLAY_EVENT, "event_id": "evt-failed"}}
    )
    failed_conn.ingest_row_map[1] = failed_conn.ingest_log[0]
    failed_conn.event_processing["evt-failed"] = failed_conn.make_processing_row(
        event_id="evt-failed",
        status="failed",
        claimed_at=now,
        lease_expires_at=now,
        updated_at=now,
        storage_written_at=now,
        analytics_written_at=None,
        completed_at=None,
        failed_at=now,
        last_error="boom",
        attempt_count=1,
    )
    failed_conn.replay_jobs["job-failed"] = {
        "replay_job_id": "job-failed",
        "job_type": "replay",
        "selector_type": "event_id",
        "selector": {"event_id": "evt-failed"},
        "source_type": "ingest_log",
        "status": "requested",
        "requested_by": "operator-api",
        "requested_at": now,
        "started_at": None,
        "completed_at": None,
        "failed_at": None,
        "updated_at": now,
        "lease_expires_at": None,
        "attempt_count": 0,
        "total_events": 0,
        "published_events": 0,
        "completed_events": 0,
        "failed_events": 0,
        "last_error": None,
    }
    replay_settings = make_replay_settings(replay_module)
    failed_claim = replay_module._claim_next_replay_job(
        failed_conn,
        now,
        replay_settings.replay_lease_timeout,
    )
    failed_result = replay_module.process_replay_job(
        failed_claim,
        replay_settings,
        failed_conn,
        ReplayProducer(failed_conn, outcome="completed"),
        replay_module.configure_json_logger("replay-eval", "INFO"),
    )

    assert failed_result.status == "completed"
    assert failed_conn.replay_job_events[0]["status"] == "completed"

    completed_conn = FakeReplayConnection()
    completed_conn.ingest_log.append(
        {"id": 1, "event_id": "evt-complete", "event_time": now, "payload": {**REPLAY_EVENT, "event_id": "evt-complete"}}
    )
    completed_conn.ingest_row_map[1] = completed_conn.ingest_log[0]
    completed_conn.event_processing["evt-complete"] = completed_conn.make_processing_row(
        event_id="evt-complete",
        status="completed",
        claimed_at=now,
        lease_expires_at=now,
        updated_at=now,
        storage_written_at=now,
        analytics_written_at=now,
        completed_at=now,
        failed_at=None,
        last_error=None,
        attempt_count=1,
    )
    completed_conn.replay_jobs["job-complete"] = {
        "replay_job_id": "job-complete",
        "job_type": "replay",
        "selector_type": "event_id",
        "selector": {"event_id": "evt-complete"},
        "source_type": "ingest_log",
        "status": "requested",
        "requested_by": "operator-api",
        "requested_at": now,
        "started_at": None,
        "completed_at": None,
        "failed_at": None,
        "updated_at": now,
        "lease_expires_at": None,
        "attempt_count": 0,
        "total_events": 0,
        "published_events": 0,
        "completed_events": 0,
        "failed_events": 0,
        "last_error": None,
    }
    completed_claim = replay_module._claim_next_replay_job(
        completed_conn,
        now,
        replay_settings.replay_lease_timeout,
    )
    completed_producer = ReplayProducer(completed_conn, outcome="completed")
    completed_result = replay_module.process_replay_job(
        completed_claim,
        replay_settings,
        completed_conn,
        completed_producer,
        replay_module.configure_json_logger("replay-eval", "INFO"),
    )

    assert completed_result.status == "completed"
    assert completed_producer.messages == []
    assert completed_conn.replay_job_events[0]["status"] == "skipped"


def test_eval_operator_telemetry_consistency(monkeypatch, load_service_module) -> None:
    pg_conn = IngestConnection()
    now = datetime.now(timezone.utc)
    pg_conn.processed_events["evt-complete"] = now
    pg_conn.dlq_events.append(
        {
            "id": 5,
            "event_id": "evt-dlq",
            "error": "redrive failed",
            "payload": {"event_id": "evt-dlq", **VALID_PAYLOAD},
            "failed_at": now,
        }
    )
    pg_conn.event_processing["evt-dlq"] = {
        "event_id": "evt-dlq",
        "status": "failed",
        "claimed_at": now,
        "lease_expires_at": now,
        "updated_at": now,
        "storage_written_at": now,
        "analytics_written_at": None,
        "completed_at": None,
        "failed_at": now,
        "last_error": "redrive failed",
        "attempt_count": 2,
    }
    pg_conn.replay_jobs["job-1"] = {
        "replay_job_id": "job-1",
        "job_type": "redrive",
        "selector_type": "dlq_event",
        "selector": {"dlq_event_id": 5, "event_id": "evt-dlq"},
        "source_type": "dlq_events",
        "status": "failed",
        "requested_by": "operator-api",
        "requested_at": now,
        "started_at": now,
        "completed_at": None,
        "failed_at": now,
        "updated_at": now,
        "total_events": 1,
        "published_events": 1,
        "completed_events": 0,
        "failed_events": 1,
        "last_error": "redrive failed",
    }
    app, _, _, _ = build_ingest_app(monkeypatch, load_service_module, pg_conn=pg_conn)

    with TestClient(app) as client:
        accepted = client.post("/ingest", json=VALID_PAYLOAD, headers=INGEST_HEADERS)
        rejected = client.post("/ingest", json=VALID_PAYLOAD)
        telemetry = client.get("/ops/telemetry", headers=OPERATOR_HEADERS)

    assert accepted.status_code == 202
    assert rejected.status_code == 401
    body = telemetry.json()
    assert body["ingest"]["accepted_total"] == 1
    assert body["ingest"]["rejected_total"] == 1
    assert body["worker"]["completed_total"] == 1
    assert body["worker"]["failed_total"] == 1
    assert body["worker"]["dlq_backlog_count"] == 1
    assert body["replay"]["failed_count"] == 1
