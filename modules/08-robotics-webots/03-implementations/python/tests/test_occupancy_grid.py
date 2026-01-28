import numpy as np

from src.robotics.math2d import Pose2D
from src.robotics.mapping.occupancy_grid import OccupancyGrid


def test_update_ray_marks_free_and_occ():
    grid = OccupancyGrid(width=10, height=10, resolution=1.0, origin=Pose2D(0, 0, 0))
    grid.update_ray(Pose2D(1, 1, 0), (5, 1), free_logodds=-1.0, occ_logodds=2.0)
    probs = grid.probabilities()

    free_cell = grid.world_to_grid(2, 1)
    occ_cell = grid.world_to_grid(5, 1)
    assert free_cell is not None and occ_cell is not None
    fx, fy = free_cell
    ox, oy = occ_cell
    assert probs[fy, fx] < 0.5
    assert probs[oy, ox] > 0.5


def test_update_ray_out_of_bounds_safe():
    grid = OccupancyGrid(width=5, height=5, resolution=1.0, origin=Pose2D(0, 0, 0))
    grid.update_ray(Pose2D(0, 0, 0), (100, 100), free_logodds=-1.0, occ_logodds=2.0)
    assert isinstance(grid.probabilities(), np.ndarray)
