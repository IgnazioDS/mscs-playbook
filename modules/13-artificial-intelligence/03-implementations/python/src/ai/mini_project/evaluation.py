from __future__ import annotations

from typing import Callable

from .route_planning import run_route_planning
from .scheduling import run_schedule
from .diagnosis import run_diagnosis


def run_evaluate() -> tuple[bool, str]:
    scenarios: list[tuple[str, Callable[[], str], list[str]]] = [
        ("route", lambda: run_route_planning(seed=42, size=10, density=0.18), ["route-plan", "path_len", "cost"]),
        ("schedule", lambda: run_schedule(seed=42), ["schedule", "solved", "assignments"]),
        ("diagnose", lambda: run_diagnosis(seed=42), ["diagnose", "P(Rain=1)", "P(Sprinkler=1)"])
    ]
    failures: list[str] = []
    for name, fn, expected in scenarios:
        output = fn()
        missing = [token for token in expected if token not in output]
        if missing:
            failures.append(f"{name}: missing {missing}")

    passed = len(failures) == 0
    summary_lines = [
        "task: evaluate",
        f"scenarios: {len(scenarios)}",
        f"passed: {len(scenarios) - len(failures)}",
        f"failed: {len(failures)}",
    ]
    if failures:
        summary_lines.append("failures:")
        summary_lines.extend(f"- {failure}" for failure in failures)
    report = "\n".join(summary_lines)
    return passed, report
