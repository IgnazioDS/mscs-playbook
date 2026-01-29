from __future__ import annotations

from typing import Iterable

from src.ai.search.bfs import bfs
from src.ai.search.dfs import dfs
from src.ai.search.ucs import ucs
from src.ai.search.astar import astar
from src.ai.search.ida_star import ida_star
from src.ai.search.problems import Problem


class GridProblem:
    def __init__(self, grid, start, goal):
        self.grid = grid
        self._start = start
        self._goal = goal

    def start_state(self):
        return self._start

    def is_goal(self, state):
        return state == self._goal

    def neighbors(self, state):
        moves = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        for dy, dx in moves:
            ny, nx = state[0] + dy, state[1] + dx
            if 0 <= ny < len(self.grid) and 0 <= nx < len(self.grid[0]):
                if self.grid[ny][nx] != "#":
                    yield (ny, nx), 1.0

    def heuristic(self, state):
        return abs(state[0] - self._goal[0]) + abs(state[1] - self._goal[1])


def test_search_algorithms_on_grid():
    grid = [
        "....",
        ".##.",
        "....",
        "..#.",
    ]
    problem = GridProblem(grid, (0, 0), (3, 3))

    bfs_path, bfs_exp = bfs(problem)
    dfs_path, dfs_exp = dfs(problem, limit=20)
    ucs_path, ucs_cost, ucs_exp = ucs(problem)
    astar_path, astar_cost, astar_exp = astar(problem)
    ida_path, ida_cost, ida_exp = ida_star(problem)

    assert len(bfs_path) - 1 == 6
    assert bfs_path[0] == (0, 0)
    assert bfs_path[-1] == (3, 3)
    assert dfs_path[0] == (0, 0)
    assert dfs_path[-1] == (3, 3)
    assert ucs_cost == 6
    assert astar_cost == 6
    assert ida_cost == 6
    assert astar_exp <= ucs_exp


def test_weighted_graph_ucs_astar():
    class WeightedProblem:
        def start_state(self):
            return "A"

        def is_goal(self, state):
            return state == "D"

        def neighbors(self, state):
            graph = {
                "A": [("B", 1), ("C", 5)],
                "B": [("C", 1), ("D", 5)],
                "C": [("D", 1)],
                "D": [],
            }
            return graph[state]

        def heuristic(self, state):
            return {"A": 3, "B": 2, "C": 1, "D": 0}[state]

    problem = WeightedProblem()
    path, cost, _ = ucs(problem)
    path_a, cost_a, _ = astar(problem)
    assert cost == 3
    assert cost_a == 3
    assert path[0] == "A" and path[-1] == "D"
    assert path_a[0] == "A" and path_a[-1] == "D"
