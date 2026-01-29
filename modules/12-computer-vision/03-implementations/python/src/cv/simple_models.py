from __future__ import annotations

from typing import Any
import numpy as np
from sklearn.linear_model import LogisticRegression


def train_classifier(X: np.ndarray, y: np.ndarray, seed: int = 0) -> tuple[Any, dict[str, float]]:
    model = LogisticRegression(random_state=seed, solver="liblinear")
    model.fit(X, y)
    preds = model.predict(X)
    accuracy = float(np.mean(preds == y))
    return model, {"accuracy": accuracy}


def predict_classifier(model: Any, X: np.ndarray) -> np.ndarray:
    return model.predict(X)
