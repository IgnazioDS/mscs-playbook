"""LTL trace checking with finite-trace semantics.

See semantics.py for the exact operator definitions.
"""

from __future__ import annotations

from typing import List, Set

from src.ltl.ast import Formula
from src.ltl.semantics import evaluate


Trace = List[Set[str]]


def check(formula: Formula, trace: Trace, t0: int = 0) -> bool:
    """Check whether a formula holds on a finite trace starting at t0.

    Empty traces return False (no explicit True literal is supported).
    """
    if t0 < 0:
        raise ValueError("t0 must be >= 0")
    if len(trace) == 0:
        return False
    return evaluate(formula, trace, t0, memo={})
