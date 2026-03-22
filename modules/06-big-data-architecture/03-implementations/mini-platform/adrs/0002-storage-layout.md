# ADR 0002: Storage Layout

## Context
We need a layout that separates raw data from curated analytics while staying
simple and local-friendly.

## Decision
Store raw events in MinIO (object storage) partitioned by date, and materialize
analytics-ready rows into ClickHouse.

## Alternatives considered
- Postgres-only analytics (simpler but less realistic for big data)
- Full lakehouse stack (too heavy for local demos)

## Consequences
- Raw storage is cheap and replayable.
- ClickHouse supports fast analytical queries and partitioning.
- Requires running two storage systems locally.


## Related Concepts

- [Big Data Architecture Foundations](../../../01-concepts/01-big-data-architecture-foundations.md)
- [Data Lake, Lakehouse, and Warehouse](../../../01-concepts/02-data-lake-lakehouse-and-warehouse.md)
- [Event-Driven Architecture and Streaming](../../../01-concepts/03-event-driven-architecture-and-streaming.md)
