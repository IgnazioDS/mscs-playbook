# Support Ticket Triage

## Problem + constraints
Classify support tickets into categories with high precision. Constraints: low
latency, noisy labels, multilingual inputs.

## Data + labeling strategy
Use historical tickets and human-labeled subsets. Add weak labels from routing
rules and periodically re-label.

## Baseline approach
TF-IDF + linear classifier with calibration. Compare to transformer baseline.

## Production considerations
- Latency budget per request
- Drift as new issues appear
- Monitoring misroutes and overrides

## Risks + mitigations
- Misclassification of urgent tickets -> rule-based overrides
- Label noise -> active learning and audits
- Domain shift -> retraining cadence

## Success metrics
- Macro F1, precision for high-priority classes
- Escalation rate and human override rate
