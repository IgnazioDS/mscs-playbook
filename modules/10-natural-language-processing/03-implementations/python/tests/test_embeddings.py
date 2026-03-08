import numpy as np

from src.nlp.embeddings import average_word_embeddings, toy_word_vectors, train_svd_embeddings
from src.nlp.vectorizers import TfidfVectorizerLite


def test_train_svd_embeddings_shape():
    vec = TfidfVectorizerLite()
    X = vec.fit_transform(["alpha beta", "beta gamma", "delta"])
    emb = train_svd_embeddings(X, dim=2)
    assert emb.shape == (3, 2)


def test_average_word_embeddings():
    wv = toy_word_vectors(dim=3)
    avg = average_word_embeddings(["alpha", "beta"], wv, dim=3)
    assert np.allclose(avg, np.array([0.5, 0.5, 0.0]))
