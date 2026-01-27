"""End-to-end data mining pipeline runner."""

from __future__ import annotations

from typing import Dict, Tuple

import numpy as np

from src.cleaning.missingness import impute_missing, missingness_report
from src.datasets.loaders import load_basket_dataset, load_sklearn_dataset
from src.evaluation.metrics import rules_summary, safe_silhouette
from src.evaluation.reporting import render_report
from src.features.encoding import one_hot_encode
from src.features.scaling import standard_scale
from src.mining.anomaly import run_isolation_forest
from src.mining.association_rules import apriori, generate_rules
from src.mining.clustering import run_kmeans
from src.profiling.profile import profile_dataframe
from src.utils.random import set_global_seed


def run_pipeline(
    task: str,
    dataset: str,
    seed: int,
    params: Dict | None = None,
) -> Tuple[str, Dict]:
    """Run a deterministic pipeline for a given task."""
    params = params or {}
    set_global_seed(seed)

    sections = []
    artifacts: Dict[str, object] = {"task": task, "dataset": dataset}

    if task == "cluster":
        X_df, _, meta = load_sklearn_dataset(dataset)
        profile = profile_dataframe(X_df)
        sections.append(("Profiling", f"Rows: {profile['n_rows']}, Cols: {profile['n_cols']}"))

        missing = missingness_report(X_df)
        X_clean = impute_missing(X_df)
        sections.append(("Cleaning", f"Missing counts: {missing['missing_counts']}"))

        X_encoded, _ = one_hot_encode(X_clean)
        X_scaled, _ = standard_scale(X_encoded)

        k = int(params.get("k", 3))
        kmeans_out = run_kmeans(X_scaled, k=k, seed=seed)
        silhouette = safe_silhouette(X_scaled, kmeans_out["labels"])

        sections.append(("Results", f"KMeans k={k}, inertia={kmeans_out['inertia']:.2f}, silhouette={silhouette}"))
        artifacts.update(
            {
                "n_rows": meta["n_rows"],
                "inertia": kmeans_out["inertia"],
                "silhouette": silhouette,
                "labels": kmeans_out["labels"],
            }
        )

    elif task == "anomaly":
        X_df, _, meta = load_sklearn_dataset(dataset)
        missing = missingness_report(X_df)
        X_clean = impute_missing(X_df)
        sections.append(("Profiling", f"Rows: {meta['n_rows']}, Cols: {X_df.shape[1]}"))
        sections.append(("Cleaning", f"Missing counts: {missing['missing_counts']}"))

        X_scaled, _ = standard_scale(X_clean)
        result = run_isolation_forest(X_scaled, seed=seed, contamination=float(params.get("contamination", 0.05)))
        sections.append(("Results", f"IsolationForest anomalies={result['n_anomalies']}"))
        artifacts.update({"n_anomalies": result["n_anomalies"], "scores": result["scores"]})

    elif task == "basket":
        transactions = load_basket_dataset(dataset)
        min_support = float(params.get("min_support", 0.2))
        min_confidence = float(params.get("min_confidence", 0.5))
        support_map = apriori(transactions, min_support=min_support)
        rules = generate_rules(support_map, min_confidence=min_confidence)
        summary = rules_summary(rules)

        sections.append(("Profiling", f"Transactions: {len(transactions)}"))
        sections.append(("Results", f"Apriori rules={summary['n_rules']}"))
        artifacts.update(
            {
                "n_rules": summary["n_rules"],
                "top_rule": summary["top_rule"],
                "n_transactions": len(transactions),
            }
        )

    else:
        raise ValueError(f"Unsupported task: {task}")

    report = render_report(f"Data Mining Pipeline: {task}", sections)
    return report, artifacts
