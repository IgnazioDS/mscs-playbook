"""Clustering helpers."""

from __future__ import annotations

from typing import Dict

import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def run_kmeans(X: np.ndarray, k: int, seed: int) -> Dict[str, object]:
    model = KMeans(n_clusters=k, random_state=seed, n_init=10)
    labels = model.fit_predict(X)
    return {
        "labels": labels,
        "centers": model.cluster_centers_,
        "inertia": float(model.inertia_),
    }


def clustering_scores(X: np.ndarray, labels: np.ndarray) -> Dict[str, object]:
    unique_labels = set(labels)
    if len(unique_labels) <= 1:
        silhouette = None
    else:
        silhouette = float(silhouette_score(X, labels))
    return {"silhouette": silhouette}
