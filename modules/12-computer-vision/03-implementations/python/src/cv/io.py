from __future__ import annotations

from pathlib import Path
import numpy as np
from PIL import Image


def load_image(path: str | Path) -> np.ndarray:
    img = Image.open(path).convert("RGB")
    arr = np.asarray(img, dtype=np.float32) / 255.0
    return arr


def save_image(path: str | Path, arr: np.ndarray) -> None:
    clipped = np.clip(arr, 0.0, 1.0)
    if clipped.ndim == 2:
        img_arr = (clipped * 255).astype(np.uint8)
        img = Image.fromarray(img_arr, mode="L")
    else:
        img_arr = (clipped * 255).astype(np.uint8)
        img = Image.fromarray(img_arr, mode="RGB")
    img.save(path)


def to_grayscale(arr: np.ndarray) -> np.ndarray:
    if arr.ndim == 2:
        gray = arr.astype(np.float32)
    else:
        weights = np.array([0.2989, 0.5870, 0.1140], dtype=np.float32)
        gray = np.tensordot(arr, weights, axes=([-1], [0]))
    return np.clip(gray, 0.0, 1.0).astype(np.float32)
