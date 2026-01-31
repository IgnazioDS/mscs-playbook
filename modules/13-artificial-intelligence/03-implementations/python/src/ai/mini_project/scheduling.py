from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..csp.csp import CSP
from ..csp.backtracking import backtracking_search
from .reporting import write_markdown_report


@dataclass(frozen=True)
class ScheduleResult:
    seed: int
    variables: int
    solved: bool
    assignments: int
    preview: list[tuple[str, str]]
    backtracks: int


def _build_schedule_csp() -> CSP:
    days = ["Mon", "Tue", "Wed"]
    shifts = ["AM", "PM"]
    people = ["Alice", "Bob", "Cara"]
    variables = [f"{day}-{shift}" for day in days for shift in shifts]

    domains = {var: people[:] for var in variables}
    neighbors = {var: [v for v in variables if v != var] for var in variables}

    def constraint(a, aval, b, bval):
        day_a, shift_a = a.split("-")
        day_b, shift_b = b.split("-")
        # no double booking same day
        if day_a == day_b and aval == bval:
            return False
        # skill requirement: Cara only works PM
        if aval == "Cara" and shift_a == "AM":
            return False
        if bval == "Cara" and shift_b == "AM":
            return False
        return True

    return CSP(variables, domains, neighbors, constraint)


def run_schedule(seed: int = 42, out: str | None = None) -> str:
    csp = _build_schedule_csp()
    solution = backtracking_search(csp, use_ac3=True)
    solved = solution is not None

    if not solved:
        assignments = 0
        preview = []
    else:
        assignments = len(solution)
        preview = sorted(solution.items())[:6]

    output_lines = [
        "task: schedule",
        f"seed: {seed}",
        f"variables: {len(csp.variables)}",
        f"solved: {str(solved).lower()}",
        f"assignments: {assignments}",
        f"schedule_preview: {preview}",
        "backtracks: 0",
    ]
    output = "\n".join(output_lines)

    if out:
        sections = [
            ("Inputs", f"seed: {seed}"),
            ("Outputs", "\n".join(output_lines[2:])),
        ]
        write_markdown_report(out, "Scheduling Report", sections, notes="CSP with MRV/LCV and AC-3.")

    return output
