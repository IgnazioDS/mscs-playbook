# Mini Platform (Phase 3 Capability Expansion)

Local, laptop-friendly big data mini-platform with production-aware safeguards plus operator replay and redrive workflows. It remains the repository's primary local deployable demo surface, not a production-ready platform.

## Current Status
- Primary hardened service surface for this repository.
- Supported locally with Docker Compose and Python 3.11.
- Includes authenticated ingest, authenticated operator APIs, durable replay jobs, tracked Postgres and ClickHouse migrations, structured logs, and deterministic evaluation coverage.
- Not claimed to be cloud-ready, production-security-complete, multi-tenant, customer-facing, or exactly-once.

## Services
- `ingest-api`: strict schema-versioned ingest and authenticated `/ops` surface
- `worker`: raw-event consumer with resumable state transitions
- `replay-runner`: durable replay and redrive executor
- `postgres`: operational state, ingest log, replay jobs, audit history
- `clickhouse`: analytics sink with tracked schema migrations
- `redpanda`: Kafka-compatible event bus
- `minio`: deterministic raw object storage

## Local Quickstart
```bash
docker compose \
  --env-file modules/06-big-data-architecture/03-implementations/mini-platform/.env.local.example \
  -f modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml \
  up -d

bash modules/06-big-data-architecture/03-implementations/mini-platform/scripts/wait-for.sh \
  modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml

curl -fsS http://localhost:8000/health
curl -fsS http://localhost:8000/ready
curl -fsS http://localhost:8000/telemetry

curl -fsS -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -H "X-API-Key: local-demo-ingest-key" \
  -d '{"schema_version":1,"event_type":"order_created","event_time":"2026-01-27T12:00:00Z","order_id":"O-1","amount":10,"currency":"USD","customer_id":"C-1"}'

curl -fsS http://localhost:8000/ops/telemetry \
  -H "X-API-Key: local-demo-ingest-key"
```

## Configuration
Environment examples:
- local: [`.env.local.example`](.env.local.example)
- production-aware: [`.env.production.example`](.env.production.example)

Important knobs:
- `APP_ENV=local|test|production`
- `INGEST_AUTH_ENABLED=true`
- `INGEST_API_KEY=...`
- `INGEST_ALLOW_INTERACTIVE_DOCS=true|false`
- `INGEST_MAX_REQUEST_BYTES=16384`
- `WORKER_LEASE_SECONDS=30`
- `REPLAY_RUNNER_POLL_SECONDS=2`
- `REPLAY_JOB_LEASE_SECONDS=30`
- `MINIO_SECURE=false|true`

Production-aware startup rules:
- production mode rejects weak or placeholder secrets
- production mode requires ingest auth to stay enabled
- production mode disables FastAPI docs and OpenAPI unless explicitly allowed
- worker production mode rejects insecure MinIO or Postgres credentials

## Ingest Contract
- Supported external contract: `order_created` at `schema_version=1`
- Unknown keys are rejected
- Unsupported schema versions are rejected
- `event_time` must include a timezone offset

See [Supported Contracts](CONTRACTS.md) for the exact contract.

## API Surface
- `/health`: unprotected liveness plus dependency status
- `/ready`: unprotected readiness check for startup, Postgres, and Kafka bootstrap connectivity
- `/telemetry`: compact machine-readable counters backed by Postgres state
- `/ingest`: authenticated ingest endpoint
- `/ops/telemetry`: authenticated durable operator telemetry and supported contract list
- `/ops/replays`: authenticated replay-job creation
- `/ops/replays/{replay_job_id}`: replay-job status plus per-event progress
- `/ops/dlq`: DLQ listing
- `/ops/dlq/{dlq_id}`: DLQ detail
- `/ops/dlq/{dlq_id}/redrive`: authenticated redrive request
- `/ops/events/{event_id}`: event lifecycle inspection

Auth behavior:
- header: `X-API-Key`
- missing key: `401`
- invalid key: `403`
- oversized ingest payload: `413`

## Replay and Redrive
Replay:
- selects events from `ingest_log` by `event_id` or `event_time` range
- publishes back through the normal raw-event topic
- completes only after selected events reach a terminal replay outcome

Redrive:
- starts from a specific `dlq_events.id`
- records a durable replay job and audit history
- keeps the original DLQ row for traceability

Operational guarantees:
- replay and redrive use the existing worker state machine instead of bypassing it
- duplicate MinIO and ClickHouse writes are still blocked by recorded worker progress and explicit existence checks
- completed events remain safe to replay because the replay runner marks them as `skipped` instead of republishing

See [Replay and Redrive](REPLAY-REDRIVE.md) and [Operator Runbook](RUNBOOK.md).

## Migrations
Tracked schema paths:
- Postgres bootstrap: [`sql/postgres/001_init.sql`](sql/postgres/001_init.sql)
- Postgres migrations: [`sql/postgres/migrations`](sql/postgres/migrations)
- Postgres runner: [`scripts/run-postgres-migrations.sh`](scripts/run-postgres-migrations.sh)
- ClickHouse bootstrap: [`sql/clickhouse/001_init.sql`](sql/clickhouse/001_init.sql)
- ClickHouse migrations: [`sql/clickhouse/migrations`](sql/clickhouse/migrations)
- ClickHouse runner: [`scripts/run-clickhouse-migrations.sh`](scripts/run-clickhouse-migrations.sh)

Manual migration commands:
```bash
docker compose \
  --env-file modules/06-big-data-architecture/03-implementations/mini-platform/.env.local.example \
  -f modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml \
  run --rm migrate

docker compose \
  --env-file modules/06-big-data-architecture/03-implementations/mini-platform/.env.local.example \
  -f modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml \
  run --rm clickhouse-migrate
```

## Verification
Deterministic unit and workflow tests:
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

Useful runtime queries:
```bash
docker compose --env-file modules/06-big-data-architecture/03-implementations/mini-platform/.env.local.example \
  -f modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml \
  exec -T postgres psql -U bd06 -d bd06 \
  -c "select status, count(*) from event_processing group by status order by status;"

docker compose --env-file modules/06-big-data-architecture/03-implementations/mini-platform/.env.local.example \
  -f modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml \
  exec -T postgres psql -U bd06 -d bd06 \
  -c "select replay_job_id, status, total_events, completed_events, failed_events from replay_jobs order by requested_at desc limit 20;"

docker compose --env-file modules/06-big-data-architecture/03-implementations/mini-platform/.env.local.example \
  -f modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml \
  exec -T clickhouse clickhouse-client \
  --query "select event_id, schema_version from analytics.events order by event_time desc limit 20;"
```

## References
- [Operator Runbook](RUNBOOK.md)
- [Replay and Redrive](REPLAY-REDRIVE.md)
- [Supported Contracts](CONTRACTS.md)
- [0001 Event Bus Choice](adrs/0001-event-bus-choice.md)
- [0002 Storage Layout](adrs/0002-storage-layout.md)
- [0003 Idempotency Strategy](adrs/0003-idempotency-strategy.md)
- [0004 Observability Baseline](adrs/0004-observability-baseline.md)

## Still Deferred
- cloud deployment and IaC
- TLS termination and external identity
- RBAC and multi-tenancy
- billing
- major observability stack
- exactly-once processing semantics
