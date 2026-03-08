"""Intent: encapsulate requests as objects with execute/undo.
When to use: queueable operations or reversible actions.
Pitfalls: missing undo logic or shared mutable state.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class Command(Protocol):
    def execute(self) -> None:
        ...

    def undo(self) -> None:
        ...


@dataclass
class Counter:
    value: int = 0


@dataclass
class IncrementCommand:
    counter: Counter
    amount: int = 1

    def execute(self) -> None:
        self.counter.value += self.amount

    def undo(self) -> None:
        self.counter.value -= self.amount
