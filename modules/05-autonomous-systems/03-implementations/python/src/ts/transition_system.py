"""Minimal transition system model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Set, Hashable


@dataclass
class TransitionSystem:
    states: Set[Hashable] = field(default_factory=set)
    initial: Hashable | None = None
    transitions: Dict[Hashable, Set[Hashable]] = field(default_factory=dict)

    def add_state(self, state: Hashable) -> None:
        self.states.add(state)
        self.transitions.setdefault(state, set())
        if self.initial is None:
            self.initial = state

    def add_transition(self, source: Hashable, target: Hashable) -> None:
        self.add_state(source)
        self.add_state(target)
        self.transitions[source].add(target)

    def successors(self, state: Hashable) -> Set[Hashable]:
        if state not in self.transitions:
            return set()
        return set(self.transitions[state])
