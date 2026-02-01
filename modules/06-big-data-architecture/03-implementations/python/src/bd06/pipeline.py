"""Deterministic pipeline helpers for BD06 tests."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from typing import Iterable


@dataclass(frozen=True)
class EventRecord:
    event_id: str
    event_type: str
    user_id: str
    amount: float
    occurred_at: str


def build_event(
    event_type: str,
    user_id: str,
    amount: float,
    timestamp: datetime | None = None,
) -> EventRecord:
    """Create a deterministic event with a stable id.

    The event_id is derived from the event payload for repeatable tests.
    """
    ts = (timestamp or datetime(2024, 1, 1, tzinfo=timezone.utc)).isoformat()
    payload = f"{event_type}|{user_id}|{amount:.2f}|{ts}"
    event_id = sha256(payload.encode("utf-8")).hexdigest()[:12]
    return EventRecord(event_id=event_id, event_type=event_type, user_id=user_id, amount=amount, occurred_at=ts)


def ingest_events(events: Iterable[EventRecord]) -> dict:
    """Return deterministic aggregation metrics for a stream of events."""
    total = 0.0
    counts: dict[str, int] = {}
    users: set[str] = set()

    for event in events:
        total += event.amount
        counts[event.event_type] = counts.get(event.event_type, 0) + 1
        users.add(event.user_id)

    return {
        "event_count": sum(counts.values()),
        "unique_users": len(users),
        "total_amount": round(total, 2),
        "event_types": dict(sorted(counts.items())),
    }
