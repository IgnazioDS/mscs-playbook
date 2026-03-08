# Inventory Sync Integration

TL;DR: Integrate an external warehouse system using an anti-corruption layer, map events into a clean domain model, and migrate with a controlled strangler approach.

## Overview
- Problem: inventory data arrives from external WMS with inconsistent schemas.
- Why it matters: stock inaccuracies cause oversells and cancellations.
- Scope: inventory updates, reservations, and reconciliation.
- Stakeholders: supply chain, backend, finance, ops.
- Out of scope: procurement and demand forecasting.
- Deliverable: reliable inventory sync with clear ownership boundaries.
- Success: downstream teams trust inventory events without manual checks.
- Constraint: legacy integration must keep running during migration.

## Requirements and Constraints
### Functional
- Ingest WMS inventory updates and reconcile local counts.
- Publish inventory events to downstream services.
- Provide manual override for reconciliation disputes.
- Support backfills and replays for outages.

### Non-functional
- SLO: inventory freshness within 5 minutes.
- Latency: ingest and publish within 60 seconds.
- Cost: sustain 5k updates per minute.
- Safety: prevent negative inventory in core system.
- Reliability: tolerate WMS outages with backfill.
- Availability: ingestion service uptime >= 99.9%.

### Assumptions
- WMS system is the source of truth for physical counts.
- Local system is the source of truth for reservations.
- WMS can batch updates at 1 minute intervals.

## System Design
### Components
- Ingestion service pulls or receives WMS updates.
- Anti-corruption layer maps WMS schema to domain model.
- Inventory domain service applies updates and reservations.
- Event publisher emits inventory events to bus.
- Reconciliation service detects and resolves mismatches.

### Data Flow
1) WMS update arrives via API or file drop.
2) ACL maps external fields into internal inventory model.
3) Domain service applies update and emits events.
4) Reconciliation compares WMS and internal counts.
5) Alerting flags discrepancies for review.

### Interfaces
- `POST /inventory/sync` for WMS updates.
- `GET /inventory/{sku}` for current counts.
- `POST /inventory/{sku}/reconcile` for manual adjustments.

### Data Schemas
- `inventory`: sku, on_hand, reserved, available, updated_at.
- `wms_updates`: wms_id, sku, quantity, status, received_at.
- `inventory_events`: event_id, sku, delta, source, timestamp.

## Data and Modeling Approach
- Domain model separates on_hand and reserved inventory.
- Patterns:
  - Adapter and ACL to isolate WMS models.
  - Repository for persistence.
  - Domain events for downstream consumers.
- Idempotency keys include wms_id and update sequence number.
- Migration strategy:
  - Strangler: new sync handles a subset of SKUs first.
  - Dual processing with consistency checks.

## Evaluation Plan
- Metrics: freshness lag, reconciliation rate, oversell rate.
- Baselines: legacy nightly sync metrics.
- Acceptance gates:
  - Freshness lag median < 2 minutes.
  - Oversell rate decreases by 30%.
  - Reconciliation discrepancies < 0.5% of SKUs.

## Failure Modes and Mitigations
- WMS schema changes -> schema versioning and contract tests.
- Duplicate updates -> idempotency keys and dedupe.
- Message loss -> persistent queue with replay.
- Drift between systems -> daily reconciliation job.
- Migration regression -> feature flags and staged rollout.

## Operational Runbook
### Logging
- Log wms_id, sku, deltas, and applied updates.
- Record reconciliation decisions and operator notes.

### Metrics
- Update throughput, lag, and error rate.
- Discrepancy count and resolution time.

### Tracing
- Trace sku across ingestion, domain update, and event publish.

### Alerts
- Lag exceeds 5 minutes for > 10 minutes.
- Discrepancy rate spikes above threshold.
- WMS update failures > 1%.

### Rollback
- Switch back to legacy sync for affected SKUs.
- Pause ingestion and backfill after fix.

### On-call Checklist
- Validate WMS connectivity and schema version.
- Check dedupe and idempotency logs.
- Trigger backfill if updates were missed.

## Security, Privacy, and Compliance
- Authenticate WMS updates with signed requests.
- Limit access to reconciliation endpoints.
- Retain audit logs for inventory adjustments.

## Iteration Plan
- Add real-time reservation sync to WMS.
- Introduce predictive alerts for low-stock anomalies.
- Expand to multi-warehouse support with routing rules.
