import numpy as np

from src.cv.metrics import (
    accuracy,
    detection_precision_recall,
    f1_macro,
    iou,
    precision_macro,
    recall_macro,
    segmentation_dice,
    segmentation_iou,
    segmentation_pixel_accuracy,
)


def test_classification_metrics():
    y_true = [0, 1, 1, 0]
    y_pred = [0, 1, 0, 0]
    assert accuracy(y_true, y_pred) == 0.75
    assert round(precision_macro(y_true, y_pred), 4) == 0.8333
    assert recall_macro(y_true, y_pred) == 0.75
    assert round(f1_macro(y_true, y_pred), 4) == 0.7333


def test_detection_metrics():
    box_a = [0, 0, 2, 2]
    box_b = [1, 1, 3, 3]
    assert round(iou(box_a, box_b), 4) == 0.2857
    precision, recall = detection_precision_recall([box_a], [box_a])
    assert precision == 1.0
    assert recall == 1.0


def test_segmentation_metrics():
    true_mask = np.array([[1, 0], [1, 0]], dtype=np.uint8)
    pred_mask = np.array([[1, 1], [0, 0]], dtype=np.uint8)
    assert segmentation_pixel_accuracy(true_mask, pred_mask) == 0.5
    assert segmentation_iou(true_mask, pred_mask) == 0.3333333333333333
    assert segmentation_dice(true_mask, pred_mask) == 0.5
