# Unsupervised Learning Toolkit

## What it is
Learning structure from unlabeled data using clustering, density, and embeddings.

## Why it matters
Useful for discovery, segmentation, and preprocessing for downstream tasks.

## Core idea
Optimize a structure objective (e.g., cluster compactness) without labels.

## Common pitfalls
- Interpreting clusters without domain validation
- Using Euclidean distance on unscaled features
- Choosing k without diagnostics

## Debug checklist
- Standardize features
- Inspect silhouette score or inertia
- Visualize clusters in 2D projections

## References
- *Introduction to Data Mining* (Tan et al.)
- *Data Mining: Concepts and Techniques* (Han et al.)
