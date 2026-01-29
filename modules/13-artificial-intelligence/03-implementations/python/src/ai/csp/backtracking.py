from __future__ import annotations

from copy import deepcopy

from .csp import CSP
from .heuristics import mrv, lcv
from .ac3 import ac3


def backtracking_search(csp: CSP, use_ac3: bool = True) -> dict[str, object] | None:
    if use_ac3:
        csp = deepcopy(csp)
        if not ac3(csp):
            return None
    return _backtrack({}, csp, use_ac3)


def _backtrack(assignment: dict[str, object], csp: CSP, use_ac3: bool) -> dict[str, object] | None:
    if len(assignment) == len(csp.variables):
        return assignment
    var = mrv(csp, assignment)
    for value in lcv(csp, var, assignment):
        if csp.is_consistent(var, value, assignment):
            local_assignment = assignment.copy()
            local_assignment[var] = value
            if use_ac3:
                csp_copy = deepcopy(csp)
                csp_copy.domains[var] = [value]
                if ac3(csp_copy):
                    result = _backtrack(local_assignment, csp_copy, use_ac3)
                else:
                    result = None
            else:
                result = _backtrack(local_assignment, csp, use_ac3)
            if result is not None:
                return result
    return None
