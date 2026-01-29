from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable


Constraint = Callable[[str, object, str, object], bool]


@dataclass
class CSP:
    variables: list[str]
    domains: dict[str, list[object]]
    neighbors: dict[str, list[str]]
    constraint: Constraint

    def is_consistent(self, var: str, value: object, assignment: dict[str, object]) -> bool:
        for neighbor in self.neighbors.get(var, []):
            if neighbor in assignment:
                if not self.constraint(var, value, neighbor, assignment[neighbor]):
                    return False
        return True
