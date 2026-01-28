"""Pricing and discount strategies (Strategy pattern)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from src.mini_project.domain.entities import Order


class DiscountPolicy(Protocol):
    def discount_cents(self, order: Order) -> int:
        ...


@dataclass(frozen=True)
class NoDiscount:
    def discount_cents(self, order: Order) -> int:
        return 0


@dataclass(frozen=True)
class PercentageDiscount:
    percent: float

    def discount_cents(self, order: Order) -> int:
        if order.total is None:
            order.compute_total()
        assert order.total is not None
        return int(order.total.cents * self.percent)


@dataclass(frozen=True)
class BuyXGetYFree:
    sku: str
    buy_qty: int
    free_qty: int

    def discount_cents(self, order: Order) -> int:
        discount = 0
        for item in order.items:
            if item.sku == self.sku:
                eligible = item.qty // (self.buy_qty + self.free_qty)
                discount += eligible * self.free_qty * item.unit_price.cents
        return discount
