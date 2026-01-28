"""Intent: add behavior without changing the wrapped object.
When to use: extend services with logging, timing, or caching.
Pitfalls: stacking too many decorators or hiding side effects.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Protocol


class Service(Protocol):
    def run(self, payload: str) -> str:
        ...


@dataclass(frozen=True)
class CoreService:
    def run(self, payload: str) -> str:
        return payload.upper()


@dataclass
class TimingDecorator:
    service: Service
    last_ms: float | None = None

    def run(self, payload: str) -> str:
        start = time.time()
        result = self.service.run(payload)
        self.last_ms = (time.time() - start) * 1000
        return result
