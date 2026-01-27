"""Deterministic random seed utilities."""

from __future__ import annotations

import numpy as np


def set_global_seed(seed: int) -> None:
    """Set global numpy seed for deterministic behavior.

    Note: full determinism may still depend on downstream library behavior.
    """
    np.random.seed(seed)
