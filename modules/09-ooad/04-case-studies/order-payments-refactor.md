# Order and Payments Refactor

TL;DR: Refactor a monolithic checkout into layered services with clear boundaries, introduce an anti-corruption layer to the payment provider, and migrate using a strangler approach.

## Overview
- Problem: checkout code is tightly coupled, fragile, and hard to change.
- Why it matters: payment failures and slow releases impact revenue.
- Scope: order placement, payment authorization, and refund flows.
- Stakeholders: backend, payments, finance, support, compliance.
- Out of scope: full rewrite of inventory or shipping services.
- Deliverable: stable checkout with contract-based integrations.
- Success: releases can ship weekly without payment regressions.
- Constraint: keep existing API contracts for mobile clients.

## Requirements and Constraints
### Functional
- Support authorization, capture, and refund workflows.
- Maintain idempotency for payment retries.
- Provide audit-ready order and payment records.
- Preserve existing public checkout API during migration.

### Non-functional
- SLO: 99.9% checkout availability.
- Latency: p95 checkout under 900 ms.
- Cost: avoid adding more than 10% compute.
- Safety: never double-charge a customer.
- Reliability: tolerate payment provider timeouts.

### Assumptions
- Payment provider API is external and rate-limited.
- Existing order data model cannot change immediately.
- Legacy system uses a shared database with other domains.

## System Design
### Components
- Presentation layer: REST controller for checkout endpoints.
- Application layer: use cases for place-order and refund.
- Domain layer: Order, Payment, and Policy aggregates.
- Infrastructure layer: repositories, provider adapters, outbox.
- Anti-corruption layer: isolates external payment API model.

### Data Flow
1) API receives checkout request and validates input.
2) Application service creates Order aggregate.
3) Payment service authorizes via anti-corruption adapter.
4) Domain events are stored in outbox for async processing.
5) Order status updates are persisted and returned.

### Interfaces
- `POST /checkout` with cart and payment token.
- `POST /payments/{order_id}/capture` for capture.
- `POST /payments/{order_id}/refund` for refunds.

### Data Schemas
- `orders`: order_id, user_id, total, status, created_at.
- `payments`: payment_id, order_id, status, provider_ref, amount.
- `outbox`: event_id, aggregate_id, event_type, payload.

## Data and Modeling Approach
- Aggregates: Order owns line items and status transitions.
- Payment as a separate aggregate with state machine.
- Patterns:
  - Repository for persistence abstraction.
  - Unit of Work for atomic writes.
  - Anti-corruption layer for provider mapping.
  - Outbox for reliable event publishing.
- Migration strategy:
  - Strangler facade keeps old endpoint while new path grows.
  - Dual-write to legacy and new payment tables during cutover.

## Evaluation Plan
- Metrics: checkout success rate, payment latency, duplicate charge rate.
- Baselines: current monolith metrics and error rates.
- Acceptance gates:
  - No increase in payment failures vs baseline.
  - p95 latency within 10% of existing flow.
  - Zero duplicate charge incidents in staging.

## Failure Modes and Mitigations
- Provider timeout -> circuit breaker and retry with idempotency key.
- Partial writes -> use Unit of Work and transactional outbox.
- Schema mismatch -> anti-corruption layer with strict mapping tests.
- Migration regression -> blue/green release with feature flags.
- Data divergence -> reconciliation job during dual-write phase.

## Operational Runbook
### Logging
- Log correlation_id across order and payment flows.
- Record provider responses and idempotency keys.

### Metrics
- Success rate, latency, provider error rate.
- Refund rate and chargeback volume.

### Tracing
- Trace order_id from API to provider adapter.

### Alerts
- Checkout success rate drops below 99%.
- Provider error rate spikes above 2%.
- Duplicate payment detection triggers.

### Rollback
- Feature flag to revert to legacy payment path.
- Keep rollback playbook for schema toggles.

### On-call Checklist
- Verify provider health and rate limits.
- Inspect outbox backlog and reconciliation status.
- Validate dual-write consistency reports.

## Security, Privacy, and Compliance
- Tokenize payment data and avoid storing PAN.
- Apply PCI scope reduction with hosted fields.
- Restrict access to payment logs and audit data.

## Iteration Plan
- Introduce payment method plugins (wallets, BNPL).
- Add saga for order, payment, and inventory consistency.
- Remove legacy tables after migration completes.
