from __future__ import annotations

import json
from datetime import datetime, timezone

from fastapi.testclient import TestClient


VALID_PAYLOAD = {
    "schema_version": 1,
    "event_type": "order_created",
    "event_time": "2026-01-27T12:00:00Z",
    "order_id": "O-1",
    "amount": 10.5,
    "currency": "USD",
    "customer_id": "C-1",
}

BASE_ENV = {
    "APP_ENV": "local",
    "KAFKA_TOPIC": "events.raw",
    "KAFKA_BOOTSTRAP_SERVERS": "redpanda:9092",
    "POSTGRES_DSN": "dbname=bd06 user=bd06 password=bd06 host=postgres port=5432",
    "INGEST_AUTH_ENABLED": "true",
    "INGEST_API_KEYS": "local-ingest:local-demo-ingest-key,rotated-ingest:local-demo-ingest-key-2",
    "OPERATOR_API_KEYS": "local-ops:local-demo-ops-key,rotated-ops:local-demo-ops-key-2",
    "INGEST_ALLOW_INTERACTIVE_DOCS": "true",
    "INGEST_MAX_REQUEST_BYTES": "16384",
    "REPLAY_JOB_TIMEOUT_SECONDS": "600",
    "LOG_LEVEL": "INFO",
    "APP_VERSION": "1.2.3",
    "APP_BUILD_SHA": "abc1234",
    "APP_BUILD_TIME": "2026-03-14T00:00:00Z",
}

INGEST_HEADERS = {"X-API-Key-Id": "local-ingest", "X-API-Key": "local-demo-ingest-key"}
INGEST_ROTATED_HEADERS = {"X-API-Key-Id": "rotated-ingest", "X-API-Key": "local-demo-ingest-key-2"}
OPERATOR_HEADERS = {"X-API-Key-Id": "local-ops", "X-API-Key": "local-demo-ops-key"}
OPERATOR_ROTATED_HEADERS = {"X-API-Key-Id": "rotated-ops", "X-API-Key": "local-demo-ops-key-2"}


class FakeProducer:
    def __init__(self, *, connected: bool = True) -> None:
        self.connected = connected
        self.messages: list[tuple[str, dict]] = []
        self.flush_calls = 0
        self.closed = False

    def send(self, topic: str, value: dict) -> None:
        self.messages.append((topic, value))

    def flush(self, timeout: int | None = None) -> None:
        self.flush_calls += 1

    def close(self) -> None:
        self.closed = True

    def bootstrap_connected(self) -> bool:
        return self.connected


