"""Finite-trace LTL semantics.

Trace model:
- A trace is a list of sets of atomic propositions (APs).
- trace[t] is the set of APs true at time t.

Finite-trace operators (evaluated at time t):
- AP p holds iff p in trace[t]
- NOT, AND, OR: standard Boolean logic
- X φ: holds iff t+1 exists and φ holds at t+1 (false at last step)
- G φ: holds iff φ holds for all k in [t..end]
- F φ: holds iff there exists k in [t..end] with φ true
- φ U ψ: holds iff exists k in [t..end] such that ψ holds at k and
  for all j in [t..k-1], φ holds at j

Limitations:
- This is finite-trace semantics (not infinite LTL).
- There is no explicit True/False literal; empty traces default to false.
"""

from __future__ import annotations

from typing import Dict, List, Set, Tuple

from src.ltl.ast import (
    AP,
    And,
    Eventually,
    Formula,
    Globally,
    Next,
    Not,
    Or,
    Until,
)


Trace = List[Set[str]]
Memo = Dict[Tuple[Formula, int], bool]


def evaluate(formula: Formula, trace: Trace, t: int, memo: Memo) -> bool:
    if t < 0:
        raise ValueError("t must be >= 0")
    if t >= len(trace):
        return False

    key = (formula, t)
    if key in memo:
        return memo[key]

    if isinstance(formula, AP):
        result = formula.name in trace[t]
    elif isinstance(formula, Not):
        result = not evaluate(formula.child, trace, t, memo)
    elif isinstance(formula, And):
        result = evaluate(formula.left, trace, t, memo) and evaluate(formula.right, trace, t, memo)
    elif isinstance(formula, Or):
        result = evaluate(formula.left, trace, t, memo) or evaluate(formula.right, trace, t, memo)
    elif isinstance(formula, Next):
        result = t + 1 < len(trace) and evaluate(formula.child, trace, t + 1, memo)
    elif isinstance(formula, Globally):
        result = all(evaluate(formula.child, trace, k, memo) for k in range(t, len(trace)))
    elif isinstance(formula, Eventually):
        result = any(evaluate(formula.child, trace, k, memo) for k in range(t, len(trace)))
    elif isinstance(formula, Until):
        result = False
        for k in range(t, len(trace)):
            if evaluate(formula.right, trace, k, memo):
                if all(evaluate(formula.left, trace, j, memo) for j in range(t, k)):
                    result = True
                break
    else:
        raise TypeError(f"Unsupported formula type: {type(formula)}")

    memo[key] = result
    return result
