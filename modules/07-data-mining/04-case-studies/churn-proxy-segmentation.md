# Churn Proxy Segmentation

TL;DR: When churn labels are delayed or missing, cluster customers using proxy signals, validate stability, and ship actionable segments to CRM for retention experiments.

## Overview
- Problem: churn labels arrive months later, slowing retention efforts.
- Why it matters: marketing needs segments now to test offers and messaging.
- Scope: monthly segmentation for B2C subscription and retail accounts.
- Stakeholders: growth, CRM, analytics, customer success.
- Out of scope: individual churn prediction or real-time scoring.
- Deliverable: segment definitions with risk heuristics and playbooks.

## Requirements and Constraints
### Functional
- Build a monthly customer feature table with behavioral signals.
- Cluster customers into 5 to 8 segments with interpretable profiles.
- Provide segment labels and counts to CRM and analytics tools.
- Support backtesting with historical snapshots.

### Non-functional
- SLO: monthly run completes in < 2 hours for 10M customers.
- Latency: export ready by day 2 of each month.
- Cost: under $300 per run.
- Privacy: remove PII and store only hashed customer IDs.
- Auditability: store feature snapshots and cluster parameters.

### Assumptions
- Engagement and spend are predictive of churn risk.
- Behavioral data arrives daily with a 24-hour delay.

## System Design
### Components
- Feature builder aggregates transactions, sessions, and support tickets.
- Clustering job trains and assigns segment labels.
- Segment profiler computes descriptive stats and heuristics.
- Segment store persists labels with run_id and snapshot date.
- CRM export writes segment labels to a shared bucket.

### Data Flow
1) Daily events land in object storage and warehouse tables.
2) Monthly feature builder creates a snapshot table.
3) Clustering job fits model and assigns segment IDs.
4) Profiler generates segment summaries and heuristics.
5) CRM export writes labels and descriptions to downstream tools.

### Interfaces
- `GET /segments/{snapshot_date}` for segment counts and summaries.
- `POST /segments/query` with filters like segment_id, spend_band.
- `GET /segments/{snapshot_date}/customers` for export sampling.

### Data Schemas
- `customer_features`: cust_id_hash, recency_days, frequency_90d, spend_90d,
  support_tickets_90d, refund_rate, tenure_days, last_login_days.
- `segment_labels`: snapshot_date, cust_id_hash, segment_id, model_version.
- `segment_profiles`: segment_id, size, medians, churn_proxy_rate.

## Data and Modeling Approach
- Feature engineering:
  - Recency, frequency, monetary (RFM) features.
  - Support load as a friction proxy.
  - Refund rate and chargebacks.
- Scaling and encoding:
  - Log-transform spend, z-score continuous features.
  - Cap outliers at p99 to stabilize clusters.
- Clustering:
  - K-Means with k=6 as default, tuned with silhouette.
  - Alternative: Gaussian Mixture for soft assignments.
- Proxy churn definition:
  - Inactivity > 60 days or no purchase in 2 billing cycles.
- Versioning:
  - Store model config, feature version, and snapshot date.

## Evaluation Plan
- Offline metrics: silhouette score, Davies-Bouldin, cluster size balance.
- Stability: adjusted Rand index across consecutive months > 0.7.
- Business coherence: monotonicity of risk proxy across segments.
- Baselines: RFM buckets and manual rules.
- Acceptance gates:
  - No segment smaller than 3% of population.
  - At least one high-risk segment with proxy churn rate > 2x average.
  - Segment profiles are interpretable by marketing.

## Failure Modes and Mitigations
- Clusters collapse into a dominant segment -> tune k and rebalance features.
- Seasonality breaks stability -> include month-of-year indicators.
- Proxy churn mislabels seasonal users -> separate seasonal cohort features.
- Data gaps create false churn -> enforce data completeness checks.
- Feature drift -> compare distributions month-over-month.

## Operational Runbook
### Logging
- Log snapshot date, input tables, missing rates, feature stats.
- Log clustering parameters, inertia, and evaluation metrics.

### Metrics
- Runtime, silhouette score, cluster size distribution.
- Proxy churn rate per segment and overall.

### Tracing
- Trace snapshot_date from feature builder to CRM export.

### Alerts
- Feature missingness > 5% for key columns.
- Segment size imbalance (largest > 50%).
- Silhouette drops by > 0.1 from prior month.

### Rollback
- Keep last 6 snapshots; CRM export can revert to previous labels.

### On-call Checklist
- Validate feature table freshness and volume.
- Inspect cluster centers for drift and anomalies.
- Recompute with conservative scaling if needed.

## Security, Privacy, and Compliance
- Hash customer IDs before export.
- Restrict access to segment labels to marketing and analytics roles.
- Document proxy churn definition for transparency.

## Iteration Plan
- Add survival-analysis labels when real churn matures.
- Incorporate product usage sequences with sequence embeddings.
- Move from batch monthly to biweekly snapshots.
