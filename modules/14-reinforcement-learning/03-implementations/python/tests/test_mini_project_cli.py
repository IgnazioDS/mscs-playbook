from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def _run_cli(args: list[str]) -> subprocess.CompletedProcess:
    repo_root = Path(__file__).resolve().parents[6]
    cmd = [sys.executable, str(repo_root / "modules/14-reinforcement-learning/03-implementations/python/src/rl/mini_project/cli.py")]
    cmd.extend(args)
    return subprocess.run(cmd, cwd=repo_root, capture_output=True, text=True, check=False)


def test_cli_gridworld_control():
    result = _run_cli(["gridworld-control", "--episodes", "50", "--seed", "42"])
    assert result.returncode == 0
    assert "task: gridworld-control" in result.stdout
    assert "final_avg_return" in result.stdout


def test_cli_bandit_compare():
    result = _run_cli(["bandit-compare", "--steps", "100", "--seed", "42"])
    assert result.returncode == 0
    assert "task: bandit-compare" in result.stdout
    assert "best_pick_rate" in result.stdout


def test_cli_reward_shaping():
    result = _run_cli(["reward-shaping", "--episodes", "50", "--seed", "42"])
    assert result.returncode == 0
    assert "task: reward-shaping" in result.stdout
    assert "delta" in result.stdout


def test_cli_evaluate():
    result = _run_cli(["evaluate"])
    assert result.returncode == 0
    assert "task: evaluate" in result.stdout
    assert "failed: 0" in result.stdout
