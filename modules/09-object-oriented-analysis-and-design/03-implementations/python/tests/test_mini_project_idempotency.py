from src.mini_project.application.services import OrderService
from src.mini_project.domain.entities import LineItem, Money
from src.mini_project.domain.policies import NoDiscount
from src.mini_project.infrastructure.notifier import EventBus
from src.mini_project.infrastructure.payments import PaymentProcessorFactory
from src.mini_project.infrastructure.repositories import OrderRepository


def test_capture_payment_idempotent():
    repo = OrderRepository()
    bus = EventBus()
    service = OrderService(repo, bus, PaymentProcessorFactory())

    items = [LineItem("sku-1", "Widget", Money(1000), 1)]
    order_id = service.place_order("cust-1", items, NoDiscount(), "stripe")

    first = service.capture_payment(order_id, "stripe")
    second = service.capture_payment(order_id, "stripe")

    assert first.status == "PAID"
    assert second.status == "PAID"
    assert first.provider == second.provider
