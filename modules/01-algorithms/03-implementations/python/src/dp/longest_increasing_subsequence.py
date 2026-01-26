from __future__ import annotations

from bisect import bisect_left
from typing import Iterable


def lis_length(nums: Iterable[int]) -> int:
    """Return the length of the longest increasing subsequence."""
    tails = []
    for x in nums:
        idx = bisect_left(tails, x)
        if idx == len(tails):
            tails.append(x)
        else:
            tails[idx] = x
    return len(tails)
