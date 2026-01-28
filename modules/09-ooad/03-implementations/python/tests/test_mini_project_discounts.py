from src.mini_project.application.services import OrderService
from src.mini_project.domain.entities import LineItem, Money
from src.mini_project.domain.policies import DiscountPolicy, NoDiscount
from src.mini_project.infrastructure.notifier import EventBus
from src.mini_project.infrastructure.payments import PaymentProcessorFactory
from src.mini_project.infrastructure.repositories import OrderRepository


class FlatDiscount:
    def __init__(self, cents: int) -> None:
        self.cents = cents

    def discount_cents(self, order) -> int:
        return self.cents


def test_new_discount_strategy_without_service_change():
    repo = OrderRepository()
    bus = EventBus()
    service = OrderService(repo, bus, PaymentProcessorFactory())

    items = [LineItem("sku-1", "Widget", Money(1000), 1)]
    order_id = service.place_order("cust-1", items, FlatDiscount(200), "stripe")
    order = repo.get(order_id)

    assert order.total.cents == 800
