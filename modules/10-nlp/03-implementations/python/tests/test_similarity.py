import numpy as np

from src.nlp.similarity import NearestNeighborsIndex, topk_cosine
from src.nlp.vectorizers import TfidfVectorizerLite


def test_topk_cosine():
    texts = ["alpha beta", "beta gamma", "delta"]
    vec = TfidfVectorizerLite()
    X = vec.fit_transform(texts)
    q = vec.transform(["beta"])
    idx = topk_cosine(q[0], X, k=1)
    assert idx[0] in [0, 1]


def test_nearest_neighbors_index():
    texts = ["alpha", "beta", "gamma"]
    vec = TfidfVectorizerLite()
    X = vec.fit_transform(texts)
    nn = NearestNeighborsIndex(n_neighbors=1)
    nn.fit(X)
    indices, distances = nn.query(X[0])
    assert indices[0][0] == 0
