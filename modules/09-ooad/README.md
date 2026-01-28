# 09-ooad

## Status
- Docs: complete
- Patterns cookbook: complete
- Mini-project: complete
- Case studies: pending

## Overview
This module covers OO analysis and design with SOLID, core design patterns,
testing strategy, and architecture styles such as hexagonal (ports and adapters).
It is structured as an engineering playbook.

## Prerequisites
- Python 3.10+
- Virtual environment tooling (venv)

## Quickstart
- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r modules/09-ooad/03-implementations/python/requirements.txt`
- `python -m pytest -q modules/09-ooad/03-implementations/python/tests`
- `python modules/09-ooad/03-implementations/python/src/mini_project/cli.py`

## Concepts
- [OOAD Foundations and UML-Lite](01-concepts/ooad-foundations-and-uml-lite.md)
- [SOLID Principles in Practice](01-concepts/solid-principles-in-practice.md)
- [Cohesion, Coupling, and Boundaries](01-concepts/cohesion-coupling-and-boundaries.md)
- [Domain Modeling and Aggregates](01-concepts/domain-modeling-and-aggregates.md)
- [Design Patterns: When and Why](01-concepts/design-patterns-when-and-why.md)
- [Testing OO Design and TDD](01-concepts/testing-oo-design-and-tdd.md)
- [Refactoring Techniques and Smells](01-concepts/refactoring-techniques-and-smells.md)
- [Architecture from OO to Hexagonal](01-concepts/architecture-from-oo-to-hexagonal.md)
- [Documentation, ADRs, and Design Docs](01-concepts/documentation-adrs-and-design-docs.md)

## Cheat sheet
- [OOAD Cheat Sheet](02-cheatsheets/ooad-cheatsheet.md)

## Case studies
- [Order & Payments Refactor](04-case-studies/order-payments-refactor.md)
- [Customer Onboarding Workflow](04-case-studies/customer-onboarding-workflow.md)
- [Inventory Sync Integration](04-case-studies/inventory-sync-integration.md)

## Implementations
- [Patterns cookbook](03-implementations/python/README.md)

## Mini-project
- [OOAD mini-project](03-implementations/python/README.md)

## Design docs and ADRs
- [Mini-project design doc](03-implementations/python/src/mini_project/docs/DESIGN.md)
- [ADR 0001 Architecture Style](03-implementations/python/src/mini_project/docs/adrs/0001-architecture-style.md)
- [ADR 0002 Domain Events](03-implementations/python/src/mini_project/docs/adrs/0002-domain-events.md)
- [ADR 0003 Repository Abstraction](03-implementations/python/src/mini_project/docs/adrs/0003-repository-abstraction.md)
- [ADR 0004 Payment Adapters](03-implementations/python/src/mini_project/docs/adrs/0004-payment-adapters.md)
