from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[5]


def test_study_report_cli_matches_golden(tmp_path: Path) -> None:
    repo_root = _repo_root()
    cli_path = repo_root / "modules/15-hci/03-implementations/python/src/hci/mini_project/cli.py"
    input_dir = "modules/15-hci/03-implementations/python/tests/fixtures/study_csvs"
    output_path = tmp_path / "report.md"

    result = subprocess.run(
        [
            sys.executable,
            str(cli_path),
            "study-report",
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
        repo_root
        / "modules/15-hci/03-implementations/python/tests/fixtures/expected_report.md"
    ).read_text()
    actual = output_path.read_text()

    assert actual == expected
    assert result.stdout == expected


def test_study_report_cli_creates_parent_dir(tmp_path: Path) -> None:
    repo_root = _repo_root()
    cli_path = repo_root / "modules/15-hci/03-implementations/python/src/hci/mini_project/cli.py"
    input_dir = "modules/15-hci/03-implementations/python/tests/fixtures/study_csvs"
    output_path = tmp_path / "nested" / "report.md"

    subprocess.run(
        [
            sys.executable,
            str(cli_path),
            "study-report",
            "--in",
            input_dir,
            "--out",
            str(output_path),
        ],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )

    assert output_path.exists()
