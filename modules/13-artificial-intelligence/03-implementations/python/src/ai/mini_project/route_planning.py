from __future__ import annotations

from dataclasses import dataclass
import math
from pathlib import Path
from typing import Iterable

import numpy as np

from ..search.astar import astar
from ..search.problems import Problem
from .reporting import write_markdown_report


@dataclass(frozen=True)
class RouteResult:
    seed: int
    size: int
    density: float
    path_len: int
    cost: float
    expansions: int
    first_steps: list[tuple[int, int]]


def _generate_grid(size: int, density: float, seed: int) -> list[str]:
    rng = np.random.RandomState(seed)
    grid = rng.rand(size, size) < density
    grid[0, 0] = False
    grid[size - 1, size - 1] = False
    return ["".join("#" if cell else "." for cell in row) for row in grid]


class GridProblem(Problem):
    def __init__(self, grid: list[str]) -> None:
        self.grid = grid
        self.size = len(grid)
        self._start = (0, 0)
        self._goal = (self.size - 1, self.size - 1)

    def start_state(self):
        return self._start

    def is_goal(self, state):
        return state == self._goal

    def neighbors(self, state):
        for dy, dx in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            ny, nx = state[0] + dy, state[1] + dx
            if 0 <= ny < self.size and 0 <= nx < self.size:
                if self.grid[ny][nx] != "#":
                    yield (ny, nx), 1.0

    def heuristic(self, state):
        return abs(state[0] - self._goal[0]) + abs(state[1] - self._goal[1])


def run_route_planning(seed: int = 42, size: int = 10, density: float = 0.18, out: str | None = None) -> str:
    grid = _generate_grid(size, density, seed)
    problem = GridProblem(grid)
    path, cost, expansions = astar(problem)

    if not path:
        path_len = -1
        cost_val = "inf"
        first_steps: list[tuple[int, int]] = []
    else:
        path_len = len(path) - 1
        cost_val = f"{cost:.3f}"
        first_steps = path[:5]

    output_lines = [
        "task: route-plan",
        f"seed: {seed}",
        f"size: {size}",
        f"density: {density:.3f}",
        f"path_len: {path_len}",
        f"cost: {cost_val}",
        f"expansions: {expansions}",
        f"first_steps: {first_steps}",
    ]
    output = "\n".join(output_lines)

    if out:
        sections = [
            ("Inputs", f"seed: {seed}\nsize: {size}\ndensity: {density}"),
            ("Outputs", "\n".join(output_lines[4:])),
        ]
        write_markdown_report(out, "Route Planning Report", sections, notes="A* on a random grid.")

    return output
