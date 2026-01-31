from __future__ import annotations

from typing import Callable

import numpy as np

from ..envs.gridworld import Gridworld


def policy_evaluation(
    env: Gridworld,
    policy: dict[tuple[int, int], dict[str, float] | str],
    gamma: float = 1.0,
    tol: float = 1e-6,
    max_iter: int = 1000,
) -> dict[tuple[int, int], float]:
    V = {s: 0.0 for s in env.states()}
    for _ in range(max_iter):
        delta = 0.0
        for s in env.states():
            if s in env.terminal_states:
                continue
            actions = env.actions(s)
            if not actions:
                continue
            action_probs: dict[str, float]
            if isinstance(policy.get(s), str):
                action_probs = {policy[s]: 1.0}
            else:
                action_probs = policy.get(s, {a: 1.0 / len(actions) for a in actions})
            new_val = 0.0
            for a, p in action_probs.items():
                s2, r, done = env.step(s, a)
                new_val += p * (r + (0.0 if done else gamma * V[s2]))
            delta = max(delta, abs(new_val - V[s]))
            V[s] = new_val
        if delta < tol:
            break
    return V
