"""Webots controller scaffold with headless fallback."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import yaml

# Add robotics core to path
CORE_ROOT = Path(__file__).resolve().parents[2] / "python" / "src"
sys.path.append(str(CORE_ROOT))

from src.robotics.math2d import Pose2D
from src.robotics.odometry import DifferentialDriveOdometry
from src.robotics.mapping.occupancy_grid import OccupancyGrid
from src.robotics.planning.grid_astar import astar


def load_config() -> dict:
    config_path = Path(__file__).resolve().parent / "config.yaml"
    return yaml.safe_load(config_path.read_text())


def run_headless_demo(demo: str) -> None:
    cfg = load_config()
    if demo == "odometry":
        odo = DifferentialDriveOdometry(cfg["wheel_base"])
        pose = Pose2D(0.0, 0.0, 0.0)
        pose = odo.update(pose, 1.0, 1.0)
        pose = odo.update(pose, -0.2, 0.2)
        print(f"odometry pose: {pose}")
    elif demo == "mapping":
        grid = OccupancyGrid(
            width=cfg["map"]["width"],
            height=cfg["map"]["height"],
            resolution=cfg["map"]["resolution"],
            origin=Pose2D(0, 0, 0),
        )
        grid.update_ray(Pose2D(1, 1, 0), (5, 1), -1.0, 2.0)
        probs = grid.probabilities()
        print(f"mapping occ at (5,1): {probs[1,5]:.2f}")
    elif demo == "planning":
        import numpy as np

        grid = np.zeros((5, 5), dtype=bool)
        grid[1, 1:4] = True
        path = astar(grid, (0, 0), (4, 4), allow_diag=cfg["planning"]["allow_diag"])
        print(f"planning path length: {len(path)}")
    else:
        raise ValueError("Unknown demo")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="headless")
    parser.add_argument("--demo", default="odometry")
    args = parser.parse_args()

    try:
        from controller import Robot  # type: ignore
    except Exception:
        if args.mode != "headless":
            raise
        run_headless_demo(args.demo)
        return

    robot = Robot()
    timestep = int(cfg["dt"] * 1000)
    while robot.step(timestep) != -1:
        # Placeholder: would integrate sensors + core here
        pass


if __name__ == "__main__":
    main()
