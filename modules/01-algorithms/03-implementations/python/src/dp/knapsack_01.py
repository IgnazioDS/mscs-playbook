from __future__ import annotations

from typing import List


def knapsack_01(values: List[int], weights: List[int], capacity: int) -> int:
    """Return the maximum value for 0/1 knapsack."""
    if capacity < 0:
        raise ValueError("capacity must be non-negative")
    if len(values) != len(weights):
        raise ValueError("values and weights must have the same length")

    n = len(values)
    dp = [0] * (capacity + 1)
    for i in range(n):
        w = weights[i]
        v = values[i]
        if w < 0:
            raise ValueError("weights must be non-negative")
        for cap in range(capacity, w - 1, -1):
            dp[cap] = max(dp[cap], dp[cap - w] + v)
    return dp[capacity]
