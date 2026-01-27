from __future__ import annotations

"""Topological sorting of a directed acyclic graph (DAG).

Problem:
    Produce a linear ordering of nodes such that for every edge u -> v,
    u appears before v.

Inputs/Outputs:
    graph: dict[node, iterable[neighbor]] -> list[node] order

Complexity:
    Time O(V + E), space O(V).

Typical use cases:
    Build systems, dependency resolution, and scheduling.
"""

from collections import deque
from typing import Dict, Hashable, Iterable, List


def topological_sort(graph: Dict[Hashable, Iterable[Hashable]]) -> List[Hashable]:
    """Return a topological ordering of a DAG, or raise on cycles.

    Args:
        graph: Adjacency list of a directed graph.

    Returns:
        A list of nodes in topological order.

    Raises:
        ValueError: If the graph contains a cycle.
    """
    indegree: Dict[Hashable, int] = {}
    for node in graph:
        indegree.setdefault(node, 0)
        for neighbor in graph[node]:
            indegree[neighbor] = indegree.get(neighbor, 0) + 1

    # Start with all nodes that have no incoming edges.
    queue = deque([n for n, deg in indegree.items() if deg == 0])
    order: List[Hashable] = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph.get(node, []):
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    # If not all nodes were processed, a cycle exists.
    if len(order) != len(indegree):
        raise ValueError("graph has a cycle")

    return order
