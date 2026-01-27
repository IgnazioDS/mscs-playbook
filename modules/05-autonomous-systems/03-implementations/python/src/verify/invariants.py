"""Invariant checks over trajectories."""

from __future__ import annotations

from typing import Callable, Optional, Tuple

import numpy as np


def check_invariant_over_trajectory(
    X: np.ndarray, predicate: Callable[[np.ndarray], bool]
) -> Tuple[bool, Optional[int]]:
    """Check predicate over each state in a trajectory.

    Returns (ok, first_bad_index). If ok is True, first_bad_index is None.
    """
    for idx, x in enumerate(X):
        if not predicate(np.asarray(x)):
            return False, idx
    return True, None
