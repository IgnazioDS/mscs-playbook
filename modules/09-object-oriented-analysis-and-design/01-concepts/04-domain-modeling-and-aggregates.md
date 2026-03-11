# Domain Modeling and Aggregates

## Overview
Domain models capture business concepts as entities and value objects. Aggregates
define transactional boundaries and invariants.

## Why it matters
Well-defined aggregates prevent inconsistent state and clarify ownership.

## Key ideas
- Entities have identity; value objects are immutable
- Aggregate roots enforce invariants
- Persistence is external to the model

## Practical workflow
- Identify aggregate roots and invariants
- Keep aggregates small and cohesive
- Expose behavior via methods, not setters

## Failure modes
- Anemic domain models
- Oversized aggregates
- Cross-aggregate writes without coordination

## Checklist
- Invariants enforced in aggregate root
- Value objects are immutable
- Transactions align with aggregates
- Domain model is persistence-agnostic

## References
- Domain-Driven Design (Evans) — https://www.domainlanguage.com/ddd/
- Implementing DDD (Vernon) — https://www.goodreads.com/book/show/15756865-implementing-domain-driven-design
