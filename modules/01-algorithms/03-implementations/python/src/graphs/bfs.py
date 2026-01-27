from __future__ import annotations

"""Breadth-first search (BFS) for unweighted graphs.

Problem:
    Compute shortest-path distances from a start node in an unweighted graph,
    or return the BFS visitation order.

Inputs/Outputs:
    graph: dict[node, iterable[neighbor]]
    start: node
    -> dict[node, int] distances or list[node] order

Complexity:
    Time O(V + E), space O(V) for queue and visited map.

Typical use cases:
    Shortest paths in unweighted graphs, reachability, and level traversal.
"""

from collections import deque
from typing import Dict, Hashable, Iterable, List


def bfs_distances(graph: Dict[Hashable, Iterable[Hashable]], start: Hashable) -> Dict[Hashable, int]:
    """Return shortest path distances in an unweighted graph.

    Args:
        graph: Adjacency list mapping nodes to neighbors.
        start: Start node.

    Returns:
        Distances from start to each reachable node (0 for start).
    """
    distances: Dict[Hashable, int] = {start: 0}
    queue: deque[Hashable] = deque([start])

    while queue:
        node = queue.popleft()
        for neighbor in graph.get(node, []):
            if neighbor not in distances:
                # First time discovered => shortest path in unweighted graphs.
                distances[neighbor] = distances[node] + 1
                queue.append(neighbor)

    return distances


def bfs_order(graph: Dict[Hashable, Iterable[Hashable]], start: Hashable) -> List[Hashable]:
    """Return nodes in BFS visitation order.

    Notes:
        Order depends on adjacency iteration order.
    """
    distances = bfs_distances(graph, start)
    return list(distances.keys())
