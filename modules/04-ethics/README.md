# 04-ethics

## Status
- Docs complete
- Case studies complete
- Toolkit complete
- Ethics Review CLI and tests complete

## Overview
This module focuses on practical engineering ethics and risk management for
computing systems. It provides decision frameworks, checklists, and applied
examples for fairness, privacy, transparency, safety, and governance.

## Prerequisites
- Python 3.10+
- Virtual environment tooling (venv)

## Quickstart
From the repo root:
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r modules/04-ethics/03-implementations/python/requirements.txt
python3 -m pytest -q modules/04-ethics/03-implementations/python/tests
python3 modules/04-ethics/03-implementations/python/src/ethics/mini_project/cli.py ethics-review \
  --in modules/04-ethics/03-implementations/python/tests/fixtures/review_inputs/complete \
  --out /tmp/eth04-report.md \
  --seed 42
```

## How to use this module
1) Read concepts
2) Use the cheat sheet in reviews
3) Apply a case study pattern
4) Use toolkit templates in PRs

## Concepts
- [Ethical Frameworks for Engineers](01-concepts/ethical-frameworks-for-engineers.md)
- [Professional Ethics and ACM Code](01-concepts/professional-ethics-acm-code.md)
- [Fairness, Bias, and Discrimination](01-concepts/fairness-bias-and-discrimination.md)
- [Privacy and Data Protection Basics](01-concepts/privacy-data-protection-basics.md)
- [Transparency, Explainability, and Disclosure](01-concepts/transparency-explainability-and-disclosure.md)
- [Safety, Security, and Misuse](01-concepts/safety-security-and-misuse.md)
- [Accountability, Governance, and Audits](01-concepts/accountability-governance-and-audits.md)
- [Ethics in the ML Lifecycle](01-concepts/ethics-in-the-ml-lifecycle.md)

## Cheat sheet
- [Ethics Cheat Sheet](02-cheatsheets/ethics-cheatsheet.md)

## Case studies
- [Biased Hiring Model](04-case-studies/biased-hiring-model.md)
- [Recommender System Radicalization](04-case-studies/recommender-system-radicalization.md)
- [Health App Data Misuse](04-case-studies/health-app-data-misuse.md)
- [GenAI Customer Support Hallucinations](04-case-studies/genai-customer-support-hallucinations.md)

## Toolkit
- [Ethics Toolkit README](03-implementations/ethics-toolkit/README.md)
- [Risk Assessment Template](03-implementations/ethics-toolkit/risk-assessment-template.md)
- [Model Card Template](03-implementations/ethics-toolkit/model-card-template.md)
- [Data Card Template](03-implementations/ethics-toolkit/data-card-template.md)
- [Incident Response Runbook](03-implementations/ethics-toolkit/incident-response-runbook.md)
- [Red-Team Checklist](03-implementations/ethics-toolkit/red-team-checklist.md)
- [Privacy Checklist](03-implementations/ethics-toolkit/privacy-checklist.md)
- [Fairness Evaluation Checklist](03-implementations/ethics-toolkit/fairness-evaluation-checklist.md)
- [Deployment Go/No-Go](03-implementations/ethics-toolkit/deployment-go-no-go.md)
- [Toolkit Worked Example](06-notes/toolkit-worked-example.md)

## Implementations
- [Python implementations](03-implementations/python/README.md)

## Mini-project
- [Ethics Review CLI](05-exercises/ethics-review-cli.md)
