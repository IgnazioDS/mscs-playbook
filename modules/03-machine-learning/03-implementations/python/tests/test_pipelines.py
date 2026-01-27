from sklearn.datasets import load_iris, make_regression

from src.preprocessing.pipelines import make_classification_pipeline, make_regression_pipeline


def test_classification_pipeline_predict_shape():
    X, y = load_iris(return_X_y=True)
    model = make_classification_pipeline(seed=42)
    model.fit(X, y)
    preds = model.predict(X)
    assert preds.shape == y.shape


def test_regression_pipeline_predict_shape():
    X, y = make_regression(n_samples=60, n_features=5, noise=0.1, random_state=0)
    model = make_regression_pipeline(seed=42)
    model.fit(X, y)
    preds = model.predict(X)
    assert preds.shape == y.shape
