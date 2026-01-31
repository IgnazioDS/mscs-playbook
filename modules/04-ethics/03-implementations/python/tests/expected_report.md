# Ethics Review Report

## Metadata
- input_dir: modules/04-ethics/03-implementations/python/tests/fixtures/review_inputs/complete
- files_present: 5/5
- seed: 42

## Missing Inputs
- None

## Executive Summary
- overall_risk: LOW
- top_issues:
  - R1: Bias against low-income applicants (score 2)
  - R3: Over-reliance on recommendations (score 2)
  - R2: PII leakage in support logs (score 1)

## Compliance Checklist
- [x] privacy: consent=yes, pii_fields=2, retention_days=180, access_controls=rbac
- [x] fairness: metric=equal_opportunity_diff, value=0.08, threshold=0.1
- [x] transparency: purpose set, limitations provided
- [x] safety: high-risk mitigations present (2/2)
- [x] governance: owner and review_date set

## Risk Register
| id | risk | severity | likelihood | mitigation | residual | residual_score |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | Bias against low-income applicants | high | med | fairness evaluation and threshold checks | med/low | 2 |
| R2 | PII leakage in support logs | high | low | redaction and log access reviews | low/low | 1 |
| R3 | Over-reliance on recommendations | med | med | human-in-the-loop policy | med/low | 2 |

## Data Handling Summary
- sources: crm, tickets
- pii_fields: name, email
- retention_days: 180
- consent: yes
- access_controls: rbac

## Evaluation & Monitoring Plan
- fairness: equal_opportunity_diff=0.08 (threshold 0.1)
- quality: f1=0.82 (threshold 0.8)
- monitoring: drift, complaints

## Shipping Gate
- gate: PASS
- rationale: overall risk low; low risk and critical inputs present
