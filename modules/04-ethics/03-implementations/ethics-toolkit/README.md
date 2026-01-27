# Ethics Toolkit

## What this toolkit is
A lightweight governance kit for engineering teams to assess, document, and
manage ethical risks in computing systems.

## When to use it
- Pre-launch review for new systems
- Change review for model/data updates
- Incident response for safety or harm events

## How to use it in a PR workflow
1) Add a new `risk-assessment-template.md` to the PR description or linked doc.
2) Attach a `model-card-template.md` and `data-card-template.md` for the release.
3) Complete `deployment-go-no-go.md` before rollout.
4) If changes touch user data, complete `privacy-checklist.md`.
5) If model outputs impact decisions, complete `fairness-evaluation-checklist.md`.
6) For high-risk launches, run `red-team-checklist.md` and record findings.

## File index
- `risk-assessment-template.md`: structured risk analysis with severity/likelihood
- `model-card-template.md`: intended use, performance, limitations
- `data-card-template.md`: data provenance and consent basis
- `incident-response-runbook.md`: response steps and roles
- `red-team-checklist.md`: adversarial testing plan
- `privacy-checklist.md`: privacy safeguards
- `fairness-evaluation-checklist.md`: group fairness evaluation
- `deployment-go-no-go.md`: release gate checklist

## Definition of done
- Risk assessment completed and reviewed
- Model card and data card filled and linked
- Monitoring plan defines harm metrics and alert thresholds
- Privacy checklist completed for data flows
- Fairness evaluation performed for impacted groups
- Incident response runbook updated with on-call contacts
- Go/no-go checklist approved by owner
- Residual risks documented and accepted
