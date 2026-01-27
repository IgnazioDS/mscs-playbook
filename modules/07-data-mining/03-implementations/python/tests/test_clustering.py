from src.datasets.loaders import load_sklearn_dataset
from src.features.scaling import standard_scale
from src.mining.clustering import run_kmeans, clustering_scores


def test_kmeans_and_silhouette():
    X, _, _ = load_sklearn_dataset("iris")
    X_scaled, _ = standard_scale(X)
    result = run_kmeans(X_scaled, k=3, seed=42)
    assert len(result["labels"]) == X.shape[0]
    scores = clustering_scores(X_scaled, result["labels"])
    assert scores["silhouette"] is not None
