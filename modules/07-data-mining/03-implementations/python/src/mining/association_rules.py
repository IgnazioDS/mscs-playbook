"""Minimal Apriori and association rule generation for small datasets."""

from __future__ import annotations

from itertools import combinations
from typing import Dict, Iterable, List, Tuple


def _itemset_support(transactions: List[set], itemset: frozenset) -> float:
    count = sum(1 for t in transactions if itemset.issubset(t))
    return count / len(transactions) if transactions else 0.0


def apriori(transactions: List[List[str]], min_support: float) -> Dict[frozenset, float]:
    """Return frequent itemsets with support >= min_support."""
    trans_sets = [set(t) for t in transactions]
    items = sorted({item for t in trans_sets for item in t})

    support_map: Dict[frozenset, float] = {}
    current_itemsets = [frozenset([item]) for item in items]
    k = 1

    while current_itemsets:
        frequent: List[frozenset] = []
        for itemset in current_itemsets:
            support = _itemset_support(trans_sets, itemset)
            if support >= min_support:
                support_map[itemset] = support
                frequent.append(itemset)

        if not frequent:
            break

        k += 1
        frequent_set = set(frequent)
        candidates = set()
        frequent_sorted = sorted(frequent, key=lambda s: tuple(sorted(s)))
        for i in range(len(frequent_sorted)):
            for j in range(i + 1, len(frequent_sorted)):
                union = frequent_sorted[i].union(frequent_sorted[j])
                if len(union) != k:
                    continue
                subsets_ok = all(
                    frozenset(subset) in frequent_set for subset in combinations(union, k - 1)
                )
                if subsets_ok:
                    candidates.add(union)

        current_itemsets = sorted(candidates, key=lambda s: tuple(sorted(s)))

    return support_map


def generate_rules(support_map: Dict[frozenset, float], min_confidence: float) -> List[Dict[str, object]]:
    """Generate association rules from frequent itemsets."""
    rules: List[Dict[str, object]] = []
    for itemset, support in support_map.items():
        if len(itemset) < 2:
            continue
        items = sorted(itemset)
        for r in range(1, len(items)):
            for antecedent_items in combinations(items, r):
                antecedent = frozenset(antecedent_items)
                consequent = itemset.difference(antecedent)
                if antecedent not in support_map or consequent not in support_map:
                    continue
                confidence = support / support_map[antecedent]
                if confidence < min_confidence:
                    continue
                lift = confidence / support_map[consequent]
                rules.append(
                    {
                        "antecedent": tuple(sorted(antecedent)),
                        "consequent": tuple(sorted(consequent)),
                        "support": support,
                        "confidence": confidence,
                        "lift": lift,
                    }
                )

    rules.sort(
        key=lambda r: (
            -r["lift"],
            -r["confidence"],
            -r["support"],
            r["antecedent"],
            r["consequent"],
        )
    )
    return rules
