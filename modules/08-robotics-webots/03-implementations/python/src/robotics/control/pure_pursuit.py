"""Pure pursuit controller for path tracking."""

from __future__ import annotations

import math
from typing import List, Tuple

from src.robotics.math2d import Pose2D, normalize_angle


class PurePursuitController:
    def __init__(self, lookahead_dist: float, wheel_base: float, v_desired: float) -> None:
        self.lookahead = lookahead_dist
        self.wheel_base = wheel_base
        self.v_desired = v_desired

    def compute_control(
        self,
        pose: Pose2D,
        path: List[Tuple[float, float]],
        idx_hint: int = 0,
    ) -> Tuple[float, float, int]:
        if not path:
            return 0.0, 0.0, idx_hint

        idx = min(idx_hint, len(path) - 1)
        while idx < len(path) - 1:
            dx = path[idx][0] - pose.x
            dy = path[idx][1] - pose.y
            if math.hypot(dx, dy) >= self.lookahead:
                break
            idx += 1

        target = path[idx]
        angle_to_target = math.atan2(target[1] - pose.y, target[0] - pose.x)
        alpha = normalize_angle(angle_to_target - pose.theta)
        if self.lookahead <= 0:
            return 0.0, 0.0, idx
        omega = 2.0 * self.v_desired * math.sin(alpha) / self.lookahead
        return self.v_desired, omega, idx
