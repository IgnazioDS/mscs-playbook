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


class FakeProducer:
    def __init__(self, conn: "FakeReplayConnection", *, outcome: str = "completed") -> None:
        self.conn = conn
        self.outcome = outcome
        self.messages: list[tuple[str, dict]] = []

    def send(self, topic: str, value: dict) -> None:
        self.messages.append((topic, value))
        now = datetime.now(timezone.utc)
        if self.outcome == "completed":
            self.conn.event_processing[value["event_id"]] = self.conn.make_processing_row(
                event_id=value["event_id"],
                status="completed",
                claimed_at=now,
                lease_expires_at=now,
                updated_at=now,
                storage_written_at=now,
                analytics_written_at=now,
                completed_at=now,
                failed_at=None,
                last_error=None,
                attempt_count=2,
            )
            self.conn.processed_events[value["event_id"]] = now
        elif self.outcome == "failed":
            self.conn.event_processing[value["event_id"]] = self.conn.make_processing_row(
                event_id=value["event_id"],
                status="failed",
                claimed_at=now,
                lease_expires_at=now,
                updated_at=now,
                storage_written_at=now,
                analytics_written_at=None,
                completed_at=None,
                failed_at=now,
                last_error="redrive failed",
                attempt_count=2,
            )

    def flush(self, timeout: int | None = None) -> None:
        _ = timeout

    def close(self) -> None:
        return None


