import numpy as np

from src.robotics.planning.grid_astar import astar


def test_astar_path_length():
    grid = np.array(
        [
            [0, 0, 0, 0],
            [1, 1, 0, 1],
            [0, 0, 0, 0],
            [0, 1, 1, 0],
        ],
        dtype=bool,
    )
    path = astar(grid, start=(0, 0), goal=(3, 3), allow_diag=False)
    assert path[0] == (0, 0)
    assert path[-1] == (3, 3)
    assert len(path) == 7
