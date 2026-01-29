from __future__ import annotations

import numpy as np

from .reproducibility import set_global_seed


def collect_returns(run_fn, seeds: list[int]) -> np.ndarray:
    curves = []
    for seed in seeds:
        set_global_seed(seed)
        curves.append(run_fn(seed))
    return np.vstack(curves)
