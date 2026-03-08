from src.patterns.observer import AuditSubscriber, Event, EventBus


def test_observer_delivery_and_unsubscribe():
    bus = EventBus()
    audit = AuditSubscriber()
    bus.subscribe("order.created", audit.handle)

    bus.publish(Event("order.created", {"id": "O-1"}))
    assert len(audit.events) == 1

    bus.unsubscribe("order.created", audit.handle)
    bus.publish(Event("order.created", {"id": "O-2"}))
    assert len(audit.events) == 1
