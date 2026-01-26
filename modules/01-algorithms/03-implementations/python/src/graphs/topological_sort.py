from __future__ import annotations

from collections import deque
from typing import Dict, Hashable, Iterable, List


def topological_sort(graph: Dict[Hashable, Iterable[Hashable]]) -> List[Hashable]:
    """Return a topological ordering of a DAG, or raise on cycles."""
    indegree: Dict[Hashable, int] = {}
    for node in graph:
        indegree.setdefault(node, 0)
        for neighbor in graph[node]:
            indegree[neighbor] = indegree.get(neighbor, 0) + 1

    queue = deque([n for n, deg in indegree.items() if deg == 0])
    order: List[Hashable] = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph.get(node, []):
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    if len(order) != len(indegree):
        raise ValueError("graph has a cycle")

    return order
