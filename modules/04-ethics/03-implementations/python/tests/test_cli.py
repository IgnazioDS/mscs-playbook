from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[5]


def test_ethics_review_cli_matches_golden(tmp_path: Path) -> None:
    repo_root = _repo_root()
    cli_path = repo_root / "modules/04-ethics/03-implementations/python/src/ethics/mini_project/cli.py"
    input_dir = "modules/04-ethics/03-implementations/python/tests/fixtures/review_inputs/complete"
    output_path = tmp_path / "report.md"

    result = subprocess.run(
        [
            sys.executable,
            str(cli_path),
            "ethics-review",
            "--in",
            input_dir,
            "--out",
            str(output_path),
            "--seed",
            "42",
        ],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )

    expected = (
        repo_root / "modules/04-ethics/03-implementations/python/tests/expected_report.md"
    ).read_text(encoding="utf-8")
    actual = output_path.read_text(encoding="utf-8")

    assert actual == expected
    assert result.stdout == expected