class FakePostgresCursor:
    def __init__(self, conn: "FakePostgresConnection") -> None:
        self.conn = conn
        self._fetchone = None
        self._fetchall = []

    def execute(self, query: str, params=None) -> None:
        normalized = " ".join(query.split())

        if normalized == "SELECT 1":
            if not self.conn.healthy:
                raise RuntimeError("postgres unavailable")
            self._fetchone = (1,)
            self._fetchall = [(1,)]
            return

        if normalized.startswith("INSERT INTO ingest_log"):
            event_id, received_at, event_type, schema_version, event_time, payload = params
            self.conn.ingest_log.append(
                {
                    "id": len(self.conn.ingest_log) + 1,
                    "event_id": event_id,
                    "received_at": received_at,
                    "event_type": event_type,
                    "schema_version": schema_version,
                    "event_time": event_time,
                    "payload": json.loads(payload),
                }
            )
            self._fetchone = None
            self._fetchall = []
            return

        if normalized == "SELECT COUNT(*) FROM ingest_log":
            self._fetchone = (len(self.conn.ingest_log),)
            self._fetchall = [self._fetchone]
            return

        if normalized == "SELECT COUNT(*) FROM ingest_rejections":
            self._fetchone = (len(self.conn.ingest_rejections),)
            self._fetchall = [self._fetchone]
            return

        if normalized == "SELECT COUNT(*) FROM processed_events":
            self._fetchone = (len(self.conn.processed_events),)
            self._fetchall = [self._fetchone]
            return

        if normalized == "SELECT COUNT(*) FROM dlq_events":
            self._fetchone = (len(self.conn.dlq_events),)
            self._fetchall = [self._fetchone]
            return

        if normalized == "SELECT COUNT(*) FROM event_processing WHERE status IN ('claimed', 'storage_written', 'analytics_written')":
            count = sum(
                1
                for row in self.conn.event_processing.values()
                if row["status"] in {"claimed", "storage_written", "analytics_written"}
            )
            self._fetchone = (count,)
            self._fetchall = [self._fetchone]
            return

        if normalized == "SELECT COUNT(*) FROM event_processing WHERE status = 'failed'":
            count = sum(1 for row in self.conn.event_processing.values() if row["status"] == "failed")
            self._fetchone = (count,)
            self._fetchall = [self._fetchone]
            return

        if "COUNT(*) FILTER (WHERE status = 'requested')" in normalized:
            counts = {
                "requested": 0,
                "running": 0,
                "completed": 0,
                "failed": 0,
                "cancelled": 0,
                "timed_out": 0,
            }
            for job in self.conn.replay_jobs.values():
                counts[job["status"]] += 1
            self._fetchone = (
                counts["requested"],
                counts["running"],
                counts["completed"],
                counts["failed"],
                counts["cancelled"],
                counts["timed_out"],
            )
            self._fetchall = [self._fetchone]
            return

        if normalized.startswith("INSERT INTO ingest_rejections"):
            self.conn.ingest_rejections.append(
                {
                    "id": len(self.conn.ingest_rejections) + 1,
                    "path": params[0],
                    "status_code": params[1],
                    "reason": params[2],
                    "detail": json.loads(params[3]),
                    "rejected_at": params[4],
                }
            )
            self._fetchone = None
            self._fetchall = []
            return

        if normalized.startswith("INSERT INTO operator_audit_log"):
            self.conn.audit_log.append(
                {
                    "id": len(self.conn.audit_log) + 1,
                    "action": params[0],
                    "actor": params[1],
                    "target_type": params[2],
                    "target_id": params[3],
                    "metadata": json.loads(params[4]),
                    "created_at": params[5],
                }
            )
            self._fetchone = None
            self._fetchall = []
            return

        if normalized.startswith("INSERT INTO replay_jobs"):
            selector = json.loads(params[3])
            job = {
                "replay_job_id": params[0],
                "job_type": params[1],
                "selector_type": params[2],
                "selector": selector,
                "source_type": params[4],
                "status": "requested",
                "requested_by": params[5],
                "requested_at": params[6],
                "started_at": None,
                "completed_at": None,
                "failed_at": None,
                "updated_at": params[7],
                "lease_expires_at": None,
                "heartbeat_at": None,
                "cancel_requested_at": None,
                "cancelled_at": None,
                "deadline_at": params[8],
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
            self.conn.replay_jobs[job["replay_job_id"]] = job
            self._fetchone = self.conn.replay_job_tuple(job)
            self._fetchall = [self._fetchone]
            return

        if normalized.startswith("UPDATE replay_jobs SET status = CASE WHEN status = 'requested' THEN 'cancelled'"):
            requested_at, cancelled_at, updated_at, reason, replay_job_id = params
            job = self.conn.replay_jobs.get(replay_job_id)
            if job is None or job["status"] not in {"requested", "running"}:
                self._fetchone = None
                self._fetchall = []
                return
            if job["status"] == "requested":
                job["status"] = "cancelled"
                job["cancelled_at"] = job["cancelled_at"] or cancelled_at
                job["terminal_reason"] = "cancelled"
                job["terminal_detail"] = reason or job["terminal_detail"]
            job["cancel_requested_at"] = job["cancel_requested_at"] or requested_at
            job["updated_at"] = updated_at
            self._fetchone = self.conn.replay_job_tuple(job)
            self._fetchall = [self._fetchone]
            return

        if normalized.startswith("SELECT replay_job_id, job_type, selector_type, selector"):
            job = self.conn.replay_jobs.get(params[0])
            self._fetchone = self.conn.replay_job_tuple(job) if job else None
            self._fetchall = [self._fetchone] if self._fetchone else []
            return

        if normalized.startswith("SELECT event_id, source_type, source_row_id, status, published_at, completed_at"):
            rows = [
                self.conn.replay_job_event_tuple(event)
                for event in self.conn.replay_job_events
                if event["replay_job_id"] == params[0]
            ]
            self._fetchall = rows
            self._fetchone = rows[0] if rows else None
            return

        if normalized.startswith("SELECT id, action, actor, target_type, target_id, metadata, created_at FROM operator_audit_log"):
            rows = [
                self.conn.audit_tuple(entry)
                for entry in self.conn.audit_log
                if entry["target_type"] == params[0] and entry["target_id"] == params[1]
            ]
            rows.sort(key=lambda row: row[6], reverse=True)
            self._fetchall = rows
            self._fetchone = rows[0] if rows else None
            return

        if normalized.startswith("SELECT id, event_id, error, payload, failed_at FROM dlq_events WHERE id ="):
            row = next((item for item in self.conn.dlq_events if item["id"] == params[0]), None)
            self._fetchone = self.conn.dlq_tuple(row) if row else None
            self._fetchall = [self._fetchone] if self._fetchone else []
            return

        if normalized.startswith("SELECT id, event_id, error, failed_at FROM dlq_events ORDER BY failed_at DESC LIMIT"):
            rows = sorted(self.conn.dlq_events, key=lambda row: row["failed_at"], reverse=True)[: params[0]]
            tuples = [(row["id"], row["event_id"], row["error"], row["failed_at"]) for row in rows]
            self._fetchall = tuples
            self._fetchone = tuples[0] if tuples else None
            return

        if normalized.startswith("SELECT event_id, status, claimed_at, lease_expires_at"):
            event_id = params[0]
            row = self.conn.event_processing.get(event_id)
            self._fetchone = self.conn.processing_tuple(row) if row else None
            self._fetchall = [self._fetchone] if self._fetchone else []
            return

        if normalized.startswith("SELECT rje.replay_job_id, rj.job_type, rje.status, rj.selector_type"):
            rows = []
            for event in self.conn.replay_job_events:
                if event["event_id"] != params[0]:
                    continue
                job = self.conn.replay_jobs[event["replay_job_id"]]
                rows.append(
                    (
                        event["replay_job_id"],
                        job["job_type"],
                        event["status"],
                        job["selector_type"],
                        event["source_type"],
                        event["published_at"],
                        event["completed_at"],
                        event["failed_at"],
                        event["last_error"],
                        event["last_observed_processing_status"],
                        job["terminal_reason"],
                        job["terminal_detail"],
                    )
                )
            rows.sort(key=lambda row: row[5] or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
            self._fetchall = rows
            self._fetchone = rows[0] if rows else None
            return

        if normalized.startswith("SELECT event_id, received_at, event_type, schema_version, event_time, payload FROM ingest_log WHERE event_id ="):
            row = next((item for item in self.conn.ingest_log if item["event_id"] == params[0]), None)
            if row is None:
                self._fetchone = None
                self._fetchall = []
            else:
                self._fetchone = (
                    row["event_id"],
                    row["received_at"],
                    row["event_type"],
                    row["schema_version"],
                    row["event_time"],
                    row["payload"],
                )
                self._fetchall = [self._fetchone]
            return

        if normalized.startswith("SELECT processed_at FROM processed_events WHERE event_id ="):
            processed_at = self.conn.processed_events.get(params[0])
            self._fetchone = (processed_at,) if processed_at else None
            self._fetchall = [self._fetchone] if self._fetchone else []
            return

        if normalized.startswith("SELECT id, error, payload, failed_at FROM dlq_events WHERE event_id ="):
            rows = [
                (row["id"], row["error"], row["payload"], row["failed_at"])
                for row in self.conn.dlq_events
                if row["event_id"] == params[0]
            ]
            rows.sort(key=lambda row: row[3], reverse=True)
            self._fetchall = rows
            self._fetchone = rows[0] if rows else None
            return

        raise AssertionError(f"Unexpected query: {normalized}")

    def fetchone(self):
        return self._fetchone

    def fetchall(self):
        return self._fetchall

    def __enter__(self) -> "FakePostgresCursor":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None


class FakePostgresConnection:
    def __init__(self, *, healthy: bool = True) -> None:
        self.healthy = healthy
        self.ingest_log: list[dict] = []
        self.ingest_rejections: list[dict] = []
        self.processed_events: dict[str, datetime] = {}
        self.event_processing: dict[str, dict] = {}
        self.dlq_events: list[dict] = []
        self.replay_jobs: dict[str, dict] = {}
        self.replay_job_events: list[dict] = []
        self.audit_log: list[dict] = []
        self.closed = False

    def cursor(self) -> FakePostgresCursor:
        return FakePostgresCursor(self)

    def close(self) -> None:
        self.closed = True

    @staticmethod
    def replay_job_tuple(job: dict | None):
        if job is None:
            return None
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
            job["total_events"],
            job["published_events"],
            job["completed_events"],
            job["failed_events"],
            job["skipped_events"],
            job["lease_expires_at"],
            job["heartbeat_at"],
            job["cancel_requested_at"],
            job["cancelled_at"],
            job["deadline_at"],
            job["timed_out_at"],
            job["terminal_reason"],
            job["terminal_detail"],
            job["last_error"],
            job["attempt_count"],
            job["lease_generation"],
        )

    @staticmethod
    def replay_job_legacy_tuple(job: dict | None):
        if job is None:
            return None
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
            job["total_events"],
            job["published_events"],
            job["completed_events"],
            job["failed_events"],
            job["last_error"],
        )

    @staticmethod
    def replay_job_event_tuple(event: dict):
        return (
            event["event_id"],
            event["source_type"],
            event["source_row_id"],
            event["status"],
            event["published_at"],
            event["completed_at"],
            event["failed_at"],
            event["updated_at"],
            event["last_error"],
            event["last_observed_processing_status"],
        )

    @staticmethod
    def audit_tuple(entry: dict):
        return (
            entry["id"],
            entry["action"],
            entry["actor"],
            entry["target_type"],
            entry["target_id"],
            entry["metadata"],
            entry["created_at"],
        )

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
    def dlq_tuple(row: dict | None):
        if row is None:
            return None
        return (row["id"], row["event_id"], row["error"], row["payload"], row["failed_at"])


