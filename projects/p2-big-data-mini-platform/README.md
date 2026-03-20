# p2-big-data-mini-platform

## Purpose

This project wraps the repository's only productized backend surface: the mini-platform under [`modules/06-big-data-architecture/03-implementations/mini-platform`](../../modules/06-big-data-architecture/03-implementations/mini-platform).

## Phase 4 Boundary

Supported:
- local Docker Compose
- Python 3.11 tests
- scoped ingest and operator auth
- fenced worker and replay-runner coordination
- replay, redrive, cancellation, timeout, and operator telemetry
- tracked Postgres and ClickHouse migrations
- retention, backup, restore, load, and SLO scripts
- release metadata and production-like env examples

Not claimed:
- cloud deployment
- customer-facing app behavior
- multi-tenant isolation
- billing
- full security platform completeness

## Run

```bash
make -C modules/06-big-data-architecture/03-implementations/mini-platform compose-config
make -C modules/06-big-data-architecture/03-implementations/mini-platform up-local
```

Example ingest:

```bash
curl -fsS -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -H "X-API-Key-Id: local-ingest" \
  -H "X-API-Key: local-demo-ingest-key" \
  -d '{"schema_version":1,"event_type":"order_created","event_time":"2026-01-27T12:00:00Z","order_id":"O-1","amount":10,"currency":"USD","customer_id":"C-1"}'
```

Operator telemetry:

```bash
curl -fsS http://localhost:8000/ops/telemetry \
  -H "X-API-Key-Id: local-ops" \
  -H "X-API-Key: local-demo-ops-key"
```

## Verify

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python3.11 -m pip install -r modules/06-big-data-architecture/03-implementations/mini-platform/requirements-dev.txt
python3.11 -m pytest -q modules/06-big-data-architecture/03-implementations/mini-platform/tests
bash modules/06-big-data-architecture/03-implementations/mini-platform/scripts/ci-integration.sh
```

## Operator References

- [Mini-platform README](../../modules/06-big-data-architecture/03-implementations/mini-platform/README.md)
- [Runbook](../../modules/06-big-data-architecture/03-implementations/mini-platform/RUNBOOK.md)
- [Replay and Redrive](../../modules/06-big-data-architecture/03-implementations/mini-platform/REPLAY-REDRIVE.md)
- [Retention, Backup, and Restore](../../modules/06-big-data-architecture/03-implementations/mini-platform/RETENTION-BACKUP-RESTORE.md)
- [Release and Rollback](../../modules/06-big-data-architecture/03-implementations/mini-platform/RELEASE-ROLLBACK.md)
- [SLO Guide](../../modules/06-big-data-architecture/03-implementations/mini-platform/SLO.md)
