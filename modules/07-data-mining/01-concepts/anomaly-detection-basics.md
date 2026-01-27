# Anomaly Detection Basics

## What it is
Techniques for identifying rare or unusual observations that deviate from
normal patterns.

## Why it matters
Anomalies can indicate fraud, failures, or data quality issues.

## Practical workflow steps
- Define anomaly context (point, contextual, collective)
- Select model (IsolationForest, z-score)
- Set contamination or threshold
- Review false positives with domain experts

## Failure modes
- Using anomalies as labels without validation
- Ignoring seasonal or contextual effects
- Treating model scores as absolute truth

## Checklist
- Contamination rate documented
- Threshold calibrated on holdout data
- Alerts reviewed for precision/recall
- Drift and seasonality monitored

## References
- Isolation Forest (Liu et al.) — https://doi.org/10.1109/ICDM.2008.17
- scikit-learn Outlier Detection — https://scikit-learn.org/stable/modules/outlier_detection.html