def _load_ingest_module(monkeypatch, load_service_module, **env_overrides):
    env = {**BASE_ENV, **env_overrides}
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    return load_service_module("mini_platform_ingest_main", "services/ingest-api/app/main.py")


def _build_app(monkeypatch, load_service_module, *, producer=None, pg_conn=None, **env_overrides):
    module = _load_ingest_module(monkeypatch, load_service_module, **env_overrides)
    producer = producer or FakeProducer()
    pg_conn = pg_conn or FakePostgresConnection()

    monkeypatch.setattr(module, "_make_producer", lambda _bootstrap: producer)
    monkeypatch.setattr(module, "_connect_postgres", lambda _dsn: pg_conn)
    return module.create_app(), producer, pg_conn, module


def test_authenticated_ingest_succeeds(monkeypatch, load_service_module) -> None:
    app, producer, pg_conn, _ = _build_app(monkeypatch, load_service_module)

    with TestClient(app) as client:
        response = client.post("/ingest", json=VALID_PAYLOAD, headers=INGEST_HEADERS)

    assert response.status_code == 202
    body = response.json()
    assert body["status"] == "accepted"
    assert body["event_id"]
    assert len(producer.messages) == 1
    assert producer.messages[0][1]["schema_version"] == 1
    assert len(pg_conn.ingest_log) == 1
    assert pg_conn.ingest_log[0]["schema_version"] == 1


