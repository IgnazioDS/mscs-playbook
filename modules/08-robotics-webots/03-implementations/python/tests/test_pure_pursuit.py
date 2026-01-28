from src.robotics.control.pure_pursuit import PurePursuitController
from src.robotics.math2d import Pose2D


def test_pure_pursuit_straight_path():
    controller = PurePursuitController(lookahead_dist=1.0, wheel_base=0.5, v_desired=1.0)
    path = [(0.0, 0.0), (5.0, 0.0)]
    v, omega, _ = controller.compute_control(Pose2D(0, 0, 0), path)
    assert abs(omega) < 1e-6
    assert v == 1.0


def test_pure_pursuit_curve():
    controller = PurePursuitController(lookahead_dist=1.0, wheel_base=0.5, v_desired=1.0)
    path = [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)]
    v, omega, _ = controller.compute_control(Pose2D(0, 0, 0), path)
    assert v == 1.0
    assert abs(omega) > 0.0
