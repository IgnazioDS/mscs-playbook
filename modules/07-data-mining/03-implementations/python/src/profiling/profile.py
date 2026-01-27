"""Basic dataframe profiling utilities."""

from __future__ import annotations

from typing import Any, Dict

import pandas as pd


def profile_dataframe(df: pd.DataFrame, max_categories: int = 10) -> Dict[str, Any]:
    """Return basic profiling stats for a dataframe."""
    summary: Dict[str, Any] = {
        "n_rows": df.shape[0],
        "n_cols": df.shape[1],
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing_counts": df.isna().sum().to_dict(),
    }

    numeric_cols = df.select_dtypes(include=["number"]).columns
    if len(numeric_cols) > 0:
        numeric_summary = df[numeric_cols].agg(["min", "mean", "std", "max"]).transpose()
        summary["numeric_summary"] = numeric_summary.round(4).to_dict(orient="index")
    else:
        summary["numeric_summary"] = {}

    category_summary: Dict[str, Any] = {}
    object_cols = df.select_dtypes(include=["object", "category"]).columns
    for col in object_cols:
        counts = df[col].value_counts(dropna=False).head(max_categories)
        category_summary[col] = counts.to_dict()
    summary["top_categories"] = category_summary

    return summary
