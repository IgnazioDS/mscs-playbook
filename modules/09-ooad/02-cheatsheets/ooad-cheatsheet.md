# OOAD Cheat Sheet

## SOLID quick checks
- SRP: one reason to change
- OCP: extend without modifying
- LSP: subtype substitutable
- ISP: small, cohesive interfaces
- DIP: depend on abstractions

## Common smells -> refactor moves
- God class -> Extract class
- Long method -> Extract method
- Feature envy -> Move method
- Shotgun surgery -> Consolidate responsibilities
- Primitive obsession -> Introduce value object

## Pattern selection guide
- Create objects flexibly -> Factory Method
- Vary algorithm -> Strategy
- Notify on events -> Observer
- Wrap behavior -> Decorator
- Encapsulate requests -> Command
- Integrate external APIs -> Adapter

## How to review OO code
- Are responsibilities clear and minimal?
- Are dependencies injected or hidden?
- Are extension points tested?
- Are invariants enforced at boundaries?

## Testing seams + dependency injection tactics
- Constructor injection for dependencies
- Interface boundaries for infrastructure
- In-memory fakes for repositories
- Events for decoupled notifications
