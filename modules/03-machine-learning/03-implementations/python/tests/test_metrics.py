import numpy as np

from src.evaluation.metrics import classification_report_dict, confusion_matrix_dict, regression_metrics


def test_classification_metrics_keys():
    y_true = np.array([0, 1, 1, 0])
    y_pred = np.array([0, 1, 0, 0])
    report = classification_report_dict(y_true, y_pred)
    assert "accuracy" in report
    cm = confusion_matrix_dict(y_true, y_pred)
    assert set(cm.keys()) == {"labels", "matrix"}
    assert len(cm["matrix"]) == len(cm["labels"])


def test_regression_metrics_keys():
    y_true = np.array([1.0, 2.0, 3.0])
    y_pred = np.array([1.0, 2.5, 2.5])
    metrics = regression_metrics(y_true, y_pred)
    assert set(metrics.keys()) == {"rmse", "mae", "r2"}
    assert metrics["rmse"] >= 0
