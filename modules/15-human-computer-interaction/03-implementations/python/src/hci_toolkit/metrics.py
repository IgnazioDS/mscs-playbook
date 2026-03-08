from __future__ import annotations

from dataclasses import dataclass
from statistics import fmean, median
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class UsabilitySession:
    """Represents a single usability task attempt."""

    task_id: str
    user_id: str
    success: bool
    time_sec: float
    errors: int


def task_success_rate(sessions: Sequence[UsabilitySession]) -> float:
    """Return the fraction of sessions marked successful."""
    total = len(sessions)
    if total == 0:
        return 0.0
    successes = sum(1 for session in sessions if session.success)
    return successes / total


def completion_rate(sessions: Sequence[UsabilitySession]) -> float:
    """Return the fraction of sessions with a recorded completion time."""
    total = len(sessions)
    if total == 0:
        return 0.0
    completed = sum(1 for session in sessions if session.time_sec > 0)
    return completed / total


def error_rate(sessions: Sequence[UsabilitySession]) -> float:
    """Return the average number of errors per session."""
    total = len(sessions)
    if total == 0:
        return 0.0
    total_errors = sum(session.errors for session in sessions)
    return total_errors / total


def time_on_task_summary(
    sessions: Sequence[UsabilitySession], *, include_failed: bool = False
) -> dict[str, float | int | None]:
    """Summarize time-on-task with mean, median, min, max, and count.

    By default, only successful sessions are included.
    """
    if include_failed:
        times = [session.time_sec for session in sessions if session.time_sec > 0]
    else:
        times = [
            session.time_sec
            for session in sessions
            if session.success and session.time_sec > 0
        ]

    if not times:
        return {
            "count": 0,
            "mean": None,
            "median": None,
            "min": None,
            "max": None,
        }

    return {
        "count": len(times),
        "mean": fmean(times),
        "median": median(times),
        "min": min(times),
        "max": max(times),
    }


def task_metrics(
    sessions: Sequence[UsabilitySession], *, include_failed: bool = False
) -> dict[str, float | dict[str, float | int | None]]:
    """Return a combined metrics summary for a set of sessions."""
    return {
        "success_rate": task_success_rate(sessions),
        "completion_rate": completion_rate(sessions),
        "error_rate": error_rate(sessions),
        "time_on_task": time_on_task_summary(
            sessions, include_failed=include_failed
        ),
    }


def sus_score(responses: Sequence[int]) -> float:
    """Calculate a SUS score for a single respondent.

    Responses must include 10 items scored from 1 to 5.
    """
    if len(responses) != 10:
        raise ValueError("SUS requires exactly 10 responses")

    total = 0
    for index, value in enumerate(responses, start=1):
        if value < 1 or value > 5:
            raise ValueError("SUS responses must be between 1 and 5")
        if index % 2 == 1:
            total += value - 1
        else:
            total += 5 - value
    return total * 2.5


def sus_scores(responses_by_user: Mapping[str, Sequence[int]]) -> dict[str, float]:
    """Calculate SUS scores for each respondent."""
    return {
        user_id: sus_score(responses)
        for user_id, responses in responses_by_user.items()
    }


def sus_aggregate(scores: Iterable[float]) -> dict[str, float | None]:
    """Aggregate SUS scores across respondents."""
    values = list(scores)
    if not values:
        return {"mean": None, "median": None, "min": None, "max": None}
    return {
        "mean": fmean(values),
        "median": median(values),
        "min": min(values),
        "max": max(values),
    }
