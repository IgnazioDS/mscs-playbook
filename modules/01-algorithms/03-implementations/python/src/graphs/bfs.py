from __future__ import annotations

from collections import deque
from typing import Dict, Hashable, Iterable, List


def bfs_distances(graph: Dict[Hashable, Iterable[Hashable]], start: Hashable) -> Dict[Hashable, int]:
    """Return shortest path distances in an unweighted graph."""
    distances: Dict[Hashable, int] = {start: 0}
    queue: deque[Hashable] = deque([start])

    while queue:
        node = queue.popleft()
        for neighbor in graph.get(node, []):
            if neighbor not in distances:
                distances[neighbor] = distances[node] + 1
                queue.append(neighbor)

    return distances


def bfs_order(graph: Dict[Hashable, Iterable[Hashable]], start: Hashable) -> List[Hashable]:
    """Return nodes in BFS visitation order."""
    distances = bfs_distances(graph, start)
    return list(distances.keys())
