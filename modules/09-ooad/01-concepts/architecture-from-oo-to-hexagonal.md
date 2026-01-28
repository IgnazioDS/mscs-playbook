# Architecture from OO to Hexagonal

## Overview
Hexagonal architecture (ports and adapters) keeps domain logic independent from
external systems by defining explicit interfaces.

## Why it matters
It enables fast testing, replaceable infrastructure, and clear boundaries.

## Key ideas
- Domain core depends on abstractions
- Adapters implement ports
- Composition root wires dependencies

## Practical workflow
- Define ports for repos and gateways
- Implement adapters in infrastructure
- Keep domain free of framework code

## Failure modes
- Business logic in adapters
- Ports too granular
- Cyclic dependencies between layers

## Checklist
- Domain has no infra imports
- Ports are minimal and stable
- Adapters are swappable
- Dependency direction is enforced

## References
- Hexagonal Architecture (Cockburn) — https://alistair.cockburn.us/hexagonal-architecture/
- Clean Architecture (Martin) — https://www.pearson.com/en-us/subject-catalog/p/clean-architecture/P200000006666
