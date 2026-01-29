from __future__ import annotations

import json
from pathlib import Path
from typing import Any
import numpy as np
from PIL import Image

from .io import load_image, save_image


def _draw_square(canvas: np.ndarray, top: int, left: int, size: int, color: tuple[float, float, float]) -> np.ndarray:
    canvas[top : top + size, left : left + size, :] = color
    return canvas


def _draw_circle(canvas: np.ndarray, center: tuple[int, int], radius: int, color: tuple[float, float, float]) -> np.ndarray:
    cy, cx = center
    y, x = np.ogrid[: canvas.shape[0], : canvas.shape[1]]
    mask = (y - cy) ** 2 + (x - cx) ** 2 <= radius ** 2
    canvas[mask] = color
    return canvas


def _draw_triangle(canvas: np.ndarray, top: int, left: int, size: int, color: tuple[float, float, float]) -> np.ndarray:
    for y in range(size):
        width = y + 1
        canvas[top + y, left : left + width, :] = color
    return canvas


def generate_tiny_images(out_dir: str | Path, seed: int = 0) -> dict[str, Any]:
    rng = np.random.RandomState(seed)
    out_path = Path(out_dir)
    images_dir = out_path / "tiny_images"
    images_dir.mkdir(parents=True, exist_ok=True)

    labels: dict[str, Any] = {}
    size = 32
    shape_types = ["square", "circle", "triangle"]

    for idx in range(12):
        label = shape_types[idx % len(shape_types)]
        canvas = np.zeros((size, size, 3), dtype=np.float32)
        color = tuple(float(c) for c in rng.uniform(0.6, 1.0, size=3))
        top = int(rng.randint(6, 12))
        left = int(rng.randint(6, 12))
        shape_size = int(rng.randint(8, 12))

        if label == "square":
            canvas = _draw_square(canvas, top, left, shape_size, color)
        elif label == "circle":
            center = (top + shape_size // 2, left + shape_size // 2)
            canvas = _draw_circle(canvas, center, shape_size // 2, color)
        else:
            canvas = _draw_triangle(canvas, top, left, shape_size, color)

        filename = f"img_{idx:02d}.png"
        save_image(images_dir / filename, canvas)

        entry: dict[str, Any] = {"class": label}
        if idx < 3:
            x1, y1 = left, top
            x2, y2 = left + shape_size - 1, top + shape_size - 1
            entry["box"] = [x1, y1, x2, y2]
            mask = np.zeros((size, size), dtype=np.float32)
            mask[top : top + shape_size, left : left + shape_size] = 1.0
            mask_name = f"mask_{idx:02d}.png"
            save_image(images_dir / mask_name, mask)
            entry["mask"] = mask_name
        labels[filename] = entry

    labels_path = out_path / "labels.json"
    labels_path.write_text(json.dumps(labels, indent=2), encoding="utf-8")
    return labels


def load_dataset(data_dir: str | Path) -> tuple[np.ndarray, list[str], dict[str, list[Any]]]:
    data_path = Path(data_dir)
    labels_path = data_path / "labels.json"
    labels_data = json.loads(labels_path.read_text(encoding="utf-8"))

    images: list[np.ndarray] = []
    labels: list[str] = []
    boxes: list[list[int] | None] = []
    masks: list[np.ndarray | None] = []

    for filename in sorted(labels_data.keys()):
        entry = labels_data[filename]
        img_path = data_path / "tiny_images" / filename
        images.append(load_image(img_path))
        labels.append(entry["class"])
        boxes.append(entry.get("box"))
        mask_name = entry.get("mask")
        if mask_name:
            mask = load_image(data_path / "tiny_images" / mask_name)
            if mask.ndim == 3:
                mask = mask[:, :, 0]
            masks.append(mask)
        else:
            masks.append(None)

    return np.stack(images), labels, {"boxes": boxes, "masks": masks}
