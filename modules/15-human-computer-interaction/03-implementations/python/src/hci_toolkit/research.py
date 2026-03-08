from __future__ import annotations

from dataclasses import dataclass
from collections import Counter
from itertools import combinations
from statistics import fmean
from typing import Iterable, Sequence


@dataclass(frozen=True)
class HeuristicFinding:
    """Represents a heuristic evaluation finding."""

    heuristic: str
    severity: int
    notes: str | None = None


def heuristic_report(findings: Sequence[HeuristicFinding]) -> dict[str, object]:
    """Aggregate heuristic evaluation findings by severity and heuristic."""
    if not findings:
        return {
            "total": 0,
            "average_severity": 0.0,
            "severity_counts": {},
            "by_heuristic": {},
        }

    severity_counts: Counter[int] = Counter()
    by_heuristic: dict[str, list[int]] = {}

    for finding in findings:
        if finding.severity < 0 or finding.severity > 4:
            raise ValueError("Severity must be between 0 and 4")
        severity_counts[finding.severity] += 1
        by_heuristic.setdefault(finding.heuristic, []).append(finding.severity)

    average = fmean(finding.severity for finding in findings)
    by_heuristic_summary = {
        heuristic: {
            "count": len(values),
            "average_severity": fmean(values),
            "max_severity": max(values),
        }
        for heuristic, values in by_heuristic.items()
    }

    return {
        "total": len(findings),
        "average_severity": average,
        "severity_counts": dict(sorted(severity_counts.items())),
        "by_heuristic": by_heuristic_summary,
    }


def parse_tags(raw: str) -> list[str]:
    """Parse a comma-separated tag string into normalized, unique tags."""
    tags = [tag.strip().lower() for tag in raw.split(",")]
    seen = set()
    normalized = []
    for tag in tags:
        if tag and tag not in seen:
            seen.add(tag)
            normalized.append(tag)
    return normalized


def _normalize_rows(rows: Iterable[Sequence[str] | str]) -> list[list[str]]:
    normalized_rows: list[list[str]] = []
    for row in rows:
        if isinstance(row, str):
            tags = parse_tags(row)
        else:
            tags = []
            seen = set()
            for tag in row:
                normalized_tag = tag.strip().lower()
                if normalized_tag and normalized_tag not in seen:
                    seen.add(normalized_tag)
                    tags.append(normalized_tag)
        normalized_rows.append(tags)
    return normalized_rows


def qualitative_theme_report(
    coded_rows: Iterable[Sequence[str] | str], *, top_n: int = 5
) -> dict[str, object]:
    """Summarize qualitative tags with counts, top themes, and co-occurrence."""
    normalized_rows = _normalize_rows(coded_rows)
    counts: Counter[str] = Counter()
    co_occurrence: Counter[tuple[str, str]] = Counter()

    for tags in normalized_rows:
        counts.update(tags)
        for pair in combinations(sorted(tags), 2):
            co_occurrence[pair] += 1

    top_themes = sorted(
        counts.items(), key=lambda item: (-item[1], item[0])
    )[:top_n]

    return {
        "counts": dict(counts),
        "top_themes": top_themes,
        "co_occurrence": dict(co_occurrence),
    }
