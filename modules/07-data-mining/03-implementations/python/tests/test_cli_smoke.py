import subprocess
import sys
from pathlib import Path


def _run_cli(args):
    cli_path = Path(__file__).resolve().parents[1] / "src" / "cli.py"
    return subprocess.run(
        [sys.executable, str(cli_path), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_cli_cluster():
    result = _run_cli(["cluster", "--dataset", "iris", "--k", "3", "--seed", "42"])
    assert result.returncode == 0
    assert "task: cluster" in result.stdout
    assert "Results" in result.stdout


def test_cli_anomaly():
    result = _run_cli(["anomaly", "--dataset", "breast_cancer", "--seed", "42", "--contamination", "0.05"])
    assert result.returncode == 0
    assert "task: anomaly" in result.stdout


def test_cli_basket():
    result = _run_cli(["basket", "--dataset", "tiny_baskets", "--min-support", "0.2", "--min-confidence", "0.6", "--seed", "42"])
    assert result.returncode == 0
    assert "task: basket" in result.stdout
