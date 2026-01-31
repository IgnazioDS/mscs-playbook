from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __name__ == "__main__" and __package__ is None:
    module_root = Path(__file__).resolve().parents[3]
    if str(module_root) not in sys.path:
        sys.path.insert(0, str(module_root))

from src.ethics.mini_project.report import generate_report, load_inputs


def _write_report(output_path: Path, content: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")


def _ethics_review(args: argparse.Namespace) -> str:
    inputs = load_inputs(args.input_dir)
    report = generate_report(inputs, seed=args.seed)
    output_path = Path(args.output_path)
    _write_report(output_path, report)
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Ethics Review CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    review_parser = subparsers.add_parser("ethics-review", help="Generate an ethics review report")
    review_parser.add_argument("--in", dest="input_dir", required=True, help="Input directory")
    review_parser.add_argument("--out", dest="output_path", required=True, help="Output report path")
    review_parser.add_argument("--seed", type=int, default=None, help="Optional seed for reporting")
    review_parser.set_defaults(func=_ethics_review)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    output = args.func(args)
    print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
