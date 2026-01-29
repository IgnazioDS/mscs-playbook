from __future__ import annotations

import numpy as np


def _convolve2d(arr: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    kh, kw = kernel.shape
    pad_h = kh // 2
    pad_w = kw // 2
    padded = np.pad(arr, ((pad_h, pad_h), (pad_w, pad_w)), mode="edge")
    out = np.zeros_like(arr, dtype=np.float32)
    for y in range(arr.shape[0]):
        for x in range(arr.shape[1]):
            window = padded[y : y + kh, x : x + kw]
            out[y, x] = float(np.sum(window * kernel))
    return out


def sobel_edges(gray: np.ndarray) -> np.ndarray:
    gx_kernel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)
    gy_kernel = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float32)
    gx = _convolve2d(gray, gx_kernel)
    gy = _convolve2d(gray, gy_kernel)
    magnitude = np.sqrt(gx * gx + gy * gy)
    return magnitude.astype(np.float32)


def harris_corners(gray: np.ndarray, k: float = 0.04, window: int = 3) -> np.ndarray:
    gx_kernel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)
    gy_kernel = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float32)
    ix = _convolve2d(gray, gx_kernel)
    iy = _convolve2d(gray, gy_kernel)

    ix2 = ix * ix
    iy2 = iy * iy
    ixy = ix * iy

    window_kernel = np.ones((window, window), dtype=np.float32)
    s_ix2 = _convolve2d(ix2, window_kernel)
    s_iy2 = _convolve2d(iy2, window_kernel)
    s_ixy = _convolve2d(ixy, window_kernel)

    det = s_ix2 * s_iy2 - s_ixy * s_ixy
    trace = s_ix2 + s_iy2
    response = det - k * (trace * trace)
    return response.astype(np.float32)


def topk_keypoints(response: np.ndarray, k: int) -> list[tuple[int, int, float]]:
    points: list[tuple[int, int, float]] = []
    for y in range(response.shape[0]):
        for x in range(response.shape[1]):
            points.append((y, x, float(response[y, x])))
    points.sort(key=lambda item: (-item[2], item[0], item[1]))
    return points[: max(k, 0)]
