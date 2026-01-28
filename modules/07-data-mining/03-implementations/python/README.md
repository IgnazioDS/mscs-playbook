# Data Mining — Python Implementations

Deterministic, small-scale reference implementations for Module 07.

## Setup
- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r modules/07-data-mining/03-implementations/python/requirements.txt`

## Tests
- `python -m pytest -q modules/07-data-mining/03-implementations/python/tests`

## CLI mini-project
- `python modules/07-data-mining/03-implementations/python/src/cli.py cluster --dataset iris --k 3 --seed 42`
- `python modules/07-data-mining/03-implementations/python/src/cli.py anomaly --dataset breast_cancer --seed 42 --contamination 0.05`
- `python modules/07-data-mining/03-implementations/python/src/cli.py basket --dataset tiny_baskets --min-support 0.2 --min-confidence 0.6 --seed 42`
- Optional: `--out out/report.md`

## Reproducibility
- Set `--seed` for deterministic results and stable ordering.
- Outputs are sorted and rounded to reduce noise.
- Known limits: underlying BLAS/OS differences may cause small numeric drift.

## Example usage (pipeline)
```python
from src.pipeline.run_pipeline import run_pipeline

report, artifacts = run_pipeline(task="cluster", dataset="iris", seed=42, params={"k": 3})
print(report)
```

```python
report, artifacts = run_pipeline(task="basket", dataset="tiny_baskets", seed=42, params={"min_support": 0.2})
print(artifacts["n_rules"])
```
