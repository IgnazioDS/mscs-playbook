"""Scaling utilities."""

from __future__ import annotations

from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


def standard_scale(X: pd.DataFrame) -> Tuple[np.ndarray, StandardScaler]:
    """Scale features with StandardScaler."""
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X.values)
    return X_scaled, scaler
