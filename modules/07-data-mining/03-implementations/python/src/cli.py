"""Mini-project CLI for data mining pipelines."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List, Tuple

from src.pipeline.run_pipeline import run_pipeline


def _round(value: float | None, ndigits: int = 3) -> float | None:
    if value is None:
        return None
    return round(float(value), ndigits)


def _format_rule(rule: Dict[str, object]) -> str:
    antecedent = ",".join(rule["antecedent"]) if rule.get("antecedent") else ""
    consequent = ",".join(rule["consequent"]) if rule.get("consequent") else ""
    lift = _round(rule.get("lift", 0.0))
    return f"{antecedent} -> {consequent} (lift={lift})"


def _print_header(task: str, dataset: str, seed: int) -> None:
    print(f"task: {task}")
    print(f"dataset: {dataset}")
    print(f"seed: {seed}")


def _print_cluster_results(artifacts: Dict[str, object], k: int) -> None:
    labels = list(artifacts["labels"])
    counts: Dict[int, int] = {}
    for label in labels:
        counts[int(label)] = counts.get(int(label), 0) + 1
    top_counts = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:3]
    top_counts_str = ", ".join([f"{k}:{v}" for k, v in top_counts])

    inertia = _round(artifacts["inertia"])
    silhouette = _round(artifacts.get("silhouette"))

    print("Results:")
    print(f"  k: {k}")
    print(f"  inertia: {inertia}")
    print(f"  silhouette: {silhouette}")
    print(f"  label_counts_top3: {top_counts_str}")


def _print_anomaly_results(artifacts: Dict[str, object], contamination: float) -> None:
    n_anomalies = int(artifacts["n_anomalies"])
    print("Results:")
    print(f"  contamination: {_round(contamination)}")
    print(f"  n_anomalies: {n_anomalies}")


def _print_basket_results(artifacts: Dict[str, object], n_transactions: int, top_rules: List[Dict[str, object]]) -> None:
    print("Results:")
    print(f"  n_transactions: {n_transactions}")
    print(f"  n_rules: {artifacts['n_rules']}")
    if top_rules:
        print("  top_rules:")
        for rule in top_rules:
            print(f"    - {_format_rule(rule)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Data mining mini-project CLI")
    subparsers = parser.add_subparsers(dest="task", required=True)

    cluster = subparsers.add_parser("cluster")
    cluster.add_argument("--dataset", required=True, choices=["iris", "wine"])
    cluster.add_argument("--k", type=int, default=3)
    cluster.add_argument("--seed", type=int, default=42)
    cluster.add_argument("--out", type=str, default=None)

    anomaly = subparsers.add_parser("anomaly")
    anomaly.add_argument("--dataset", required=True, choices=["breast_cancer"])
    anomaly.add_argument("--contamination", type=float, default=0.05)
    anomaly.add_argument("--seed", type=int, default=42)
    anomaly.add_argument("--out", type=str, default=None)

    basket = subparsers.add_parser("basket")
    basket.add_argument("--dataset", required=True, choices=["tiny_baskets"])
    basket.add_argument("--min-support", type=float, default=0.2, dest="min_support")
    basket.add_argument("--min-confidence", type=float, default=0.6, dest="min_confidence")
    basket.add_argument("--seed", type=int, default=42)
    basket.add_argument("--out", type=str, default=None)

    args = parser.parse_args()

    if args.task == "cluster":
        params = {"k": args.k}
    elif args.task == "anomaly":
        params = {"contamination": args.contamination}
    else:
        params = {"min_support": args.min_support, "min_confidence": args.min_confidence}

    report, artifacts = run_pipeline(args.task, args.dataset, args.seed, params=params)

    _print_header(args.task, args.dataset, args.seed)
    if args.task == "cluster":
        _print_cluster_results(artifacts, k=args.k)
    elif args.task == "anomaly":
        _print_anomaly_results(artifacts, contamination=args.contamination)
    else:
        top_rules = []
        top_rule = artifacts.get("top_rule")
        if top_rule:
            top_rules = [top_rule]
        _print_basket_results(
            artifacts,
            n_transactions=int(artifacts.get("n_transactions", 0)),
            top_rules=top_rules,
        )

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
