from __future__ import annotations

from pathlib import Path
from typing import Iterable


def write_markdown_report(path: str | Path, title: str, sections: Iterable[tuple[str, str]]) -> Path:
    report_path = Path(path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# {title}", ""]
    for heading, content in sections:
        lines.append(f"## {heading}")
        lines.append("")
        lines.append(content.rstrip())
        lines.append("")
    report_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return report_path
