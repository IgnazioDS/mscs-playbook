from __future__ import annotations

"""Segment tree supporting range-sum queries and point updates.

Problem:
    Maintain an array with fast range sum queries and point updates.

Inputs/Outputs:
    values: initial list of ints
    query(l, r) -> sum on [l, r)
    update(i, v) -> set values[i] = v

Complexity:
    Build O(n), query O(log n), update O(log n), space O(n).

Typical use cases:
    Time-series aggregation, online analytics, and interval queries.
"""

from typing import List


class SegmentTreeSum:
    """Segment tree for range sum queries and point updates on [l, r).

    Invariant:
        tree[1] stores the sum of the full range; each internal node holds the
        sum of its two children.
    """

    def __init__(self, values: List[int]) -> None:
        """Build the segment tree from initial values."""
        if not values:
            raise ValueError("values must be non-empty")
        self.n = len(values)
        self.tree = [0] * (2 * self.n)
        # Place leaves in the second half of the array.
        for i, v in enumerate(values):
            self.tree[self.n + i] = v
        # Build internal nodes bottom-up.
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]

    def update(self, index: int, value: int) -> None:
        """Set values[index] = value and update affected segment sums."""
        if index < 0 or index >= self.n:
            raise IndexError("index out of range")
        pos = self.n + index
        self.tree[pos] = value
        pos //= 2
        # Recompute parent sums along the path to the root.
        while pos >= 1:
            self.tree[pos] = self.tree[2 * pos] + self.tree[2 * pos + 1]
            pos //= 2

    def query(self, left: int, right: int) -> int:
        """Return the sum over [left, right)."""
        if left < 0 or right > self.n or left > right:
            raise ValueError("invalid range")
        res = 0
        l = self.n + left
        r = self.n + right
        while l < r:
            if l % 2 == 1:
                res += self.tree[l]
                l += 1
            if r % 2 == 1:
                r -= 1
                res += self.tree[r]
            l //= 2
            r //= 2
        return res
