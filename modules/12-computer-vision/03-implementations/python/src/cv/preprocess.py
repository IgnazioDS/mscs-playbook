from __future__ import annotations

from typing import Sequence
import numpy as np
from PIL import Image


def resize(arr: np.ndarray, size: tuple[int, int]) -> np.ndarray:
    height, width = size
    if arr.ndim == 2:
        img = Image.fromarray((np.clip(arr, 0.0, 1.0) * 255).astype(np.uint8), mode="L")
        resized = img.resize((width, height), resample=Image.BILINEAR)
        return np.asarray(resized, dtype=np.float32) / 255.0
    img = Image.fromarray((np.clip(arr, 0.0, 1.0) * 255).astype(np.uint8), mode="RGB")
    resized = img.resize((width, height), resample=Image.BILINEAR)
    return np.asarray(resized, dtype=np.float32) / 255.0


def normalize(arr: np.ndarray, mean: Sequence[float], std: Sequence[float]) -> np.ndarray:
    data = arr.astype(np.float32)
    if data.ndim == 2:
        mean_val = float(mean[0])
        std_val = float(std[0])
        return (data - mean_val) / std_val
    mean_arr = np.array(mean, dtype=np.float32)
    std_arr = np.array(std, dtype=np.float32)
    return (data - mean_arr) / std_arr


def random_flip(arr: np.ndarray, seed: int, p: float = 0.5) -> np.ndarray:
    rng = np.random.RandomState(seed)
    if rng.rand() < p:
        if arr.ndim == 2:
            return np.ascontiguousarray(np.fliplr(arr))
        return np.ascontiguousarray(arr[:, ::-1, :])
    return arr.copy()


def random_crop(arr: np.ndarray, crop_size: tuple[int, int], seed: int) -> np.ndarray:
    crop_h, crop_w = crop_size
    height, width = arr.shape[:2]
    if crop_h > height or crop_w > width:
        raise ValueError("crop_size must be <= image size")
    rng = np.random.RandomState(seed)
    max_y = height - crop_h
    max_x = width - crop_w
    y = int(rng.randint(0, max_y + 1))
    x = int(rng.randint(0, max_x + 1))
    if arr.ndim == 2:
        return arr[y : y + crop_h, x : x + crop_w].copy()
    return arr[y : y + crop_h, x : x + crop_w, :].copy()
