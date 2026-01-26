from __future__ import annotations

from typing import Dict, Hashable, Iterable, List


def dfs_order(graph: Dict[Hashable, Iterable[Hashable]], start: Hashable) -> List[Hashable]:
    """Return nodes in DFS visitation order (iterative)."""
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
        stack.extend(reversed(neighbors))

    return order
