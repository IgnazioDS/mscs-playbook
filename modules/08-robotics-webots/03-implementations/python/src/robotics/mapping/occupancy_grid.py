"""Occupancy grid mapping with log-odds."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Tuple

import numpy as np

from src.robotics.math2d import Pose2D


@dataclass
class OccupancyGrid:
    width: int
    height: int
    resolution: float
    origin: Pose2D

    def __post_init__(self) -> None:
        self.logodds = np.zeros((self.height, self.width), dtype=float)

    def world_to_grid(self, x: float, y: float) -> Tuple[int, int] | None:
        gx = int((x - self.origin.x) / self.resolution)
        gy = int((y - self.origin.y) / self.resolution)
        if 0 <= gx < self.width and 0 <= gy < self.height:
            return gx, gy
        return None

    def update_ray(
        self,
        sensor_pose: Pose2D,
        endpoint_world: Tuple[float, float],
        free_logodds: float,
        occ_logodds: float,
    ) -> None:
        sx, sy = sensor_pose.x, sensor_pose.y
        ex, ey = endpoint_world
        dx = ex - sx
        dy = ey - sy
        dist = math.hypot(dx, dy)
        if dist == 0:
            return
        steps = int(dist / self.resolution)
        for i in range(steps):
            t = i / max(steps, 1)
            x = sx + dx * t
            y = sy + dy * t
            idx = self.world_to_grid(x, y)
            if idx is None:
                continue
            gx, gy = idx
            self.logodds[gy, gx] += free_logodds
        end_idx = self.world_to_grid(ex, ey)
        if end_idx is not None:
            gx, gy = end_idx
            self.logodds[gy, gx] += occ_logodds

    def probabilities(self) -> np.ndarray:
        return 1.0 / (1.0 + np.exp(-self.logodds))
