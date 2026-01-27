"""Clustering utilities with safe silhouette scoring."""

from __future__ import annotations

from typing import Iterable

import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def kmeans_cluster(X: np.ndarray, k: int, seed: int = 42) -> np.ndarray:
    """Run KMeans clustering and return labels."""
    if k <= 0:
        raise ValueError("k must be positive")
    model = KMeans(n_clusters=k, n_init="auto", random_state=seed)
    return model.fit_predict(X)


def silhouette_score_safe(X: np.ndarray, labels: Iterable[int]) -> float:
    """Compute silhouette score; return 0.0 for invalid label configurations."""
    labels = np.asarray(list(labels))
    unique = np.unique(labels)
    if len(unique) < 2 or len(unique) >= len(labels):
        return 0.0
    return float(silhouette_score(X, labels))
