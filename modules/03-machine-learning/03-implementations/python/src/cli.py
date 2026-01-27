"""CLI runner for ML baselines and unsupervised demos."""

from __future__ import annotations

import argparse
import sys
from typing import Any, Dict

import numpy as np

from src.datasets.loading import load_dataset, train_val_test_split
from src.evaluation.metrics import classification_report_dict, regression_metrics
from src.preprocessing.pipelines import make_classification_pipeline, make_regression_pipeline
from src.unsupervised.clustering import kmeans_cluster, silhouette_score_safe
from src.unsupervised.dimensionality_reduction import pca_reduce
from src.utils.random import set_global_seed


SUPPORTED_DATASETS = {"iris", "breast_cancer", "california_housing"}


def _print_header(title: str) -> None:
    print(f"\n== {title} ==")


def _print_dataset_info(name: str, X: np.ndarray, y: np.ndarray) -> None:
    print(f"dataset: {name}")
    print(f"shapes: X={X.shape}, y={y.shape}")


def _print_interpretation(line: str) -> None:
    print(f"interpretation: {line}")


def _train_classifier(args: argparse.Namespace) -> int:
    X, y, _, target_name, task_type = load_dataset(args.dataset)
    if task_type != "classification":
        print("Error: dataset is not classification")
        return 2

    set_global_seed(args.seed)
    X_train, X_val, X_test, y_train, y_val, y_test = train_val_test_split(
        X, y, seed=args.seed, test_size=args.test_size, val_size=args.val_size
    )

    model = make_classification_pipeline(seed=args.seed)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_val)
    report = classification_report_dict(y_val, y_pred)

    _print_header("Classification")
    _print_dataset_info(args.dataset, X, y)
    print(f"target: {target_name}")
    print("pipeline: StandardScaler + LogisticRegression")
    print(f"metrics: accuracy={report['accuracy']:.3f}")
    _print_interpretation("Check class-wise precision/recall before tuning thresholds.")

    return 0


def _train_regressor(args: argparse.Namespace) -> int:
    X, y, _, target_name, task_type = load_dataset(args.dataset)
    if task_type != "regression":
        print("Error: dataset is not regression")
        return 2

    set_global_seed(args.seed)
    X_train, X_val, X_test, y_train, y_val, y_test = train_val_test_split(
        X, y, seed=args.seed, test_size=args.test_size, val_size=args.val_size
    )

    model = make_regression_pipeline(seed=args.seed)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_val)
    metrics = regression_metrics(y_val, y_pred)

    _print_header("Regression")
    _print_dataset_info(args.dataset, X, y)
    print(f"target: {target_name}")
    print("pipeline: StandardScaler + Ridge")
    print(f"metrics: rmse={metrics['rmse']:.3f}, mae={metrics['mae']:.3f}, r2={metrics['r2']:.3f}")
    _print_interpretation("Compare to baseline RMSE and check residual patterns.")

    return 0


def _cluster(args: argparse.Namespace) -> int:
    X, y, _, target_name, task_type = load_dataset(args.dataset)

    set_global_seed(args.seed)
    labels = kmeans_cluster(X, k=args.k, seed=args.seed)
    score = silhouette_score_safe(X, labels)
    X_red, var = pca_reduce(X, n_components=2, seed=args.seed)

    _print_header("Clustering")
    _print_dataset_info(args.dataset, X, y)
    print(f"pipeline: KMeans(k={args.k}) + PCA(2)")
    print(f"metrics: silhouette={score:.3f}, pca_var_sum={var.sum():.3f}")
    _print_interpretation("If silhouette is low, try different k or feature scaling.")

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ML Module 03 CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--dataset", required=True, choices=sorted(SUPPORTED_DATASETS))
    common.add_argument("--seed", type=int, default=42)
    common.add_argument("--test-size", type=float, default=0.2)
    common.add_argument("--val-size", type=float, default=0.2)

    cls = sub.add_parser("train-classifier", parents=[common], help="Train a classifier baseline")
    cls.set_defaults(func=_train_classifier)

    reg = sub.add_parser("train-regressor", parents=[common], help="Train a regressor baseline")
    reg.set_defaults(func=_train_regressor)

    clust = sub.add_parser("cluster", parents=[common], help="Run clustering demo")
    clust.add_argument("--k", type=int, default=3)
    clust.set_defaults(func=_cluster)

    return parser


def main(argv: list[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
