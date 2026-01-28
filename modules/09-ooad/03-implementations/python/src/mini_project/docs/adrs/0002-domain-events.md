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
