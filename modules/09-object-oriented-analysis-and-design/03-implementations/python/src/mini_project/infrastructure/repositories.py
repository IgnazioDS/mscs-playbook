"""In-memory repositories."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

from src.mini_project.domain.entities import Order


class OrderRepository:
    def __init__(self) -> None:
        self._store: Dict[int, Order] = {}
        self._next_id = 1

    def next_id(self) -> int:
        value = self._next_id
        self._next_id += 1
        return value

    def save(self, order: Order) -> None:
        self._store[order.order_id] = order

    def get(self, order_id: int) -> Optional[Order]:
        return self._store.get(order_id)
