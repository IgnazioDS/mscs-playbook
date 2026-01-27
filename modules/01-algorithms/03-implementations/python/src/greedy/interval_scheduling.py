from __future__ import annotations

"""Interval scheduling via earliest-finish-time greedy selection.

Problem:
    Select the maximum number of non-overlapping intervals.

Inputs/Outputs:
    intervals: list of (start, end) pairs -> selected subset (list of intervals)

Complexity:
    Time O(n log n) for sorting, space O(n) for the result.

Typical use cases:
    Booking systems, CPU job scheduling, and resource allocation.
"""

from typing import List, Tuple

Interval = Tuple[int, int]


def select_max_non_overlapping(intervals: List[Interval]) -> List[Interval]:
    """Select a maximum-size set of non-overlapping intervals.

    Args:
        intervals: List of (start, end) pairs with start <= end.

    Returns:
        A maximum-size subset of non-overlapping intervals.

    Raises:
        ValueError: If any interval has start > end.

    Invariant:
        current_end is the finish time of the last accepted interval.
    """
    if not intervals:
        return []

    # Greedy choice: pick intervals with earliest finishing time first.
    sorted_intervals = sorted(intervals, key=lambda x: x[1])
    result: List[Interval] = []
    current_end = None

    for start, end in sorted_intervals:
        if start > end:
            raise ValueError("interval start must be <= end")
        if current_end is None or start >= current_end:
            result.append((start, end))
            current_end = end

    return result
