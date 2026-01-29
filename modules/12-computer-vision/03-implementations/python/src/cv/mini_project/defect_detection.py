from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

from ..datasets import generate_tiny_images, load_dataset
from ..detection import detect_objects
from ..io import to_grayscale
from ..metrics import detection_precision_recall
from .reporting import write_markdown_report


@dataclass(frozen=True)
class DefectResult:
    seed: int
    iou: float
    image_count: int
    predicted_total: int
    precision: float
    recall: float
    example_boxes: list[list[int]]


def _prepare_dataset(seed: int, base_dir: Path) -> tuple[np.ndarray, list[list[int]]]:
    generate_tiny_images(base_dir, seed=seed)
    images, _, extra = load_dataset(base_dir)
    boxes = [box for box in extra["boxes"] if box is not None]
    return images, boxes


def run_defect_detection(seed: int = 42, iou: float = 0.5, out: str | None = None) -> str:
    base_dir = Path(__file__).resolve().parents[3] / "data"
    images, gt_boxes = _prepare_dataset(seed, base_dir)

    pred_boxes: list[list[int]] = []
    for img in images:
        gray = to_grayscale(img)
        detections = detect_objects(gray, threshold=0.4, min_area=8)
        pred_boxes.extend([det[0] for det in detections])

    precision, recall = detection_precision_recall(pred_boxes, gt_boxes, iou_threshold=iou)
    example = pred_boxes[0] if pred_boxes else []

    output_lines = [
        "task: defect-detect",
        f"seed: {seed}",
        f"iou: {iou}",
        f"images: {len(images)}",
        f"predicted_boxes_total: {len(pred_boxes)}",
        f"metrics: precision={precision:.3f}, recall={recall:.3f}",
        f"example: {example}",
    ]
    output = "\n".join(output_lines)

    if out:
        sections = [
            ("Inputs", f"seed: {seed}\niou: {iou}"),
            ("Metrics", f"precision: {precision:.3f}\nrecall: {recall:.3f}"),
            ("Example", f"first_boxes: {example}"),
        ]
        write_markdown_report(out, "Defect Detection Report", sections, notes="Toy detection on synthetic data.")

    return output
