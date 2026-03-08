"""Intent: translate one interface into another expected by clients.
When to use: integrate legacy or third-party APIs.
Pitfalls: leaky abstractions and insufficient error translation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class PaymentGateway(Protocol):
    def pay(self, amount_cents: int) -> str:
        ...


class LegacyGateway:
    def send_payment(self, amount_cents: int) -> str:
        if amount_cents <= 0:
            raise ValueError("amount_cents must be positive")
        return f"legacy:{amount_cents}"


@dataclass(frozen=True)
class LegacyGatewayAdapter:
    legacy: LegacyGateway

    def pay(self, amount_cents: int) -> str:
        try:
            return self.legacy.send_payment(amount_cents)
        except ValueError as exc:
            raise RuntimeError("payment failed") from exc
