from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageDraw

from ..metrics import detection_precision_recall
from .reporting import write_markdown_report


@dataclass(frozen=True)
class OCRResult:
    seed: int
    iou: float
    token_count: int
    precision: float
    recall: float
    example_boxes: list[list[int]]


def _generate_document(seed: int, size: tuple[int, int] = (64, 64)) -> tuple[np.ndarray, list[list[int]]]:
    rng = np.random.RandomState(seed)
    img = Image.new("L", size, color=255)
    draw = ImageDraw.Draw(img)
    boxes: list[list[int]] = []
    for idx in range(5):
        x = int(rng.randint(5, 40))
        y = int(rng.randint(5, 50))
        w = int(rng.randint(8, 14))
        h = int(rng.randint(4, 8))
        x2 = min(x + w, size[0] - 2)
        y2 = min(y + h, size[1] - 2)
        draw.rectangle([x, y, x2, y2], fill=0)
        boxes.append([x, y, x2, y2])
    arr = np.asarray(img, dtype=np.float32) / 255.0
    return arr, boxes


def _connected_components(mask: np.ndarray, min_area: int = 4) -> list[list[int]]:
    height, width = mask.shape
    visited = np.zeros_like(mask, dtype=bool)
    boxes: list[list[int]] = []

    for y in range(height):
        for x in range(width):
            if mask[y, x] and not visited[y, x]:
                stack = [(y, x)]
                visited[y, x] = True
                coords = []
                while stack:
                    cy, cx = stack.pop()
                    coords.append((cy, cx))
                    for ny, nx in (
                        (cy - 1, cx),
                        (cy + 1, cx),
                        (cy, cx - 1),
                        (cy, cx + 1),
                    ):
                        if 0 <= ny < height and 0 <= nx < width:
                            if mask[ny, nx] and not visited[ny, nx]:
                                visited[ny, nx] = True
                                stack.append((ny, nx))
                if len(coords) < min_area:
                    continue
                ys, xs = zip(*coords)
                boxes.append([min(xs), min(ys), max(xs), max(ys)])
    boxes.sort(key=lambda item: (item[1], item[0]))
    return boxes


def run_doc_ocr_lite(seed: int = 42, out: str | None = None) -> str:
    image, gt_boxes = _generate_document(seed)
    gray = image
    mask = gray < 0.5
    pred_boxes = _connected_components(mask, min_area=6)

    precision, recall = detection_precision_recall(pred_boxes, gt_boxes, iou_threshold=0.5)
    example = pred_boxes[0] if pred_boxes else []

    output_lines = [
        "task: doc-ocr-lite",
        f"seed: {seed}",
        f"tokens: {len(gt_boxes)}",
        f"predicted_tokens: {len(pred_boxes)}",
        f"metrics: precision={precision:.3f}, recall={recall:.3f}",
        f"example: {example}",
    ]
    output = "\n".join(output_lines)

    if out:
        sections = [
            ("Inputs", f"seed: {seed}"),
            ("Metrics", f"precision: {precision:.3f}\nrecall: {recall:.3f}"),
            ("Example", f"first_token_box: {example}"),
        ]
        write_markdown_report(out, "Document OCR-lite Report", sections, notes="Heuristic token detection on synthetic docs.")

    return output
