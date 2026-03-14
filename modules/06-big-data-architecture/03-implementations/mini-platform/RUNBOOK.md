# Operator Runbook

## Auth Setup
- Local demo path: use [`.env.local.example`](.env.local.example) and `INGEST_API_KEY=local-demo-ingest-key`.
- Production-aware path: start from [`.env.production.example`](.env.production.example), replace all placeholder secrets, keep `INGEST_AUTH_ENABLED=true`, and leave `INGEST_ALLOW_INTERACTIVE_DOCS=false` unless there is a deliberate reason to expose docs.
- The same `X-API-Key` currently protects `/ingest` and `/ops/...`.

## Migrations
- Compose includes `migrate` for Postgres and `clickhouse-migrate` for ClickHouse.
- The API waits on Postgres migrations. The worker and replay-runner wait on both Postgres and ClickHouse migrations.
- Manual run:
  `docker compose --env-file modules/06-big-data-architecture/03-implementations/mini-platform/.env.local.example -f modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml run --rm migrate`
- Manual ClickHouse run:
  `docker compose --env-file modules/06-big-data-architecture/03-implementations/mini-platform/.env.local.example -f modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml run --rm clickhouse-migrate`
- Check applied versions:
  `docker compose --env-file modules/06-big-data-architecture/03-implementations/mini-platform/.env.local.example -f modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml exec -T postgres psql -U bd06 -d bd06 -c "select * from schema_migrations order by version;"`
- Check ClickHouse versions:
  `docker compose --env-file modules/06-big-data-architecture/03-implementations/mini-platform/.env.local.example -f modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml exec -T clickhouse clickhouse-client --query "select * from analytics.schema_migrations order by version;"`

## Health, Readiness, Telemetry
- `/health` reports current startup, Postgres, and Kafka bootstrap status.
- `/ready` uses the same dependency checks and is the endpoint the integration flow waits on before ingest.
- `/telemetry` is a compact machine-readable view intended for quick checks.
- `/ops/telemetry` is the authoritative operator view. It returns:
  - durable ingest accepted and rejected totals
  - durable worker completed and failed totals
  - current in-progress count
  - current DLQ backlog count
  - replay job counts by status
  - supported contracts

Telemetry source of truth:
- `ingest_log` for accepted totals
- `ingest_rejections` for rejected totals
- `processed_events` for completed totals
- `dlq_events` for failed totals
- `event_processing` for current in-progress and current failed backlog
- `replay_jobs` and `replay_job_events` for replay/redrive history

## Replay and Redrive
- Replay requests are created through `POST /ops/replays`.
- Redrive requests are created through `POST /ops/dlq/{dlq_id}/redrive`.
- The replay-runner claims durable replay jobs from Postgres and republishes only when the current worker state makes that safe.
- Replay by `event_id` or `event_time` range reads from `ingest_log`.
- Redrive reads from the selected `dlq_events` row.
- Completed events are marked as `skipped` for replay instead of being republished.
- Failed or stale in-progress events are republished with the same `event_id` so the worker can resume safely.

Quick commands:
```bash
curl -fsS -X POST http://localhost:8000/ops/replays \
  -H "Content-Type: application/json" \
  -H "X-API-Key: local-demo-ingest-key" \
  -d '{"selector_type":"event_id","event_id":"<event-id>"}'

curl -fsS http://localhost:8000/ops/replays/<replay-job-id> \
  -H "X-API-Key: local-demo-ingest-key"

curl -fsS http://localhost:8000/ops/dlq \
  -H "X-API-Key: local-demo-ingest-key"

curl -fsS -X POST http://localhost:8000/ops/dlq/<dlq-id>/redrive \
  -H "X-API-Key: local-demo-ingest-key"
```

## Stale-claim Recovery
- Worker state transitions are tracked in `event_processing`.
- Stale rows in `claimed`, `storage_written`, or `analytics_written` become reclaimable after `WORKER_LEASE_SECONDS`.
- Replay jobs also use a lease through `REPLAY_JOB_LEASE_SECONDS`, so a crashed replay-runner instance does not strand the replay queue forever.
- Recovery is explicit:
  - MinIO progress resumes from deterministic object existence.
  - ClickHouse progress resumes from `event_id` existence checks.
  - replay-job event rows preserve whether an event is still `pending`, already `published`, terminal `completed`, terminal `failed`, or safely `skipped`

## Failure Triage
- Inspect event state:
  `docker compose --env-file modules/06-big-data-architecture/03-implementations/mini-platform/.env.local.example -f modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml exec -T postgres psql -U bd06 -d bd06 -c "select * from event_processing order by updated_at desc limit 20;"`
- Inspect replay jobs:
  `docker compose --env-file modules/06-big-data-architecture/03-implementations/mini-platform/.env.local.example -f modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml exec -T postgres psql -U bd06 -d bd06 -c "select replay_job_id, status, total_events, completed_events, failed_events, last_error from replay_jobs order by requested_at desc limit 20;"`
- Inspect replay job events:
  `docker compose --env-file modules/06-big-data-architecture/03-implementations/mini-platform/.env.local.example -f modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml exec -T postgres psql -U bd06 -d bd06 -c "select replay_job_id, event_id, status, last_observed_processing_status, last_error from replay_job_events order by updated_at desc limit 20;"`
- Inspect DLQ rows:
  `docker compose --env-file modules/06-big-data-architecture/03-implementations/mini-platform/.env.local.example -f modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml exec -T postgres psql -U bd06 -d bd06 -c "select id, event_id, error, failed_at from dlq_events order by failed_at desc limit 20;"`
- Inspect analytics rows:
  `docker compose --env-file modules/06-big-data-architecture/03-implementations/mini-platform/.env.local.example -f modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml exec -T clickhouse clickhouse-client --query "select event_id, event_type, schema_version from analytics.events order by event_time desc limit 20;"`

## Inspect an Event Lifecycle
- API path:
  `curl -fsS http://localhost:8000/ops/events/<event-id> -H "X-API-Key: local-demo-ingest-key"`
- The response includes:
  - ingest payload and contract metadata
  - current processing state
  - completion time if the event is in `processed_events`
  - DLQ rows for the event
  - replay attempts
  - operator audit rows linked to the event

## DLQ Handling
- The worker records failures in `dlq_events` and also publishes the failure envelope to the Kafka DLQ topic.
- Redrive does not delete or rewrite historical DLQ rows. Remediation is shown through the latest `event_processing` state plus replay job results.
- Repeated failure after redrive creates another failure record and leaves the replay job in `failed`.
- Successful remediation leaves the historical DLQ row visible, but the event's latest processing state becomes `completed`.

## Deferred Phase 4 Work
- automated replay cancellation
- richer backlog/throughput metrics
- external identity and secret management
- cloud deployment and managed infra
