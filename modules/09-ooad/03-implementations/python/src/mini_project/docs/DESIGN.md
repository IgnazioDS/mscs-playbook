# Order & Payments Mini-Project Design

## Problem statement
Provide a small, realistic OO example that demonstrates boundaries, SOLID
principles, and several GoF patterns with tests and a runnable CLI.

## Goals
- Show clear domain/application/infrastructure separation
- Use Strategy, Adapter, Factory Method, Observer, Command patterns
- Provide deterministic tests and output

## Non-goals
- Production-grade persistence or external integrations
- Full payment lifecycle or refunds

## Architecture overview
- Domain: entities, pricing policies, domain events
- Application: services and commands
- Infrastructure: repositories, payments, notifier/event bus

## Key classes + responsibilities
- OrderService: coordinates placing and capturing orders
- OrderRepository: stores orders with stable IDs
- PaymentProcessorFactory: selects gateway by type
- EventBus: publishes domain events to subscribers
- DiscountPolicy: strategy for pricing adjustments

## Extension points
- Add a new discount strategy (Strategy)
- Add a new payment gateway adapter
- Add new subscribers for domain events
- Add new commands for use cases

## Run scenario
- `python modules/09-ooad/03-implementations/python/src/mini_project/cli.py`
