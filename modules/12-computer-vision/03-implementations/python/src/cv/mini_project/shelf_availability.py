from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from ..error_analysis import confusion_matrix, worst_k_examples
from ..metrics import accuracy, f1_macro
from ..simple_models import train_classifier
from .reporting import write_markdown_report


@dataclass(frozen=True)
class ShelfResult:
    seed: int
    total: int
    accuracy: float
    f1: float
    confusion: list[list[int]]
    worst: list[tuple[int, int, int, float]]


def _generate_shelf_data(seed: int, samples_per_class: int = 6) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.RandomState(seed)
    images: list[np.ndarray] = []
    labels: list[int] = []

    for _ in range(samples_per_class):
        empty = rng.uniform(0.0, 0.2, size=(16, 16)).astype(np.float32)
        images.append(empty)
        labels.append(0)

    for _ in range(samples_per_class):
        stocked = rng.uniform(0.0, 0.2, size=(16, 16)).astype(np.float32)
        for col in range(2, 14, 3):
            stocked[:, col : col + 1] += 0.8
        stocked = np.clip(stocked, 0.0, 1.0)
        images.append(stocked)
        labels.append(1)

    X = np.stack(images).reshape(len(images), -1)
    y = np.array(labels)
    return X, y


def run_shelf_availability(seed: int = 42, out: str | None = None) -> str:
    X, y = _generate_shelf_data(seed)
    model, _ = train_classifier(X, y, seed=seed)
    preds = model.predict(X)
    probs = model.predict_proba(X)

    acc = accuracy(y, preds)
    f1 = f1_macro(y, preds)
    conf = confusion_matrix(y, preds, labels=[0, 1])
    worst = worst_k_examples(y, preds, probs, k=3)

    formatted_worst = [
        (int(idx), int(true), int(pred), round(float(loss), 3)) for idx, true, pred, loss in worst
    ]

    output_lines = [
        "task: shelf-availability",
        f"seed: {seed}",
        f"counts: total={len(y)}, empty={int(np.sum(y == 0))}, stocked={int(np.sum(y == 1))}",
        f"metrics: accuracy={acc:.3f}, f1_macro={f1:.3f}",
        f"confusion_matrix: {conf.tolist()}",
        f"worst_examples: {formatted_worst}",
    ]
    output = "\n".join(output_lines)

    if out:
        sections = [
            ("Inputs", f"seed: {seed}"),
            ("Metrics", f"accuracy: {acc:.3f}\nf1_macro: {f1:.3f}"),
            ("Confusion Matrix", str(conf.tolist())),
            ("Worst Examples", str(formatted_worst)),
        ]
        write_markdown_report(out, "Shelf Availability Report", sections, notes="Tiny synthetic dataset classifier.")

    return output
