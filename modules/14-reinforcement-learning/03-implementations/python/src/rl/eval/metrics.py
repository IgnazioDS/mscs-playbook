from __future__ import annotations

import numpy as np


def moving_avg(values: list[float], window: int) -> list[float]:
    if window <= 0:
        raise ValueError("window must be positive")
    out = []
    for i in range(len(values)):
        start = max(0, i - window + 1)
        out.append(float(np.mean(values[start : i + 1])))
    return out


def returns(rewards: list[float]) -> float:
    return float(np.sum(rewards))


def regret(regrets: list[float]) -> float:
    return float(np.sum(regrets))
