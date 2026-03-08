from src.nlp.evaluation import retrieval_metrics_at_k
from src.nlp.mini_project.kb_search import (
    DEFAULT_QUERIES,
    relevance_sets_for_queries,
    retrieved_lists,
    run_kb_search,
)
from src.nlp.mini_project.ticket_triage import run_ticket_triage


def test_ticket_triage_metrics_deterministic():
    result = run_ticket_triage(seed=42)
    metrics = result["metrics"]
    rounded = {key: round(value, 3) for key, value in metrics.items()}
    assert rounded == {
        "accuracy": 0.333,
        "precision_macro": 0.111,
        "recall_macro": 0.333,
        "f1_macro": 0.167,
    }


def test_kb_search_top_hits_deterministic():
    result = run_kb_search(k=3, seed=42, query=None)
    queries = result["queries"]
    assert queries == list(DEFAULT_QUERIES)
    top_hits = [item["hits"][0]["id"] for item in result["results"]]
    assert top_hits == ["d1", "d2", "d5"]


def test_retrieval_metrics_deterministic():
    result = run_kb_search(k=3, seed=42, query=None)
    relevance = relevance_sets_for_queries(result["queries"])
    retrieved = retrieved_lists(result["results"])
    metrics = retrieval_metrics_at_k(relevance, retrieved, k=3)
    assert round(metrics["precision_at_k"], 3) == 0.444
    assert round(metrics["recall_at_k"], 3) == 0.833
    assert round(metrics["mrr_at_k"], 3) == 1.0
