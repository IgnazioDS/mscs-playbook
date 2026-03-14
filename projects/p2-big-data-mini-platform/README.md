# p2-big-data-mini-platform

## Purpose
Run the repository's primary hardened local service demo: a laptop-friendly ingest-to-analytics mini-platform with explicit auth, tracked migrations, resumable worker recovery, operator replay/redrive workflows, and deterministic verification.

## Phase 3 Boundary
- Supported: local Docker Compose, Python 3.11 test workflows, Postgres and ClickHouse migrations, API-key protected `/ingest` and `/ops`, durable replay/redrive jobs, event lifecycle inspection, and dedicated integration CI.
- Not claimed: cloud readiness, production security completeness, multi-tenant support, customer-facing product readiness, or a broader repo-wide deployment model.

## How to Run
```bash
docker compose \
  --env-file modules/06-big-data-architecture/03-implementations/mini-platform/.env.local.example \
  -f modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml \
  up -d

curl -fsS http://localhost:8000/health
curl -fsS http://localhost:8000/ready

curl -fsS -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -H "X-API-Key: local-demo-ingest-key" \
  -d '{"schema_version":1,"event_type":"order_created","event_time":"2026-01-27T12:00:00Z","order_id":"O-1","amount":10,"currency":"USD","customer_id":"C-1"}'

curl -fsS http://localhost:8000/ops/telemetry \
  -H "X-API-Key: local-demo-ingest-key"
```

## How to Test
```bash
python3.11 -m venv .venv
source .venv/bin/activate
python3.11 -m pip install -r modules/06-big-data-architecture/03-implementations/mini-platform/requirements-dev.txt
python3.11 -m pytest -q modules/06-big-data-architecture/03-implementations/mini-platform/tests
bash modules/06-big-data-architecture/03-implementations/mini-platform/scripts/ci-integration.sh
```

## What Phase 3 Added
- Explicit `schema_version` support for the `order_created` contract.
- Authenticated `/ops` endpoints for replay creation, replay status, DLQ inspection, redrive, durable telemetry, and event lifecycle lookup.
- Durable replay job state and audit history in Postgres.
- ClickHouse migration tracking alongside the existing Postgres migration runner.
- Deterministic scenario evaluations for replay, redrive, stale-claim recovery, and operator telemetry.

## What Phase 2 Added
- Startup config validation for `APP_ENV=local|test|production`.
- `X-API-Key` authentication on `/ingest`.
- Postgres migration tracking through `schema_migrations`.
- Lease-based worker recovery with resumable storage and analytics progress.
- Structured JSON logs and `/telemetry`.

## Operator References
- [Mini-platform README](../../modules/06-big-data-architecture/03-implementations/mini-platform/README.md)
- [Operator Runbook](../../modules/06-big-data-architecture/03-implementations/mini-platform/RUNBOOK.md)
- [Replay and Redrive Guide](../../modules/06-big-data-architecture/03-implementations/mini-platform/REPLAY-REDRIVE.md)
- [Supported Contracts](../../modules/06-big-data-architecture/03-implementations/mini-platform/CONTRACTS.md)
