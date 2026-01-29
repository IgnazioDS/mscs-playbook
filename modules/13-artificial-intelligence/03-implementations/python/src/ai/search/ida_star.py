from __future__ import annotations

from typing import Any

from .problems import Problem


def ida_star(problem: Problem, max_iterations: int = 1000) -> tuple[list[Any], float, int]:
    start = problem.start_state()
    bound = problem.heuristic(start)
    expansions = 0

    def search(path: list[Any], g: float, bound_val: float) -> tuple[float, bool]:
        nonlocal expansions
        state = path[-1]
        f = g + problem.heuristic(state)
        if f > bound_val:
            return f, False
        expansions += 1
        if problem.is_goal(state):
            return g, True
        min_bound = float("inf")
        for neighbor, step in problem.neighbors(state):
            if neighbor in path:
                continue
            path.append(neighbor)
            t, found = search(path, g + step, bound_val)
            if found:
                return t, True
            if t < min_bound:
                min_bound = t
            path.pop()
        return min_bound, False

    path = [start]
    for _ in range(max_iterations):
        t, found = search(path, 0.0, bound)
        if found:
            return path.copy(), t, expansions
        if t == float("inf"):
            break
        bound = t

    return [], float("inf"), expansions
