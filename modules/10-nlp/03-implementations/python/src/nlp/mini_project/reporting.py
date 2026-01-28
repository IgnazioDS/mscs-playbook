"""Reporting helpers for the NLP mini-project."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, List


def build_report(
    title: str,
    setup_lines: Iterable[str],
    result_lines: Iterable[str],
    notes_lines: Iterable[str],
    reproducibility_lines: Iterable[str],
) -> str:
    sections = [
        f"# {title}",
        "",
        "## Setup",
        *_format_lines(setup_lines),
        "",
        "## Results",
        *_format_lines(result_lines),
        "",
        "## Notes",
        *_format_lines(notes_lines),
        "",
        "## Reproducibility",
        *_format_lines(reproducibility_lines),
        "",
    ]
    return "\n".join(sections).strip() + "\n"


def write_report(path: str, content: str) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return target


def _format_lines(lines: Iterable[str]) -> List[str]:
    formatted = []
    for line in lines:
        if line.strip() == "":
            continue
        formatted.append(f"- {line}")
    return formatted
