"""Discrete-time LTI simulation."""

from __future__ import annotations

import numpy as np


def _as_2d(matrix: np.ndarray, name: str) -> np.ndarray:
    if matrix.ndim == 1:
        return matrix.reshape(-1, 1)
    if matrix.ndim != 2:
        raise ValueError(f"{name} must be 1D or 2D, got shape {matrix.shape}")
    return matrix


def simulate_discrete(A: np.ndarray, B: np.ndarray, x0: np.ndarray, U: np.ndarray) -> np.ndarray:
    """Simulate x_{k+1} = A x_k + B u_k.

    Args:
        A: (n, n) state matrix
        B: (n, m) input matrix
        x0: (n,) initial state
        U: (T, m) or (T,) inputs over time
    Returns:
        X: (T+1, n) trajectory with X[0] = x0
    """
    A = np.asarray(A, dtype=float)
    B = np.asarray(B, dtype=float)
    x0 = np.asarray(x0, dtype=float)
    U = np.asarray(U, dtype=float)

    if x0.ndim != 1:
        raise ValueError(f"x0 must be 1D, got shape {x0.shape}")
    n = x0.shape[0]

    if A.shape != (n, n):
        raise ValueError(f"A must be shape ({n}, {n}), got {A.shape}")

    B = _as_2d(B, "B")
    if B.shape[0] != n:
        raise ValueError(f"B must have {n} rows, got {B.shape}")
    m = B.shape[1]

    if U.ndim == 1:
        U = U.reshape(-1, 1)
    elif U.ndim != 2:
        raise ValueError(f"U must be 1D or 2D, got shape {U.shape}")

    if U.shape[1] != m:
        raise ValueError(f"U must have {m} columns, got {U.shape}")

    T = U.shape[0]
    X = np.zeros((T + 1, n), dtype=float)
    X[0] = x0

    for k in range(T):
        u_k = U[k]
        X[k + 1] = A @ X[k] + B @ u_k

    return X
