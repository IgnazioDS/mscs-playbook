from __future__ import annotations

"""Disjoint Set Union (Union-Find) data structure.

Problem:
    Maintain a partition of elements into disjoint sets with fast union/find.

Inputs/Outputs:
    Elements are indexed 0..n-1.
    find(x) -> representative, union(a, b) -> bool merged?

Complexity:
    Amortized near O(1) per operation (inverse Ackermann).

Typical use cases:
    Connectivity queries, Kruskal's MST, clustering.
"""

from typing import List


class UnionFind:
    """Disjoint set union with path compression and union by rank.

    Invariant:
        parent[x] points to the parent of x; roots are their own parent.
    """

    def __init__(self, size: int) -> None:
        """Initialize size disjoint singleton sets.

        Args:
            size: Number of elements (0..size-1).
        """
        if size < 0:
            raise ValueError("size must be non-negative")
        self.parent: List[int] = list(range(size))
        self.rank: List[int] = [0] * size

    def find(self, x: int) -> int:
        """Return the representative for x with path compression."""
        if self.parent[x] != x:
            # Path compression flattens the tree for faster future queries.
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: int, b: int) -> bool:
        """Union the sets of a and b. Returns True if a merge occurred."""
        root_a = self.find(a)
        root_b = self.find(b)
        if root_a == root_b:
            return False
        # Union by rank keeps trees shallow.
        if self.rank[root_a] < self.rank[root_b]:
            root_a, root_b = root_b, root_a
        self.parent[root_b] = root_a
        if self.rank[root_a] == self.rank[root_b]:
            self.rank[root_a] += 1
        return True

    def connected(self, a: int, b: int) -> bool:
        """Return True if a and b are in the same set."""
        return self.find(a) == self.find(b)
