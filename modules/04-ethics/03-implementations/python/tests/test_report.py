from pathlib import Path

from src.ethics.mini_project.report import generate_report, load_inputs


FIXTURES = Path(__file__).resolve().parent / "fixtures" / "review_inputs"


def test_generate_report_matches_expected():
    inputs = load_inputs(
        "modules/04-ethics/03-implementations/python/tests/fixtures/review_inputs/complete"
    )
    report = generate_report(inputs, seed=42)
    expected = (Path(__file__).resolve().parent / "expected_report.md").read_text(encoding="utf-8")
    assert report == expected


def test_missing_inputs_reported():
    inputs = load_inputs(FIXTURES / "missing")
    report = generate_report(inputs, seed=7)
    assert "data.json" in report
    assert "overall_risk: HIGH" in report
    assert "gate: FAIL" in report
