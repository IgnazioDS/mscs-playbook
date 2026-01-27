from __future__ import annotations

"""Kruskal's algorithm for minimum spanning tree (MST).

Problem:
    Given an undirected weighted graph, find a minimum spanning tree.

Inputs/Outputs:
    num_vertices: number of vertices (0..n-1)
    edges: list of (u, v, weight)
    -> (total_weight, mst_edges)

Complexity:
    Time O(E log E) from sorting edges, space O(V) for union-find.

Typical use cases:
    Network design, clustering, and cable/road cost minimization.
"""

from typing import List, Tuple

from src.data_structures.union_find import UnionFind

Edge = Tuple[int, int, int]


def kruskal_mst(num_vertices: int, edges: List[Edge]) -> Tuple[int, List[Edge]]:
    """Return total weight and edges for a minimum spanning tree.

    Args:
        num_vertices: Number of vertices (assumed labeled 0..n-1).
        edges: List of (u, v, weight) tuples.

    Returns:
        Tuple of total MST weight and list of chosen edges.

    Raises:
        ValueError: If num_vertices is negative or any edge has invalid vertices.
    """
    if num_vertices < 0:
        raise ValueError("num_vertices must be non-negative")

    uf = UnionFind(num_vertices)
    mst: List[Edge] = []
    total_weight = 0

    # Sort edges by weight; greedily add if they do not create a cycle.
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        if u < 0 or v < 0 or u >= num_vertices or v >= num_vertices:
            raise ValueError("edge contains invalid vertex")
        if uf.union(u, v):
            mst.append((u, v, w))
            total_weight += w
            # Early stop when MST has V-1 edges.
            if len(mst) == num_vertices - 1:
                break

    return total_weight, mst
