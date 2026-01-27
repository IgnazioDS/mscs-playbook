"""Cross-validation utilities."""

from __future__ import annotations

from typing import Dict, List

import numpy as np
from sklearn.base import clone
from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, StratifiedKFold


def cross_validate_model(
    estimator,
    X,
    y,
    task_type: str,
    seed: int,
    cv: int = 5,
) -> Dict[str, Dict[str, float] | List[Dict[str, float]]]:
    """Run k-fold CV and return per-fold metrics with mean/std.

    Args:
        estimator: sklearn-compatible estimator.
        X: feature matrix.
        y: target array.
        task_type: "classification" or "regression".
        seed: random seed.
        cv: number of folds.
    """
    if task_type not in {"classification", "regression"}:
        raise ValueError("task_type must be 'classification' or 'regression'")

    splitter = (
        StratifiedKFold(n_splits=cv, shuffle=True, random_state=seed)
        if task_type == "classification"
        else KFold(n_splits=cv, shuffle=True, random_state=seed)
    )

    folds: List[Dict[str, float]] = []
    for train_idx, val_idx in splitter.split(X, y):
        model = clone(estimator)
        model.fit(X[train_idx], y[train_idx])
        preds = model.predict(X[val_idx])
        if task_type == "classification":
            acc = accuracy_score(y[val_idx], preds)
            f1 = f1_score(y[val_idx], preds, average="weighted")
            folds.append({"accuracy": float(acc), "f1": float(f1)})
        else:
            rmse = mean_squared_error(y[val_idx], preds, squared=False)
            mae = mean_absolute_error(y[val_idx], preds)
            r2 = r2_score(y[val_idx], preds)
            folds.append({"rmse": float(rmse), "mae": float(mae), "r2": float(r2)})

    metrics = list(folds[0].keys())
    mean = {m: float(np.mean([f[m] for f in folds])) for m in metrics}
    std = {m: float(np.std([f[m] for f in folds])) for m in metrics}
    return {"folds": folds, "mean": mean, "std": std}
