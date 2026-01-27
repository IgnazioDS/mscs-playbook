"""Bounded reachability helpers for transition systems."""

from __future__ import annotations

from collections import deque
from typing import Hashable, Iterable, List, Set, Tuple

from src.ts.transition_system import TransitionSystem


def _ordered_successors(successors: Iterable[Hashable]) -> List[Hashable]:
    successors_list = list(successors)
    try:
        return sorted(successors_list)
    except TypeError:
        return successors_list


def bounded_reachable(ts: TransitionSystem, start: Hashable, goal: Hashable, k: int) -> bool:
    """Return True if goal is reachable from start within depth k."""
    return len(bounded_find_path(ts, start, goal, k)) > 0


def bounded_find_path(
    ts: TransitionSystem, start: Hashable, goal: Hashable, k: int
) -> List[Hashable]:
    """Find a path to goal within depth k (inclusive). Returns [] if not found."""
    if k < 0:
        raise ValueError("k must be >= 0")
    if start not in ts.states:
        return []

    queue: deque[Tuple[Hashable, List[Hashable], int]] = deque([(start, [start], 0)])
    visited: Set[Tuple[Hashable, int]] = {(start, 0)}

    while queue:
        node, path, depth = queue.popleft()
        if node == goal:
            return path
        if depth == k:
            continue

        for nxt in _ordered_successors(ts.successors(node)):
            key = (nxt, depth + 1)
            if key in visited:
                continue
            visited.add(key)
            queue.append((nxt, path + [nxt], depth + 1))

    return []
