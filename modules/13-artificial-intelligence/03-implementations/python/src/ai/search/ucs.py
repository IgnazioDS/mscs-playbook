from __future__ import annotations

from typing import Any

from ..utils.priority_queue import PriorityQueue
from .problems import Problem


def ucs(problem: Problem) -> tuple[list[Any], float, int]:
    start = problem.start_state()
    frontier = PriorityQueue()
    frontier.push(0.0, start)
    parents: dict[Any, Any] = {start: None}
    costs: dict[Any, float] = {start: 0.0}
    expansions = 0

    while frontier:
        cost, state = frontier.pop()
        if cost > costs.get(state, float("inf")):
            continue
        expansions += 1
        if problem.is_goal(state):
            return _reconstruct(parents, state), cost, expansions
        for neighbor, step in problem.neighbors(state):
            new_cost = cost + step
            if new_cost < costs.get(neighbor, float("inf")):
                costs[neighbor] = new_cost
                parents[neighbor] = state
                frontier.push(new_cost, neighbor)

    return [], float("inf"), expansions


def _reconstruct(parents: dict[Any, Any], goal: Any) -> list[Any]:
    path = [goal]
    current = goal
    while parents[current] is not None:
        current = parents[current]
        path.append(current)
    path.reverse()
    return path
