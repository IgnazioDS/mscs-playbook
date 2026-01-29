from __future__ import annotations

import numpy as np


def make_rng(seed: int | None) -> np.random.RandomState:
    return np.random.RandomState(seed)
