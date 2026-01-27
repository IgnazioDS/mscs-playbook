# Ethics Cheat Sheet

## Red flags
- Missing consent or unclear data provenance
- Disparate error rates across groups
- High-stakes decisions without recourse
- No monitoring or rollback plan

## Decision flow (ship / pause / redesign)
1) Are harms understood and bounded?
2) Are protections and mitigations in place?
3) Is there a clear owner and monitoring plan?
- If any answer is no → pause or redesign.

## Privacy and data handling do/don’t
- Do minimize data collection and retention
- Do restrict access with least privilege
- Don’t reuse data outside stated purpose
- Don’t ship with unclear consent

## Fairness evaluation quick guide
- Define protected groups and outcomes
- Compute error rates by group
- Investigate large disparities
- Document tradeoffs and decisions

## Disclosure template bullets
- Intended use and limitations
- Known failure modes and risk scenarios
- Data sources and update cadence
- Contact for issues and recourse
