# p4-data-mining-pipeline

## Purpose
Deliver a deterministic data-mining baseline pipeline for profiling, cleaning, feature engineering, and clustering.

## Scope
- Use module CLI to run clustering and pipeline-style commands.
- Validate data-mining utilities with tests.
- Define stable outputs for future project-level orchestration.

## Modules Used
- 03-machine-learning
- 07-data-mining
- 06-big-data-architecture

## How to Run
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r modules/07-data-mining/03-implementations/python/requirements.txt
python3 modules/07-data-mining/03-implementations/python/src/cli.py cluster --dataset iris --k 3 --seed 42
python3 modules/07-data-mining/03-implementations/python/src/cli.py anomaly --dataset breast_cancer --contamination 0.05 --seed 42
python3 modules/07-data-mining/03-implementations/python/src/cli.py basket --dataset tiny_baskets --min-support 0.2 --min-confidence 0.6 --seed 42
```

## How to Test
```bash
python3 -m pytest -q modules/07-data-mining/03-implementations/python/tests
```

## Expected Output
- CLI commands print deterministic clustering/evaluation summaries.
- Test suite passes for cleaning, mining, features, loaders, and pipeline smoke checks.
