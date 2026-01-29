from __future__ import annotations

from collections import deque
from typing import Any

from .problems import Problem


def bfs(problem: Problem) -> tuple[list[Any], int]:
    start = problem.start_state()
    if problem.is_goal(start):
        return [start], 0
    queue = deque([start])
    parents: dict[Any, Any] = {start: None}
    expansions = 0

    while queue:
        state = queue.popleft()
        expansions += 1
        for neighbor, _ in problem.neighbors(state):
            if neighbor in parents:
                continue
            parents[neighbor] = state
            if problem.is_goal(neighbor):
                return _reconstruct(parents, neighbor), expansions
            queue.append(neighbor)

    return [], expansions


def _reconstruct(parents: dict[Any, Any], goal: Any) -> list[Any]:
    path = [goal]
    current = goal
    while parents[current] is not None:
        current = parents[current]
        path.append(current)
    path.reverse()
    return path
