from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass
class Gridworld:
    width: int = 4
    height: int = 4
    terminal_states: dict[tuple[int, int], float] | None = None
    step_cost: float = -1.0
    start_state: tuple[int, int] = (0, 0)

    def __post_init__(self) -> None:
        if self.terminal_states is None:
            self.terminal_states = {(0, 0): 0.0, (self.height - 1, self.width - 1): 0.0}
        self._state = self.start_state

    def states(self) -> list[tuple[int, int]]:
        return [(r, c) for r in range(self.height) for c in range(self.width)]

    def actions(self, state: tuple[int, int]) -> list[str]:
        if state in self.terminal_states:
            return []
        return ["U", "D", "L", "R"]

    def step(self, state: tuple[int, int], action: str) -> tuple[tuple[int, int], float, bool]:
        if state in self.terminal_states:
            return state, 0.0, True
        r, c = state
        if action == "U":
            r = max(0, r - 1)
        elif action == "D":
            r = min(self.height - 1, r + 1)
        elif action == "L":
            c = max(0, c - 1)
        elif action == "R":
            c = min(self.width - 1, c + 1)
        next_state = (r, c)
        if next_state in self.terminal_states:
            return next_state, float(self.terminal_states[next_state]), True
        return next_state, self.step_cost, False

    def reset(self, seed: int | None = None) -> tuple[int, int]:
        self._state = self.start_state
        return self._state

    def set_state(self, state: tuple[int, int]) -> None:
        self._state = state
