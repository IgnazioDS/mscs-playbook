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


## Related Concepts

- [OOAD Foundations and UML Lite](../../../../../../01-concepts/01-ooad-foundations-and-uml-lite.md)
- [Cohesion, Coupling, and Boundaries](../../../../../../01-concepts/02-cohesion-coupling-and-boundaries.md)
- [SOLID Principles in Practice](../../../../../../01-concepts/03-solid-principles-in-practice.md)
