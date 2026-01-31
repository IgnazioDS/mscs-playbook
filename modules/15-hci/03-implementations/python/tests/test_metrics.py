from __future__ import annotations

import csv
from pathlib import Path

from src.hci_toolkit.metrics import (
    UsabilitySession,
    completion_rate,
    error_rate,
    sus_score,
    task_success_rate,
    time_on_task_summary,
)

FIXTURES = Path(__file__).parent / "fixtures"


def _load_sessions() -> list[UsabilitySession]:
    sessions: list[UsabilitySession] = []
    with (FIXTURES / "usability_sessions.csv").open() as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            sessions.append(
                UsabilitySession(
                    task_id=row["task_id"],
                    user_id=row["user_id"],
                    success=row["success"] == "1",
                    time_sec=float(row["time_sec"]),
                    errors=int(row["errors"]),
                )
            )
    return sessions


def test_task_metrics_from_fixture():
    sessions = _load_sessions()
    assert task_success_rate(sessions) == 0.8
    assert completion_rate(sessions) == 0.8
    assert error_rate(sessions) == 0.6

    summary = time_on_task_summary(sessions)
    assert summary["count"] == 4
    assert summary["mean"] == 32.5
    assert summary["median"] == 32.5
    assert summary["min"] == 25
    assert summary["max"] == 40


def test_sus_known_scores():
    assert sus_score([3] * 10) == 50.0
    assert sus_score([5, 1, 5, 1, 5, 1, 5, 1, 5, 1]) == 100.0
