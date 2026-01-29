from __future__ import annotations

from typing import Iterable
import numpy as np


def confusion_matrix(y_true: Iterable[int], y_pred: Iterable[int], labels: Iterable[int]) -> np.ndarray:
    labels_list = list(labels)
    label_to_idx = {label: idx for idx, label in enumerate(labels_list)}
    matrix = np.zeros((len(labels_list), len(labels_list)), dtype=int)
    for true, pred in zip(y_true, y_pred):
        if true not in label_to_idx or pred not in label_to_idx:
            continue
        matrix[label_to_idx[true], label_to_idx[pred]] += 1
    return matrix


def worst_k_examples(
    y_true: Iterable[int],
    y_pred: Iterable[int],
    probs: np.ndarray,
    k: int,
) -> list[tuple[int, int, int, float]]:
    y_true_list = list(y_true)
    y_pred_list = list(y_pred)
    losses: list[tuple[int, int, int, float]] = []
    for idx, (true, pred) in enumerate(zip(y_true_list, y_pred_list)):
        if true < 0 or true >= probs.shape[1]:
            raise ValueError("true label out of range for probs")
        confidence = float(probs[idx, true])
        loss = 1.0 - confidence
        losses.append((idx, true, pred, loss))
    losses.sort(key=lambda item: (-item[3], item[0]))
    return losses[: max(k, 0)]
