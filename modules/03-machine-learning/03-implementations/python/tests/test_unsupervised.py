import numpy as np
from sklearn.datasets import load_iris

from src.unsupervised.clustering import kmeans_cluster, silhouette_score_safe
from src.unsupervised.dimensionality_reduction import pca_reduce


def test_kmeans_labels_shape():
    X, _ = load_iris(return_X_y=True)
    labels = kmeans_cluster(X, k=3, seed=0)
    assert labels.shape[0] == X.shape[0]


def test_silhouette_safe_invalid():
    X = np.random.RandomState(0).randn(5, 2)
    labels = np.zeros(5, dtype=int)
    assert silhouette_score_safe(X, labels) == 0.0


def test_pca_reduce_shape_and_variance():
    X, _ = load_iris(return_X_y=True)
    X_red, var = pca_reduce(X, n_components=2, seed=0)
    assert X_red.shape == (X.shape[0], 2)
    assert var.sum() <= 1.0 + 1e-6
