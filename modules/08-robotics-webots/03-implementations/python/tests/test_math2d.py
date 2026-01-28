import math

import numpy as np

from src.robotics.math2d import Pose2D, inverse_transform_point, normalize_angle, rot2, transform_point


def test_normalize_angle_edges():
    assert math.isclose(normalize_angle(math.pi), -math.pi)
    assert math.isclose(normalize_angle(-math.pi), -math.pi)
    assert math.isclose(normalize_angle(0.0), 0.0)


def test_transform_inverse_roundtrip():
    pose = Pose2D(1.0, 2.0, math.pi / 4)
    point = (3.0, -1.0)
    world = transform_point(pose, point)
    local = inverse_transform_point(pose, world)
    assert np.allclose(local, point, atol=1e-6)
