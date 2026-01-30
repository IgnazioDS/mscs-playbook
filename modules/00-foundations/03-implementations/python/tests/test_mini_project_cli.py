import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "src" / "foundations" / "mini_project" / "cli.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _run_cli(args: list[str]) -> str:
    result = subprocess.run(
        [sys.executable, str(CLI), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip().replace("\r\n", "\n")


def test_cli_stats_golden():
    expected = (FIXTURES / "expected_stats_report.txt").read_text(encoding="utf-8").strip()
    output = _run_cli(["stats", "--csv", str(FIXTURES / "numbers.csv")])
    assert output == expected


def test_cli_number_theory_smoke():
    output = _run_cli(["number-theory", "30", "18", "11"])
    assert "task: number-theory" in output
    assert "gcd: 6" in output
    assert "mod_inverse: 7" in output