class FakeReplayCursor:
    def __init__(self, conn: "FakeReplayConnection") -> None:
        self.conn = conn
        self._fetchone = None
        self._fetchall = []

    def execute(self, query: str, params=None) -> None:
        normalized = " ".join(query.split())

        if normalized.startswith("SELECT replay_job_id FROM replay_jobs"):
            now = params[0]
            candidates = [
                job
                for job in self.conn.replay_jobs.values()
                if (
                    job["status"] == "requested"
                    and job.get("cancel_requested_at") is None
                    and (job.get("deadline_at") is None or job["deadline_at"] >= params[1])
                )
                or (
                    job["status"] == "running"
                    and job["lease_expires_at"] is not None
                    and job["lease_expires_at"] < now
                    and (job.get("deadline_at") is None or job["deadline_at"] >= params[1])
                )
            ]
            candidates.sort(key=lambda job: job["requested_at"])
            self._fetchone = (candidates[0]["replay_job_id"],) if candidates else None
            self._fetchall = [self._fetchone] if self._fetchone else []
            return

        if normalized.startswith("UPDATE replay_jobs SET status = 'running'"):
            started_at, updated_at, lease_expires_at, heartbeat_at, owner_token, replay_job_id, now = params
            job = self.conn.replay_jobs[replay_job_id]
            if (
                (job["status"] == "requested" and job.get("cancel_requested_at") is None)
                or (
                    job["status"] == "running"
                    and job["lease_expires_at"] is not None
                    and job["lease_expires_at"] < now
                )
            ):
                job.update(
                    {
                        "status": "running",
                        "started_at": job["started_at"] or started_at,
                        "updated_at": updated_at,
                        "lease_expires_at": lease_expires_at,
                        "heartbeat_at": heartbeat_at,
                        "attempt_count": job["attempt_count"] + 1,
                        "failed_at": None,
                        "timed_out_at": None,
                        "cancelled_at": None,
                        "last_error": None,
                        "owner_token": owner_token,
                        "lease_generation": job.get("lease_generation", 0) + 1,
                    }
                )
                self._fetchone = self.conn.replay_job_tuple(job)
            else:
                self._fetchone = None
            self._fetchall = [self._fetchone]
            return

        if normalized.startswith("SELECT COUNT(*) FROM replay_job_events WHERE replay_job_id ="):
            count = sum(1 for row in self.conn.replay_job_events if row["replay_job_id"] == params[0])
            self._fetchone = (count,)
            self._fetchall = [self._fetchone]
            return

        if normalized.startswith("SELECT id, event_id, payload FROM ingest_log WHERE event_id ="):
            rows = [
                (row["id"], row["event_id"], row["payload"])
                for row in self.conn.ingest_log
                if row["event_id"] == params[0]
            ]
            self._fetchall = rows
            self._fetchone = rows[0] if rows else None
            return

        if normalized.startswith("SELECT id, event_id, payload FROM ingest_log WHERE event_time >="):
            start_time, end_time = params
            if isinstance(start_time, str):
                start_time = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
            if isinstance(end_time, str):
                end_time = datetime.fromisoformat(end_time.replace("Z", "+00:00"))
            rows = [
                (row["id"], row["event_id"], row["payload"])
                for row in self.conn.ingest_log
                if start_time <= row["event_time"] <= end_time
            ]
            rows.sort(key=lambda row: (self.conn.ingest_row_map[row[0]]["event_time"], row[1]))
            self._fetchall = rows
            self._fetchone = rows[0] if rows else None
            return

        if normalized.startswith("SELECT id, event_id, payload FROM dlq_events WHERE id ="):
            rows = [
                (row["id"], row["event_id"], row["payload"])
                for row in self.conn.dlq_events
                if row["id"] == params[0]
            ]
            self._fetchall = rows
            self._fetchone = rows[0] if rows else None
            return

        if normalized.startswith("INSERT INTO replay_job_events"):
            self.conn.replay_job_events.append(
                {
                    "replay_job_id": params[0],
                    "event_id": params[1],
                    "source_type": params[2],
                    "source_row_id": params[3],
                    "event_payload": self.conn.json_loads(params[4]),
                    "status": "pending",
                    "published_at": None,
                    "completed_at": None,
                    "failed_at": None,
                    "updated_at": params[5],
                    "last_error": None,
                    "last_observed_processing_status": None,
                }
            )
            self._fetchone = None
            self._fetchall = []
            return

        if normalized.startswith("SELECT COUNT(*), COUNT(*) FILTER (WHERE published_at IS NOT NULL)"):
            rows = [row for row in self.conn.replay_job_events if row["replay_job_id"] == params[0]]
            self._fetchone = (
                len(rows),
                sum(1 for row in rows if row["published_at"] is not None),
                sum(1 for row in rows if row["status"] == "completed"),
                sum(1 for row in rows if row["status"] == "failed"),
                sum(1 for row in rows if row["status"] == "skipped"),
            )
            self._fetchall = [self._fetchone]
            return

        if normalized.startswith("UPDATE replay_jobs SET total_events ="):
            total_events, published_events, completed_events, failed_events, skipped_events, updated_at, replay_job_id, owner_token, lease_generation = params
            job = self.conn.replay_jobs[replay_job_id]
            if job.get("owner_token") == owner_token and job.get("lease_generation") == lease_generation:
                job.update(
                    {
                        "total_events": total_events,
                        "published_events": published_events,
                        "completed_events": completed_events,
                        "failed_events": failed_events,
                        "skipped_events": skipped_events,
                        "updated_at": updated_at,
                    }
                )
                self._fetchone = self.conn.replay_job_tuple(job)
            else:
                self._fetchone = None
            self._fetchall = [self._fetchone]
            return

        if normalized.startswith("SELECT replay_job_id, job_type, selector_type, selector"):
            job = self.conn.replay_jobs.get(params[0])
            self._fetchone = self.conn.replay_job_tuple(job) if job else None
            self._fetchall = [self._fetchone] if self._fetchone else []
            return

        if normalized.startswith("SELECT replay_job_id, event_id, source_type, source_row_id, event_payload"):
            rows = [
                self.conn.replay_job_event_tuple(row)
                for row in self.conn.replay_job_events
                if row["replay_job_id"] == params[0]
            ]
            self._fetchall = rows
            self._fetchone = rows[0] if rows else None
            return

        if normalized.startswith("SELECT event_id, status, claimed_at, lease_expires_at"):
            row = self.conn.event_processing.get(params[0])
            self._fetchone = self.conn.processing_tuple(row) if row else None
            self._fetchall = [self._fetchone] if self._fetchone else []
            return

        if normalized.startswith("UPDATE replay_job_events SET status ="):
            (
                status,
                published_at,
                completed_at,
                failed_at,
                updated_at,
                last_error,
                last_observed_processing_status,
                replay_job_id,
                event_id,
                replay_job_id_check,
                owner_token,
                lease_generation,
            ) = params
            job = self.conn.replay_jobs[replay_job_id_check]
            if job.get("owner_token") != owner_token or job.get("lease_generation") != lease_generation:
                self._fetchone = None
                self._fetchall = []
                return
            row = next(
                item
                for item in self.conn.replay_job_events
                if item["replay_job_id"] == replay_job_id and item["event_id"] == event_id
            )
            row.update(
                {
                    "status": status,
                    "published_at": published_at or row["published_at"],
                    "completed_at": completed_at or row["completed_at"],
                    "failed_at": failed_at or row["failed_at"],
                    "updated_at": updated_at,
                    "last_error": last_error,
                    "last_observed_processing_status": last_observed_processing_status,
                }
            )
            self._fetchone = None
            self._fetchall = []
            return

        if normalized.startswith("UPDATE replay_jobs SET updated_at = %s, heartbeat_at = %s, lease_expires_at = %s"):
            updated_at, heartbeat_at, lease_expires_at, replay_job_id, owner_token, lease_generation = params
            job = self.conn.replay_jobs[replay_job_id]
            if (
                job["status"] == "running"
                and job.get("owner_token") == owner_token
                and job.get("lease_generation") == lease_generation
            ):
                job["updated_at"] = updated_at
                job["heartbeat_at"] = heartbeat_at
                job["lease_expires_at"] = lease_expires_at
                self._fetchone = self.conn.replay_job_tuple(job)
                self._fetchall = [self._fetchone]
            else:
                self._fetchone = None
                self._fetchall = []
            return

        if normalized.startswith("UPDATE replay_jobs SET status = %s, updated_at = %s, completed_at = CASE"):
            (
                status,
                updated_at,
                completed_marker,
                completed_at,
                failed_marker,
                failed_at,
                cancelled_marker,
                cancelled_at,
                timed_out_marker,
                timed_out_at,
                lease_expires_at,
                heartbeat_at,
                last_error,
                terminal_reason,
                terminal_detail,
                replay_job_id,
                owner_token,
                lease_generation,
            ) = params
            job = self.conn.replay_jobs[replay_job_id]
            if job.get("owner_token") == owner_token and job.get("lease_generation") == lease_generation:
                job.update(
                    {
                        "status": status,
                        "updated_at": updated_at,
                        "completed_at": completed_at if completed_marker == "completed" else job["completed_at"],
                        "failed_at": failed_at if failed_marker == "failed" else job["failed_at"],
                        "cancelled_at": cancelled_at if cancelled_marker == "cancelled" else job.get("cancelled_at"),
                        "timed_out_at": timed_out_at if timed_out_marker == "timed_out" else job.get("timed_out_at"),
                        "lease_expires_at": lease_expires_at,
                        "heartbeat_at": heartbeat_at,
                        "last_error": last_error,
                        "terminal_reason": terminal_reason,
                        "terminal_detail": terminal_detail,
                    }
                )
                self._fetchone = self.conn.replay_job_tuple(job)
            else:
                self._fetchone = None
            self._fetchall = [self._fetchone]
            return

        if normalized.startswith("UPDATE replay_jobs SET status = 'cancelled'"):
            updated_at = params[0]
            now = params[-1]
            if "status = 'requested'" in normalized:
                candidates = [
                    job for job in self.conn.replay_jobs.values() if job["status"] == "requested" and job.get("cancel_requested_at") is not None
                ]
                for job in candidates:
                    job.update(
                        {
                            "status": "cancelled",
                            "updated_at": updated_at,
                            "cancelled_at": job.get("cancelled_at") or params[1],
                            "terminal_reason": job.get("terminal_reason") or "cancelled",
                            "terminal_detail": job.get("terminal_detail") or "cancellation requested before replay claim",
                            "lease_expires_at": params[2],
                            "heartbeat_at": params[3],
                        }
                    )
                self._fetchall = [self.conn.replay_job_tuple(job) for job in candidates]
                self._fetchone = self._fetchall[0] if self._fetchall else None
                return
            candidates = [
                job
                for job in self.conn.replay_jobs.values()
                if job["status"] == "running"
                and job.get("cancel_requested_at") is not None
                and job.get("lease_expires_at") is not None
                and job["lease_expires_at"] < now
            ]
            for job in candidates:
                job.update(
                    {
                        "status": "cancelled",
                        "updated_at": updated_at,
                        "cancelled_at": job.get("cancelled_at") or params[1],
                        "terminal_reason": job.get("terminal_reason") or "cancelled",
                        "terminal_detail": job.get("terminal_detail") or "cancelled after runner lease expiry",
                        "lease_expires_at": params[2],
                        "heartbeat_at": params[3],
                    }
                )
            self._fetchall = [self.conn.replay_job_tuple(job) for job in candidates]
            self._fetchone = self._fetchall[0] if self._fetchall else None
            return

        if normalized.startswith("UPDATE replay_jobs SET status = 'timed_out'"):
            updated_at, timed_out_at, lease_expires_at, heartbeat_at, now = params
            candidates = [
                job
                for job in self.conn.replay_jobs.values()
                if job["status"] in {"requested", "running"}
                and job.get("deadline_at") is not None
                and job["deadline_at"] < now
            ]
            for job in candidates:
                job.update(
                    {
                        "status": "timed_out",
                        "updated_at": updated_at,
                        "timed_out_at": job.get("timed_out_at") or timed_out_at,
                        "terminal_reason": job.get("terminal_reason") or "deadline_exceeded",
                        "terminal_detail": job.get("terminal_detail") or "replay job deadline exceeded",
                        "lease_expires_at": lease_expires_at,
                        "heartbeat_at": heartbeat_at,
                    }
                )
            self._fetchall = [self.conn.replay_job_tuple(job) for job in candidates]
            self._fetchone = self._fetchall[0] if self._fetchall else None
            return

        if normalized.startswith("INSERT INTO operator_audit_log"):
            self.conn.audit_log.append(
                {
                    "action": params[0],
                    "actor": params[1],
                    "target_type": params[2],
                    "target_id": params[3],
                    "metadata": self.conn.json_loads(params[4]),
                    "created_at": params[5],
                }
            )
            self._fetchone = None
            self._fetchall = []
            return

        raise AssertionError(f"Unexpected query: {normalized}")

    def fetchone(self):
        return self._fetchone

    def fetchall(self):
        return self._fetchall

    def __enter__(self) -> "FakeReplayCursor":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None


