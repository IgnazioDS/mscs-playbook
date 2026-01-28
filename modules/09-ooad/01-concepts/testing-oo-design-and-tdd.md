# Testing OO Design and TDD

## Overview
Testing OO design focuses on behavior at boundaries. TDD drives design by
writing tests first and evolving interfaces through feedback.

## Why it matters
Testable OO designs tend to be cohesive and loosely coupled.

## Key ideas
- Test behavior, not internals
- Use fakes at boundaries
- Keep dependencies injectable

## Practical workflow
- Define use case behavior in tests
- Mock infrastructure behind interfaces
- Refactor only with green tests

## Failure modes
- Over-mocking implementation details
- Tests that couple to private methods
- Fragile tests that block refactoring

## Checklist
- Tests target public behavior
- Dependencies are abstracted
- Extension points are covered
- Tests run deterministically

## References
- Test-Driven Development (Beck) — https://www.oreilly.com/library/view/test-driven-development/0321146530/
- xUnit Test Patterns (Meszaros) — https://www.pearson.com/en-us/subject-catalog/p/xunit-test-patterns/P200000006793
