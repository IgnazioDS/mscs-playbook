from __future__ import annotations

from typing import List, Tuple

from src.data_structures.union_find import UnionFind

Edge = Tuple[int, int, int]


def kruskal_mst(num_vertices: int, edges: List[Edge]) -> Tuple[int, List[Edge]]:
    """Return total weight and edges for a minimum spanning tree."""
    if num_vertices < 0:
        raise ValueError("num_vertices must be non-negative")

    uf = UnionFind(num_vertices)
    mst: List[Edge] = []
    total_weight = 0

    for u, v, w in sorted(edges, key=lambda e: e[2]):
        if u < 0 or v < 0 or u >= num_vertices or v >= num_vertices:
            raise ValueError("edge contains invalid vertex")
        if uf.union(u, v):
            mst.append((u, v, w))
            total_weight += w
            if len(mst) == num_vertices - 1:
                break

    return total_weight, mst
