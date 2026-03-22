# Mini-Project: Event Pipeline Readiness

## Goal
Define a minimal, production-ready event pipeline plan for the mini platform.
You will validate schemas, idempotency strategy, and success metrics before shipping.

## Deliverables
- A short schema for raw events (JSON) and warehouse tables (SQL sketch).
- A retry/idempotency strategy for ingest + worker.
- A monitoring checklist with SLOs and alert thresholds.

## Steps
1. Draft an `events.raw` schema with required fields.
2. Define how `event_id` is generated and deduplicated.
3. Specify a dead-letter strategy and replay plan.
4. Write three SLOs (latency, error rate, freshness).

## Suggested Checks
- Data freshness < 10 minutes (p95)
- Ingest success rate > 99.5%
- Idempotent replay produces identical aggregates

## How to Run
Use the mini platform quickstart in `modules/06-big-data-architecture/README.md`.


## Related Concepts

- [Big Data Architecture Foundations](../01-concepts/01-big-data-architecture-foundations.md)
- [Data Lake, Lakehouse, and Warehouse](../01-concepts/02-data-lake-lakehouse-and-warehouse.md)
- [Event-Driven Architecture and Streaming](../01-concepts/03-event-driven-architecture-and-streaming.md)
