"""Knowledge base semantic search mini-project task."""

from __future__ import annotations

from typing import Dict, Iterable, List, Sequence, Set

import numpy as np

from src.nlp.datasets import load_tiny_corpus
from src.nlp.similarity import cosine_sim_matrix
from src.nlp.vectorizers import TfidfVectorizerLite

DEFAULT_QUERIES = [
    "reset password",
    "refund invoice",
    "export csv",
]

RELEVANCE_MAP = {
    "reset password": {"d1", "d4"},
    "refund invoice": {"d2", "d7"},
    "export csv": {"d5"},
}


def run_kb_search(k: int = 3, seed: int = 42, query: str | None = None) -> Dict[str, object]:
    _ = seed
    corpus = load_tiny_corpus()
    doc_texts = [item["text"] for item in corpus]
    doc_ids = [item["id"] for item in corpus]

    vectorizer = TfidfVectorizerLite()
    doc_mat = vectorizer.fit_transform(doc_texts)

    queries = [query] if query else list(DEFAULT_QUERIES)
    results = []
    for q in queries:
        query_vec = vectorizer.transform([q])
        sims = cosine_sim_matrix(query_vec, doc_mat).ravel()
        topk_idx = np.argsort(-sims, kind="stable")[:k]
        hits = []
        for idx in topk_idx:
            text = doc_texts[int(idx)]
            hits.append(
                {
                    "id": doc_ids[int(idx)],
                    "score": float(sims[int(idx)]),
                    "snippet": text[:80],
                }
            )
        results.append({"query": q, "hits": hits})

    return {
        "task": "kb-search",
        "k": k,
        "queries": queries,
        "results": results,
        "doc_ids": doc_ids,
    }


def relevance_sets_for_queries(queries: Sequence[str]) -> List[Set[str]]:
    return [set(RELEVANCE_MAP.get(q, set())) for q in queries]


def retrieved_lists(results: Iterable[Dict[str, object]]) -> List[List[str]]:
    lists = []
    for item in results:
        hits = item["hits"]
        lists.append([hit["id"] for hit in hits])
    return lists
