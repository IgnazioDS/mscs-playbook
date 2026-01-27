"""Convenience pipelines combining preprocessing and model selection."""

from __future__ import annotations

from typing import Literal

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.models.baselines import logistic_regression, ridge_regression


def make_classification_pipeline(
    model: Literal["logreg"] = "logreg",
    seed: int = 42,
    standardize: bool = True,
) -> Pipeline:
    """Build a classification pipeline with optional standardization."""
    if model != "logreg":
        raise ValueError(f"unsupported model: {model}")

    steps = []
    if standardize:
        steps.append(("scaler", StandardScaler()))
    steps.append(("model", logistic_regression(seed)))
    return Pipeline(steps)


def make_regression_pipeline(
    model: Literal["ridge"] = "ridge",
    seed: int = 42,
    standardize: bool = True,
) -> Pipeline:
    """Build a regression pipeline with optional standardization."""
    if model != "ridge":
        raise ValueError(f"unsupported model: {model}")

    steps = []
    if standardize:
        steps.append(("scaler", StandardScaler()))
    steps.append(("model", ridge_regression(seed)))
    return Pipeline(steps)
