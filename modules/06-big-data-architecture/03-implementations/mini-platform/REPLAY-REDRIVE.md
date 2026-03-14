# Replay and Redrive

Replay and redrive are operator workflows. Both use the authenticated `/ops` API and both keep the existing worker state machine in the loop.

## Replay vs Redrive

Replay:
- selects one or more events from `ingest_log`
- supports `event_id` or `event_time` range selection
- is useful for backfill or explicit reprocessing checks

Redrive:
- starts from a specific `dlq_events.id`
- is useful for remediating a known failure record
- leaves the original DLQ row in place for auditability

## What Replay Guarantees

- replay jobs are durable in Postgres
- replay publication is auditable through `operator_audit_log`
- replay reuses the existing worker state machine
- duplicate MinIO and ClickHouse writes are still blocked by the worker's recorded progress and explicit existence checks

## What Replay Does Not Guarantee

- exactly-once semantics across Kafka, storage, and analytics
- automatic repair of external dependency outages
- immediate completion if the worker is down or still holds a live lease

## Request Replay

By event id:

```bash
curl -fsS -X POST http://localhost:8000/ops/replays \
  -H "Content-Type: application/json" \
  -H "X-API-Key: local-demo-ingest-key" \
  -d '{"selector_type":"event_id","event_id":"<event-id>"}'
```

By event-time range:

```bash
curl -fsS -X POST http://localhost:8000/ops/replays \
  -H "Content-Type: application/json" \
  -H "X-API-Key: local-demo-ingest-key" \
  -d '{"selector_type":"time_range","start_time":"2026-01-27T00:00:00Z","end_time":"2026-01-27T23:59:59Z"}'
```

Check replay status:

```bash
curl -fsS http://localhost:8000/ops/replays/<replay-job-id> \
  -H "X-API-Key: local-demo-ingest-key"
```

## Inspect DLQ and Redrive

List recent DLQ rows:

```bash
curl -fsS http://localhost:8000/ops/dlq \
  -H "X-API-Key: local-demo-ingest-key"
```

Inspect one DLQ row:

```bash
curl -fsS http://localhost:8000/ops/dlq/<dlq-id> \
  -H "X-API-Key: local-demo-ingest-key"
```

Request redrive:

```bash
curl -fsS -X POST http://localhost:8000/ops/dlq/<dlq-id>/redrive \
  -H "X-API-Key: local-demo-ingest-key"
```

## Inspect an Event Lifecycle

```bash
curl -fsS http://localhost:8000/ops/events/<event-id> \
  -H "X-API-Key: local-demo-ingest-key"
```

The response includes:
- ingest metadata and payload
- current `event_processing` state
- `processed_events` completion time if present
- DLQ rows for the event
- replay attempts
- operator audit history
