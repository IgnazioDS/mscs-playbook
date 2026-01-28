"""2D pose and transform utilities."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Tuple

import numpy as np


@dataclass(frozen=True)
class Pose2D:
    x: float
    y: float
    theta: float


def normalize_angle(theta: float) -> float:
    """Normalize angle to [-pi, pi)."""
    return (theta + math.pi) % (2 * math.pi) - math.pi


def rot2(theta: float) -> np.ndarray:
    c = math.cos(theta)
    s = math.sin(theta)
    return np.array([[c, -s], [s, c]], dtype=float)


def transform_point(pose: Pose2D, point: Tuple[float, float]) -> Tuple[float, float]:
    p = np.array([point[0], point[1]], dtype=float)
    t = rot2(pose.theta) @ p + np.array([pose.x, pose.y])
    return float(t[0]), float(t[1])


def inverse_transform_point(pose: Pose2D, point: Tuple[float, float]) -> Tuple[float, float]:
    p = np.array([point[0], point[1]], dtype=float)
    t = rot2(pose.theta).T @ (p - np.array([pose.x, pose.y]))
    return float(t[0]), float(t[1])
