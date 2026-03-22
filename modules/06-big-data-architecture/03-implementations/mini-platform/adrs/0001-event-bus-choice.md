# ADR 0001: Event Bus Choice

## Context
We need a Kafka-compatible event bus that runs locally with minimal resources
and supports consumer groups and topic management.

## Decision
Use Redpanda as the event bus for the mini platform.

## Alternatives considered
- Apache Kafka with Zookeeper (heavier footprint)
- RabbitMQ (different API and semantics)

## Consequences
- Simplifies local setup and reduces resource usage.
- Kafka-compatible API supports common client libraries.
- Some Kafka features may differ; use only core features.


## Related Concepts

- [Big Data Architecture Foundations](../../../01-concepts/01-big-data-architecture-foundations.md)
- [Data Lake, Lakehouse, and Warehouse](../../../01-concepts/02-data-lake-lakehouse-and-warehouse.md)
- [Event-Driven Architecture and Streaming](../../../01-concepts/03-event-driven-architecture-and-streaming.md)
