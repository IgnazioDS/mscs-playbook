"""Greedy safety policy selector for a transition system.

This is not full controller synthesis. It picks a successor that avoids
bad states if possible.
"""

from __future__ import annotations

from typing import Hashable, Iterable, List, Set

from src.ts.transition_system import TransitionSystem


def _ordered_successors(successors: Iterable[Hashable]) -> List[Hashable]:
    successors_list = list(successors)
    try:
        return sorted(successors_list)
    except TypeError:
        return successors_list


def choose_next_state(
    ts: TransitionSystem, current: Hashable, bad_states: Set[Hashable]
) -> Hashable | None:
    """Choose a next state that avoids bad states if possible.

    If no successors exist, returns None. If all successors are bad, returns
    the first one in deterministic order.
    """
    successors = _ordered_successors(ts.successors(current))
    if not successors:
        return None

    for nxt in successors:
        if nxt not in bad_states:
            return nxt

    return successors[0]
