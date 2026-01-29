from __future__ import annotations

from functools import lru_cache
from typing import Callable


def memoize(maxsize: int = 1024) -> Callable:
    return lru_cache(maxsize=maxsize)
