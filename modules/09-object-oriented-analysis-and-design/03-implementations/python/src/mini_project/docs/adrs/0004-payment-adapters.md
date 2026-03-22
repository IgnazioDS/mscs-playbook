# ADR 0004: Payment Adapters and Factory

## Context
Payment gateways have different interfaces (cents vs dollars). We need a unified
interface and simple selection.

## Decision
Use Adapters to normalize gateway APIs and a factory to select processors.

## Alternatives
- Branching logic in the service
- Direct gateway usage in domain

## Consequences
- Clear separation and easy extension
- Slightly more classes for a small example


## Related Concepts

- [OOAD Foundations and UML Lite](../../../../../../01-concepts/01-ooad-foundations-and-uml-lite.md)
- [Cohesion, Coupling, and Boundaries](../../../../../../01-concepts/02-cohesion-coupling-and-boundaries.md)
- [SOLID Principles in Practice](../../../../../../01-concepts/03-solid-principles-in-practice.md)
