from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import pytest


EVENT = {
    "event_id": "evt-1",
    "schema_version": 1,
    "event_type": "order_created",
    "event_time": "2026-01-27T12:00:00Z",
    "received_at": "2026-01-27T12:00:01Z",
    "order_id": "O-1",
    "amount": 10.5,
    "currency": "USD",
    "customer_id": "C-1",
}


@dataclass(frozen=True)
class ReleaseMetadata:
    version: str
    build_sha: str
    build_time: str


class FakeS3Error(Exception):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


class FakeWorkerCursor:
    def __init__(self, conn: "FakeWorkerConnection") -> None:
        self.conn = conn
        self._fetchone = None

    def execute(self, query: str, params=None) -> None:
        normalized = " ".join(query.split())

        if normalized.startswith("INSERT INTO event_processing") and "attempt_count" in normalized:
            event_id, claimed_at, lease_expires_at, heartbeat_at, updated_at, owner_token = params
            row = self.conn.event_processing.get(event_id)
            if row is None:
                self.conn.event_processing[event_id] = self.conn.make_row(
                    event_id=event_id,
                    status="claimed",
                    claimed_at=claimed_at,
                    lease_expires_at=lease_expires_at,
                    heartbeat_at=heartbeat_at,
                    updated_at=updated_at,
                    storage_written_at=None,
                    analytics_written_at=None,
                    completed_at=None,
                    failed_at=None,
                    last_error=None,
                    attempt_count=1,
                    owner_token=owner_token,
                    lease_generation=1,
                )
                self._fetchone = self.conn.row_tuple(self.conn.event_processing[event_id])
            else:
                self._fetchone = None
            return

        if normalized.startswith("UPDATE event_processing SET status = 'claimed'"):
            claimed_at, lease_expires_at, heartbeat_at, updated_at, owner_token, event_id, now = params
            row = self.conn.event_processing.get(event_id)
            if row and (
                row["status"] == "failed"
                or (row["status"] in {"claimed", "storage_written", "analytics_written"} and row["lease_expires_at"] < now)
            ):
                row.update(
                    {
                        "status": "claimed",
                        "claimed_at": claimed_at,
                        "lease_expires_at": lease_expires_at,
                        "heartbeat_at": heartbeat_at,
                        "updated_at": updated_at,
                        "failed_at": None,
                        "last_error": None,
                        "attempt_count": row["attempt_count"] + 1,
                        "owner_token": owner_token,
                        "lease_generation": row.get("lease_generation", 0) + 1,
                    }
                )
                self._fetchone = self.conn.row_tuple(row)
            else:
                self._fetchone = None
            return

        if normalized.startswith("UPDATE event_processing SET heartbeat_at ="):
            heartbeat_at, updated_at, lease_expires_at, event_id, owner_token, lease_generation = params
            row = self.conn.event_processing.get(event_id)
            if row and row.get("owner_token") == owner_token and row.get("lease_generation") == lease_generation:
                row.update(
                    {
                        "heartbeat_at": heartbeat_at,
                        "updated_at": updated_at,
                        "lease_expires_at": lease_expires_at,
                    }
                )
                self._fetchone = self.conn.row_tuple(row)
            else:
                self._fetchone = None
            return

        if normalized.startswith("SELECT event_id, status, claimed_at, lease_expires_at"):
            event_id = params[0]
            row = self.conn.event_processing.get(event_id)
            self._fetchone = self.conn.row_tuple(row) if row else None
            return

        if normalized.startswith("UPDATE event_processing SET status = 'storage_written'"):
            written_at, heartbeat_at, updated_at, lease_expires_at, event_id, owner_token, lease_generation = params
            row = self.conn.event_processing[event_id]
            if row.get("owner_token") == owner_token and row.get("lease_generation") == lease_generation:
                row.update(
                    {
                        "status": "storage_written",
                        "storage_written_at": row["storage_written_at"] or written_at,
                        "heartbeat_at": heartbeat_at,
                        "updated_at": updated_at,
                        "lease_expires_at": lease_expires_at,
                        "failed_at": None,
                        "last_error": None,
                    }
                )
                self._fetchone = self.conn.row_tuple(row)
            else:
                self._fetchone = None
            return

        if normalized.startswith("UPDATE event_processing SET status = 'analytics_written'"):
            written_at, heartbeat_at, updated_at, lease_expires_at, event_id, owner_token, lease_generation = params
            row = self.conn.event_processing[event_id]
            if row.get("owner_token") == owner_token and row.get("lease_generation") == lease_generation:
                row.update(
                    {
                        "status": "analytics_written",
                        "analytics_written_at": row["analytics_written_at"] or written_at,
                        "heartbeat_at": heartbeat_at,
                        "updated_at": updated_at,
                        "lease_expires_at": lease_expires_at,
                        "failed_at": None,
                        "last_error": None,
                    }
                )
                self._fetchone = self.conn.row_tuple(row)
            else:
                self._fetchone = None
            return

        if normalized.startswith("WITH updated AS ( UPDATE event_processing SET status = 'completed'"):
            heartbeat_at, updated_at, completed_at, event_id, owner_token, lease_generation, processed_at = params
            row = self.conn.event_processing[event_id]
            if row.get("owner_token") == owner_token and row.get("lease_generation") == lease_generation:
                row.update(
                    {
                        "status": "completed",
                        "heartbeat_at": heartbeat_at,
                        "updated_at": updated_at,
                        "completed_at": row["completed_at"] or completed_at,
                        "failed_at": None,
                        "last_error": None,
                    }
                )
                self.conn.processed_events[event_id] = processed_at
                self._fetchone = self.conn.row_tuple(row)
            else:
                self._fetchone = None
            return

        if normalized.startswith("UPDATE event_processing SET status = 'failed'"):
            heartbeat_at, updated_at, failed_at, lease_expires_at, error, event_id, owner_token, lease_generation = params
            row = self.conn.event_processing[event_id]
            if row.get("owner_token") == owner_token and row.get("lease_generation") == lease_generation:
                row.update(
                    {
                        "status": "failed",
                        "heartbeat_at": heartbeat_at,
                        "updated_at": updated_at,
                        "failed_at": failed_at,
                        "lease_expires_at": lease_expires_at,
                        "last_error": error,
                    }
                )
                self._fetchone = self.conn.row_tuple(row)
            else:
                self._fetchone = None
            return

        if normalized.startswith("SELECT COUNT(*) FROM event_processing WHERE status IN ('claimed', 'storage_written', 'analytics_written')"):
            now = params[0]
            stale_count = sum(
                1
                for row in self.conn.event_processing.values()
                if row["status"] in {"claimed", "storage_written", "analytics_written"} and row["lease_expires_at"] < now
            )
            self._fetchone = (stale_count,)
            return

        if normalized.startswith("INSERT INTO dlq_events"):
            self.conn.dlq_events.append(
                {
                    "event_id": params[0],
                    "error": params[1],
                    "payload": params[2],
                    "failed_at": params[3],
                }
            )
            self._fetchone = None
            return

        raise AssertionError(f"Unexpected query: {normalized}")

    def fetchone(self):
        return self._fetchone

    def __enter__(self) -> "FakeWorkerCursor":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None


