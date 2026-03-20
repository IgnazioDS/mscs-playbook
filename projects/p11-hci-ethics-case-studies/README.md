---
summary: Portfolio project that combines HCI evaluation workflows with ethics review tooling for human-centered system analysis.
tags:
  - project
  - portfolio
  - hci
status: stable
format: project-brief
difficulty: advanced
---

# p11-hci-ethics-case-studies

## Purpose
Combine human-computer interaction study analysis and ethics review tooling into a practical human-centered evaluation baseline.

## Scope
- Generate a deterministic human-computer interaction study report from CSV fixtures.
- Generate an ethics review report from structured risk inputs.
- Validate both toolchains with automated tests.

## Modules Used
- [Human-Computer Interaction](../../modules/15-human-computer-interaction/README.md)
- [Computing Ethics and Society](../../modules/04-ethics/README.md)
- [Generative AI](../../modules/11-generative-ai/README.md)

## How to Run
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r modules/15-human-computer-interaction/03-implementations/python/requirements.txt
python3 -m pip install -r modules/04-ethics/03-implementations/python/requirements.txt
python3 modules/15-human-computer-interaction/03-implementations/python/src/hci/mini_project/cli.py study-report \
  --in modules/15-human-computer-interaction/03-implementations/python/tests/fixtures/study_csvs \
  --out /tmp/hci15-report.md \
  --seed 42
python3 modules/04-ethics/03-implementations/python/src/ethics/mini_project/cli.py ethics-review \
  --in modules/04-ethics/03-implementations/python/tests/fixtures/review_inputs/complete \
  --out /tmp/eth04-report.md \
  --seed 42
```

## How to Test
```bash
python3 -m pytest -q modules/15-human-computer-interaction/03-implementations/python/tests
python3 -m pytest -q modules/04-ethics/03-implementations/python/tests
```

## Expected Output
- Human-computer interaction command writes `/tmp/hci15-report.md` with study metrics and recommendations.
- Ethics command writes `/tmp/eth04-report.md` with risk findings and review summary.
- Both test suites pass.
