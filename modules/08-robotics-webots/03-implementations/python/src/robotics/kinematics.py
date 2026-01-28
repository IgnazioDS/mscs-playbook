"""Differential drive kinematics."""

from __future__ import annotations

import math
from typing import Tuple

from src.robotics.math2d import Pose2D, normalize_angle


def forward_kinematics(v_l: float, v_r: float, wheel_base: float) -> Tuple[float, float]:
    v = 0.5 * (v_r + v_l)
    omega = (v_r - v_l) / wheel_base
    return v, omega


def integrate_pose(pose: Pose2D, v: float, omega: float, dt: float) -> Pose2D:
    if abs(omega) < 1e-6:
        dx = v * math.cos(pose.theta) * dt
        dy = v * math.sin(pose.theta) * dt
        return Pose2D(pose.x + dx, pose.y + dy, pose.theta)

    dtheta = omega * dt
    r = v / omega
    dx = r * (math.sin(pose.theta + dtheta) - math.sin(pose.theta))
    dy = -r * (math.cos(pose.theta + dtheta) - math.cos(pose.theta))
    return Pose2D(pose.x + dx, pose.y + dy, normalize_angle(pose.theta + dtheta))