class FakeWorkerConnection:
    def __init__(self) -> None:
        self.event_processing: dict[str, dict] = {}
        self.processed_events: dict[str, datetime] = {}
        self.dlq_events: list[dict] = []

    def make_row(self, **kwargs):
        return dict(kwargs)

    def row_tuple(self, row: dict | None):
        if row is None:
            return None
        return (
            row["event_id"],
            row["status"],
            row["claimed_at"],
            row["lease_expires_at"],
            row.get("heartbeat_at"),
            row["updated_at"],
            row["storage_written_at"],
            row["analytics_written_at"],
            row["completed_at"],
            row["failed_at"],
            row["last_error"],
            row["attempt_count"],
            row.get("owner_token"),
            row.get("lease_generation", 0),
        )

    def cursor(self) -> FakeWorkerCursor:
        return FakeWorkerCursor(self)


class FakeMinio:
    def __init__(self, *, fail_puts: int = 0, s3_error_class=FakeS3Error) -> None:
        self.fail_puts = fail_puts
        self.objects: dict[str, bytes] = {}
        self.put_calls = 0
        self.s3_error_class = s3_error_class

    def put_object(self, bucket: str, object_name: str, data, length: int, content_type: str) -> None:
        _ = bucket, length, content_type
        payload = data.read()
        self.put_calls += 1
        if self.fail_puts > 0:
            self.fail_puts -= 1
            raise RuntimeError("minio unavailable")
        self.objects[object_name] = payload

    def stat_object(self, bucket: str, object_name: str):
        _ = bucket
        if object_name not in self.objects:
            raise self.s3_error_class("NoSuchKey")
        return {"object_name": object_name}


