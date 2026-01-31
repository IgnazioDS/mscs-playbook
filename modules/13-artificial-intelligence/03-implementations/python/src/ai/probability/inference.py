from __future__ import annotations

from typing import Dict

from .bayes_net import BayesNet


def query(net: BayesNet, var: str, evidence: dict[str, bool]) -> dict[bool, float]:
    dist = {}
    for value in [True, False]:
        extended = dict(evidence)
        extended[var] = value
        dist[value] = _enumerate_all(net, net.variables(), extended)
    total = dist[True] + dist[False]
    if total == 0:
        return {True: 0.0, False: 0.0}
    return {True: dist[True] / total, False: dist[False] / total}


def _enumerate_all(net: BayesNet, variables: list[str], evidence: dict[str, bool]) -> float:
    if not variables:
        return 1.0
    first, rest = variables[0], variables[1:]
    if first in evidence:
        prob = net.probability(first, evidence[first], evidence)
        return prob * _enumerate_all(net, rest, evidence)
    total = 0.0
    for value in [True, False]:
        new_evidence = dict(evidence)
        new_evidence[first] = value
        prob = net.probability(first, value, new_evidence)
        total += prob * _enumerate_all(net, rest, new_evidence)
    return total
