"""Evaluation metrics helpers."""

from __future__ import annotations

from typing import Dict, List, Optional

import numpy as np
from sklearn.metrics import silhouette_score


def safe_silhouette(X: np.ndarray, labels: np.ndarray) -> Optional[float]:
    unique_labels = set(labels)
    if len(unique_labels) <= 1:
        return None
    return float(silhouette_score(X, labels))


def rules_summary(rules: List[Dict[str, object]]) -> Dict[str, object]:
    if not rules:
        return {"n_rules": 0, "top_rule": None}
    top_rule = rules[0]
    return {"n_rules": len(rules), "top_rule": top_rule}
