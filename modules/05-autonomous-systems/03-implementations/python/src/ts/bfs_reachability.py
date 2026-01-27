"""Deterministic BFS reachability for transition systems."""

from __future__ import annotations

from collections import deque
from typing import Dict, Hashable, Iterable, List, Tuple

from src.ts.transition_system import TransitionSystem


def _ordered_successors(successors: Iterable[Hashable]) -> List[Hashable]:
    """Return successors in deterministic order when possible.

    If elements are not comparable, falls back to the container iteration order,
    which may be non-deterministic for sets.
    """
    successors_list = list(successors)
    try:
        return sorted(successors_list)
    except TypeError:
        return successors_list


def bfs_reachable(
    ts: TransitionSystem, start: Hashable, goal: Hashable
) -> Tuple[bool, Dict[Hashable, Hashable | None]]:
    """Breadth-first search with a parent map."""
    if start not in ts.states:
        return False, {}

    parent: Dict[Hashable, Hashable | None] = {start: None}
    queue: deque[Hashable] = deque([start])

    while queue:
        current = queue.popleft()
        if current == goal:
            return True, parent
        for nxt in _ordered_successors(ts.successors(current)):
            if nxt not in parent:
                parent[nxt] = current
                queue.append(nxt)

    return False, parent


def reconstruct_path(
    parent: Dict[Hashable, Hashable | None], start: Hashable, goal: Hashable
) -> List[Hashable]:
    """Reconstruct a path from start to goal using a parent map."""
    if goal not in parent:
        return []

    path: List[Hashable] = []
    node: Hashable | None = goal
    while node is not None:
        path.append(node)
        node = parent.get(node)

    path.reverse()
    if not path or path[0] != start:
        return []
    return path
