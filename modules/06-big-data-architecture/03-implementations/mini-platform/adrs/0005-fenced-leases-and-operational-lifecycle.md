# ADR 0005: Fenced Leases, Replay Termination, and Operational Lifecycle Controls

## Context

Phase 3 made replay durable and auditable, but still assumed a single effective replay runner and a single effective worker owner at a time. Phase 4 needs safer horizontal execution, replay cancellation and timeout handling, retention, and packaged operator workflows without turning this repo into a full platform product.

## Decision

Extend Postgres coordination state with fenced lease ownership:

- `event_processing` now tracks `owner_token`, `lease_generation`, and `heartbeat_at`
- `replay_jobs` now tracks `owner_token`, `lease_generation`, `heartbeat_at`, cancellation fields, deadline fields, terminal reason fields, and summary counters

Execution rules:
- workers and replay runners must update owned rows using both `owner_token` and `lease_generation`
- takeover increments `lease_generation`
- stale owners cannot advance state after takeover because fenced updates stop matching
- replay jobs can terminate as `completed`, `failed`, `cancelled`, or `timed_out`
- a sweeper path handles requested or stale-running jobs that should become terminal without a live runner

Operational lifecycle rules:
- retention is explicit and age-based
- active in-progress event state is excluded from deletion
- terminal replay history is retained until the configured replay retention window expires
- control-plane backup and restore is handled through JSON snapshot scripts tied to the tracked migration model

## Consequences

- concurrent claim pressure is safer than the Phase 3 single-owner assumption
- replay cancellation is real control flow, not just metadata
- release validation, retention, backup, and SLO scripts are now part of the supported operator surface
- this is still not exactly-once distributed execution and still not a managed cloud platform
