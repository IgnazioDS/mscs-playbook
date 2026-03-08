"""Intent: define a one-to-many dependency for event notifications.
When to use: publish events to multiple subscribers without tight coupling.
Pitfalls: unordered delivery or missing unsubscribe logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List


@dataclass(frozen=True)
class Event:
    name: str
    payload: dict


class EventBus:
    def __init__(self) -> None:
        self._subscribers: Dict[str, List[Callable[[Event], None]]] = {}

    def subscribe(self, event_name: str, handler: Callable[[Event], None]) -> None:
        self._subscribers.setdefault(event_name, []).append(handler)

    def unsubscribe(self, event_name: str, handler: Callable[[Event], None]) -> None:
        if event_name in self._subscribers:
            self._subscribers[event_name] = [h for h in self._subscribers[event_name] if h != handler]

    def publish(self, event: Event) -> None:
        for handler in list(self._subscribers.get(event.name, [])):
            handler(event)


class AuditSubscriber:
    def __init__(self) -> None:
        self.events: List[Event] = []

    def handle(self, event: Event) -> None:
        self.events.append(event)
