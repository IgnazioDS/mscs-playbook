"""Payment gateways with adapters and factory method."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Protocol


class PaymentProcessor(Protocol):
    def charge(self, amount_cents: int) -> str:
        ...


@dataclass(frozen=True)
class FakeStripeGateway:
    def charge_cents(self, amount_cents: int) -> str:
        if amount_cents <= 0:
            raise ValueError("amount_cents must be positive")
        return f"stripe:{amount_cents}"


@dataclass(frozen=True)
class LegacyPayPalGateway:
    def send_payment(self, amount_dollars: float) -> str:
        if amount_dollars <= 0:
            raise ValueError("amount_dollars must be positive")
        return f"paypal:{amount_dollars:.2f}"


@dataclass(frozen=True)
class StripeAdapter:
    gateway: FakeStripeGateway

    def charge(self, amount_cents: int) -> str:
        return self.gateway.charge_cents(amount_cents)


@dataclass(frozen=True)
class PayPalAdapter:
    gateway: LegacyPayPalGateway

    def charge(self, amount_cents: int) -> str:
        return self.gateway.send_payment(amount_cents / 100.0)


class PaymentProcessorFactory:
    def __init__(self) -> None:
        self._registry: Dict[str, PaymentProcessor] = {
            "stripe": StripeAdapter(FakeStripeGateway()),
            "paypal": PayPalAdapter(LegacyPayPalGateway()),
        }

    def create(self, kind: str) -> PaymentProcessor:
        if kind not in self._registry:
            raise ValueError(f"Unknown payment method: {kind}")
        return self._registry[kind]

    def register(self, kind: str, processor: PaymentProcessor) -> None:
        self._registry[kind] = processor
