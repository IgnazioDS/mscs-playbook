# ADR 0004: Payment Adapters and Factory

## Context
Payment gateways have different interfaces (cents vs dollars). We need a unified
interface and simple selection.

## Decision
Use Adapters to normalize gateway APIs and a factory to select processors.

## Alternatives
- Branching logic in the service
- Direct gateway usage in domain

## Consequences
- Clear separation and easy extension
- Slightly more classes for a small example
