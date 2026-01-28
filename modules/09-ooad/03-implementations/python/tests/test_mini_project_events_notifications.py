from src.mini_project.application.services import OrderService
from src.mini_project.domain.entities import LineItem, Money
from src.mini_project.domain.policies import NoDiscount
from src.mini_project.infrastructure.notifier import AuditLogSubscriber, EmailNotifier, EventBus
from src.mini_project.infrastructure.payments import PaymentProcessorFactory
from src.mini_project.infrastructure.repositories import OrderRepository


def test_events_trigger_notifications():
    repo = OrderRepository()
    bus = EventBus()
    service = OrderService(repo, bus, PaymentProcessorFactory())

    emails: list[str] = []
    audits: list[str] = []
    bus.subscribe("OrderPlaced", EmailNotifier(emails).handle)
    bus.subscribe("OrderPlaced", AuditLogSubscriber(audits).handle)

    items = [LineItem("sku-1", "Widget", Money(1000), 1)]
    service.place_order("cust-1", items, NoDiscount(), "stripe")

    assert emails == ["email:OrderPlaced"]
    assert audits == ["audit:OrderPlaced"]
