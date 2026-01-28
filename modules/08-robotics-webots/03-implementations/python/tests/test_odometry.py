import math

from src.robotics.math2d import Pose2D
from src.robotics.odometry import DifferentialDriveOdometry


def test_square_path_approx_closure():
    odo = DifferentialDriveOdometry(wheel_base=0.5)
    pose = Pose2D(0.0, 0.0, 0.0)

    # Four segments: forward, turn, forward, turn, ...
    turn = math.pi * odo.wheel_base / 4.0
    for _ in range(4):
        pose = odo.update(pose, delta_left=1.0, delta_right=1.0)
        pose = odo.update(pose, delta_left=-turn, delta_right=turn)

    assert math.hypot(pose.x, pose.y) < 0.5
