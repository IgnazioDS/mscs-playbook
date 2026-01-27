"""Dataset loading and deterministic splitting utilities."""

from __future__ import annotations

from typing import Tuple

import numpy as np
from sklearn.datasets import load_breast_cancer, load_iris, fetch_california_housing
from sklearn.model_selection import train_test_split


DatasetReturn = Tuple[np.ndarray, np.ndarray, list[str], str, str]


def load_dataset(name: str) -> DatasetReturn:
    """Load a built-in dataset and return standardized metadata.

    Args:
        name: One of "iris", "breast_cancer", "california_housing".

    Returns:
        X: feature matrix (numpy array)
        y: target array (numpy array)
        feature_names: list of feature names
        target_name: target name
        task_type: "classification" or "regression"
    """
    name = name.lower()
    if name == "iris":
        ds = load_iris()
        return ds.data, ds.target, list(ds.feature_names), "species", "classification"
    if name == "breast_cancer":
        ds = load_breast_cancer()
        return ds.data, ds.target, list(ds.feature_names), "diagnosis", "classification"
    if name == "california_housing":
        ds = fetch_california_housing()
        return ds.data, ds.target, list(ds.feature_names), "median_house_value", "regression"
    raise ValueError(f"unsupported dataset: {name}")


def _should_stratify(y: np.ndarray, stratify_if_classification: bool) -> bool:
    if not stratify_if_classification:
        return False
    if y.ndim != 1:
        return False
    if np.issubdtype(y.dtype, np.integer) or np.issubdtype(y.dtype, np.bool_):
        unique = np.unique(y)
        # Heuristic: small number of discrete classes implies classification.
        return len(unique) <= min(20, max(2, int(0.2 * len(y))))
    return False


def train_val_test_split(
    X: np.ndarray,
    y: np.ndarray,
    seed: int,
    test_size: float = 0.2,
    val_size: float = 0.2,
    stratify_if_classification: bool = True,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split data into train/val/test with deterministic behavior.

    Args:
        X: Feature matrix.
        y: Target array.
        seed: Random seed.
        test_size: Fraction for test split.
        val_size: Fraction for validation split (of remaining after test split).
        stratify_if_classification: Use stratified splits if y looks categorical.

    Returns:
        X_train, X_val, X_test, y_train, y_val, y_test
    """
    stratify = y if _should_stratify(y, stratify_if_classification) else None
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=seed,
        stratify=stratify,
    )
    stratify_val = y_train_val if _should_stratify(y_train_val, stratify_if_classification) else None
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val,
        y_train_val,
        test_size=val_size,
        random_state=seed,
        stratify=stratify_val,
    )
    return X_train, X_val, X_test, y_train, y_val, y_test
