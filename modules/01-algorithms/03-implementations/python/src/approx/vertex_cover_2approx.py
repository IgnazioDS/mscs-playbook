from __future__ import annotations

"""2-approximation for unweighted vertex cover.

Problem:
    Choose a set of vertices that covers all edges with at most 2x optimal size.

Inputs/Outputs:
    num_vertices: number of vertices (0..n-1)
    edges: list of (u, v)
    -> set of vertices forming a cover

Complexity:
    Time O(E^2) in the worst case due to repeated filtering, space O(E).

Typical use cases:
    Fast approximate solutions for NP-hard covering problems.
"""

from typing import List, Set, Tuple

Edge = Tuple[int, int]


def vertex_cover_2approx(num_vertices: int, edges: List[Edge]) -> Set[int]:
    """Return a 2-approximate vertex cover for an unweighted graph.

    Args:
        num_vertices: Number of vertices labeled 0..n-1.
        edges: List of undirected edges.

    Returns:
        A set of vertices that covers all edges.

    Raises:
        ValueError: If num_vertices is negative or edges include invalid vertices.

    Notes:
        Picking both endpoints of an arbitrary edge constructs a maximal matching,
        which yields a 2-approximation for vertex cover.
    """
    if num_vertices < 0:
        raise ValueError("num_vertices must be non-negative")

    remaining = set()
    for u, v in edges:
        if u < 0 or v < 0 or u >= num_vertices or v >= num_vertices:
            raise ValueError("edge contains invalid vertex")
        if u != v:
            remaining.add((min(u, v), max(u, v)))

    cover: Set[int] = set()
    while remaining:
        # Take any edge and add both endpoints to the cover.
        u, v = next(iter(remaining))
        cover.add(u)
        cover.add(v)
        # Remove all edges incident to u or v since they are now covered.
        remaining = {e for e in remaining if u not in e and v not in e}

    return cover
