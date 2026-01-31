from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __name__ == "__main__" and __package__ is None:
    repo_root = Path(__file__).resolve().parents[3]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

from src.rl.mini_project.scenarios import (
    run_bandit_compare,
    run_gridworld_control,
    run_reward_shaping,
)
from src.rl.mini_project.evaluate import run_evaluate, format_output
from src.rl.mini_project.reporting import write_markdown_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="RL mini-project CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    grid = subparsers.add_parser("gridworld-control", help="Run gridworld control comparison")
    grid.add_argument("--algo", choices=["q_learning", "sarsa", "expected_sarsa"], default="q_learning")
    grid.add_argument("--episodes", type=int, default=200)
    grid.add_argument("--seed", type=int, default=42)
    grid.add_argument("--epsilon", type=float, default=0.1)
    grid.add_argument("--alpha", type=float, default=0.5)
    grid.add_argument("--gamma", type=float, default=0.99)
    grid.add_argument("--out")

    bandit = subparsers.add_parser("bandit-compare", help="Run bandit comparison")
    bandit.add_argument("--steps", type=int, default=500)
    bandit.add_argument("--seed", type=int, default=42)
    bandit.add_argument("--out")

    shaping = subparsers.add_parser("reward-shaping", help="Run reward shaping comparison")
    shaping.add_argument("--episodes", type=int, default=200)
    shaping.add_argument("--seed", type=int, default=42)
    shaping.add_argument("--out")

    subparsers.add_parser("evaluate", help="Run deterministic checks")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "gridworld-control":
        result = run_gridworld_control(
            algo=args.algo,
            episodes=args.episodes,
            seed=args.seed,
            epsilon=args.epsilon,
            alpha=args.alpha,
            gamma=args.gamma,
        )
        output = format_output(result)
        print(output)
        if args.out:
            sections = [
                ("Command", "gridworld-control"),
                ("Inputs", f"algo: {args.algo}\nseed: {args.seed}\nepisodes: {args.episodes}"),
                ("Outputs", output),
            ]
            write_markdown_report(args.out, "Gridworld Control Report", sections, notes="Tabular TD control on gridworld.")
        return 0

    if args.command == "bandit-compare":
        result = run_bandit_compare(steps=args.steps, seed=args.seed)
        output = format_output(result)
        print(output)
        if args.out:
            sections = [
                ("Command", "bandit-compare"),
                ("Inputs", f"seed: {args.seed}\nsteps: {args.steps}"),
                ("Outputs", output),
            ]
            write_markdown_report(args.out, "Bandit Comparison Report", sections, notes="Bandit algorithms on fixed probs.")
        return 0

    if args.command == "reward-shaping":
        result = run_reward_shaping(episodes=args.episodes, seed=args.seed)
        output = format_output(result)
        print(output)
        if args.out:
            sections = [
                ("Command", "reward-shaping"),
                ("Inputs", f"seed: {args.seed}\nepisodes: {args.episodes}"),
                ("Outputs", output),
            ]
            write_markdown_report(args.out, "Reward Shaping Report", sections, notes="Baseline vs shaped reward.")
        return 0

    if args.command == "evaluate":
        passed, report = run_evaluate()
        print(report)
        return 0 if passed else 1

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
