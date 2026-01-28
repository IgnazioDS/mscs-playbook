# Cohesion, Coupling, and Boundaries

## Overview
Cohesion measures how well responsibilities fit together; coupling measures
how strongly modules depend on each other.

## Why it matters
High cohesion and low coupling reduce change cost and enable testability.

## Key ideas
- Favor cohesive modules with narrow responsibilities
- Reduce direct dependencies with interfaces
- Define boundaries between domain, application, infrastructure

## Practical workflow
- Identify seams where dependencies can be inverted
- Split large classes into cohesive units
- Enforce layer boundaries with package structure

## Failure modes
- God objects with mixed concerns
- Cyclic dependencies between layers
- Leaky abstractions across boundaries

## Checklist
- Modules have single responsibility
- Dependencies point inward
- Boundaries are enforced in code
- Infra changes do not affect domain logic

## References
- Modular Design (Parnas) — https://doi.org/10.1145/361598.361623
- Agile Principles, Patterns, and Practices (Martin) — https://www.pearson.com/en-us/subject-catalog/p/agile-principles-patterns-and-practices-in-c/P200000006492
