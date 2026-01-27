from __future__ import annotations

"""Dijkstra's algorithm for shortest paths with nonnegative weights.

Problem:
    Compute shortest-path distances from a start node in a weighted graph
    with nonnegative edge weights.

Inputs/Outputs:
    graph: dict[node, iterable[(neighbor, weight)]], start: node -> distances dict

Complexity:
    Time O((V + E) log V) using a binary heap, space O(V).

Typical use cases:
    Routing, map navigation, and latency-aware path selection.
"""

import heapq
from typing import Dict, Hashable, Iterable, List, Tuple


def dijkstra(graph: Dict[Hashable, Iterable[Tuple[Hashable, int]]], start: Hashable) -> Dict[Hashable, int]:
    """Return shortest path distances for nonnegative weighted graphs.

    Args:
        graph: Adjacency list mapping nodes to (neighbor, weight) edges.
        start: Start node.

    Returns:
        Shortest distances from start to each reachable node.

    Raises:
        ValueError: If a negative edge weight is found.
    """
    distances: Dict[Hashable, int] = {start: 0}
    heap: List[Tuple[int, Hashable]] = [(0, start)]

    while heap:
        dist, node = heapq.heappop(heap)
        # Skip stale entries that are longer than the best known distance.
        if dist != distances.get(node):
            continue
        for neighbor, weight in graph.get(node, []):
            if weight < 0:
                raise ValueError("negative edge weight not allowed")
            new_dist = dist + weight
            if neighbor not in distances or new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))

    return distances
