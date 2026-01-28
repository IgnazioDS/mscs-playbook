"""Encoding utilities."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

import pandas as pd


def one_hot_encode(
    df: pd.DataFrame,
    categorical_cols: Optional[List[str]] = None,
    drop_first: bool = False,
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """One-hot encode categorical columns using pandas.get_dummies."""
    if categorical_cols is None:
        categorical_cols = list(df.select_dtypes(include=["object", "category", "string"]).columns)

    encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=drop_first)
    meta = {
        "categorical_cols": categorical_cols,
        "drop_first": drop_first,
        "feature_names": list(encoded.columns),
    }
    return encoded, meta
