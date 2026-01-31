from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from src.ai.mini_project.route_planning import run_route_planning
from src.ai.mini_project.scheduling import run_schedule
from src.ai.mini_project.diagnosis import run_diagnosis
from src.ai.mini_project.evaluation import run_evaluate


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[5]


def _run_cli(args: list[str]) -> str:
    repo_root = _repo_root()
    cli_path = repo_root / "modules/13-artificial-intelligence/03-implementations/python/src/ai13/mini_project/cli.py"
    result = subprocess.run(
        [sys.executable, str(cli_path), *args],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip().replace("\r\n", "\n")


def test_cli_route_plan_matches_library():
    expected = run_route_planning(seed=7, size=6, density=0.1)
    output = _run_cli(["route-plan", "--seed", "7", "--size", "6", "--density", "0.1"])
    assert output == expected


def test_cli_schedule_matches_library():
    expected = run_schedule(seed=11)
    output = _run_cli(["schedule", "--seed", "11"])
    assert output == expected


def test_cli_diagnose_matches_library():
    expected = run_diagnosis(seed=5)
    output = _run_cli(["diagnose", "--seed", "5"])
    assert output == expected


def test_cli_evaluate_summary():
    _, report = run_evaluate()
    output = _run_cli(["evaluate", "--seed", "42"])
    assert output == f"seed: 42\n{report}"