def test_missing_api_key_fails(monkeypatch, load_service_module) -> None:
    app, _, _, _ = _build_app(monkeypatch, load_service_module)

    with TestClient(app) as client:
        response = client.post("/ingest", json=VALID_PAYLOAD)

    assert response.status_code == 401
    assert response.json()["detail"] == "Missing API key id"


def test_invalid_api_key_fails(monkeypatch, load_service_module) -> None:
    app, _, _, _ = _build_app(monkeypatch, load_service_module)

    with TestClient(app) as client:
        response = client.post(
            "/ingest",
            json=VALID_PAYLOAD,
            headers={"X-API-Key-Id": "local-ingest", "X-API-Key": "wrong"},
        )

    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid API key"


def test_ingest_key_cannot_access_operator_endpoints(monkeypatch, load_service_module) -> None:
    app, _, _, _ = _build_app(monkeypatch, load_service_module)

    with TestClient(app) as client:
        response = client.get("/ops/telemetry", headers=INGEST_HEADERS)

    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid API key"


def test_operator_endpoint_requires_operator_key(monkeypatch, load_service_module) -> None:
    app, _, _, _ = _build_app(monkeypatch, load_service_module)

    with TestClient(app) as client:
        response = client.get("/ops/telemetry")

    assert response.status_code == 401
    assert response.json()["detail"] == "Missing API key id"


