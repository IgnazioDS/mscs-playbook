# Supervised Learning Foundations

## What it is
Learning a function from labeled examples to predict targets for new inputs.

## Why it matters
Most production ML systems are supervised, from forecasting to classification.

## Core idea
Minimize a loss function that measures prediction error on labeled data.

## Common pitfalls
- Training on leaked or non-representative data
- Using the wrong metric for the business goal
- Overfitting with too complex models

## Debug checklist
- Verify label distribution and feature ranges
- Compare baseline vs model metrics
- Check train/val/test splits for leakage

## References
- *Introduction to Statistical Learning* (ISL)
- *Pattern Recognition and Machine Learning* (Bishop)
