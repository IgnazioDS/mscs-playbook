"""Domain entities and value objects."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass(frozen=True)
class Money:
    cents: int
    currency: str = "USD"

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Currency mismatch")
        return Money(self.cents + other.cents, self.currency)

    def __mul__(self, multiplier: int) -> "Money":
        return Money(self.cents * multiplier, self.currency)

    def __str__(self) -> str:
        return f"{self.currency} {self.cents / 100:.2f}"


@dataclass(frozen=True)
class LineItem:
    sku: str
    name: str
    unit_price: Money
    qty: int

    def total(self) -> Money:
        return self.unit_price * self.qty


@dataclass
class Order:
    order_id: int
    customer_id: str
    items: List[LineItem]
    status: str = "CREATED"
    total: Money | None = None

    def compute_total(self) -> Money:
        total = Money(0, self.items[0].unit_price.currency if self.items else "USD")
        for item in self.items:
            total = total + item.total()
        self.total = total
        return total

    def apply_discount(self, discount_cents: int) -> None:
        if self.total is None:
            self.compute_total()
        assert self.total is not None
        self.total = Money(max(0, self.total.cents - discount_cents), self.total.currency)

    def mark_paid(self) -> None:
        self.status = "PAID"

    def mark_failed(self) -> None:
        self.status = "PAYMENT_FAILED"