def test_rotated_keys_work_during_overlap_window(monkeypatch, load_service_module) -> None:
    app, producer, _, _ = _build_app(monkeypatch, load_service_module)

    with TestClient(app) as client:
        ingest_response = client.post("/ingest", json=VALID_PAYLOAD, headers=INGEST_ROTATED_HEADERS)
        ops_response = client.get("/ops/telemetry", headers=OPERATOR_ROTATED_HEADERS)

    assert ingest_response.status_code == 202
    assert ops_response.status_code == 200
    assert len(producer.messages) == 1


def test_retired_key_is_rejected_after_rotation(monkeypatch, load_service_module) -> None:
    app, _, _, _ = _build_app(
        monkeypatch,
        load_service_module,
        INGEST_API_KEYS="rotated-ingest:local-demo-ingest-key-2",
        OPERATOR_API_KEYS="rotated-ops:local-demo-ops-key-2",
    )

    with TestClient(app) as client:
        ingest_response = client.post("/ingest", json=VALID_PAYLOAD, headers=INGEST_HEADERS)
        ops_response = client.get("/ops/telemetry", headers=OPERATOR_HEADERS)

    assert ingest_response.status_code == 403
    assert ops_response.status_code == 403


def test_local_mode_keeps_docs_enabled(monkeypatch, load_service_module) -> None:
    app, _, _, _ = _build_app(monkeypatch, load_service_module, APP_ENV="local", INGEST_ALLOW_INTERACTIVE_DOCS="true")

    with TestClient(app) as client:
        response = client.get("/docs")

    assert response.status_code == 200
    assert app.docs_url == "/docs"


def test_docs_are_disabled_in_production(monkeypatch, load_service_module) -> None:
    app, _, _, _ = _build_app(
        monkeypatch,
        load_service_module,
        APP_ENV="production",
        POSTGRES_DSN="dbname=bd06 user=bd06 password=StrongPass123 host=postgres port=5432",
        INGEST_API_KEYS="prod-ingest:StrongIngestApiKey123",
        OPERATOR_API_KEYS="prod-ops:StrongOpsApiKey123",
        INGEST_ALLOW_INTERACTIVE_DOCS="false",
    )

    with TestClient(app) as client:
        docs_response = client.get("/docs")
        openapi_response = client.get("/openapi.json")

    assert app.docs_url is None
    assert docs_response.status_code == 404
    assert openapi_response.status_code == 404


