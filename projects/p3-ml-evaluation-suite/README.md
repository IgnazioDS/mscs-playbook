---
summary: Portfolio project for deterministic machine-learning training and evaluation workflows across common supervised tasks.
tags:
  - project
  - portfolio
  - machine-learning
status: stable
format: project-brief
difficulty: intermediate
---

# p3-ml-evaluation-suite

## Purpose
Provide a reproducible baseline for model training/evaluation workflows across classification, regression, and clustering tasks.

## Scope
- Use module CLI commands as the first project baseline.
- Capture deterministic model metrics with fixed seeds.
- Validate evaluation behavior through automated tests.

## Modules Used
- [Foundations](../../modules/00-foundations/README.md)
- [Machine Learning](../../modules/03-machine-learning/README.md)
- [Computing Ethics and Society](../../modules/04-ethics/README.md)

## How to Run
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r modules/03-machine-learning/03-implementations/python/requirements.txt
python3 modules/03-machine-learning/03-implementations/python/src/cli.py train-classifier --dataset iris --seed 42
python3 modules/03-machine-learning/03-implementations/python/src/cli.py train-regressor --dataset california_housing --seed 42
python3 modules/03-machine-learning/03-implementations/python/src/cli.py cluster --dataset iris --k 3 --seed 42
```

## How to Test
```bash
python3 -m pytest -q modules/03-machine-learning/03-implementations/python/tests
```

## Expected Output
- CLI runs print deterministic metrics (`accuracy`, regression error, clustering summary).
- Test suite passes and protects regression-sensitive behaviors.
