from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __name__ == "__main__" and __package__ is None:
    repo_root = Path(__file__).resolve().parents[3]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

from src.cv.mini_project.defect_detection import run_defect_detection
from src.cv.mini_project.document_ocr_lite import run_doc_ocr_lite
from src.cv.mini_project.evaluation import run_evaluate
from src.cv.mini_project.shelf_availability import run_shelf_availability


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Local CV mini-project CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    defect = subparsers.add_parser("defect-detect", help="Run toy defect detection")
    defect.add_argument("--seed", type=int, default=42)
    defect.add_argument("--iou", type=float, default=0.5)
    defect.add_argument("--out")

    doc = subparsers.add_parser("doc-ocr-lite", help="Run OCR-lite pipeline")
    doc.add_argument("--seed", type=int, default=42)
    doc.add_argument("--out")

    shelf = subparsers.add_parser("shelf-availability", help="Run shelf availability classifier")
    shelf.add_argument("--seed", type=int, default=42)
    shelf.add_argument("--out")

    subparsers.add_parser("evaluate", help="Run built-in deterministic checks")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "defect-detect":
        print(run_defect_detection(seed=args.seed, iou=args.iou, out=args.out))
        return 0
    if args.command == "doc-ocr-lite":
        print(run_doc_ocr_lite(seed=args.seed, out=args.out))
        return 0
    if args.command == "shelf-availability":
        print(run_shelf_availability(seed=args.seed, out=args.out))
        return 0
    if args.command == "evaluate":
        passed, report = run_evaluate()
        print(report)
        return 0 if passed else 1
    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
