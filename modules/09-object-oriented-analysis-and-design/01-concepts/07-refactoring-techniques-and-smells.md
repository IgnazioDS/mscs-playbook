# Refactoring Techniques and Smells

## Overview
Refactoring improves internal structure without changing behavior. Smells
highlight areas that need attention.

## Why it matters
Refactoring keeps systems maintainable and prevents design decay.

## Key ideas
- Small, reversible refactors
- Tests as safety nets
- Smells as signals, not proofs

## Practical workflow
- Identify smell and target scope
- Add or verify tests
- Apply small refactor steps

## Failure modes
- Refactoring without tests
- Mixing behavior changes with refactors
- Large, risky rewrites

## Checklist
- Tests pass before and after
- Changes are incremental
- Public interfaces remain stable
- Smells reduced over time

## References
- Refactoring (Fowler) — https://martinfowler.com/books/refactoring.html
- Refactoring.Guru Smells — https://refactoring.guru/refactoring/smells
