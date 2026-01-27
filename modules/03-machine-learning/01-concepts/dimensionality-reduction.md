# Dimensionality Reduction

## What it is
Reducing feature dimensions while preserving signal (e.g., PCA).

## Why it matters
Improves model stability, reduces noise, and speeds training.

## Core idea
Project data to a lower-dimensional subspace that captures variance or structure.

## Common pitfalls
- Applying PCA before train/test split (leakage)
- Losing interpretability without tracking components
- Over-reducing and discarding signal

## Debug checklist
- Fit PCA on training data only
- Check explained variance ratio
- Compare model metrics with/without reduction

## References
- *Principal Component Analysis* (Jolliffe)
- *Machine Learning* (Murphy)
