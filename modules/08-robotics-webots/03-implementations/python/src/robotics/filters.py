"""Simple filters for robotics signals."""

from __future__ import annotations

from typing import List, Tuple


def moving_average(seq: List[float], window: int) -> List[float]:
    if window <= 0:
        raise ValueError("window must be positive")
    out = []
    for i in range(len(seq)):
        start = max(0, i - window + 1)
        chunk = seq[start : i + 1]
        out.append(sum(chunk) / len(chunk))
    return out


def alpha_beta_filter(measurements: List[float], alpha: float, beta: float, dt: float) -> Tuple[List[float], List[float]]:
    if not measurements:
        return [], []
    x = measurements[0]
    v = 0.0
    xs = [x]
    vs = [v]
    for z in measurements[1:]:
        x_pred = x + v * dt
        v_pred = v
        residual = z - x_pred
        x = x_pred + alpha * residual
        v = v_pred + (beta * residual) / dt
        xs.append(x)
        vs.append(v)
    return xs, vs
