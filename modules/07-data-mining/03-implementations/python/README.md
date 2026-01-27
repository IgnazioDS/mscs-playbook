# Data Mining — Python Implementations

Deterministic, small-scale reference implementations for Module 07.

## Setup
- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r modules/07-data-mining/03-implementations/python/requirements.txt`

## Tests
- `python -m pytest -q modules/07-data-mining/03-implementations/python/tests`

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
