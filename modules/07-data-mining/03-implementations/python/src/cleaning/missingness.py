"""Missingness utilities and imputation."""

from __future__ import annotations

from typing import Any, Dict

import pandas as pd


def missingness_report(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    counts = df.isna().sum()
    percents = (counts / len(df)).fillna(0)
    return {
        "missing_counts": counts.to_dict(),
        "missing_percent": percents.to_dict(),
    }


def impute_missing(
    df: pd.DataFrame,
    strategy_numeric: str = "median",
    strategy_categorical: str = "mode",
) -> pd.DataFrame:
    """Impute missing values by column type."""
    result = df.copy()
    numeric_cols = result.select_dtypes(include=["number"]).columns
    cat_cols = result.select_dtypes(include=["object", "category"]).columns

    for col in numeric_cols:
        if strategy_numeric == "median":
            value = result[col].median()
        elif strategy_numeric == "mean":
            value = result[col].mean()
        else:
            raise ValueError("Unsupported numeric strategy")
        result[col] = result[col].fillna(value)

    for col in cat_cols:
        if strategy_categorical != "mode":
            raise ValueError("Unsupported categorical strategy")
        if result[col].mode(dropna=True).empty:
            value = "missing"
        else:
            value = result[col].mode(dropna=True).iloc[0]
        result[col] = result[col].fillna(value)

    return result
