"""Similarity utilities."""

from __future__ import annotations

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors


def cosine_sim_matrix(A, B):
    return cosine_similarity(A, B)


def topk_cosine(query_vec, doc_mat, k: int):
    sims = cosine_similarity(query_vec.reshape(1, -1), doc_mat).ravel()
    return sims.argsort()[::-1][:k].tolist()


class NearestNeighborsIndex:
    def __init__(self, n_neighbors: int = 5):
        self._nn = NearestNeighbors(n_neighbors=n_neighbors, metric="cosine")

    def fit(self, X):
        self._nn.fit(X)

    def query(self, X):
        distances, indices = self._nn.kneighbors(X)
        return indices, distances
