from __future__ import annotations

from typing import Any

from ..utils.priority_queue import PriorityQueue
from .problems import Problem


def astar(problem: Problem) -> tuple[list[Any], float, int]:
    start = problem.start_state()
    frontier = PriorityQueue()
    frontier.push(problem.heuristic(start), start)
    parents: dict[Any, Any] = {start: None}
    g_scores: dict[Any, float] = {start: 0.0}
    expansions = 0

    while frontier:
        _, state = frontier.pop()
        current_g = g_scores.get(state, float("inf"))
        expansions += 1
        if problem.is_goal(state):
            return _reconstruct(parents, state), current_g, expansions
        for neighbor, step in problem.neighbors(state):
            tentative_g = current_g + step
            if tentative_g < g_scores.get(neighbor, float("inf")):
                g_scores[neighbor] = tentative_g
                parents[neighbor] = state
                f = tentative_g + problem.heuristic(neighbor)
                frontier.push(f, neighbor)

    return [], float("inf"), expansions


def _reconstruct(parents: dict[Any, Any], goal: Any) -> list[Any]:
    path = [goal]
    current = goal
    while parents[current] is not None:
        current = parents[current]
        path.append(current)
    path.reverse()
    return path
