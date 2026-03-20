# Replay and Redrive

Replay and redrive are authenticated operator workflows. Both stay inside the existing worker state machine and both are durable in Postgres.

## Replay vs Redrive

Replay:
- selects source rows from `ingest_log`
- supports `event_id` or time range selectors
- is used for backfill, replay-safe verification, and retained-window rebuilds

Redrive:
- starts from a specific `dlq_events.id`
- is used for explicit failure remediation
- preserves the original DLQ row for auditability

## Guarantees

- replay jobs are durable and auditable
- replay runners use fenced ownership with `owner_token` and `lease_generation`
- two runners cannot keep progressing the same owned job through the same fenced state
- completed events are recorded as `skipped` instead of being republished
- worker replay safety still depends on the same MinIO object identity and ClickHouse existence checks used on the normal path

## Non-guarantees

- no exactly-once claim across Kafka, MinIO, and ClickHouse
- no automatic repair of external outages
- no promise that expired retention windows can still be replayed

## Request Replay

By event id:

```bash
curl -fsS -X POST http://localhost:8000/ops/replays \
  -H "Content-Type: application/json" \
  -H "X-API-Key-Id: local-ops" \
  -H "X-API-Key: local-demo-ops-key" \
  -d '{"selector_type":"event_id","event_id":"<event-id>"}'
```

By time range:

```bash
curl -fsS -X POST http://localhost:8000/ops/replays \
  -H "Content-Type: application/json" \
  -H "X-API-Key-Id: local-ops" \
  -H "X-API-Key: local-demo-ops-key" \
  -d '{"selector_type":"time_range","start_time":"2026-01-27T00:00:00Z","end_time":"2026-01-27T23:59:59Z"}'
```

Inspect a replay job:

```bash
curl -fsS http://localhost:8000/ops/replays/<replay-job-id> \
  -H "X-API-Key-Id: local-ops" \
  -H "X-API-Key: local-demo-ops-key"
```

Cancel a replay job:

```bash
curl -fsS -X POST http://localhost:8000/ops/replays/<replay-job-id>/cancel \
  -H "Content-Type: application/json" \
  -H "X-API-Key-Id: local-ops" \
  -H "X-API-Key: local-demo-ops-key" \
  -d '{"reason":"operator abort"}'
```

## Inspect DLQ and Redrive

List DLQ rows:

```bash
curl -fsS http://localhost:8000/ops/dlq \
  -H "X-API-Key-Id: local-ops" \
  -H "X-API-Key: local-demo-ops-key"
```

Inspect one DLQ row:

```bash
curl -fsS http://localhost:8000/ops/dlq/<dlq-id> \
  -H "X-API-Key-Id: local-ops" \
  -H "X-API-Key: local-demo-ops-key"
```

Request redrive:

```bash
curl -fsS -X POST http://localhost:8000/ops/dlq/<dlq-id>/redrive \
  -H "X-API-Key-Id: local-ops" \
  -H "X-API-Key: local-demo-ops-key"
```

## How to Interpret Replay Status

- `requested`: durable job created, not yet claimed
- `running`: actively owned by a replay runner
- `completed`: terminal success
- `failed`: terminal failure after one or more replayed events failed
- `cancelled`: terminal operator stop
- `timed_out`: terminal deadline breach

Summary fields:
- `total_events`
- `completed_events`
- `failed_events`
- `skipped_events`

Terminal detail fields:
- `terminal_reason`
- `terminal_detail`

## Event Lifecycle Inspection

```bash
curl -fsS http://localhost:8000/ops/events/<event-id> \
  -H "X-API-Key-Id: local-ops" \
  -H "X-API-Key: local-demo-ops-key"
```

That response distinguishes:
- original ingest
- current worker state
- DLQ history
- replay or redrive attempts
- operator audit actions
