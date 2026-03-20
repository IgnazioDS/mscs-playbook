# Mini Platform (Phase 4 Scale / Productization)

The mini-platform remains the repository's only productization target. It is a production-like backend package for local Docker Compose and operator workflows, not a cloud-ready or customer-facing platform.

## Phase 4 Summary

What is now productized in-repo:
- schema-versioned ingest for `order_created` at `schema_version=1`
- scoped API-key auth with separate ingest and operator keys plus rotation overlap support
- authenticated `/ops/...` APIs for replay, cancellation, DLQ inspection, redrive, telemetry, and event lifecycle inspection
- fenced worker and replay-runner leases with owner tokens, lease generations, heartbeat renewal, and stale-owner takeover
- replay job cancellation, timeout handling, and stuck-job sweeping
- executable retention, backup, restore, load, and SLO scripts
- release metadata in logs and telemetry
- Makefile entrypoints and production-like env examples

Still not claimed:
- cloud deployment
- multi-tenancy
- billing
- full security platform completeness
- exactly-once distributed semantics

## Services

- `ingest-api`: strict ingest contract, scoped auth, health/readiness, telemetry, and `/ops`
- `worker`: fenced event lifecycle execution into MinIO and ClickHouse
- `replay-runner`: fenced replay/redrive execution, cancellation, timeout, and sweeping
- `postgres`: authoritative control-plane state
- `clickhouse`: analytics projection with tracked schema evolution
- `redpanda`: Kafka-compatible event bus
- `minio`: deterministic raw object storage

## Quickstart

Local compose:

```bash
make -C modules/06-big-data-architecture/03-implementations/mini-platform compose-config
make -C modules/06-big-data-architecture/03-implementations/mini-platform up-local
```

Health and telemetry:

```bash
curl -fsS http://localhost:8000/health
curl -fsS http://localhost:8000/ready
curl -fsS http://localhost:8000/telemetry
curl -fsS http://localhost:8000/ops/telemetry \
  -H "X-API-Key-Id: local-ops" \
  -H "X-API-Key: local-demo-ops-key"
```

Authenticated ingest:

```bash
curl -fsS -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -H "X-API-Key-Id: local-ingest" \
  -H "X-API-Key: local-demo-ingest-key" \
  -d '{"schema_version":1,"event_type":"order_created","event_time":"2026-01-27T12:00:00Z","order_id":"O-1","amount":10,"currency":"USD","customer_id":"C-1"}'
```

Authenticated replay request:

```bash
curl -fsS -X POST http://localhost:8000/ops/replays \
  -H "Content-Type: application/json" \
  -H "X-API-Key-Id: local-ops" \
  -H "X-API-Key: local-demo-ops-key" \
  -d '{"selector_type":"event_id","event_id":"<event-id>"}'
```

## Config and Packaging

Env examples:
- local: [`.env.local.example`](.env.local.example)
- production-like: [`.env.production.example`](.env.production.example)

Packaged command surface:
- [Makefile](Makefile)
- [docker-compose.yml](docker-compose.yml)
- [RELEASE-ROLLBACK.md](RELEASE-ROLLBACK.md)

Important env knobs:
- `APP_ENV=local|test|production`
- `APP_VERSION`
- `APP_BUILD_SHA`
- `APP_BUILD_TIME`
- `INGEST_API_KEYS`
- `OPERATOR_API_KEYS`
- `REPLAY_JOB_TIMEOUT_SECONDS`
- `WORKER_LEASE_SECONDS`
- `REPLAY_JOB_LEASE_SECONDS`
- retention windows under `RETENTION_*`

Production-aware startup rules:
- production mode rejects weak or placeholder secrets
- production mode requires ingest auth
- production mode keeps FastAPI docs disabled unless explicitly allowed
- ingest and operator scopes must use different secrets

## Operator Surface

Unprotected:
- `/health`
- `/ready`
- `/telemetry`

Operator authenticated:
- `/ops/telemetry`
- `/ops/replays`
- `/ops/replays/{replay_job_id}`
- `/ops/replays/{replay_job_id}/cancel`
- `/ops/dlq`
- `/ops/dlq/{dlq_id}`
- `/ops/dlq/{dlq_id}/redrive`
- `/ops/events/{event_id}`

Auth behavior:
- headers: `X-API-Key-Id` and `X-API-Key`
- missing header: `401`
- wrong scope or invalid secret: `403`
- ingest and operator scopes are independent

## Replay and Lifecycle Guarantees

Replay and redrive:
- re-enter the normal worker path
- stay durable in Postgres
- remain auditable in `operator_audit_log`
- respect cancellation and deadline termination

Worker and replay coordination:
- fenced `owner_token` plus `lease_generation`
- lease heartbeat renewal
- stale-owner takeover after lease expiry
- completed events stay replay-safe because the replay runner records them as `skipped`

These controls materially improve horizontal safety, but they still do not claim exactly-once distributed guarantees.

## Retention, Backup, Restore, and SLOs

- retention and lifecycle controls: [RETENTION-BACKUP-RESTORE.md](RETENTION-BACKUP-RESTORE.md)
- release and rollback: [RELEASE-ROLLBACK.md](RELEASE-ROLLBACK.md)
- SLO and alert guidance: [SLO.md](SLO.md)
- operator procedures: [RUNBOOK.md](RUNBOOK.md)
- replay and redrive details: [REPLAY-REDRIVE.md](REPLAY-REDRIVE.md)
- contracts: [CONTRACTS.md](CONTRACTS.md)

## Verification

Deterministic tests:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python3.11 -m pip install -r modules/06-big-data-architecture/03-implementations/mini-platform/requirements-dev.txt
python3.11 -m pytest -q modules/06-big-data-architecture/03-implementations/mini-platform/tests
```

Integration stack check:

```bash
bash modules/06-big-data-architecture/03-implementations/mini-platform/scripts/ci-integration.sh
```

## References

- [RUNBOOK.md](RUNBOOK.md)
- [REPLAY-REDRIVE.md](REPLAY-REDRIVE.md)
- [CONTRACTS.md](CONTRACTS.md)
- [RETENTION-BACKUP-RESTORE.md](RETENTION-BACKUP-RESTORE.md)
- [RELEASE-ROLLBACK.md](RELEASE-ROLLBACK.md)
- [SLO.md](SLO.md)
- [0003 Idempotency Strategy](adrs/0003-idempotency-strategy.md)
- [0005 Fenced Leases and Operational Lifecycle](adrs/0005-fenced-leases-and-operational-lifecycle.md)
