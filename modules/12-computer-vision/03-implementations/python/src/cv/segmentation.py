from __future__ import annotations

import numpy as np


def _dilate(mask: np.ndarray) -> np.ndarray:
    height, width = mask.shape
    out = np.zeros_like(mask, dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            y0 = max(0, y - 1)
            y1 = min(height, y + 2)
            x0 = max(0, x - 1)
            x1 = min(width, x + 2)
            if np.any(mask[y0:y1, x0:x1]):
                out[y, x] = 1
    return out


def _erode(mask: np.ndarray) -> np.ndarray:
    height, width = mask.shape
    out = np.zeros_like(mask, dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            y0 = max(0, y - 1)
            y1 = min(height, y + 2)
            x0 = max(0, x - 1)
            x1 = min(width, x + 2)
            if np.all(mask[y0:y1, x0:x1]):
                out[y, x] = 1
    return out


def segment_threshold(gray: np.ndarray, threshold: float = 0.5, iterations: int = 1) -> np.ndarray:
    mask = (gray > threshold).astype(np.uint8)
    for _ in range(iterations):
        mask = _dilate(mask)
        mask = _erode(mask)
    return mask
