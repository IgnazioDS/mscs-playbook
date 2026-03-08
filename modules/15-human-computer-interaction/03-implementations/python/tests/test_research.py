from __future__ import annotations

import csv
from pathlib import Path

from src.hci_toolkit.research import HeuristicFinding, heuristic_report, qualitative_theme_report

FIXTURES = Path(__file__).parent / "fixtures"


def test_heuristic_report():
    findings = [
        HeuristicFinding("Consistency", 2),
        HeuristicFinding("Consistency", 3),
        HeuristicFinding("Visibility", 1),
    ]
    report = heuristic_report(findings)
    assert report["total"] == 3
    assert report["severity_counts"][1] == 1
    assert report["severity_counts"][2] == 1
    assert report["severity_counts"][3] == 1
    assert report["by_heuristic"]["Consistency"]["average_severity"] == 2.5


def test_qualitative_theme_report():
    with (FIXTURES / "qual_codes.csv").open() as handle:
        reader = csv.DictReader(handle)
        tags = [row["tags"] for row in reader]

    report = qualitative_theme_report(tags, top_n=3)
    assert report["counts"]["confusion"] == 3
    assert report["counts"]["login"] == 2
    assert report["co_occurrence"][("confusion", "login")] == 2

    assert report["top_themes"] == [
        ("confusion", 3),
        ("login", 2),
        ("search", 2),
    ]
