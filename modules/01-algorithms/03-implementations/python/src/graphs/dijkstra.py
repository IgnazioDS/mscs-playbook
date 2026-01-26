from __future__ import annotations

import heapq
from typing import Dict, Hashable, Iterable, List, Tuple


def dijkstra(graph: Dict[Hashable, Iterable[Tuple[Hashable, int]]], start: Hashable) -> Dict[Hashable, int]:
    """Return shortest path distances for nonnegative weighted graphs."""
    distances: Dict[Hashable, int] = {start: 0}
    heap: List[Tuple[int, Hashable]] = [(0, start)]

    while heap:
        dist, node = heapq.heappop(heap)
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