class FakeReplayConnection:
    def __init__(self) -> None:
        self.ingest_log: list[dict] = []
        self.ingest_row_map: dict[int, dict] = {}
        self.dlq_events: list[dict] = []
        self.event_processing: dict[str, dict] = {}
        self.processed_events: dict[str, datetime] = {}
        self.replay_jobs: dict[str, dict] = {}
        self.replay_job_events: list[dict] = []
        self.audit_log: list[dict] = []

    def cursor(self) -> FakeReplayCursor:
        return FakeReplayCursor(self)

    @staticmethod
    def json_loads(value):
        if isinstance(value, dict):
            return value
        import json

        return json.loads(value)

    @staticmethod
    def make_processing_row(**kwargs):
        return dict(kwargs)

    @staticmethod
    def processing_tuple(row: dict | None):
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

    @staticmethod
    def replay_job_tuple(job: dict):
        return (
            job["replay_job_id"],
            job["job_type"],
            job["selector_type"],
            job["selector"],
            job["source_type"],
            job["status"],
            job["requested_by"],
            job["requested_at"],
            job["started_at"],
            job["completed_at"],
            job["failed_at"],
            job["updated_at"],
            job["lease_expires_at"],
            job.get("heartbeat_at"),
            job.get("cancel_requested_at"),
            job.get("cancelled_at"),
            job.get("deadline_at"),
            job.get("timed_out_at"),
            job.get("terminal_reason"),
            job.get("terminal_detail"),
            job["attempt_count"],
            job["total_events"],
            job["published_events"],
            job["completed_events"],
            job["failed_events"],
            job.get("skipped_events", 0),
            job["last_error"],
            job.get("owner_token"),
            job.get("lease_generation", 0),
        )

    @staticmethod
    def replay_job_event_tuple(row: dict):
        return (
            row["replay_job_id"],
            row["event_id"],
            row["source_type"],
            row["source_row_id"],
            row["event_payload"],
            row["status"],
            row["published_at"],
            row["completed_at"],
            row["failed_at"],
            row["updated_at"],
            row["last_error"],
            row["last_observed_processing_status"],
        )


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
        "replay_poll_seconds": 0.01,
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
def replay_module(load_service_module, monkeypatch):
    module = load_service_module(
        "mini_platform_replay_runner",
        "services/worker/app/replay_runner.py",
    )
    monkeypatch.setattr(module.time, "sleep", lambda _seconds: None)
    return module


