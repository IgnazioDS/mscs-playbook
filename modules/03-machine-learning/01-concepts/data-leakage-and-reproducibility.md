# Data Leakage and Reproducibility

## What it is

Leakage occurs when training data contains information unavailable at inference time.
Reproducibility ensures consistent results across runs.

## Why it matters

Leakage can inflate metrics and fail catastrophically in production.

## Core idea

Separate training, validation, and test data; fix seeds and deterministic splits.

## Common pitfalls

- Fitting scalers on full data before splitting
- Using time-based data without proper temporal split
- Uncontrolled randomness in pipelines

## Debug checklist

- Enforce fit/transform separation with pipelines
- Pin random seeds and document splits
- Run repeat experiments to verify stability

## References

- *Reproducible Machine Learning* (papers/tutorials)
- scikit-learn documentation: Pipelines and model selection
