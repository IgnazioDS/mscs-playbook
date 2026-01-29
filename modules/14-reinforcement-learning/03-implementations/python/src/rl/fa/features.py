from __future__ import annotations

import numpy as np


def one_hot(index: int, size: int) -> np.ndarray:
    vec = np.zeros(size, dtype=np.float32)
    vec[index] = 1.0
    return vec


def chain_features(state: int, length: int) -> np.ndarray:
    return one_hot(state, length)
