import numpy as np

from src.cv.simple_models import predict_classifier, train_classifier


def test_train_classifier_deterministic():
    rng = np.random.RandomState(0)
    class0 = rng.normal(loc=-2.0, scale=0.3, size=(6, 2))
    class1 = rng.normal(loc=2.0, scale=0.3, size=(6, 2))
    X = np.vstack([class0, class1])
    y = np.array([0] * 6 + [1] * 6)
    model, metrics = train_classifier(X, y, seed=0)
    preds = predict_classifier(model, X)
    assert metrics["accuracy"] >= 0.9
    assert np.mean(preds == y) >= 0.9
