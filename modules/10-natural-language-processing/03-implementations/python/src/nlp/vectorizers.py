"""Vectorizer utilities."""

from __future__ import annotations

from sklearn.feature_extraction.text import TfidfVectorizer


class TfidfVectorizerLite:
    def __init__(self) -> None:
        self._vectorizer = TfidfVectorizer(stop_words=None, min_df=1, ngram_range=(1, 2))

    def fit_transform(self, texts):
        return self._vectorizer.fit_transform(texts)

    def transform(self, texts):
        return self._vectorizer.transform(texts)

    @property
    def vocabulary_(self):
        return self._vectorizer.vocabulary_
