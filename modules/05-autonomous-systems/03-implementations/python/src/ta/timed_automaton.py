"""Simplified timed automaton model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple

Constraint = Tuple[str, str, float]


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    guard: List[Constraint]
    resets: List[str]


def _eval_constraint(value: float, op: str, bound: float) -> bool:
    if op == "<=":
        return value <= bound
    if op == "<":
        return value < bound
    if op == ">=":
        return value >= bound
    if op == ">":
        return value > bound
    raise ValueError(f"Unsupported operator: {op}")


def constraints_hold(constraints: Iterable[Constraint], clocks: Dict[str, float]) -> bool:
    for clock, op, bound in constraints:
        if clock not in clocks:
            raise KeyError(f"Unknown clock: {clock}")
        if not _eval_constraint(clocks[clock], op, bound):
            return False
    return True


class TimedAutomaton:
    def __init__(
        self,
        locations: Iterable[str],
        initial_location: str,
        clocks: Iterable[str],
        invariants: Dict[str, List[Constraint]] | None = None,
        edges: List[Edge] | None = None,
    ) -> None:
        self.locations = set(locations)
        if initial_location not in self.locations:
            raise ValueError("initial_location must be in locations")
        self.initial_location = initial_location
        self.clocks = list(clocks)
        self.invariants = invariants or {}
        self.edges = edges or []

    def enabled_edges(self, location: str, clocks: Dict[str, float]) -> List[Edge]:
        enabled: List[Edge] = []
        for edge in self.edges:
            if edge.source != location:
                continue
            if constraints_hold(edge.guard, clocks):
                enabled.append(edge)
        return enabled
