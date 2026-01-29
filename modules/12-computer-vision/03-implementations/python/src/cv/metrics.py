from __future__ import annotations

from typing import Iterable
import numpy as np


def accuracy(y_true: Iterable[int], y_pred: Iterable[int]) -> float:
    y_true_arr = np.array(list(y_true))
    y_pred_arr = np.array(list(y_pred))
    if y_true_arr.size == 0:
        return 0.0
    return float(np.mean(y_true_arr == y_pred_arr))


def _precision_recall_f1(y_true: np.ndarray, y_pred: np.ndarray, label: int) -> tuple[float, float, float]:
    tp = int(np.sum((y_true == label) & (y_pred == label)))
    fp = int(np.sum((y_true != label) & (y_pred == label)))
    fn = int(np.sum((y_true == label) & (y_pred != label)))
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    return precision, recall, f1


def precision_macro(y_true: Iterable[int], y_pred: Iterable[int]) -> float:
    y_true_arr = np.array(list(y_true))
    y_pred_arr = np.array(list(y_pred))
    labels = sorted(set(y_true_arr.tolist()) | set(y_pred_arr.tolist()))
    if not labels:
        return 0.0
    scores = [_precision_recall_f1(y_true_arr, y_pred_arr, label)[0] for label in labels]
    return float(np.mean(scores))


def recall_macro(y_true: Iterable[int], y_pred: Iterable[int]) -> float:
    y_true_arr = np.array(list(y_true))
    y_pred_arr = np.array(list(y_pred))
    labels = sorted(set(y_true_arr.tolist()) | set(y_pred_arr.tolist()))
    if not labels:
        return 0.0
    scores = [_precision_recall_f1(y_true_arr, y_pred_arr, label)[1] for label in labels]
    return float(np.mean(scores))


def f1_macro(y_true: Iterable[int], y_pred: Iterable[int]) -> float:
    y_true_arr = np.array(list(y_true))
    y_pred_arr = np.array(list(y_pred))
    labels = sorted(set(y_true_arr.tolist()) | set(y_pred_arr.tolist()))
    if not labels:
        return 0.0
    scores = [_precision_recall_f1(y_true_arr, y_pred_arr, label)[2] for label in labels]
    return float(np.mean(scores))


def iou(box_a: Iterable[int], box_b: Iterable[int]) -> float:
    ax1, ay1, ax2, ay2 = box_a
    bx1, by1, bx2, by2 = box_b
    ix1 = max(ax1, bx1)
    iy1 = max(ay1, by1)
    ix2 = min(ax2, bx2)
    iy2 = min(ay2, by2)
    inter_w = max(0, ix2 - ix1 + 1)
    inter_h = max(0, iy2 - iy1 + 1)
    inter = inter_w * inter_h
    area_a = max(0, ax2 - ax1 + 1) * max(0, ay2 - ay1 + 1)
    area_b = max(0, bx2 - bx1 + 1) * max(0, by2 - by1 + 1)
    union = area_a + area_b - inter
    return float(inter / union) if union > 0 else 0.0


def detection_precision_recall(
    pred_boxes: list[list[int]],
    gt_boxes: list[list[int]],
    iou_threshold: float = 0.5,
) -> tuple[float, float]:
    matched_gt = set()
    tp = 0
    for pred in pred_boxes:
        best_iou = 0.0
        best_idx = None
        for idx, gt in enumerate(gt_boxes):
            if idx in matched_gt:
                continue
            score = iou(pred, gt)
            if score > best_iou:
                best_iou = score
                best_idx = idx
        if best_iou >= iou_threshold and best_idx is not None:
            tp += 1
            matched_gt.add(best_idx)
    fp = len(pred_boxes) - tp
    fn = len(gt_boxes) - tp
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    return precision, recall


def segmentation_pixel_accuracy(mask_true: np.ndarray, mask_pred: np.ndarray) -> float:
    total = mask_true.size
    if total == 0:
        return 0.0
    return float(np.mean(mask_true == mask_pred))


def segmentation_iou(mask_true: np.ndarray, mask_pred: np.ndarray) -> float:
    intersection = np.logical_and(mask_true, mask_pred).sum()
    union = np.logical_or(mask_true, mask_pred).sum()
    return float(intersection / union) if union > 0 else 0.0


def segmentation_dice(mask_true: np.ndarray, mask_pred: np.ndarray) -> float:
    intersection = np.logical_and(mask_true, mask_pred).sum()
    total = mask_true.sum() + mask_pred.sum()
    return float(2 * intersection / total) if total > 0 else 0.0
