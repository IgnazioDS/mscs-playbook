"""Intent: encapsulate interchangeable algorithms behind a common interface.
When to use: vary behavior (pricing, routing) without modifying clients.
Pitfalls: too many strategies without clear selection rules.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class PricingStrategy(Protocol):
    def price(self, base_price: float) -> float:
        ...


@dataclass(frozen=True)
class NoDiscount:
    def price(self, base_price: float) -> float:
        return base_price


@dataclass(frozen=True)
class PercentageDiscount:
    percent: float

    def price(self, base_price: float) -> float:
        return base_price * (1.0 - self.percent)


class PriceCalculator:
    def __init__(self, strategy: PricingStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: PricingStrategy) -> None:
        self._strategy = strategy

    def total(self, base_price: float) -> float:
        return round(self._strategy.price(base_price), 2)
