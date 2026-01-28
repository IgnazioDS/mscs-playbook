# SOLID Principles in Practice

## Overview
SOLID is a set of OO design principles that improve extensibility and
maintainability: SRP, OCP, LSP, ISP, DIP.

## Why it matters
Applying SOLID reduces ripple effects and enables safe change.

## Key ideas
- Single responsibility per class
- Extension via composition
- Dependency inversion toward abstractions

## Practical workflow
- Audit responsibilities per class
- Extract interfaces at seams
- Replace inheritance with composition when behavior varies

## Failure modes
- Over-abstracting prematurely
- “Interface everywhere” without need
- Inheritance hierarchies violating substitutability

## Checklist
- Each class has one reason to change
- Dependencies flow toward domain
- Interfaces are small and focused
- Subtypes are safely substitutable

## References
- Clean Architecture (Martin) — https://www.pearson.com/en-us/subject-catalog/p/clean-architecture/P200000006666
- SOLID Principles (Martin) — https://blog.cleancoder.com/
