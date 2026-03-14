# ADR 0003: Resumable Worker State and Explicit Side-effect Recovery

## Context
Phase 1 introduced reservation-before-side-effects to stop duplicate ClickHouse writes on simple replay paths. Phase 2 converted that into a resumable worker state machine with lease recovery. Phase 3 adds durable operator replay and redrive jobs, so resumability now has to work both for normal Kafka delivery and for explicit operator-initiated reprocessing.

## Decision
Use a resumable Postgres state machine in `event_processing` with explicit progress checkpoints:

- `claimed`
- `storage_written`
- `analytics_written`
- `completed`
- `failed`

Each row tracks claim time, lease expiry, update time, completion time, failure time, last error, and progress timestamps for storage and analytics writes.

Recovery rules:
- A worker can reclaim stale in-progress rows after the configured lease timeout.
- MinIO progress resumes from deterministic object names plus object existence checks.
- ClickHouse progress resumes from `event_id` existence checks before any resumed insert.
- Completed rows are never reprocessed.
- Failed rows remain observable and can be resumed with the same `event_id` if replayed intentionally.
- Replay and redrive jobs publish the original payload back through the normal raw-event topic instead of bypassing the worker state machine.
- Replay job history is tracked separately in `replay_jobs` and `replay_job_events` so the operator action is auditable without weakening the worker's duplicate-write protections.

## Alternatives Considered
- Exact-once processing with Kafka transactions: too complex for this repo surface.
- Blind retries after failure: unsafe for ClickHouse because ambiguous insert errors can already have committed.
- Manual cleanup of stale rows: no longer acceptable after Phase 2.

## Consequences
- Crash recovery no longer depends on deleting stale rows by hand.
- Duplicate ClickHouse prevention is explicit both before insert and during resumed processing.
- Replay-after-completion is safe because the replay runner records the event as `skipped` instead of republishing it.
- The operator model is auditable: replay requests, redrive requests, and terminal replay outcomes are durable Postgres records.
- The state model is more complex than the Phase 1 reservation table, but the flow remains small and repo-native.
