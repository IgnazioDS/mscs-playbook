from __future__ import annotations

import re

from .scenarios import run_gridworld_control, run_bandit_compare, run_reward_shaping


def run_evaluate() -> tuple[bool, str]:
    scenarios = [
        ("gridworld", lambda: run_gridworld_control(seed=42), ["gridworld-control", "final_avg_return", "success_rate"]),
        ("bandit", lambda: run_bandit_compare(seed=42), ["bandit-compare", "total_reward", "regret"]),
        ("shaping", lambda: run_reward_shaping(seed=42), ["reward-shaping", "baseline_final_avg_return", "shaped_final_avg_return"]),
    ]
    failures: list[str] = []
    for name, fn, expected in scenarios:
        output = format_output(fn())
        missing = [token for token in expected if token not in output]
        if missing:
            failures.append(f"{name}: missing {missing}")
            continue
        if name == "gridworld":
            success = _extract_float(output, "success_rate")
            if success is None or not (0.0 <= success <= 1.0):
                failures.append(f"{name}: success_rate out of range")
        if name == "bandit":
            best_rate = _extract_float(output, "best_pick_rate")
            if best_rate is None or not (0.2 <= best_rate <= 1.0):
                failures.append(f"{name}: best_pick_rate out of range")
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


def _extract_float(text: str, key: str) -> float | None:
    match = re.search(rf"{key}[:=]\s*([0-9.]+)", text)
    if not match:
        return None
    return float(match.group(1))


def format_output(result: dict) -> str:
    if result["task"] == "gridworld-control":
        lines = [
            "task: gridworld-control",
            f"algo: {result['algo']}",
            f"seed: {result['seed']}",
            f"episodes: {result['episodes']}",
            f"final_avg_return: {result['final_avg_return']:.3f}",
            f"success_rate: {result['success_rate']:.3f}",
            f"policy_preview: {result['policy_preview']}",
            f"curve_summary: first={result['curve_summary']['first']:.3f}, last={result['curve_summary']['last']:.3f}",
        ]
        return "\n".join(lines)
    if result["task"] == "bandit-compare":
        lines = [
            "task: bandit-compare",
            f"seed: {result['seed']}",
            f"steps: {result['steps']}",
            f"probs: {result['probs']}",
        ]
        for name in sorted(result["results"].keys()):
            metrics = result["results"][name]
            lines.append(
                f"{name}: total_reward={metrics['total_reward']:.3f}, regret={metrics['regret']:.3f}, best_pick_rate={metrics['best_pick_rate']:.3f}"
            )
        return "\n".join(lines)
    lines = [
        "task: reward-shaping",
        f"seed: {result['seed']}",
        f"episodes: {result['episodes']}",
        f"baseline_final_avg_return: {result['baseline_final_avg_return']:.3f}",
        f"shaped_final_avg_return: {result['shaped_final_avg_return']:.3f}",
        f"delta: {result['delta']:.3f}",
    ]
    return "\n".join(lines)
