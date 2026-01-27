"""Deterministic random helpers."""

import numpy as np


def seeded_rng(seed: int) -> np.random.Generator:
    """Return a fresh, deterministic RNG for repeatable experiments."""
    return np.random.default_rng(seed)
