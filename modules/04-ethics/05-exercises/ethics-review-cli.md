# Ethics Review CLI

Generate a deterministic Markdown ethics review from structured inputs. The report is suitable for internal design reviews, launch checklists, and audit trails.

## Inputs
Place JSON files in a folder and run the CLI against it.

Required files:
- `system.json`: purpose, users, deployment context, owner, review date
- `data.json`: sources, retention_days, pii_fields, consent, access_controls
- `model.json`: model_type, training, evaluation, limitations
- `risks.json`: list of risks with severity/likelihood and mitigations
- `metrics.json`: fairness/quality metrics and monitoring plan

Missing files will be listed under **Missing Inputs** and contribute to the gate decision.

## Example
```bash
python3 modules/04-ethics/03-implementations/python/src/ethics/mini_project/cli.py ethics-review \
  --in modules/04-ethics/03-implementations/python/tests/fixtures/review_inputs/complete \
  --out /tmp/eth04-report.md \
  --seed 42
```

## Scoring rules
- severity ∈ {low, med, high} → points {1, 2, 3}
- likelihood ∈ {low, med, high} → points {1, 2, 3}
- risk_score = severity_points * likelihood_points
- overall risk:
  - HIGH if any residual risk_score ≥ 6 or missing critical inputs
  - MED if average residual risk_score ≥ 3
  - LOW otherwise
- shipping gate:
  - FAIL if missing critical inputs or HIGH with no mitigations
  - CONDITIONAL if HIGH with mitigations or MED
  - PASS if LOW and critical inputs are present

## How to extend
- Add JSON schema validation for inputs.
- Add more checklist items for jurisdiction-specific compliance.
- Integrate export to PR templates or ticketing systems.
