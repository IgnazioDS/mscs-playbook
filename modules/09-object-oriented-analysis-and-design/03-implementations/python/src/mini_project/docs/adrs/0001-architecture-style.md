# ADR 0001: Architecture Style

## Context
We need clear boundaries for domain logic, use cases, and infrastructure to
show OOAD principles and testability.

## Decision
Use a layered/hexagonal-inspired structure: domain, application, infrastructure.

## Alternatives
- Single module with mixed responsibilities
- Framework-centric architecture

## Consequences
- Domain remains framework-agnostic
- Dependencies flow inward
- Slightly more structure in a small codebase


## Related Concepts

- [OOAD Foundations and UML Lite](../../../../../../01-concepts/01-ooad-foundations-and-uml-lite.md)
- [Cohesion, Coupling, and Boundaries](../../../../../../01-concepts/02-cohesion-coupling-and-boundaries.md)
- [SOLID Principles in Practice](../../../../../../01-concepts/03-solid-principles-in-practice.md)
