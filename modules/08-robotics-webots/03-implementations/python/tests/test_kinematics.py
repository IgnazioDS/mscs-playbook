import math

from src.robotics.kinematics import forward_kinematics, integrate_pose
from src.robotics.math2d import Pose2D


def test_forward_kinematics_straight():
    v, omega = forward_kinematics(1.0, 1.0, 0.5)
    assert v == 1.0
    assert omega == 0.0


def test_integrate_pose_straight():
    pose = Pose2D(0.0, 0.0, 0.0)
    new_pose = integrate_pose(pose, v=1.0, omega=0.0, dt=1.0)
    assert math.isclose(new_pose.x, 1.0)
    assert math.isclose(new_pose.y, 0.0)


def test_integrate_pose_rotation():
    pose = Pose2D(0.0, 0.0, 0.0)
    new_pose = integrate_pose(pose, v=0.0, omega=1.0, dt=1.0)
    assert math.isclose(new_pose.theta, 1.0, abs_tol=1e-6)


def test_integrate_pose_small_omega_limit():
    pose = Pose2D(0.0, 0.0, 0.0)
    new_pose = integrate_pose(pose, v=1.0, omega=1e-8, dt=1.0)
    assert math.isclose(new_pose.x, 1.0, abs_tol=1e-6)
