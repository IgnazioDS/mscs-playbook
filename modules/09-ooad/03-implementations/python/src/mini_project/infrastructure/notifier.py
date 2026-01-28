"""Event bus and subscribers (Observer pattern)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List


@dataclass(frozen=True)
class EventEnvelope:
    name: str
    payload: object


class EventBus:
    def __init__(self) -> None:
        self._subs: Dict[str, List[Callable[[EventEnvelope], None]]] = {}

    def subscribe(self, name: str, handler: Callable[[EventEnvelope], None]) -> None:
        self._subs.setdefault(name, []).append(handler)

    def publish(self, event: object) -> None:
        name = type(event).__name__
        envelope = EventEnvelope(name=name, payload=event)
        for handler in list(self._subs.get(name, [])):
            handler(envelope)


@dataclass
class EmailNotifier:
    messages: List[str]

    def handle(self, envelope: EventEnvelope) -> None:
        self.messages.append(f"email:{envelope.name}")


@dataclass
class AuditLogSubscriber:
    logs: List[str]

    def handle(self, envelope: EventEnvelope) -> None:
        self.logs.append(f"audit:{envelope.name}")
