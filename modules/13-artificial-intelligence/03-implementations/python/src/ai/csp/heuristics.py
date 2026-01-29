from __future__ import annotations

from typing import Iterable

from .csp import CSP


def mrv(csp: CSP, assignment: dict[str, object]) -> str:
    unassigned = [v for v in csp.variables if v not in assignment]
    return min(unassigned, key=lambda v: len(csp.domains[v]))


def degree_heuristic(csp: CSP, assignment: dict[str, object], variables: Iterable[str]) -> str:
    return max(variables, key=lambda v: len([n for n in csp.neighbors[v] if n not in assignment]))


def lcv(csp: CSP, var: str, assignment: dict[str, object]) -> list[object]:
    def conflicts(value: object) -> int:
        count = 0
        for neighbor in csp.neighbors.get(var, []):
            if neighbor in assignment:
                continue
            for nval in csp.domains[neighbor]:
                if not csp.constraint(var, value, neighbor, nval):
                    count += 1
        return count

    return sorted(csp.domains[var], key=conflicts)
