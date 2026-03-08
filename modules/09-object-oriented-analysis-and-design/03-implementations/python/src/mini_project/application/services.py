"""Application services (use cases)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Protocol

from src.mini_project.domain.entities import LineItem, Money, Order
from src.mini_project.domain.events import OrderPlaced, PaymentCaptured, PaymentFailed
from src.mini_project.domain.policies import DiscountPolicy
from src.mini_project.infrastructure.notifier import EventBus
from src.mini_project.infrastructure.payments import PaymentProcessorFactory
from src.mini_project.infrastructure.repositories import OrderRepository


@dataclass
class Receipt:
    order_id: int
    total: Money
    status: str
    provider: str


class OrderService:
    def __init__(
        self,
        repo: OrderRepository,
        bus: EventBus,
        payment_factory: PaymentProcessorFactory,
    ) -> None:
        self._repo = repo
        self._bus = bus
        self._payment_factory = payment_factory
        self._captured: dict[int, str] = {}

    def place_order(
        self,
        customer_id: str,
        items: List[LineItem],
        discount_policy: DiscountPolicy,
        payment_method: str,
    ) -> int:
        order_id = self._repo.next_id()
        order = Order(order_id=order_id, customer_id=customer_id, items=items)
        order.compute_total()
        order.apply_discount(discount_policy.discount_cents(order))
        self._repo.save(order)
        self._bus.publish(OrderPlaced(order_id, customer_id, order.total.cents))
        return order_id

    def capture_payment(self, order_id: int, payment_method: str) -> Receipt:
        order = self._repo.get(order_id)
        if order is None:
            raise ValueError("Order not found")
        if order_id in self._captured:
            provider = self._captured[order_id]
            return Receipt(order_id, order.total or Money(0), order.status, provider)

        processor = self._payment_factory.create(payment_method)
        try:
            provider = processor.charge(order.total.cents)
            order.mark_paid()
            self._captured[order_id] = provider
            self._bus.publish(PaymentCaptured(order_id, order.total.cents, provider))
            return Receipt(order_id, order.total, order.status, provider)
        except Exception as exc:
            order.mark_failed()
            self._bus.publish(PaymentFailed(order_id, str(exc), payment_method))
            return Receipt(order_id, order.total, order.status, payment_method)
