# Evaluation Metrics and Validation

## What it is

Methods to measure model performance and estimate generalization.

## Why it matters

A model that scores well on training data can fail in production without proper validation.

## Core idea

Use metrics aligned to outcomes and validation procedures that mimic deployment.

## Common pitfalls

- Optimizing accuracy for imbalanced classes
- Data leakage across splits
- Tuning on the test set

## Debug checklist

- Confirm stratified splits for classification
- Review confusion matrix and calibration
- Use cross-validation for small datasets

## References

- *Hands-On Machine Learning* (Géron)
- *Evaluating Machine Learning Models* (Kuhn and Johnson)
