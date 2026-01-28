"""Mini-project CLI for the NLP module."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Dict, Iterable, List

if __name__ == "__main__":
    ROOT = Path(__file__).resolve().parents[3]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))

from src.nlp.evaluation import retrieval_metrics_at_k
from src.nlp.mini_project.kb_search import (
    DEFAULT_QUERIES,
    relevance_sets_for_queries,
    retrieved_lists,
    run_kb_search,
)
from src.nlp.mini_project.reporting import build_report, write_report
from src.nlp.mini_project.ticket_triage import run_ticket_triage


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="NLP mini-project CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    triage = sub.add_parser("ticket-triage", help="Run support ticket triage")
    triage.add_argument("--seed", type=int, default=42)
    triage.add_argument("--out", type=str, default=None)

    search = sub.add_parser("kb-search", help="Run knowledge base search")
    search.add_argument("--k", type=int, default=3)
    search.add_argument("--seed", type=int, default=42)
    search.add_argument("--query", type=str, default=None)
    search.add_argument("--out", type=str, default=None)

    evaluate = sub.add_parser("evaluate", help="Run combined evaluation")
    evaluate.add_argument("--k", type=int, default=3)
    evaluate.add_argument("--seed", type=int, default=42)
    evaluate.add_argument("--out", type=str, default=None)

    return parser


def run_cli(argv: List[str] | None = None) -> str:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "ticket-triage":
        output, report = _run_ticket_triage_cli(args.seed)
        if args.out:
            write_report(args.out, report)
        print(output)
        return output

    if args.command == "kb-search":
        output, report = _run_kb_search_cli(args.k, args.seed, args.query)
        if args.out:
            write_report(args.out, report)
        print(output)
        return output

    if args.command == "evaluate":
        output, report = _run_evaluate_cli(args.k, args.seed)
        if args.out:
            write_report(args.out, report)
        print(output)
        return output

    parser.error("Unknown command")
    return ""


def _run_ticket_triage_cli(seed: int) -> tuple[str, str]:
    result = run_ticket_triage(seed=seed)
    metrics = result["metrics"]
    label_dist = result["label_distribution"]

    lines = [
        "task: ticket-triage",
        f"seed: {seed}",
        f"train_size: {result['train_size']}",
        f"test_size: {result['test_size']}",
        f"label_distribution: {_format_mapping(label_dist)}",
        f"model: {result['model_summary']}",
        "Results:",
        f"  accuracy: {_fmt(metrics['accuracy'])}",
        f"  precision_macro: {_fmt(metrics['precision_macro'])}",
        f"  recall_macro: {_fmt(metrics['recall_macro'])}",
        f"  f1_macro: {_fmt(metrics['f1_macro'])}",
    ]

    report = build_report(
        "Ticket Triage",
        [
            f"seed={seed}",
            f"train_size={result['train_size']}",
            f"test_size={result['test_size']}",
            f"label_distribution={_format_mapping(label_dist)}",
        ],
        [
            f"model={result['model_summary']}",
            f"accuracy={_fmt(metrics['accuracy'])}",
            f"precision_macro={_fmt(metrics['precision_macro'])}",
            f"recall_macro={_fmt(metrics['recall_macro'])}",
            f"f1_macro={_fmt(metrics['f1_macro'])}",
        ],
        ["Small dataset; metrics are illustrative."],
        ["Deterministic split via seed; no timestamps."] ,
    )
    return "\n".join(lines), report


def _run_kb_search_cli(k: int, seed: int, query: str | None) -> tuple[str, str]:
    result = run_kb_search(k=k, seed=seed, query=query)
    lines = ["task: kb-search", f"k: {k}"]
    for item in result["results"]:
        lines.append(f"query: {item['query']}")
        for hit in item["hits"]:
            lines.append(
                f"  {hit['id']} | score={_fmt(hit['score'])} | {hit['snippet']}"
            )

    report = build_report(
        "Knowledge Base Search",
        [f"k={k}", f"queries={', '.join(result['queries'])}"],
        [*lines[2:]],
        ["TF-IDF + cosine similarity on tiny corpus."],
        ["Deterministic ranking via stable sorting."],
    )
    return "\n".join(lines), report


def _run_evaluate_cli(k: int, seed: int) -> tuple[str, str]:
    triage = run_ticket_triage(seed=seed)
    search = run_kb_search(k=k, seed=seed, query=None)

    relevance = relevance_sets_for_queries(search["queries"])
    retrieved = retrieved_lists(search["results"])
    retrieval_metrics = retrieval_metrics_at_k(relevance, retrieved, k=k)

    lines = [
        "task: evaluate",
        f"seed: {seed}",
        f"k: {k}",
        "Ticket triage metrics:",
        f"  accuracy: {_fmt(triage['metrics']['accuracy'])}",
        f"  precision_macro: {_fmt(triage['metrics']['precision_macro'])}",
        f"  recall_macro: {_fmt(triage['metrics']['recall_macro'])}",
        f"  f1_macro: {_fmt(triage['metrics']['f1_macro'])}",
        "Retrieval metrics:",
        f"  precision@k: {_fmt(retrieval_metrics['precision_at_k'])}",
        f"  recall@k: {_fmt(retrieval_metrics['recall_at_k'])}",
        f"  mrr@k: {_fmt(retrieval_metrics['mrr_at_k'])}",
    ]

    report = build_report(
        "Mini-project Evaluation",
        [f"seed={seed}", f"k={k}", f"queries={', '.join(DEFAULT_QUERIES)}"],
        [
            f"triage_accuracy={_fmt(triage['metrics']['accuracy'])}",
            f"triage_f1_macro={_fmt(triage['metrics']['f1_macro'])}",
            f"precision@k={_fmt(retrieval_metrics['precision_at_k'])}",
            f"recall@k={_fmt(retrieval_metrics['recall_at_k'])}",
            f"mrr@k={_fmt(retrieval_metrics['mrr_at_k'])}",
        ],
        ["Combined summary for ticket triage + KB search."],
        ["Deterministic metrics with seed=42."],
    )

    return "\n".join(lines), report


def _fmt(value: float) -> str:
    return f"{value:.3f}"


def _format_mapping(mapping: Dict[str, int]) -> str:
    items = [f"{k}={mapping[k]}" for k in sorted(mapping.keys())]
    return "{" + ", ".join(items) + "}"


if __name__ == "__main__":
    run_cli()