def test_production_settings_reject_insecure_defaults(monkeypatch, load_service_module) -> None:
    try:
        _load_ingest_module(
            monkeypatch,
            load_service_module,
            APP_ENV="production",
            POSTGRES_DSN="dbname=bd06 user=bd06 password=bd06password host=postgres port=5432",
            INGEST_API_KEYS="prod-ingest:local-demo-ingest-key",
            OPERATOR_API_KEYS="prod-ops:StrongOpsApiKey123",
            INGEST_ALLOW_INTERACTIVE_DOCS="false",
        )
    except ValueError as exc:
        assert "insecure" in str(exc)
    else:
        raise AssertionError("Expected production settings validation to fail")


def test_ingest_rejects_request_body_over_limit(monkeypatch, load_service_module) -> None:
    app, _, pg_conn, _ = _build_app(monkeypatch, load_service_module, INGEST_MAX_REQUEST_BYTES="32")

    with TestClient(app) as client:
        response = client.post(
            "/ingest",
            json=VALID_PAYLOAD,
            headers=INGEST_HEADERS,
        )

    assert response.status_code == 413
    assert response.json()["detail"] == "Request body too large"
    assert pg_conn.ingest_rejections[-1]["reason"] == "request_too_large"


def test_ingest_rejects_unknown_keys(monkeypatch, load_service_module) -> None:
    app, _, _, _ = _build_app(monkeypatch, load_service_module)

    with TestClient(app) as client:
        response = client.post(
            "/ingest",
            json={**VALID_PAYLOAD, "extra_field": "nope"},
            headers=INGEST_HEADERS,
        )

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"][-1] == "extra_field"


def test_ingest_rejects_invalid_timestamp(monkeypatch, load_service_module) -> None:
    app, _, _, _ = _build_app(monkeypatch, load_service_module)

    with TestClient(app) as client:
        response = client.post(
            "/ingest",
            json={**VALID_PAYLOAD, "event_time": "2026-01-27 12:00:00"},
            headers=INGEST_HEADERS,
        )

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"][-1] == "event_time"


def test_ingest_rejects_unsupported_schema_version(monkeypatch, load_service_module) -> None:
    app, _, _, _ = _build_app(monkeypatch, load_service_module)

    with TestClient(app) as client:
        response = client.post(
            "/ingest",
            json={**VALID_PAYLOAD, "schema_version": 2},
            headers=INGEST_HEADERS,
        )

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"][-1] == "schema_version"


