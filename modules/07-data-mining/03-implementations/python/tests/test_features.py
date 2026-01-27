import pandas as pd
import numpy as np

from src.features.encoding import one_hot_encode
from src.features.scaling import standard_scale


def test_one_hot_encode():
    df = pd.DataFrame({"color": ["red", "blue"], "value": [1, 2]})
    X, meta = one_hot_encode(df)
    assert "color_red" in X.columns
    assert "color_blue" in X.columns
    assert meta["categorical_cols"] == ["color"]


def test_standard_scale_mean_close_to_zero():
    df = pd.DataFrame({"x": [1.0, 2.0, 3.0], "y": [4.0, 5.0, 6.0]})
    X_scaled, _ = standard_scale(df)
    assert np.allclose(X_scaled.mean(axis=0), 0.0, atol=1e-7)
