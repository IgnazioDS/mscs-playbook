from __future__ import annotations

import argparse
import sys
from pathlib import Path


if __name__ == "__main__" and __package__ is None:
    repo_root = Path(__file__).resolve().parents[3]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

from src.genai.mini_project.agentic_analyst import run_agentic_analyst
from src.genai.mini_project.meeting_summarizer import run_meeting_summarize
from src.genai.mini_project.support_assistant import run_support_assistant


def run_evaluate() -> tuple[bool, str]:
    scenarios = [
        ("support", lambda: run_support_assistant("reset password", 2, None), ["kb-02:0", "support-assistant"]),
        ("support", lambda: run_support_assistant("invoice download", 2, None), ["kb-03:0", "retrieved"]),
        ("meeting", lambda: run_meeting_summarize(None, None), ["meeting-summarize", "bullets"]),
        ("analyst", lambda: run_agentic_analyst("What is (12*7) + 5?", None), ["agentic-analyst", "Computed result"]),
    ]
    failures: list[str] = []
    outputs: list[str] = []
    for name, fn, expected in scenarios:
        output = fn()
        outputs.append(output)
        missing = [token for token in expected if token not in output]
        if missing:
            failures.append(f"{name}: missing {missing}")
    passed = len(failures) == 0
    summary_lines = [
        "task: evaluate",
        f"scenarios: {len(scenarios)}",
        f"passed: {len(scenarios) - len(failures)}",
        f"failed: {len(failures)}",
    ]
    if failures:
        summary_lines.append("failures:")
        summary_lines.extend(f"- {failure}" for failure in failures)
    report = "\n".join(summary_lines)
    return passed, report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Local GenAI mini-project CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    support = subparsers.add_parser("support-assistant", help="Run the RAG support assistant")
    support.add_argument("--query", required=True)
    support.add_argument("--k", type=int, default=3)
    support.add_argument("--out")

    meeting = subparsers.add_parser("meeting-summarize", help="Summarize meeting notes")
    meeting.add_argument("--text")
    meeting.add_argument("--out")

    analyst = subparsers.add_parser("agentic-analyst", help="Run the agentic analyst")
    analyst.add_argument("--question", required=True)
    analyst.add_argument("--out")

    evaluate = subparsers.add_parser("evaluate", help="Run built-in deterministic checks")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "support-assistant":
        output = run_support_assistant(args.query, args.k, args.out)
        print(output)
        return 0
    if args.command == "meeting-summarize":
        output = run_meeting_summarize(args.text, args.out)
        print(output)
        return 0
    if args.command == "agentic-analyst":
        output = run_agentic_analyst(args.question, args.out)
        print(output)
        return 0
    if args.command == "evaluate":
        passed, report = run_evaluate()
        print(report)
        return 0 if passed else 1
    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