def test_health_and_telemetry_are_machine_readable(monkeypatch, load_service_module) -> None:
    pg_conn = FakePostgresConnection()
    now = datetime(2026, 1, 27, 12, 0, tzinfo=timezone.utc)
    pg_conn.processed_events["evt-completed"] = now
    pg_conn.dlq_events.append(
        {"id": 1, "event_id": "evt-failed", "error": "boom", "payload": {"event_id": "evt-failed"}, "failed_at": now}
    )
    pg_conn.event_processing["evt-claimed"] = {
        "event_id": "evt-claimed",
        "status": "claimed",
        "claimed_at": now,
        "lease_expires_at": now,
        "updated_at": now,
        "storage_written_at": None,
        "analytics_written_at": None,
        "completed_at": None,
        "failed_at": None,
        "last_error": None,
        "attempt_count": 1,
    }
    pg_conn.event_processing["evt-failed"] = {
        "event_id": "evt-failed",
        "status": "failed",
        "claimed_at": now,
        "lease_expires_at": now,
        "updated_at": now,
        "storage_written_at": now,
        "analytics_written_at": None,
        "completed_at": None,
        "failed_at": now,
        "last_error": "boom",
        "attempt_count": 2,
    }
    app, _, pg_conn, _ = _build_app(monkeypatch, load_service_module, pg_conn=pg_conn)

    with TestClient(app) as client:
        accepted = client.post("/ingest", json=VALID_PAYLOAD, headers=INGEST_HEADERS)
        rejected = client.post("/ingest", json=VALID_PAYLOAD)
        health_response = client.get("/health")
        telemetry_response = client.get("/telemetry")
        ops_telemetry_response = client.get("/ops/telemetry", headers=OPERATOR_HEADERS)

    assert accepted.status_code == 202
    assert rejected.status_code == 401
    assert health_response.status_code == 200
    telemetry = telemetry_response.json()
    assert telemetry_response.status_code == 200
    assert telemetry["ingest"]["accepted_count"] == 1
    assert telemetry["ingest"]["rejected_count"] == 1
    assert telemetry["worker"]["completed_count"] == 1
    assert telemetry["worker"]["failed_count"] == 1
    assert telemetry["worker"]["in_progress_count"] == 1
    assert telemetry["worker"]["dlq_count"] == 1
    assert telemetry["release"]["version"] == "1.2.3"

    ops_telemetry = ops_telemetry_response.json()
    assert ops_telemetry_response.status_code == 200
    assert ops_telemetry["ingest"]["accepted_total"] == 1
    assert ops_telemetry["ingest"]["rejected_total"] == 1
    assert ops_telemetry["worker"]["completed_total"] == 1
    assert ops_telemetry["worker"]["failed_total"] == 1
    assert ops_telemetry["worker"]["dlq_backlog_count"] == 1
    assert ops_telemetry["release"]["build_sha"] == "abc1234"
    assert ops_telemetry["contracts"] == [
        {"event_type": "order_created", "schema_version": 1, "model": "OrderCreatedV1"}
    ]


def test_persisted_telemetry_survives_restart_equivalent(monkeypatch, load_service_module) -> None:
    pg_conn = FakePostgresConnection()

    app1, _, _, _ = _build_app(monkeypatch, load_service_module, pg_conn=pg_conn)
    with TestClient(app1) as client:
        accepted = client.post("/ingest", json=VALID_PAYLOAD, headers=INGEST_HEADERS)
        rejected = client.post("/ingest", json=VALID_PAYLOAD)
    assert accepted.status_code == 202
    assert rejected.status_code == 401

    app2, _, _, _ = _build_app(monkeypatch, load_service_module, pg_conn=pg_conn)
    with TestClient(app2) as client:
        response = client.get("/ops/telemetry", headers=OPERATOR_HEADERS)

    assert response.status_code == 200
    assert response.json()["ingest"]["accepted_total"] == 1
    assert response.json()["ingest"]["rejected_total"] == 1


def test_replay_job_creation_and_status_are_authenticated_and_durable(monkeypatch, load_service_module) -> None:
    pg_conn = FakePostgresConnection()
    now = datetime(2026, 1, 27, 12, 0, tzinfo=timezone.utc)
    pg_conn.ingest_log.append(
        {
            "id": 1,
            "event_id": "evt-ops",
            "received_at": now,
            "event_type": "order_created",
            "schema_version": 1,
            "event_time": now,
            "payload": {"event_id": "evt-ops", **VALID_PAYLOAD},
        }
    )
    app, _, pg_conn, _ = _build_app(monkeypatch, load_service_module, pg_conn=pg_conn)

    with TestClient(app) as client:
        unauthorized = client.post("/ops/replays", json={"selector_type": "event_id", "event_id": "evt-ops"})
        create_response = client.post(
            "/ops/replays",
            json={"selector_type": "event_id", "event_id": "evt-ops"},
            headers=OPERATOR_HEADERS,
        )

    assert unauthorized.status_code == 401
    assert create_response.status_code == 202
    replay_job_id = create_response.json()["replay_job_id"]
    assert replay_job_id in pg_conn.replay_jobs
    assert pg_conn.audit_log[-1]["action"] == "replay_requested"

    pg_conn.replay_job_events.append(
        {
            "replay_job_id": replay_job_id,
            "event_id": "evt-ops",
            "source_type": "ingest_log",
            "source_row_id": 1,
            "event_payload": {"event_id": "evt-ops", **VALID_PAYLOAD},
            "status": "published",
            "published_at": now,
            "completed_at": None,
            "failed_at": None,
            "updated_at": now,
            "last_error": None,
            "last_observed_processing_status": "claimed",
        }
    )

    with TestClient(app) as client:
        detail_response = client.get(f"/ops/replays/{replay_job_id}", headers=OPERATOR_HEADERS)

    assert detail_response.status_code == 200
    detail = detail_response.json()
    assert detail["replay_job"]["status"] == "requested"
    assert detail["events"][0]["event_id"] == "evt-ops"
    assert detail["audit"][0]["action"] == "replay_requested"


