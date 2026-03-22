# ADR 0002: Domain Events and Observer

## Context
We need decoupled notifications when an order is placed or payment captured.

## Decision
Use domain events and an in-memory event bus (Observer pattern).

## Alternatives
- Direct calls to notifier services
- Global singleton event bus

## Consequences
- Decouples domain actions from notification delivery
- Enables adding subscribers without changing service code


## Related Concepts

- [OOAD Foundations and UML Lite](../../../../../../01-concepts/01-ooad-foundations-and-uml-lite.md)
- [Cohesion, Coupling, and Boundaries](../../../../../../01-concepts/02-cohesion-coupling-and-boundaries.md)
- [SOLID Principles in Practice](../../../../../../01-concepts/03-solid-principles-in-practice.md)
