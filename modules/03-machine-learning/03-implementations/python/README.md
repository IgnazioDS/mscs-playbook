# Module 03 — Machine Learning (Python)

## Overview
Folders:
- `src/datasets`: built-in dataset loading and deterministic splits
- `src/preprocessing`: sklearn pipelines
- `src/models`: baseline estimators
- `src/evaluation`: metrics, cross-validation, plots
- `src/unsupervised`: clustering and PCA helpers
- `src/utils`: reproducibility utilities

Supported datasets: `iris`, `breast_cancer`, `california_housing`

Reproducibility: set `--seed` in CLI and keep deterministic splits.

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r modules/03-machine-learning/03-implementations/python/requirements.txt
```

## Run tests
```bash
python -m pytest -q modules/03-machine-learning/03-implementations/python/tests
```

## CLI examples
```bash
python modules/03-machine-learning/03-implementations/python/src/cli.py train-classifier --dataset iris --seed 42
python modules/03-machine-learning/03-implementations/python/src/cli.py train-regressor --dataset california_housing --seed 42
python modules/03-machine-learning/03-implementations/python/src/cli.py cluster --dataset iris --k 3 --seed 42
```
