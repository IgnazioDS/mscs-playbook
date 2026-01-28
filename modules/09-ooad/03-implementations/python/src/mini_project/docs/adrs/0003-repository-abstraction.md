# ADR 0003: Repository Abstraction

## Context
We need persistence that is deterministic and testable without external
infrastructure.

## Decision
Use an in-memory OrderRepository with stable ID generation.

## Alternatives
- Direct dictionary use in services
- External database adapters

## Consequences
- Easy to test and deterministic
- Repository interface can be swapped later
