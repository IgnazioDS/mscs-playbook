from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __name__ == "__main__" and __package__ is None:
    module_root = Path(__file__).resolve().parents[3]
    if str(module_root) not in sys.path:
        sys.path.insert(0, str(module_root))

from src.foundations.mini_project.core import (
    compute_stats,
    format_value,
    load_numbers_from_csv,
    matrix_summary,
    number_theory_summary,
    parse_numbers,
)


def _render_report(task: str, results: dict[str, object], seed: str = "n/a") -> str:
    lines = [f"task: {task}", f"seed: {seed}", "Results:"]
    for key, value in results.items():
        lines.append(f"  {key}: {format_value(value)}")
    return "\n".join(lines)


def _stats_command(args: argparse.Namespace) -> str:
    if args.csv:
        numbers = load_numbers_from_csv(args.csv)
    else:
        numbers = parse_numbers(args.nums)
    results = compute_stats(numbers)
    return _render_report("stats", results)


def _number_theory_command(args: argparse.Namespace) -> str:
    results = number_theory_summary(args.a, args.b, args.m)
    return _render_report("number-theory", results)


def _matrix_command(args: argparse.Namespace) -> str:
    results = matrix_summary(args.json)
    return _render_report("matrix", results)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Foundations Toolkit CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    stats_parser = subparsers.add_parser("stats", help="Compute basic statistics")
    stats_group = stats_parser.add_mutually_exclusive_group(required=True)
    stats_group.add_argument("--nums", type=str, help="Numbers as a space-separated string")
    stats_group.add_argument("--csv", type=str, help="Path to a CSV/text file of numbers")
    stats_parser.set_defaults(func=_stats_command)

    nt_parser = subparsers.add_parser("number-theory", help="Compute number theory utilities")
    nt_parser.add_argument("a", type=int, help="First integer")
    nt_parser.add_argument("b", type=int, help="Second integer")
    nt_parser.add_argument("m", type=int, help="Modulus for inverse")
    nt_parser.set_defaults(func=_number_theory_command)

    matrix_parser = subparsers.add_parser("matrix", help="Compute matrix operations")
    matrix_parser.add_argument("--json", type=str, help="JSON string with matrices a and b")
    matrix_parser.set_defaults(func=_matrix_command)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    output = args.func(args)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
