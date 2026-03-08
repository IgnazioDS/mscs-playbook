"""Support ticket triage mini-project task."""

from __future__ import annotations

from collections import Counter
from typing import Dict

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from src.nlp.datasets import make_ticket_dataset
from src.nlp.evaluation import classification_report_simple
from src.nlp.vectorizers import TfidfVectorizerLite


def run_ticket_triage(seed: int = 42) -> Dict[str, object]:
    data = make_ticket_dataset()
    texts = data["texts"]
    labels = data["labels"]
    label_dist = dict(sorted(Counter(labels).items()))

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
    preds = pipeline.predict(X_test)
    metrics = classification_report_simple(y_test, preds)

    return {
        "task": "ticket-triage",
        "seed": seed,
        "train_size": len(X_train),
        "test_size": len(X_test),
        "label_distribution": label_dist,
        "model_summary": "TF-IDF + LogisticRegression",
        "metrics": metrics,
    }
