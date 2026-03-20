---
summary: Portfolio project for verification-oriented autonomy demos that combine system modeling and AI planning diagnostics.
tags:
  - project
  - portfolio
  - autonomy
status: stable
format: project-brief
difficulty: advanced
---

# p9-autonomous-verification-demo

## Purpose
Provide a verification-oriented autonomy baseline combining system modeling and AI planning diagnostics.

## Scope
- Run autonomous-systems demo and AI mini-project evaluation flow.
- Validate deterministic outputs for reachability/diagnosis/scheduling style checks.
- Establish a reproducible baseline for formal verification demos.

## Modules Used
- [Autonomous Systems](../../modules/05-autonomous-systems/README.md)
- [Artificial Intelligence](../../modules/13-artificial-intelligence/README.md)
- [Reinforcement Learning](../../modules/14-reinforcement-learning/README.md)

## How to Run
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r modules/05-autonomous-systems/03-implementations/python/requirements.txt
python3 -m pip install -r modules/13-artificial-intelligence/03-implementations/python/requirements.txt
python3 modules/05-autonomous-systems/03-implementations/python/src/demo.py
python3 modules/13-artificial-intelligence/03-implementations/python/src/ai13/mini_project/cli.py evaluate --seed 42
```

## How to Test
```bash
python3 -m pytest -q modules/05-autonomous-systems/03-implementations/python/tests
python3 -m pytest -q modules/13-artificial-intelligence/03-implementations/python/tests
```

## Expected Output
- Autonomous demo prints deterministic modeling/verification summaries.
- AI13 evaluation reports pass/fail status for bundled scenarios.
- Both module test suites pass.
