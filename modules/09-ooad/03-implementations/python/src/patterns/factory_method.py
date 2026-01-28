"""Intent: define an interface for object creation, letting subclasses decide.
When to use: construct objects based on type or configuration.
Pitfalls: too many factory branches and hidden dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Protocol


class PaymentProcessor(Protocol):
    def charge(self, amount: float) -> str:
        ...


@dataclass(frozen=True)
class CardProcessor:
    def charge(self, amount: float) -> str:
        return f"card:{amount:.2f}"


@dataclass(frozen=True)
class BankTransferProcessor:
    def charge(self, amount: float) -> str:
        return f"bank:{amount:.2f}"


class PaymentProcessorFactory:
    _registry: Dict[str, PaymentProcessor] = {
        "card": CardProcessor(),
        "bank": BankTransferProcessor(),
    }

    @classmethod
    def create(cls, kind: str) -> PaymentProcessor:
        if kind not in cls._registry:
            raise ValueError(f"Unknown processor type: {kind}")
        return cls._registry[kind]

    @classmethod
    def register(cls, kind: str, processor: PaymentProcessor) -> None:
        cls._registry[kind] = processor
