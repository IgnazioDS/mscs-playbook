from __future__ import annotations

from typing import Any

from .problems import Problem


def dfs(problem: Problem, limit: int | None = None) -> tuple[list[Any], int]:
    start = problem.start_state()
    stack: list[tuple[Any, int]] = [(start, 0)]
    parents: dict[Any, Any] = {start: None}
    expansions = 0

    while stack:
        state, depth = stack.pop()
        expansions += 1
        if problem.is_goal(state):
            return _reconstruct(parents, state), expansions
        if limit is not None and depth >= limit:
            continue
        for neighbor, _ in reversed(list(problem.neighbors(state))):
            if neighbor in parents:
                continue
            parents[neighbor] = state
            stack.append((neighbor, depth + 1))

    return [], expansions


def _reconstruct(parents: dict[Any, Any], goal: Any) -> list[Any]:
    path = [goal]
    current = goal
    while parents[current] is not None:
        current = parents[current]
        path.append(current)
    path.reverse()
    return path
