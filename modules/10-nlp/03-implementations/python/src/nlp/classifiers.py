"""Text classification utilities."""

from __future__ import annotations

from typing import List, Tuple

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from src.nlp.vectorizers import TfidfVectorizerLite


def train_linear_text_classifier(texts: List[str], labels: List[str], seed: int):
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.3, random_state=seed, stratify=labels
    )
    pipeline = Pipeline(
        [
            ("tfidf", TfidfVectorizerLite()._vectorizer),
            ("clf", LogisticRegression(max_iter=200, random_state=seed)),
        ]
    )
    pipeline.fit(X_train, y_train)
    return pipeline


def predict_proba(model, texts: List[str]):
    return model.predict_proba(texts)
