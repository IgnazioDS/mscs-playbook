from __future__ import annotations

from functools import lru_cache


def fibonacci(n: int) -> int:
    """Return the nth Fibonacci number using memoization."""
    if n < 0:
        raise ValueError("n must be non-negative")

    @lru_cache(maxsize=None)
    def _fib(k: int) -> int:
        if k < 2:
            return k
        return _fib(k - 1) + _fib(k - 2)

    return _fib(n)
