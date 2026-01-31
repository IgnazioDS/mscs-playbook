from __future__ import annotations

from collections import deque

from .csp import CSP


def ac3(csp: CSP) -> bool:
    queue = deque([(xi, xj) for xi in csp.variables for xj in csp.neighbors.get(xi, [])])
    while queue:
        xi, xj = queue.popleft()
        if _revise(csp, xi, xj):
            if not csp.domains[xi]:
                return False
            for xk in csp.neighbors.get(xi, []):
                if xk != xj:
                    queue.append((xk, xi))
    return True


def _revise(csp: CSP, xi: str, xj: str) -> bool:
    revised = False
    domain = csp.domains[xi][:]
    for x in domain:
        if not any(csp.constraint(xi, x, xj, y) for y in csp.domains[xj]):
            csp.domains[xi].remove(x)
            revised = True
    return revised
