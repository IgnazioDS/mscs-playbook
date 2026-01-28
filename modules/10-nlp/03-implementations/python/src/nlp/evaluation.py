"""Evaluation utilities for NLP tasks."""

from __future__ import annotations

from typing import Dict, List, Set

import numpy as np


def classification_report_simple(y_true: List[str], y_pred: List[str]) -> Dict[str, float]:
    labels = sorted(set(y_true) | set(y_pred))
    precisions = []
    recalls = []
    f1s = []
    correct = sum(1 for t, p in zip(y_true, y_pred) if t == p)
    accuracy = correct / len(y_true) if y_true else 0.0

    for label in labels:
        tp = sum(1 for t, p in zip(y_true, y_pred) if t == label and p == label)
        fp = sum(1 for t, p in zip(y_true, y_pred) if t != label and p == label)
        fn = sum(1 for t, p in zip(y_true, y_pred) if t == label and p != label)
        precision = tp / (tp + fp) if tp + fp > 0 else 0.0
        recall = tp / (tp + fn) if tp + fn > 0 else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0.0
        precisions.append(precision)
        recalls.append(recall)
        f1s.append(f1)

    return {
        "accuracy": accuracy,
        "precision_macro": float(np.mean(precisions)) if precisions else 0.0,
        "recall_macro": float(np.mean(recalls)) if recalls else 0.0,
        "f1_macro": float(np.mean(f1s)) if f1s else 0.0,
    }


def retrieval_metrics_at_k(
    relevant_sets: List[Set[str]], retrieved_lists: List[List[str]], k: int
) -> Dict[str, float]:
    precisions = []
    recalls = []
    mrrs = []
    for relevant, retrieved in zip(relevant_sets, retrieved_lists):
        topk = retrieved[:k]
        hits = [doc for doc in topk if doc in relevant]
        precisions.append(len(hits) / k if k else 0.0)
        recalls.append(len(hits) / len(relevant) if relevant else 0.0)
        rank = 0
        for i, doc in enumerate(topk, start=1):
            if doc in relevant:
                rank = i
                break
        mrrs.append(1.0 / rank if rank > 0 else 0.0)

    return {
        "precision_at_k": float(np.mean(precisions)) if precisions else 0.0,
        "recall_at_k": float(np.mean(recalls)) if recalls else 0.0,
        "mrr_at_k": float(np.mean(mrrs)) if mrrs else 0.0,
    }
