"""Baseline model factories for classification and regression."""

from __future__ import annotations

from typing import Any

from sklearn.linear_model import LogisticRegression, Ridge


def logistic_regression(seed: int, **kwargs: Any) -> LogisticRegression:
    """Create a logistic regression classifier with sensible defaults."""
    params = {
        "max_iter": 1000,
        "solver": "lbfgs",
        "random_state": seed,
    }
    params.update(kwargs)
    return LogisticRegression(**params)


def ridge_regression(seed: int, alpha: float = 1.0, **kwargs: Any) -> Ridge:
    """Create a ridge regression model with configurable regularization."""
    params = {
        "alpha": alpha,
        "random_state": seed,
    }
    params.update(kwargs)
    return Ridge(**params)
