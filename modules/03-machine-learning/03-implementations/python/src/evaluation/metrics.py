"""Metric wrappers for classification and regression."""

from __future__ import annotations

from typing import Dict

import numpy as np
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)


def classification_report_dict(y_true, y_pred) -> Dict[str, dict]:
    """Return sklearn classification report as a dict."""
    return classification_report(y_true, y_pred, output_dict=True, zero_division=0)


def confusion_matrix_dict(y_true, y_pred) -> Dict[str, list]:
    """Return confusion matrix and labels as a dict."""
    labels = np.unique(np.concatenate([np.asarray(y_true), np.asarray(y_pred)]))
    matrix = confusion_matrix(y_true, y_pred, labels=labels)
    return {"labels": labels.tolist(), "matrix": matrix.tolist()}


def regression_metrics(y_true, y_pred) -> Dict[str, float]:
    """Return common regression metrics."""
    rmse = mean_squared_error(y_true, y_pred, squared=False)
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    return {"rmse": float(rmse), "mae": float(mae), "r2": float(r2)}
