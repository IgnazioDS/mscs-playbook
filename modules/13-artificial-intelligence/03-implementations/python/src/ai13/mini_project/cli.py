from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __name__ == "__main__" and __package__ is None:
    repo_root = Path(__file__).resolve().parents[3]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

from src.ai.mini_project.route_planning import run_route_planning
from src.ai.mini_project.scheduling import run_schedule
from src.ai.mini_project.diagnosis import run_diagnosis
from src.ai.mini_project.evaluation import run_evaluate


def _format_output(output: str) -> str:
    return output.replace("density: ", "density: ")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AI13 Mini-Project CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    route = subparsers.add_parser("route-plan", help="Run A* route planning")
    route.add_argument("--seed", type=int, default=42)
    route.add_argument("--size", type=int, default=10)
    route.add_argument("--density", type=float, default=0.18)
    route.add_argument("--out")

    schedule = subparsers.add_parser("schedule", help="Run CSP scheduling")
    schedule.add_argument("--seed", type=int, default=42)
    schedule.add_argument("--out")

    diagnose = subparsers.add_parser("diagnose", help="Run Bayes net diagnosis")
    diagnose.add_argument("--seed", type=int, default=42)
    diagnose.add_argument("--out")

    evaluate = subparsers.add_parser("evaluate", help="Run deterministic checks")
    evaluate.add_argument("--seed", type=int, default=42)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "route-plan":
        output = run_route_planning(seed=args.seed, size=args.size, density=args.density, out=args.out)
        print(_format_output(output))
        return 0
    if args.command == "schedule":
        output = run_schedule(seed=args.seed, out=args.out)
        print(_format_output(output))
        return 0
    if args.command == "diagnose":
        output = run_diagnosis(seed=args.seed, out=args.out)
        print(_format_output(output))
        return 0
    if args.command == "evaluate":
        passed, report = run_evaluate()
        summary = f"seed: {args.seed}\n{report}"
        print(summary)
        return 0 if passed else 1

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
