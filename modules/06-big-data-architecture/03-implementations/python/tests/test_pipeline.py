from datetime import datetime, timezone

from src.bd06.pipeline import build_event, ingest_events


def test_build_event_is_deterministic():
    timestamp = datetime(2024, 1, 1, tzinfo=timezone.utc)
    first = build_event("order_paid", "user-1", 12.5, timestamp)
    second = build_event("order_paid", "user-1", 12.5, timestamp)
    assert first == second
    assert first.event_id == "71056901614a"


def test_ingest_events_aggregates_metrics():
    timestamp = datetime(2024, 1, 1, tzinfo=timezone.utc)
    events = [
        build_event("order_paid", "user-1", 10.0, timestamp),
        build_event("order_paid", "user-2", 15.0, timestamp),
        build_event("refund", "user-1", -4.5, timestamp),
    ]
    metrics = ingest_events(events)

    assert metrics["event_count"] == 3
    assert metrics["unique_users"] == 2
    assert metrics["total_amount"] == 20.5
    assert metrics["event_types"] == {"order_paid": 2, "refund": 1}
