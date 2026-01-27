"""Randomness control utilities for reproducibility."""

from __future__ import annotations

import random
from typing import Optional

import numpy as np


def set_global_seed(seed: int, deterministic_hash: bool = False) -> None:
    """Set global seeds for Python and NumPy.

    Args:
        seed: Integer seed value.
        deterministic_hash: If True, sets PYTHONHASHSEED for new processes.

    Notes:
        Some scikit-learn algorithms accept a random_state parameter; prefer
        passing the seed explicitly to those estimators for full determinism.
    """
    random.seed(seed)
    np.random.seed(seed)
    if deterministic_hash:
        # This only affects new Python processes, but is useful to document.
        import os

        os.environ.setdefault("PYTHONHASHSEED", str(seed))
