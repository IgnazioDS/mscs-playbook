from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from ..utils.rng import make_rng


@dataclass
class BernoulliBandit:
    probs: list[float]
    seed: int | None = None

    def __post_init__(self) -> None:
        self.rng = make_rng(self.seed)

    def step(self, action: int) -> float:
        p = self.probs[action]
        return 1.0 if self.rng.rand() < p else 0.0

    def optimal_prob(self) -> float:
        return max(self.probs)