def test_replay_job_cancellation_is_auditable(monkeypatch, load_service_module) -> None:
    pg_conn = FakePostgresConnection()
    now = datetime(2026, 1, 27, 12, 0, tzinfo=timezone.utc)
    pg_conn.replay_jobs["job-cancel"] = {
        "replay_job_id": "job-cancel",
        "job_type": "replay",
        "selector_type": "event_id",
        "selector": {"event_id": "evt-cancel"},
        "source_type": "ingest_log",
        "status": "requested",
        "requested_by": "operator-key:local-ops",
        "requested_at": now,
        "started_at": None,
        "completed_at": None,
        "failed_at": None,
        "updated_at": now,
        "lease_expires_at": None,
        "heartbeat_at": None,
        "cancel_requested_at": None,
        "cancelled_at": None,
        "deadline_at": now,
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
    app, _, _, _ = _build_app(monkeypatch, load_service_module, pg_conn=pg_conn)

    with TestClient(app) as client:
        response = client.post(
            "/ops/replays/job-cancel/cancel",
            json={"reason": "operator abort"},
            headers=OPERATOR_HEADERS,
        )

    assert response.status_code == 202
    assert response.json()["status"] == "cancelled"
    assert pg_conn.replay_jobs["job-cancel"]["cancel_requested_at"] is not None
    assert any(entry["action"] == "replay_cancel_requested" for entry in pg_conn.audit_log)


def test_dlq_list_detail_and_redrive_request_are_available(monkeypatch, load_service_module) -> None:
    pg_conn = FakePostgresConnection()
    now = datetime(2026, 1, 27, 12, 0, tzinfo=timezone.utc)
    pg_conn.dlq_events.append(
        {
            "id": 7,
            "event_id": "evt-dlq",
            "error": "clickhouse timeout",
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
        "last_error": "clickhouse timeout",
        "attempt_count": 2,
    }
    app, _, pg_conn, _ = _build_app(monkeypatch, load_service_module, pg_conn=pg_conn)

    with TestClient(app) as client:
        list_response = client.get("/ops/dlq", headers=OPERATOR_HEADERS)
        detail_response = client.get("/ops/dlq/7", headers=OPERATOR_HEADERS)
        redrive_response = client.post("/ops/dlq/7/redrive", headers=OPERATOR_HEADERS)

    assert list_response.status_code == 200
    assert list_response.json()[0]["event_id"] == "evt-dlq"
    assert detail_response.status_code == 200
    assert detail_response.json()["processing_state"]["status"] == "failed"
    assert redrive_response.status_code == 202
    replay_job_id = redrive_response.json()["replay_job_id"]
    assert pg_conn.replay_jobs[replay_job_id]["job_type"] == "redrive"
    assert any(entry["action"] == "redrive_requested" for entry in pg_conn.audit_log)


def test_health_returns_503_when_postgres_check_fails(monkeypatch, load_service_module) -> None:
    app, _, _, _ = _build_app(monkeypatch, load_service_module, pg_conn=FakePostgresConnection(healthy=False))

    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 503
    assert response.json()["checks"]["postgres"]["status"] == "error"
