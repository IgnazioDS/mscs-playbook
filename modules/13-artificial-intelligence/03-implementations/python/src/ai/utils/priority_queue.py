from __future__ import annotations

import heapq
from dataclasses import dataclass, field
from typing import Any


@dataclass(order=True)
class PrioritizedItem:
    priority: float
    count: int
    item: Any = field(compare=False)


class PriorityQueue:
    def __init__(self) -> None:
        self._heap: list[PrioritizedItem] = []
        self._counter = 0

    def push(self, priority: float, item: Any) -> None:
        self._counter += 1
        heapq.heappush(self._heap, PrioritizedItem(priority, self._counter, item))

    def pop(self) -> tuple[float, Any]:
        element = heapq.heappop(self._heap)
        return element.priority, element.item

    def __len__(self) -> int:
        return len(self._heap)
