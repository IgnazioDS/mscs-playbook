import subprocess
import sys
from pathlib import Path


def test_cli_train_classifier_smoke():
    cli_path = Path(__file__).resolve().parents[2] / "src" / "cli.py"
    result = subprocess.run(
        [
            sys.executable,
            str(cli_path),
            "train-classifier",
            "--dataset",
            "iris",
            "--seed",
            "42",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    stdout = result.stdout.lower()
    assert "dataset" in stdout
    assert "accuracy" in stdout
