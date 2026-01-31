from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable


@dataclass
class MDP:
    states: list[str]
    actions: dict[str, list[str]]
    transitions: dict[tuple[str, str, str], float]
    rewards: dict[tuple[str, str, str], float]
    gamma: float = 0.9

    def next_states(self, state: str, action: str) -> list[str]:
        return [s2 for (s, a, s2), p in self.transitions.items() if s == state and a == action and p > 0]

    def transition_prob(self, state: str, action: str, next_state: str) -> float:
        return self.transitions.get((state, action, next_state), 0.0)

    def reward(self, state: str, action: str, next_state: str) -> float:
        return self.rewards.get((state, action, next_state), 0.0)
