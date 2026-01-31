from __future__ import annotations

from ..envs.gridworld import Gridworld


def value_iteration(
    env: Gridworld,
    gamma: float = 1.0,
    tol: float = 1e-6,
    max_iter: int = 1000,
) -> tuple[dict[tuple[int, int], float], dict[tuple[int, int], str]]:
    V = {s: 0.0 for s in env.states()}
    for _ in range(max_iter):
        delta = 0.0
        for s in env.states():
            if s in env.terminal_states:
                continue
            actions = env.actions(s)
            if not actions:
                continue
            values = []
            for a in actions:
                s2, r, done = env.step(s, a)
                values.append(r + (0.0 if done else gamma * V[s2]))
            new_val = max(values)
            delta = max(delta, abs(new_val - V[s]))
            V[s] = new_val
        if delta < tol:
            break

    policy: dict[tuple[int, int], str] = {}
    for s in env.states():
        if s in env.terminal_states:
            continue
        actions = env.actions(s)
        if not actions:
            continue
        best_action = max(actions, key=lambda a: env.step(s, a)[1] + gamma * V[env.step(s, a)[0]])
        policy[s] = best_action
    return V, policy
