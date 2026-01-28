"""Command objects to encapsulate use cases."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from src.mini_project.application.services import OrderService, Receipt
from src.mini_project.domain.entities import LineItem
from src.mini_project.domain.policies import DiscountPolicy


@dataclass
class PlaceOrderCommand:
    service: OrderService
    customer_id: str
    items: List[LineItem]
    discount_policy: DiscountPolicy
    payment_method: str

    def execute(self) -> int:
        return self.service.place_order(
            self.customer_id,
            self.items,
            self.discount_policy,
            self.payment_method,
        )


@dataclass
class CapturePaymentCommand:
    service: OrderService
    order_id: int
    payment_method: str

    def execute(self) -> Receipt:
        return self.service.capture_payment(self.order_id, self.payment_method)
