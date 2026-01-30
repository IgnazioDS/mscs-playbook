# From Baseline to Deployable Model

## Problem statement

Predict customer churn for a subscription service to prioritize retention outreach.

## Baseline model

- Logistic regression with standard scaling and class weights.
- Metric: PR-AUC and recall at fixed precision.

## Evaluation plan

- Deterministic train/val/test split with fixed seed.
- Stratified cross-validation on training set.
- Final evaluation on untouched test set.

## Iteration loop

1) Feature hygiene: remove leakage features, normalize numeric features.
2) Regularization tuning: L2 strength via CV.
3) Model selection: compare logistic vs tree-based baseline.

## Error analysis + mitigations

- Analyze false negatives by segment (tenure, region).
- Add interaction features or segment-specific thresholds.
- Improve labeling for ambiguous churn cases.

## Deployment considerations

- Monitor data drift (input distribution shift).
- Track PR-AUC and recall over time.
- Retrain cadence and model versioning.
