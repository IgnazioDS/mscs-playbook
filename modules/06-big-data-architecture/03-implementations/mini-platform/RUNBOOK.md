# Operator Runbook

This runbook covers the mini-platform's supported operator path in Phase 4.

## Auth Setup

Ingest scope:
- header `X-API-Key-Id`
- header `X-API-Key`
- env source `INGEST_API_KEYS`

Operator scope:
- header `X-API-Key-Id`
- header `X-API-Key`
- env source `OPERATOR_API_KEYS`

Rotation:
- overlap old and new keys in the same env value
- retire old ids only after callers have switched
- helper: [`scripts/rotate_api_keys.py`](scripts/rotate_api_keys.py)

Example local headers:

```bash
-H "X-API-Key-Id: local-ingest" -H "X-API-Key: local-demo-ingest-key"
-H "X-API-Key-Id: local-ops" -H "X-API-Key: local-demo-ops-key"
```

## Migrations and Startup Order

Postgres:
- init: [`sql/postgres/001_init.sql`](sql/postgres/001_init.sql)
- tracked migrations: [`sql/postgres/migrations`](sql/postgres/migrations)
- runner: [`scripts/run-postgres-migrations.sh`](scripts/run-postgres-migrations.sh)

ClickHouse:
- init: [`sql/clickhouse/001_init.sql`](sql/clickhouse/001_init.sql)
- tracked migrations: [`sql/clickhouse/migrations`](sql/clickhouse/migrations)
- runner: [`scripts/run-clickhouse-migrations.sh`](scripts/run-clickhouse-migrations.sh)

Packaged flow:

```bash
make -C modules/06-big-data-architecture/03-implementations/mini-platform compose-config
make -C modules/06-big-data-architecture/03-implementations/mini-platform up-local
```

## Health, Readiness, Telemetry

- `/health`: startup, Postgres, and Kafka status
- `/ready`: same dependency-aware readiness signal
- `/telemetry`: compact machine-readable view with release metadata
- `/ops/telemetry`: durable operator telemetry with replay counts, release metadata, and contract support

Primary telemetry source of truth:
- `ingest_log`
- `ingest_rejections`
- `processed_events`
- `dlq_events`
- `event_processing`
- `replay_jobs`
- `replay_job_events`

## Replay, Redrive, Cancellation, and Timeout

Replay request:

```bash
curl -fsS -X POST http://localhost:8000/ops/replays \
  -H "Content-Type: application/json" \
  -H "X-API-Key-Id: local-ops" \
  -H "X-API-Key: local-demo-ops-key" \
  -d '{"selector_type":"event_id","event_id":"<event-id>"}'
```

Cancellation:

```bash
curl -fsS -X POST http://localhost:8000/ops/replays/<replay-job-id>/cancel \
  -H "Content-Type: application/json" \
  -H "X-API-Key-Id: local-ops" \
  -H "X-API-Key: local-demo-ops-key" \
  -d '{"reason":"operator abort"}'
```

Redrive:

```bash
curl -fsS -X POST http://localhost:8000/ops/dlq/<dlq-id>/redrive \
  -H "X-API-Key-Id: local-ops" \
  -H "X-API-Key: local-demo-ops-key"
```

Lifecycle behavior:
- running jobs heartbeat and renew leases
- stale runners can be taken over by a new owner with a higher `lease_generation`
- cancelled jobs stop before further replay progress
- overdue jobs terminate as `timed_out`
- the replay loop sweeps requested or stale-running jobs that should already be terminal

## Inspect an Event Lifecycle

```bash
curl -fsS http://localhost:8000/ops/events/<event-id> \
  -H "X-API-Key-Id: local-ops" \
  -H "X-API-Key: local-demo-ops-key"
```

The response includes:
- ingest metadata
- current processing state
- processed timestamp if completed
- DLQ history
- replay attempts
- audit history

## Failure Triage

Primary checks:
- recent worker state:
  `select event_id, status, lease_generation, owner_token, last_error from event_processing order by updated_at desc limit 20;`
- recent replay jobs:
  `select replay_job_id, status, total_events, completed_events, failed_events, skipped_events, terminal_reason from replay_jobs order by requested_at desc limit 20;`
- recent replay job events:
  `select replay_job_id, event_id, status, last_observed_processing_status, last_error from replay_job_events order by updated_at desc limit 20;`
- recent DLQ rows:
  `select id, event_id, error, failed_at from dlq_events order by failed_at desc limit 20;`

Interpretation:
- `claimed` / `storage_written` / `analytics_written`: active or stale worker progress
- `failed`: observable worker failure, eligible for redrive or replay
- `cancelled`: operator-stopped replay job
- `timed_out`: replay job exceeded `REPLAY_JOB_TIMEOUT_SECONDS`

## Retention and Disaster Recovery

Retention entrypoint:

```bash
python3.11 modules/06-big-data-architecture/03-implementations/mini-platform/scripts/retention.py
```

Control-plane backup:

```bash
python3.11 modules/06-big-data-architecture/03-implementations/mini-platform/scripts/backup_control_plane.py \
  --output modules/06-big-data-architecture/03-implementations/mini-platform/artifacts/control-plane-backup.json
```

Control-plane restore:

```bash
python3.11 modules/06-big-data-architecture/03-implementations/mini-platform/scripts/restore_control_plane.py \
  modules/06-big-data-architecture/03-implementations/mini-platform/artifacts/control-plane-backup.json
```

See [RETENTION-BACKUP-RESTORE.md](RETENTION-BACKUP-RESTORE.md) for the full recovery order.

## Capacity and SLO Checks

Lightweight load smoke:

```bash
python3.11 modules/06-big-data-architecture/03-implementations/mini-platform/scripts/load_harness.py \
  --base-url http://localhost:8000 \
  --ingest-key-id local-ingest \
  --ingest-key local-demo-ingest-key \
  --operator-key-id local-ops \
  --operator-key local-demo-ops-key \
  --requests 3 \
  --output modules/06-big-data-architecture/03-implementations/mini-platform/artifacts/load-smoke.json
```

SLO evaluation:

```bash
python3.11 modules/06-big-data-architecture/03-implementations/mini-platform/scripts/slo_check.py \
  --base-url http://localhost:8000 \
  --operator-key-id local-ops \
  --operator-key local-demo-ops-key \
  --capacity-report modules/06-big-data-architecture/03-implementations/mini-platform/artifacts/load-smoke.json \
  --readiness-availability 1.0
```

## Deferred After Phase 4

- full cloud deployment packaging
- managed secret distribution
- human-user RBAC
- customer tenancy
- vendor observability stack integration
