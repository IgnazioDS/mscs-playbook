from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


@dataclass(frozen=True)
class Doc:
    id: str
    text: str
    meta: dict[str, Any]


@dataclass(frozen=True)
class ScoredDoc:
    id: str
    score: float
    text: str
    meta: dict[str, Any]


class TfidfVectorStore:
    def __init__(self) -> None:
        self._vectorizer = TfidfVectorizer(norm="l2")
        self._matrix: np.ndarray | None = None
        self._docs: list[Doc] = []

    def fit(self, docs: list[Doc]) -> None:
        self._docs = list(docs)
        texts = [doc.text for doc in self._docs]
        if not texts:
            self._matrix = None
            return
        self._matrix = self._vectorizer.fit_transform(texts)

    def query(self, text: str, k: int) -> list[ScoredDoc]:
        if self._matrix is None or not self._docs:
            return []
        query_vec = self._vectorizer.transform([text])
        scores = (self._matrix @ query_vec.T).toarray().ravel()
        scored = [
            ScoredDoc(id=doc.id, score=float(score), text=doc.text, meta=doc.meta)
            for doc, score in zip(self._docs, scores)
        ]
        scored.sort(key=lambda item: (-item.score, item.id))
        return scored[: max(k, 0)]
