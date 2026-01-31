from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ChainEnv:
    length: int = 5
    start: int = 2
    reward_right: float = 1.0
    step_cost: float = 0.0

    def __post_init__(self) -> None:
        self._state = self.start

    def states(self) -> list[int]:
        return list(range(self.length))

    def actions(self, state: int) -> list[str]:
        if state == 0 or state == self.length - 1:
            return []
        return ["L", "R"]

    def step(self, state: int, action: str) -> tuple[int, float, bool]:
        if state == 0 or state == self.length - 1:
            return state, 0.0, True
        next_state = state - 1 if action == "L" else state + 1
        if next_state == self.length - 1:
            return next_state, self.reward_right, True
        if next_state == 0:
            return next_state, 0.0, True
        return next_state, self.step_cost, False

    def reset(self, seed: int | None = None) -> int:
        self._state = self.start
        return self._state

    def set_state(self, state: int) -> None:
        self._state = state
