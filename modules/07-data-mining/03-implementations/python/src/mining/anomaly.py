"""Anomaly detection helpers."""

from __future__ import annotations

from typing import Dict

import numpy as np
from sklearn.ensemble import IsolationForest


def run_isolation_forest(
    X: np.ndarray, seed: int, contamination: float = 0.05
) -> Dict[str, object]:
    model = IsolationForest(random_state=seed, contamination=contamination)
    labels = model.fit_predict(X)
    scores = model.decision_function(X)
    n_anomalies = int((labels == -1).sum())
    return {
        "labels": labels,
        "scores": scores,
        "n_anomalies": n_anomalies,
    }
