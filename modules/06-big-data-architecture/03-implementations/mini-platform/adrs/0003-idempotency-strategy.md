# ADR 0003: Idempotency Strategy

## Context
At-least-once delivery means consumers may see duplicate events.

## Decision
Use an idempotency table in Postgres keyed by event_id. The worker checks
processed_events before writing to storage and analytics.

## Alternatives considered
- Exactly-once processing (complex and brittle)
- Kafka transactions (overkill for a local demo)

## Consequences
- Simple to reason about and easy to demonstrate.
- Requires storage for dedupe keys and a retention policy in production.
