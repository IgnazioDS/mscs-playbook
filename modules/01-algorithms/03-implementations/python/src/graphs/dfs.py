from __future__ import annotations

"""Depth-first search (DFS) traversal for graphs.

Problem:
    Visit nodes reachable from a start node using depth-first order.

Inputs/Outputs:
    graph: dict[node, iterable[neighbor]], start: node -> list[node] order

Complexity:
    Time O(V + E), space O(V) for stack and visited set.

Typical use cases:
    Reachability, cycle detection, and topological ordering (in DAGs).
"""

from typing import Dict, Hashable, Iterable, List


def dfs_order(graph: Dict[Hashable, Iterable[Hashable]], start: Hashable) -> List[Hashable]:
    """Return nodes in DFS visitation order (iterative).

    Args:
        graph: Adjacency list mapping nodes to neighbors.
        start: Start node.

    Returns:
        DFS visitation order from the start node.
    """
    visited = set()
    order: List[Hashable] = []
    stack = [start]

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        neighbors = list(graph.get(node, []))
        # Reverse to preserve the input neighbor order in the traversal.
        stack.extend(reversed(neighbors))

    return order
