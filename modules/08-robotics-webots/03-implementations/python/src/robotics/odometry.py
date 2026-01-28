"""Wheel odometry for differential drive."""

from __future__ import annotations

from typing import Tuple

from src.robotics.kinematics import forward_kinematics, integrate_pose
from src.robotics.math2d import Pose2D


class DifferentialDriveOdometry:
    def __init__(self, wheel_base: float) -> None:
        self.wheel_base = wheel_base

    def update(self, pose: Pose2D, delta_left: float, delta_right: float) -> Pose2D:
        v, omega = forward_kinematics(delta_left, delta_right, self.wheel_base)
        return integrate_pose(pose, v, omega, dt=1.0)
