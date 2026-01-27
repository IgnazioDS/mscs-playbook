from src.pipeline.run_pipeline import run_pipeline


def test_pipeline_cluster_smoke():
    report, artifacts = run_pipeline("cluster", "iris", seed=42, params={"k": 3})
    assert "Profiling" in report
    assert "Cleaning" in report
    assert "Results" in report
    assert "KMeans" in report
    assert artifacts["inertia"] > 0


def test_pipeline_anomaly_smoke():
    report, artifacts = run_pipeline("anomaly", "breast_cancer", seed=42, params=None)
    assert "Profiling" in report
    assert "Cleaning" in report
    assert "Results" in report
    assert "IsolationForest" in report
    assert artifacts["n_anomalies"] > 0


def test_pipeline_basket_smoke():
    report, artifacts = run_pipeline("basket", "tiny_baskets", seed=42, params={"min_support": 0.2})
    assert "Profiling" in report
    assert "Results" in report
    assert "Apriori" in report
    assert artifacts["n_rules"] >= 0
