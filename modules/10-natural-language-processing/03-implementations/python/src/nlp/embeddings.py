"""Lightweight embedding utilities."""

from __future__ import annotations

from typing import Dict, List

import numpy as np
from sklearn.decomposition import TruncatedSVD


def train_svd_embeddings(tfidf_matrix, dim: int):
    svd = TruncatedSVD(n_components=dim, random_state=42)
    return svd.fit_transform(tfidf_matrix)


def average_word_embeddings(tokens: List[str], word_to_vec: Dict[str, np.ndarray], dim: int):
    vectors = [word_to_vec[t] for t in tokens if t in word_to_vec]
    if not vectors:
        return np.zeros(dim)
    return np.mean(vectors, axis=0)


def toy_word_vectors(dim: int = 3) -> Dict[str, np.ndarray]:
    return {
        "alpha": np.array([1.0, 0.0, 0.0])[:dim],
        "beta": np.array([0.0, 1.0, 0.0])[:dim],
        "gamma": np.array([0.0, 0.0, 1.0])[:dim],
    }
