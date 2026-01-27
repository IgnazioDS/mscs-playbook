import pandas as pd

from src.cleaning.missingness import impute_missing, missingness_report
from src.cleaning.outliers import iqr_outlier_mask, winsorize_series


def test_impute_missing():
    df = pd.DataFrame({"a": [1.0, None, 3.0], "b": ["x", None, "x"]})
    report = missingness_report(df)
    assert report["missing_counts"]["a"] == 1
    out = impute_missing(df)
    assert out.isna().sum().sum() == 0


def test_outlier_mask_and_winsorize():
    series = pd.Series([1, 1, 1, 1, 100])
    mask = iqr_outlier_mask(series)
    assert mask.iloc[-1] == True
    wins = winsorize_series(series, lower_q=0.0, upper_q=0.8)
    assert wins.max() <= series.max()
