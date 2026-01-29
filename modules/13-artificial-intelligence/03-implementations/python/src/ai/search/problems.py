from __future__ import annotations

from typing import Protocol, Iterable, Tuple, Any


class Problem(Protocol):
    def start_state(self) -> Any:
        ...

    def is_goal(self, state: Any) -> bool:
        ...

    def neighbors(self, state: Any) -> Iterable[Tuple[Any, float]]:
        ...

    def heuristic(self, state: Any) -> float:
        return 0.0
