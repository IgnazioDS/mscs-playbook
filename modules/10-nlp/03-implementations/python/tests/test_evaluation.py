from src.nlp.evaluation import classification_report_simple, retrieval_metrics_at_k


def test_classification_report_simple():
    y_true = ["a", "a", "b", "b"]
    y_pred = ["a", "b", "b", "b"]
    metrics = classification_report_simple(y_true, y_pred)
    assert metrics["accuracy"] == 0.75


def test_retrieval_metrics_at_k():
    relevant = [{"d1"}, {"d2", "d3"}]
    retrieved = [["d1", "d4"], ["d3", "d2"]]
    metrics = retrieval_metrics_at_k(relevant, retrieved, k=2)
    assert metrics["precision_at_k"] == 0.75
    assert metrics["recall_at_k"] == 1.0
    assert metrics["mrr_at_k"] == 1.0