class FakeClickHouseClient:
    def __init__(self, *, fail_after_insert_once: bool = False) -> None:
        self.fail_after_insert_once = fail_after_insert_once
        self.rows: list[tuple] = []
        self.insert_calls = 0

    def execute(self, query: str, params=None):
        if query.startswith("SELECT count()"):
            event_id = params["event_id"]
            count = sum(1 for row in self.rows if row[3] == event_id)
            return [(count,)]

        self.insert_calls += 1
        self.rows.extend(params)
        if self.fail_after_insert_once:
            self.fail_after_insert_once = False
            raise RuntimeError("clickhouse write acknowledgement lost")
        return None


def _make_settings(module, **overrides):
    base = {
        "app_env": "test",
        "kafka_bootstrap_servers": "redpanda:9092",
        "kafka_topic": "events.raw",
        "kafka_dlq_topic": "events.dlq",
        "kafka_group_id": "worker-group",
        "postgres_dsn": "dbname=bd06 user=bd06 password=bd06 host=postgres port=5432",
        "minio_endpoint": "minio:9000",
        "minio_access_key": "bd06admin",
        "minio_secret_key": "bd06password",
        "minio_bucket": "events",
        "minio_secure": False,
        "clickhouse_host": "clickhouse",
        "clickhouse_port": 9000,
        "clickhouse_database": "analytics",
        "lease_seconds": 30,
        "replay_poll_seconds": 1,
        "replay_lease_seconds": 30,
        "replay_job_timeout_seconds": 600,
        "maintenance_poll_seconds": 30,
        "retention_ingest_days": 30,
        "retention_processing_days": 30,
        "retention_dlq_days": 30,
        "retention_replay_days": 30,
        "retention_audit_days": 90,
        "retention_rejections_days": 30,
        "minio_retention_days": 30,
        "clickhouse_retention_days": 30,
        "log_level": "INFO",
        "release_metadata": ReleaseMetadata(version="1.2.3", build_sha="abc1234", build_time="2026-03-14T00:00:00Z"),
    }
    return module.WorkerSettings(**{**base, **overrides})


@pytest.fixture
def worker_module(load_service_module, monkeypatch):
    module = load_service_module("mini_platform_worker", "services/worker/app/worker.py")
    monkeypatch.setattr(module.time, "sleep", lambda _seconds: None)
    monkeypatch.setattr(module, "S3Error", FakeS3Error)
    return module


