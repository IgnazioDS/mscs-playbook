"""Grid-based A* path planning."""

from __future__ import annotations

import heapq
from typing import Dict, List, Optional, Tuple

import numpy as np


def _heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(
    grid: np.ndarray,
    start: Tuple[int, int],
    goal: Tuple[int, int],
    allow_diag: bool = False,
) -> List[Tuple[int, int]]:
    if grid[start[1], start[0]]:
        return []
    if grid[goal[1], goal[0]]:
        return []

    neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    if allow_diag:
        neighbors += [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    open_set: List[Tuple[float, Tuple[int, int]]] = []
    heapq.heappush(open_set, (0.0, start))
    came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
    g_score: Dict[Tuple[int, int], float] = {start: 0.0}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            return _reconstruct_path(came_from, current)

        for dx, dy in neighbors:
            nx, ny = current[0] + dx, current[1] + dy
            if nx < 0 or ny < 0 or nx >= grid.shape[1] or ny >= grid.shape[0]:
                continue
            if grid[ny, nx]:
                continue
            tentative = g_score[current] + 1
            neighbor = (nx, ny)
            if tentative < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative
                f_score = tentative + _heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score, neighbor))

    return []


def _reconstruct_path(came_from: Dict[Tuple[int, int], Tuple[int, int]], current: Tuple[int, int]) -> List[Tuple[int, int]]:
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path
