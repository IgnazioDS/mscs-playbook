from src.datasets.loaders import load_sklearn_dataset
from src.features.scaling import standard_scale
from src.mining.anomaly import run_isolation_forest


def test_isolation_forest_outputs():
    X, _, _ = load_sklearn_dataset("breast_cancer")
    X_scaled, _ = standard_scale(X)
    result = run_isolation_forest(X_scaled, seed=42, contamination=0.05)
    assert "labels" in result and "scores" in result
    assert result["n_anomalies"] > 0
