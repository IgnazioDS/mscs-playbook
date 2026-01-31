# Retail Basket Analysis

TL;DR: Build an association-rule mining pipeline on retail transactions to surface bundle insights, validate them with controlled experiments, and ship recommendations to merchandising and promo tools.

## Overview
- Problem: discover product bundles that drive higher basket size and margin.
- Why it matters: merchandising and promotions need evidence-backed bundles, not intuition.
- Scope: store-level and category-level insights for weekly promo planning.
- Stakeholders: merchandising, pricing, data science, store ops.
- Out of scope: real-time personalization and ad targeting.
- Deliverable: weekly bundle report with top 50 rules per region.
- Success: planners can act without additional analysis support.

## Requirements and Constraints
### Functional
- Ingest daily transaction logs and product catalog updates.
- Compute frequent itemsets and association rules per store and per region.
- Serve top rules via an insights API and export CSV for planners.
- Provide rule explanations with support/confidence/lift and sample baskets.

### Non-functional
- SLO: weekly batch completes in < 4 hours for 100M line items.
- Latency: API responses < 200 ms p95 for top rules queries.
- Cost: pipeline under $400 per weekly run on commodity compute.
- Privacy: remove customer identifiers; aggregate at store or region.
- Auditability: keep reproducible runs with versions and parameters.

### Assumptions
- Transactions are immutable; corrections arrive as separate events.
- Product catalog contains stable category hierarchy and pricing.

## System Design
### Components
- Ingestion job reads transaction events and catalog snapshots.
- Cleaning job normalizes product IDs, removes invalid baskets.
- Mining service computes frequent itemsets and rules.
- Rule store persists rules with metadata and version tags.
- Insights API provides filtered rule queries.
- Export job writes CSVs to a shared planning bucket.

### Data Flow
1) Raw transactions land in object storage partitioned by date.
2) Cleaning job builds basket records and dedupes items per basket.
3) Mining service builds frequent itemsets per segment.
4) Rule store writes top rules with metrics and sample baskets.
5) Insights API and export job read rules for downstream users.

### Interfaces
- `POST /rules/query` with filters: store_id, category, min_lift.
- `GET /rules/{run_id}/top` for precomputed top rules.
- `GET /rules/{run_id}/samples` for sample baskets.

### Data Schemas
- `transactions`: basket_id, store_id, timestamp, product_id, qty, price.
- `catalog`: product_id, name, category, brand, active_flag.
- `rules`: run_id, lhs_items, rhs_items, support, confidence, lift, coverage.

## Data and Modeling Approach
- Basket building: group by basket_id, remove duplicate product_id.
- Item filtering: drop items with < 0.01% frequency to control noise.
- Association rules: FP-Growth with min_support and min_confidence.
- Segmentation: rules computed per store, region, and top categories.
- Versioning: store run parameters and input snapshot IDs.
- Examples of rule artifacts:
  - LHS: ["pasta", "tomato_sauce"] => RHS: ["parmesan"] lift 3.1
  - LHS: ["tortilla", "beans"] => RHS: ["salsa"] confidence 0.42

## Evaluation Plan
- Offline metrics: support, confidence, lift, coverage, novelty rate.
- Stability checks: rule overlap week-over-week > 0.6 for top 50.
- Baselines: frequent-item-only bundles without lift requirement.
- Online metric: basket size uplift in A/B test for featured bundles.
- Acceptance gates:
  - Top rules coverage >= 5% of baskets per store.
  - Lift >= 1.5 for promoted bundles.
  - No single brand dominates > 40% of top rules.

## Failure Modes and Mitigations
- Seasonality causes spurious rules -> compute seasonal baselines.
- Promotions leak into rules -> exclude promo weeks for baseline runs.
- Long tail items create noise -> increase min_support and prune.
- Basket fragmentation -> dedupe and enforce min basket size.
- Category drift -> refresh catalog mapping each run.

## Operational Runbook
### Logging
- Record input partitions, run parameters, rule counts per segment.
- Log top rules and coverage by store and category.

### Metrics
- Pipeline duration, rule counts, coverage, lift distribution.
- API latency and error rate per endpoint.

### Tracing
- Trace run_id from ingestion through rule store and API response.

### Alerts
- Pipeline runtime > 2x baseline.
- Rule coverage drops by > 30% week-over-week.
- API p95 latency > 300 ms for 15 minutes.

### Rollback
- Keep last 4 weekly runs in rule store.
- API defaults to latest successful run_id.

### On-call Checklist
- Check ingestion partitions and catalog snapshot.
- Validate item frequency distribution for anomalies.
- Recompute with conservative thresholds if needed.

## Security, Privacy, and Compliance
- Remove customer IDs and hash store IDs for exports.
- Limit rule exports to aggregated segments.
- Store exports in access-controlled buckets.
- Retain raw transactions under least-privilege policies.

## Iteration Plan
- Add time-of-day and day-of-week segmentation.
- Integrate margin to prioritize high-profit bundles.
- Add simple uplift modeling for promo targeting.
