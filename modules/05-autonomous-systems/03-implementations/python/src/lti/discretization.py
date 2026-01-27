"""Zero-order hold discretization using a truncated series expansion.

Limitations:
- Accuracy depends on the truncation order and dt.
- For stiff or large-magnitude systems, use a higher order or a smaller dt.
- This avoids SciPy by using a simple series approximation.
"""

from __future__ import annotations

import numpy as np


def zoh_discretize(Ac: np.ndarray, Bc: np.ndarray, dt: float, order: int = 8) -> tuple[np.ndarray, np.ndarray]:
    """Discretize continuous-time (Ac, Bc) with ZOH using series expansion.

    The augmented matrix is:
        M = [[Ac, Bc],
             [0 ,  0]]
    and exp(M * dt) is approximated by a truncated series.
    """
    if dt <= 0:
        raise ValueError("dt must be positive")
    if order < 1:
        raise ValueError("order must be >= 1")

    Ac = np.asarray(Ac, dtype=float)
    Bc = np.asarray(Bc, dtype=float)

    if Ac.ndim != 2 or Ac.shape[0] != Ac.shape[1]:
        raise ValueError("Ac must be a square 2D array")
    n = Ac.shape[0]

    if Bc.ndim == 1:
        Bc = Bc.reshape(-1, 1)
    if Bc.ndim != 2 or Bc.shape[0] != n:
        raise ValueError("Bc must be a 2D array with the same row dimension as Ac")
    m = Bc.shape[1]

    M = np.zeros((n + m, n + m), dtype=float)
    M[:n, :n] = Ac
    M[:n, n:] = Bc

    scaled = M * dt
    expm = np.eye(n + m, dtype=float)
    term = np.eye(n + m, dtype=float)

    for i in range(1, order + 1):
        term = term @ scaled / i
        expm = expm + term

    Ad = expm[:n, :n]
    Bd = expm[:n, n:]
    return Ad, Bd
