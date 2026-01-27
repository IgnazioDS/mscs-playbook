"""Markdown reporting utilities."""

from __future__ import annotations

from typing import List, Tuple


def render_report(title: str, sections: List[Tuple[str, str]]) -> str:
    """Render a simple markdown report."""
    lines = [f"# {title}", ""]
    for header, body in sections:
        lines.append(f"## {header}")
        lines.append(body)
        lines.append("")
    return "\n".join(lines).strip() + "\n"
