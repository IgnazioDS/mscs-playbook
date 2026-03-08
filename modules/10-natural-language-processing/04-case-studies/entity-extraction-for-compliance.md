# Entity Extraction for Compliance

## Problem + constraints
Extract regulated entities (PII, financial identifiers) from text. Constraints:
high recall, low false negatives, auditability.

## Data + labeling strategy
Combine rule-based labeling with human review. Build a gold set for evaluation.

## Baseline approach
Regex + dictionary baseline, then sequence labeling with CRF/transformer.

## Production considerations
- Explainability for compliance reviews
- Drift as new entity formats appear
- Redaction and storage policies

## Risks + mitigations
- Missed entities -> conservative thresholds + review queue
- Over-redaction -> class-specific tuning
- Data leakage -> strict access controls

## Success metrics
- Recall and precision per entity type
- Audit pass rate and review time
