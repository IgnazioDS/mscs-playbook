# Clustering and Evaluation

## What it is

Grouping data points into clusters based on similarity, and evaluating cluster
quality with internal metrics.

## Why it matters

Clustering is sensitive to feature scaling and distance metrics; evaluation
keeps the results grounded.

## Practical workflow steps

- Standardize features
- Select k or clustering algorithm
- Evaluate with silhouette or inertia
- Inspect cluster profiles

## Failure modes

- Choosing k without evaluation
- Using unscaled features with distance metrics
- Over-interpreting clusters without stability checks

## Checklist

- Features scaled
- Multiple k values compared
- Metrics reported (silhouette, inertia)
- Cluster centroids and profiles reviewed

## References

- scikit-learn Clustering — <https://scikit-learn.org/stable/modules/clustering.html>
- Silhouette Analysis — <https://doi.org/10.1016/0377-0427(87)90125-7>
