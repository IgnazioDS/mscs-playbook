# Object-Oriented Analysis and Design

## Overview

This module covers how to model responsibilities, choose boundaries, apply core OO design principles, and scale those decisions into testing, refactoring, and architecture. The reading path moves from basic modeling and responsibility assignment toward maintainability and long-lived design decisions.

## Reading Path

1. [OOAD Foundations and UML Lite](01-concepts/01-ooad-foundations-and-uml-lite.md)
2. [Cohesion, Coupling, and Boundaries](01-concepts/02-cohesion-coupling-and-boundaries.md)
3. [SOLID Principles in Practice](01-concepts/03-solid-principles-in-practice.md)
4. [Domain Modeling and Aggregates](01-concepts/04-domain-modeling-and-aggregates.md)
5. [Design Patterns: When and Why](01-concepts/05-design-patterns-when-and-why.md)
6. [Testing OO Design and TDD](01-concepts/06-testing-oo-design-and-tdd.md)
7. [Refactoring Techniques and Smells](01-concepts/07-refactoring-techniques-and-smells.md)
8. [Architecture from OO to Hexagonal](01-concepts/08-architecture-from-oo-to-hexagonal.md)
9. [Documentation, ADRs, and Design Docs](01-concepts/09-documentation-adrs-and-design-docs.md)

## Module Map

- Concepts: [ordered concept index](01-concepts/README.md)
- Cheat sheet: [OOAD cheat sheet](02-cheatsheets/ooad-cheatsheet.md)
- Python implementations: [patterns cookbook and mini-project](03-implementations/python/README.md)
- TypeScript implementations: [implementation notes](03-implementations/typescript/README.md)
- Case studies: [case study index](04-case-studies/README.md)
- Exercises: [exercise index](05-exercises/README.md)
- Notes: [further notes](06-notes/README.md)

## Quickstart

- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `python3 -m pip install -r modules/09-object-oriented-analysis-and-design/03-implementations/python/requirements.txt`
- `python3 -m pytest -q modules/09-object-oriented-analysis-and-design/03-implementations/python/tests`
- `python3 modules/09-object-oriented-analysis-and-design/03-implementations/python/src/mini_project/cli.py`

## Design Document Trail

- [Mini-project design document](03-implementations/python/src/mini_project/docs/DESIGN.md)
- [ADR 0001: Architecture Style](03-implementations/python/src/mini_project/docs/adrs/0001-architecture-style.md)
- [ADR 0002: Domain Events](03-implementations/python/src/mini_project/docs/adrs/0002-domain-events.md)
- [ADR 0003: Repository Abstraction](03-implementations/python/src/mini_project/docs/adrs/0003-repository-abstraction.md)
- [ADR 0004: Payment Adapters](03-implementations/python/src/mini_project/docs/adrs/0004-payment-adapters.md)
