"""Outlier utilities."""

from __future__ import annotations

import pandas as pd


def iqr_outlier_mask(series: pd.Series, k: float = 1.5) -> pd.Series:
    """Return a boolean mask of IQR-based outliers."""
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - k * iqr
    upper = q3 + k * iqr
    return (series < lower) | (series > upper)


def winsorize_series(series: pd.Series, lower_q: float = 0.01, upper_q: float = 0.99) -> pd.Series:
    """Clamp values to quantile bounds."""
    lower = series.quantile(lower_q)
    upper = series.quantile(upper_q)
    return series.clip(lower=lower, upper=upper)
