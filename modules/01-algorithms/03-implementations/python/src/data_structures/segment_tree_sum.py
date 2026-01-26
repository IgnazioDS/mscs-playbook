from __future__ import annotations

from typing import List


class SegmentTreeSum:
    """Segment tree for range sum queries and point updates on [l, r)."""

    def __init__(self, values: List[int]) -> None:
        if not values:
            raise ValueError("values must be non-empty")
        self.n = len(values)
        self.tree = [0] * (2 * self.n)
        for i, v in enumerate(values):
            self.tree[self.n + i] = v
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]

    def update(self, index: int, value: int) -> None:
        if index < 0 or index >= self.n:
            raise IndexError("index out of range")
        pos = self.n + index
        self.tree[pos] = value
        pos //= 2
        while pos >= 1:
            self.tree[pos] = self.tree[2 * pos] + self.tree[2 * pos + 1]
            pos //= 2

    def query(self, left: int, right: int) -> int:
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
