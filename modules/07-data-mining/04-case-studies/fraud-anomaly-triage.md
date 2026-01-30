# Fraud Anomaly Triage

TL;DR: Use unsupervised anomaly detection to triage suspicious transactions, prioritize analyst review, and reduce loss with controlled false positives.

## Overview
- Problem: fraud labels are sparse and delayed; losses accumulate quickly.
- Why it matters: analysts need a ranked queue of suspicious activity.
- Scope: card-present and card-not-present transaction monitoring.
- Stakeholders: risk, fraud ops, compliance, data science.
- Out of scope: hard real-time blocking or chargeback automation.
- Deliverable: daily triage queue with explanations and evidence.

## Requirements and Constraints
### Functional
- Score transactions daily and produce a top-N review queue.
- Provide reasons: velocity, amount deviation, geo mismatch.
- Support feedback loop from analysts for model refinement.
- Export results to case management system.

### Non-functional
- SLO: daily batch completes in < 1 hour for 5M transactions.
- Latency: queue available by 7am local time.
- Cost: under $200 per day.
- Privacy: mask card identifiers and PII.
- Compliance: retain audit trails for 12 months.

### Assumptions
- Fraud exhibits outlier behavior in amount, velocity, or geo.
- Labels from chargebacks are available after 30 to 60 days.

## System Design
### Components
- Feature builder aggregates transaction and customer history.
- Anomaly detector scores transactions and writes risk scores.
- Triage service ranks and filters the review queue.
- Feedback processor ingests analyst decisions.
- Case export integrates with case management.

### Data Flow
1) Transactions land in warehouse and feature store.
2) Feature builder creates per-transaction feature rows.
3) Anomaly detector scores and writes risk scores.
4) Triage service filters by thresholds and risk policies.
5) Feedback processor updates labeled dataset for evaluation.

### Interfaces
- `POST /triage/queue` with params: date, top_n, min_score.
- `GET /triage/{case_id}` for evidence and feature breakdown.
- `POST /triage/feedback` with analyst decision and notes.

### Data Schemas
- `txn_features`: txn_id, cust_id_hash, amount, merchant_id, mcc,
  geo_country, device_id_hash, velocity_24h, avg_amount_30d.
- `txn_scores`: run_id, txn_id, anomaly_score, risk_band, reasons.
- `triage_cases`: case_id, txn_id, status, analyst_decision.

## Data and Modeling Approach
- Feature engineering:
  - Amount z-score vs customer baseline.
  - Velocity features: txns per hour/day.
  - Geo and device changes within a short window.
- Modeling:
  - Isolation Forest for global anomalies.
  - Local Outlier Factor per merchant category.
  - Ensemble score with normalized ranks.
- Explainability:
  - Provide top 3 contributing features per case.
- Versioning:
  - Store model parameters and training window.

## Evaluation Plan
- Offline metrics: precision at K, recall at review budget.
- Use delayed labels for backtesting.
- Baselines: rules-only thresholding on amount and velocity.
- Acceptance gates:
  - Precision at K >= 0.25 for top 500 cases.
  - Recall at budget >= 0.6 vs baseline.
  - Case queue size matches analyst capacity.

## Failure Modes and Mitigations
- Model flags normal high-spend customers -> add customer tiers.
- Merchant-specific spikes -> segment by merchant category.
- Data leakage from labels -> train on pre-label windows only.
- Feedback loop bias -> separate evaluation and training windows.
- Sudden fraud shift -> add drift detection on feature distributions.

## Operational Runbook
### Logging
- Log model version, training window, score distributions.
- Log triage queue size and risk band counts.

### Metrics
- Precision at K, analyst acceptance rate, time-to-decision.
- Pipeline runtime and data freshness.

### Tracing
- Trace txn_id from scoring to case export.

### Alerts
- Queue size deviates by > 30% from 7-day average.
- Data freshness lag > 2 hours.
- Score distribution shifts beyond defined thresholds.

### Rollback
- Keep last 7 model versions and thresholds.
- Revert to prior risk thresholds if precision drops.

### On-call Checklist
- Validate transaction volume and feature completeness.
- Inspect top reasons for queue spikes.
- Coordinate with fraud ops on threshold changes.

## Security, Privacy, and Compliance
- Tokenize card identifiers and device IDs.
- Restrict case access to fraud ops only.
- Retain evidence and decisions for audit requests.

## Iteration Plan
- Add supervised model once labels reach coverage.
- Integrate graph features for connected fraud rings.
- Move to near-real-time scoring for top merchants.
