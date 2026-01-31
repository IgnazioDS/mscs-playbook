from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable


@dataclass
class BayesNode:
    name: str
    parents: list[str]
    cpt: dict[tuple[bool, ...], float]

    def prob(self, value: bool, evidence: dict[str, bool]) -> float:
        key = tuple(evidence[parent] for parent in self.parents)
        p_true = self.cpt[key]
        return p_true if value else 1.0 - p_true


class BayesNet:
    def __init__(self) -> None:
        self.nodes: dict[str, BayesNode] = {}
        self.order: list[str] = []

    def add_node(self, node: BayesNode) -> None:
        self.nodes[node.name] = node
        if node.name not in self.order:
            self.order.append(node.name)

    def variables(self) -> list[str]:
        return list(self.order)

    def probability(self, var: str, value: bool, evidence: dict[str, bool]) -> float:
        return self.nodes[var].prob(value, evidence)
