from sklearn.datasets import load_iris

from src.evaluation.validation import cross_validate_model
from src.preprocessing.pipelines import make_classification_pipeline


def test_cross_validation_classification():
    X, y = load_iris(return_X_y=True)
    model = make_classification_pipeline(seed=42)
    results = cross_validate_model(model, X, y, task_type="classification", seed=42, cv=3)
    assert len(results["folds"]) == 3
    assert set(results["mean"].keys()) == {"accuracy", "f1"}
    assert set(results["std"].keys()) == {"accuracy", "f1"}
