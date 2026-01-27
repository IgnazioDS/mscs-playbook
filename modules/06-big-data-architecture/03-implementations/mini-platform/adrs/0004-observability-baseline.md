# ADR 0004: Observability Baseline

## Context
We need minimal signals to verify pipeline health without full observability
infrastructure.

## Decision
Use service logs plus key database queries to confirm ingestion, processing,
and analytics materialization. Provide example commands for operators.

## Alternatives considered
- Prometheus + Grafana stack (more setup overhead)
- Custom dashboards (beyond scope)

## Consequences
- Easy to run locally, limited visualization.
- Operators rely on basic queries and log inspection.
