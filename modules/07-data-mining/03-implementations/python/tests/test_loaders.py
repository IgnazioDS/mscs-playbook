from src.datasets.loaders import load_basket_dataset, load_sklearn_dataset


def test_load_sklearn_datasets():
    for name in ["iris", "wine", "breast_cancer", "california_housing"]:
        X, y, meta = load_sklearn_dataset(name)
        assert X.shape[0] == meta["n_rows"]
        assert len(meta["feature_names"]) == X.shape[1]
        if name == "california_housing":
            assert y is None or len(y) == X.shape[0]
        else:
            assert y is not None


def test_load_basket_dataset():
    transactions = load_basket_dataset("tiny_baskets")
    assert isinstance(transactions, list)
    assert len(transactions) > 0
    assert isinstance(transactions[0], list)
