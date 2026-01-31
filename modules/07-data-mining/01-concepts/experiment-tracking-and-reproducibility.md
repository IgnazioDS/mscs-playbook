# Experiment Tracking and Reproducibility

## What it is

Practices to ensure data mining results can be reproduced and audited over time.

## Why it matters

Data mining outcomes change with data versions, seeds, and preprocessing.
Without tracking, results are not trustworthy.

## Practical workflow steps

- Record dataset version and preprocessing steps
- Fix random seeds and split strategies
- Log metrics, parameters, and artifacts
- Store reports with metadata

## Failure modes

- Untracked dataset changes
- Non-deterministic pipelines
- Missing run context for decisions

## Checklist

- Random seeds set and logged
- Versions for data and code captured
- Outputs stored with timestamps
- Reproducibility documented in README

## References

- MLflow Tracking — <https://mlflow.org/docs/latest/tracking.html>
- Reproducible Data Science (Kitzes et al.) — <https://www.practicereproducibility.org/>
