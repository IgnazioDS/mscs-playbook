"""Dimensionality reduction utilities."""

from __future__ import annotations

from typing import Tuple

import numpy as np
from sklearn.decomposition import PCA


def pca_reduce(X: np.ndarray, n_components: int, seed: int = 42) -> Tuple[np.ndarray, np.ndarray]:
    """Reduce dimensionality with PCA and return reduced data + variance ratios."""
    if n_components <= 0:
        raise ValueError("n_components must be positive")
    pca = PCA(n_components=n_components, random_state=seed)
    X_reduced = pca.fit_transform(X)
    return X_reduced, pca.explained_variance_ratio_
