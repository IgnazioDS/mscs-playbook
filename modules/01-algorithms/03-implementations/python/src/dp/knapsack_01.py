from __future__ import annotations

"""0/1 knapsack via dynamic programming.

Problem:
    Select a subset of items (each at most once) that maximizes total value
    without exceeding the capacity.

Inputs/Outputs:
    values: list of item values (ints)
    weights: list of item weights (ints)
    capacity: max total weight (int)
    -> maximum achievable value (int)

Complexity:
    Time O(n * capacity), space O(capacity) using a 1D DP array.

Typical use cases:
    Budgeted selection, packing, or resource allocation with discrete items.
"""

from typing import List


def knapsack_01(values: List[int], weights: List[int], capacity: int) -> int:
    """Return the maximum value for 0/1 knapsack.

    Args:
        values: Item values, aligned by index with weights.
        weights: Item weights, aligned by index with values.
        capacity: Maximum total weight allowed.

    Returns:
        The maximum total value achievable without exceeding capacity.

    Raises:
        ValueError: If capacity is negative or inputs are inconsistent.

    Invariant:
        dp[cap] is the best value achievable using items processed so far
        with total weight <= cap.
    """
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
        # Iterate capacity descending to avoid reusing the same item twice.
        for cap in range(capacity, w - 1, -1):
            dp[cap] = max(dp[cap], dp[cap - w] + v)
    return dp[capacity]
