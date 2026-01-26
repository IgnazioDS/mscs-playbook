from __future__ import annotations

from typing import List, Tuple

Interval = Tuple[int, int]


def select_max_non_overlapping(intervals: List[Interval]) -> List[Interval]:
    """Select a maximum-size set of non-overlapping intervals."""
    if not intervals:
        return []

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
