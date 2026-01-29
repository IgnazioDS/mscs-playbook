from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from ..tools import summarize
from .reporting import write_markdown_report


SAMPLE_TRANSCRIPT = (
    "Alice: We need to ship the onboarding update by next Friday. "
    "Bob: I will draft the checklist and share it by Wednesday. "
    "Carla: Testing should cover the reset password flow and billing portal. "
    "Alice: Decision: prioritize the onboarding update over the analytics revamp."
)


@dataclass(frozen=True)
class MeetingSummary:
    summary: str
    bullets: list[str]


def _format_bullets(bullets: Iterable[str]) -> str:
    return "\n".join(f"- {bullet}" for bullet in bullets) if bullets else "- (none)"


def run_meeting_summarize(text: str | None = None, out: str | None = None) -> str:
    transcript = text or SAMPLE_TRANSCRIPT
    result = summarize(transcript)
    output_lines = [
        "task: meeting-summarize",
        "summary:",
        result.summary,
        "bullets:",
        _format_bullets(result.bullets),
    ]
    output = "\n".join(output_lines)
    if out:
        sections = [
            ("Input", transcript),
            ("Summary", result.summary),
            ("Bullets", _format_bullets(result.bullets)),
        ]
        write_markdown_report(out, "Meeting Notes Summary", sections)
    return output
