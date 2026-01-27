import numpy as np

from src.datasets.loading import load_dataset, train_val_test_split


def test_split_determinism():
    X, y, *_ = load_dataset("iris")
    split1 = train_val_test_split(X, y, seed=123, test_size=0.2, val_size=0.2)
    split2 = train_val_test_split(X, y, seed=123, test_size=0.2, val_size=0.2)
    for a, b in zip(split1, split2):
        np.testing.assert_array_equal(a, b)


def test_split_shapes():
    X, y, *_ = load_dataset("iris")
    X_train, X_val, X_test, y_train, y_val, y_test = train_val_test_split(X, y, seed=7)
    assert X_train.shape[0] + X_val.shape[0] + X_test.shape[0] == X.shape[0]
    assert y_train.shape[0] + y_val.shape[0] + y_test.shape[0] == y.shape[0]
