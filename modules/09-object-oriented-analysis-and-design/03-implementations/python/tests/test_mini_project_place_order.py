from src.mini_project.application.services import OrderService
from src.mini_project.domain.entities import LineItem, Money
from src.mini_project.domain.policies import NoDiscount
from src.mini_project.infrastructure.notifier import EventBus
from src.mini_project.infrastructure.payments import PaymentProcessorFactory
from src.mini_project.infrastructure.repositories import OrderRepository


def test_place_order_creates_order():
    repo = OrderRepository()
    bus = EventBus()
    service = OrderService(repo, bus, PaymentProcessorFactory())

    items = [LineItem("sku-1", "Widget", Money(1000), 1)]
    order_id = service.place_order("cust-1", items, NoDiscount(), "stripe")

    order = repo.get(order_id)
    assert order is not None
    assert order.total.cents == 1000
