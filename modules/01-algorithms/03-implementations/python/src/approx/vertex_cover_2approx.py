from __future__ import annotations

from typing import List, Set, Tuple

Edge = Tuple[int, int]


def vertex_cover_2approx(num_vertices: int, edges: List[Edge]) -> Set[int]:
    """Return a 2-approximate vertex cover for an unweighted graph."""
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
        u, v = next(iter(remaining))
        cover.add(u)
        cover.add(v)
        remaining = {e for e in remaining if u not in e and v not in e}

    return cover
