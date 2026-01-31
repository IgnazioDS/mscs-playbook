from __future__ import annotations

from typing import Any

LEVEL_POINTS = {
    "low": 1,
    "med": 2,
    "medium": 2,
    "high": 3,
}


def normalize_level(value: Any) -> str:
    if value is None:
        return "low"
    text = str(value).strip().lower()
    if text in LEVEL_POINTS:
        return "med" if text == "medium" else text
    return "low"


def level_points(value: Any) -> int:
    return LEVEL_POINTS[normalize_level(value)]


def risk_score(severity: Any, likelihood: Any) -> int:
    return level_points(severity) * level_points(likelihood)