def test_stale_claim_can_be_reclaimed_after_timeout(worker_module) -> None:
    pg_conn = FakeWorkerConnection()
    now = datetime(2026, 1, 27, 12, 0, tzinfo=timezone.utc)
    pg_conn.event_processing["evt-1"] = pg_conn.make_row(
        event_id="evt-1",
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
    minio = FakeMinio()
    clickhouse = FakeClickHouseClient()
    settings = _make_settings(worker_module)

    result = worker_module.process_event(dict(EVENT), settings, pg_conn, minio, clickhouse, worker_module.configure_json_logger("worker-test", "INFO"))

    assert result == "processed"
    assert pg_conn.event_processing["evt-1"]["status"] == "completed"
    assert pg_conn.event_processing["evt-1"]["attempt_count"] == 2
    assert len(minio.objects) == 1
    assert len(clickhouse.rows) == 1


def test_concurrent_claim_attempt_for_same_event_is_safe(worker_module) -> None:
    pg_conn = FakeWorkerConnection()
    now = datetime(2026, 1, 27, 12, 0, tzinfo=timezone.utc)

    first = worker_module._claim_or_resume_event(pg_conn, "evt-1", now, timedelta(seconds=30), "worker-a")
    second = worker_module._claim_or_resume_event(pg_conn, "evt-1", now, timedelta(seconds=30), "worker-b")

    assert first.acquired is True
    assert second.acquired is False
    assert second.state.owner_token == "worker-a"
    assert second.state.lease_generation == 1


def test_completed_event_is_never_reprocessed(worker_module) -> None:
    pg_conn = FakeWorkerConnection()
    now = datetime(2026, 1, 27, 12, 0, tzinfo=timezone.utc)
    pg_conn.event_processing["evt-1"] = pg_conn.make_row(
        event_id="evt-1",
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
    pg_conn.processed_events["evt-1"] = now
    minio = FakeMinio()
    clickhouse = FakeClickHouseClient()
    settings = _make_settings(worker_module)

    result = worker_module.process_event(dict(EVENT), settings, pg_conn, minio, clickhouse, worker_module.configure_json_logger("worker-test", "INFO"))

    assert result == "skipped"
    assert minio.put_calls == 0
    assert clickhouse.insert_calls == 0


def test_takeover_fences_old_owner_from_transition(worker_module) -> None:
    pg_conn = FakeWorkerConnection()
    now = datetime(2026, 1, 27, 12, 0, tzinfo=timezone.utc)
    first = worker_module._claim_or_resume_event(pg_conn, "evt-1", now, timedelta(seconds=30), "worker-a")
    pg_conn.event_processing["evt-1"]["lease_expires_at"] = now - timedelta(seconds=1)
    second = worker_module._claim_or_resume_event(
        pg_conn,
        "evt-1",
        now + timedelta(seconds=31),
        timedelta(seconds=30),
        "worker-b",
    )

    assert second.acquired is True
    assert second.state.owner_token == "worker-b"
    assert second.state.lease_generation == 2

    with pytest.raises(worker_module.ClaimLostError):
        worker_module._mark_storage_written(
            pg_conn,
            state=first.state,
            now=now + timedelta(seconds=31),
            lease_timeout=timedelta(seconds=30),
        )


def test_failed_event_state_is_recorded_and_observable(worker_module) -> None:
    pg_conn = FakeWorkerConnection()
    minio = FakeMinio(fail_puts=3)
    clickhouse = FakeClickHouseClient()
    settings = _make_settings(worker_module)

    with pytest.raises(RuntimeError, match="minio unavailable"):
        worker_module.process_event(dict(EVENT), settings, pg_conn, minio, clickhouse, worker_module.configure_json_logger("worker-test", "INFO"))

    state = pg_conn.event_processing["evt-1"]
    assert state["status"] == "failed"
    assert state["failed_at"] is not None
    assert state["last_error"] == "minio unavailable"


def test_partial_progress_resume_does_not_duplicate_downstream_writes(worker_module) -> None:
    pg_conn = FakeWorkerConnection()
    now = datetime(2026, 1, 27, 12, 0, tzinfo=timezone.utc)
    pg_conn.event_processing["evt-1"] = pg_conn.make_row(
        event_id="evt-1",
        status="claimed",
        claimed_at=now - timedelta(minutes=5),
        lease_expires_at=now - timedelta(minutes=4),
        updated_at=now - timedelta(minutes=5),
        storage_written_at=now - timedelta(minutes=5),
        analytics_written_at=None,
        completed_at=None,
        failed_at=None,
        last_error=None,
        attempt_count=1,
    )
    minio = FakeMinio()
    clickhouse = FakeClickHouseClient()
    clickhouse.rows.append(
        (
            now.date(),
            now,
            now,
            "evt-1",
            "order_created",
            1,
            '{"event_id":"evt-1"}',
        )
    )
    settings = _make_settings(worker_module)

    result = worker_module.process_event(dict(EVENT), settings, pg_conn, minio, clickhouse, worker_module.configure_json_logger("worker-test", "INFO"))

    assert result == "processed"
    assert minio.put_calls == 0
    assert clickhouse.insert_calls == 0
    assert pg_conn.event_processing["evt-1"]["analytics_written_at"] is not None
    assert pg_conn.event_processing["evt-1"]["status"] == "completed"


def test_replay_after_completion_remains_safe(worker_module) -> None:
    pg_conn = FakeWorkerConnection()
    minio = FakeMinio()
    clickhouse = FakeClickHouseClient()
    settings = _make_settings(worker_module)

    first = worker_module.process_event(dict(EVENT), settings, pg_conn, minio, clickhouse, worker_module.configure_json_logger("worker-test", "INFO"))
    second = worker_module.process_event(dict(EVENT), settings, pg_conn, minio, clickhouse, worker_module.configure_json_logger("worker-test", "INFO"))

    assert first == "processed"
    assert second == "skipped"
    assert len(minio.objects) == 1
    assert len(clickhouse.rows) == 1
