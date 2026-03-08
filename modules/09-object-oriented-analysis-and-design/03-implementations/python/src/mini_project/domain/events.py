"""Domain events."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class OrderPlaced:
    order_id: int
    customer_id: str
    total_cents: int


@dataclass(frozen=True)
class PaymentCaptured:
    order_id: int
    amount_cents: int
    provider: str


@dataclass(frozen=True)
class PaymentFailed:
    order_id: int
    reason: str
    provider: str
