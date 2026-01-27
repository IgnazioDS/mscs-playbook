from __future__ import annotations

"""Fibonacci numbers via top-down memoization.

Problem:
    Compute F(n) where F(0)=0, F(1)=1, and F(n)=F(n-1)+F(n-2).

Inputs/Outputs:
    n (int, n >= 0) -> int result.

Complexity:
    Time O(n) with memoization, space O(n) for the cache and recursion stack.

Typical use cases:
    Demonstrating overlapping subproblems, memoization patterns, and caching.
"""

from functools import lru_cache


def fibonacci(n: int) -> int:
    """Return the nth Fibonacci number using memoization.

    Args:
        n: Non-negative index into the Fibonacci sequence.

    Returns:
        The nth Fibonacci number.

    Raises:
        ValueError: If n is negative.

    Notes:
        The memoized helper preserves the invariant that each subproblem F(k)
        is computed once, preventing exponential recursion.
    """
    if n < 0:
        raise ValueError("n must be non-negative")

    @lru_cache(maxsize=None)
    def _fib(k: int) -> int:
        if k < 2:
            return k
        # Reuse cached subproblems to avoid repeated recursion.
        return _fib(k - 1) + _fib(k - 2)

    return _fib(n)