def test_stale_claimed_row_can_be_reclaimed_and_replayed(replay_module) -> None:
    conn = FakeReplayConnection()
    now = datetime.now(timezone.utc)
    conn.ingest_log.append(
        {"id": 1, "event_id": "evt-1", "event_time": now, "payload": dict(EVENT)}
    )
    conn.ingest_row_map[1] = conn.ingest_log[0]
    conn.event_processing["evt-1"] = conn.make_processing_row(
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
    conn.replay_jobs["job-1"] = {
        "replay_job_id": "job-1",
        "job_type": "replay",
        "selector_type": "event_id",
        "selector": {"event_id": "evt-1"},
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
    producer = FakeProducer(conn, outcome="completed")
    settings = _make_settings(replay_module)

    claimed = replay_module._claim_next_replay_job(conn, now, settings.replay_lease_timeout)
    finalized = replay_module.process_replay_job(
        claimed,
        settings,
        conn,
        producer,
        replay_module.configure_json_logger("replay-test", "INFO"),
    )

    assert len(producer.messages) == 1
    assert finalized.status == "completed"
    assert conn.replay_job_events[0]["status"] == "completed"
    assert conn.audit_log[-1]["action"] == "replay_completed"


def test_concurrent_replay_runner_claim_attempt_is_safe(replay_module) -> None:
    conn = FakeReplayConnection()
    now = datetime.now(timezone.utc)
    conn.replay_jobs["job-claim"] = {
        "replay_job_id": "job-claim",
        "job_type": "replay",
        "selector_type": "event_id",
        "selector": {"event_id": "evt-1"},
        "source_type": "ingest_log",
        "status": "requested",
        "requested_by": "operator-api",
        "requested_at": now,
        "started_at": None,
        "completed_at": None,
        "failed_at": None,
        "updated_at": now,
        "lease_expires_at": None,
        "heartbeat_at": None,
        "cancel_requested_at": None,
        "cancelled_at": None,
        "deadline_at": now + timedelta(minutes=10),
        "timed_out_at": None,
        "terminal_reason": None,
        "terminal_detail": None,
        "attempt_count": 0,
        "total_events": 0,
        "published_events": 0,
        "completed_events": 0,
        "failed_events": 0,
        "skipped_events": 0,
        "last_error": None,
        "owner_token": None,
        "lease_generation": 0,
    }
    settings = _make_settings(replay_module)

    first = replay_module._claim_next_replay_job(conn, now, settings.replay_lease_timeout, owner_token="runner-a")
    second = replay_module._claim_next_replay_job(conn, now, settings.replay_lease_timeout, owner_token="runner-b")

    assert first is not None
    assert first.owner_token == "runner-a"
    assert first.lease_generation == 1
    assert second is None


def test_completed_event_is_skipped_without_duplicate_publish(replay_module) -> None:
    conn = FakeReplayConnection()
    now = datetime.now(timezone.utc)
    conn.ingest_log.append(
        {"id": 1, "event_id": "evt-1", "event_time": now, "payload": dict(EVENT)}
    )
    conn.ingest_row_map[1] = conn.ingest_log[0]
    conn.event_processing["evt-1"] = conn.make_processing_row(
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
    conn.replay_jobs["job-1"] = {
        "replay_job_id": "job-1",
        "job_type": "replay",
        "selector_type": "event_id",
        "selector": {"event_id": "evt-1"},
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
    producer = FakeProducer(conn, outcome="completed")
    settings = _make_settings(replay_module)

    claimed = replay_module._claim_next_replay_job(conn, now, settings.replay_lease_timeout)
    finalized = replay_module.process_replay_job(
        claimed,
        settings,
        conn,
        producer,
        replay_module.configure_json_logger("replay-test", "INFO"),
    )

    assert finalized.status == "completed"
    assert producer.messages == []
    assert conn.replay_job_events[0]["status"] == "skipped"


def test_redrive_failure_is_recorded_and_observable(replay_module) -> None:
    conn = FakeReplayConnection()
    now = datetime.now(timezone.utc)
    conn.dlq_events.append(
        {"id": 5, "event_id": "evt-1", "payload": dict(EVENT), "failed_at": now}
    )
    conn.replay_jobs["job-1"] = {
        "replay_job_id": "job-1",
        "job_type": "redrive",
        "selector_type": "dlq_event",
        "selector": {"dlq_event_id": 5, "event_id": "evt-1"},
        "source_type": "dlq_events",
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
    producer = FakeProducer(conn, outcome="failed")
    settings = _make_settings(replay_module)

    claimed = replay_module._claim_next_replay_job(conn, now, settings.replay_lease_timeout)
    finalized = replay_module.process_replay_job(
        claimed,
        settings,
        conn,
        producer,
        replay_module.configure_json_logger("replay-test", "INFO"),
    )

    assert finalized.status == "failed"
    assert finalized.last_error == "redrive failed"
    assert conn.replay_job_events[0]["status"] == "failed"
    assert conn.audit_log[-1]["action"] == "redrive_failed"


def test_cancelled_job_stops_without_publishing(replay_module) -> None:
    conn = FakeReplayConnection()
    now = datetime.now(timezone.utc)
    conn.ingest_log.append({"id": 1, "event_id": "evt-cancel", "event_time": now, "payload": {**EVENT, "event_id": "evt-cancel"}})
    conn.ingest_row_map[1] = conn.ingest_log[0]
    conn.replay_jobs["job-cancel"] = {
        "replay_job_id": "job-cancel",
        "job_type": "replay",
        "selector_type": "event_id",
        "selector": {"event_id": "evt-cancel"},
        "source_type": "ingest_log",
        "status": "running",
        "requested_by": "operator-api",
        "requested_at": now,
        "started_at": now,
        "completed_at": None,
        "failed_at": None,
        "updated_at": now,
        "lease_expires_at": now + timedelta(seconds=30),
        "heartbeat_at": now,
        "cancel_requested_at": now,
        "cancelled_at": None,
        "deadline_at": now + timedelta(minutes=10),
        "timed_out_at": None,
        "terminal_reason": None,
        "terminal_detail": None,
        "attempt_count": 1,
        "total_events": 0,
        "published_events": 0,
        "completed_events": 0,
        "failed_events": 0,
        "skipped_events": 0,
        "last_error": None,
        "owner_token": "runner-a",
        "lease_generation": 1,
    }
    producer = FakeProducer(conn, outcome="completed")
    settings = _make_settings(replay_module)

    result = replay_module.process_replay_job(
        replay_module._load_replay_job(conn, "job-cancel"),
        settings,
        conn,
        producer,
        replay_module.configure_json_logger("replay-test", "INFO"),
    )

    assert result.status == "cancelled"
    assert producer.messages == []


def test_sweeper_marks_timed_out_jobs(replay_module) -> None:
    conn = FakeReplayConnection()
    now = datetime.now(timezone.utc)
    conn.replay_jobs["job-timeout"] = {
        "replay_job_id": "job-timeout",
        "job_type": "replay",
        "selector_type": "event_id",
        "selector": {"event_id": "evt-timeout"},
        "source_type": "ingest_log",
        "status": "running",
        "requested_by": "operator-api",
        "requested_at": now - timedelta(minutes=20),
        "started_at": now - timedelta(minutes=20),
        "completed_at": None,
        "failed_at": None,
        "updated_at": now - timedelta(minutes=20),
        "lease_expires_at": now - timedelta(minutes=10),
        "heartbeat_at": now - timedelta(minutes=10),
        "cancel_requested_at": None,
        "cancelled_at": None,
        "deadline_at": now - timedelta(minutes=1),
        "timed_out_at": None,
        "terminal_reason": None,
        "terminal_detail": None,
        "attempt_count": 1,
        "total_events": 0,
        "published_events": 0,
        "completed_events": 0,
        "failed_events": 0,
        "skipped_events": 0,
        "last_error": None,
        "owner_token": "runner-a",
        "lease_generation": 1,
    }

    swept = replay_module._sweep_replay_jobs(conn, now)

    assert swept[0].status == "timed_out"
    assert conn.replay_jobs["job-timeout"]["terminal_reason"] == "deadline_exceeded"
    assert conn.audit_log[-1]["action"] == "replay_timed_out"


def test_time_range_replay_materializes_multiple_events_once(replay_module) -> None:
    conn = FakeReplayConnection()
    start = datetime.now(timezone.utc) - timedelta(minutes=5)
    first_time = start + timedelta(minutes=1)
    second_time = start + timedelta(minutes=2)
    conn.ingest_log.extend(
        [
            {"id": 1, "event_id": "evt-1", "event_time": first_time, "payload": {**EVENT, "event_id": "evt-1"}},
            {"id": 2, "event_id": "evt-2", "event_time": second_time, "payload": {**EVENT, "event_id": "evt-2"}},
        ]
    )
    conn.ingest_row_map = {row["id"]: row for row in conn.ingest_log}
    conn.replay_jobs["job-1"] = {
        "replay_job_id": "job-1",
        "job_type": "replay",
        "selector_type": "time_range",
        "selector": {"start_time": start.isoformat(), "end_time": (start + timedelta(minutes=3)).isoformat()},
        "source_type": "ingest_log",
        "status": "requested",
        "requested_by": "operator-api",
        "requested_at": start,
        "started_at": None,
        "completed_at": None,
        "failed_at": None,
        "updated_at": start,
        "lease_expires_at": None,
        "attempt_count": 0,
        "total_events": 0,
        "published_events": 0,
        "completed_events": 0,
        "failed_events": 0,
        "last_error": None,
    }
    producer = FakeProducer(conn, outcome="completed")
    settings = _make_settings(replay_module)

    claimed = replay_module._claim_next_replay_job(conn, start, settings.replay_lease_timeout)
    finalized = replay_module.process_replay_job(
        claimed,
        settings,
        conn,
        producer,
        replay_module.configure_json_logger("replay-test", "INFO"),
    )

    assert finalized.status == "completed"
    assert finalized.total_events == 2
    assert len(producer.messages) == 2
