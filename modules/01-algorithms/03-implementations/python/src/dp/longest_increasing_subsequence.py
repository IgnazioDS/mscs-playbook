from __future__ import annotations

"""Longest Increasing Subsequence (LIS) length via patience sorting.

Problem:
    Find the length of the longest strictly increasing subsequence in a sequence.

Inputs/Outputs:
    nums: iterable of comparable items (ints expected) -> LIS length (int)

Complexity:
    Time O(n log n), space O(n).

Typical use cases:
    Trend analysis, sequence alignment heuristics, and DP optimization patterns.
"""

from bisect import bisect_left
from typing import Iterable


def lis_length(nums: Iterable[int]) -> int:
    """Return the length of the longest increasing subsequence.

    Args:
        nums: Iterable of integers.

    Returns:
        Length of the longest strictly increasing subsequence.

    Invariant:
        tails[i] stores the minimum possible tail value of an increasing
        subsequence of length i + 1.
    """
    tails = []
    for x in nums:
        # Find the leftmost tail >= x to keep tails minimal.
        idx = bisect_left(tails, x)
        if idx == len(tails):
            tails.append(x)
        else:
            tails[idx] = x
    return len(tails)
