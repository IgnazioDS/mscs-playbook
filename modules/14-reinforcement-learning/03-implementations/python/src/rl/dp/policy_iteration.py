from __future__ import annotations

from ..envs.gridworld import Gridworld
from .policy_eval import policy_evaluation


def policy_iteration(
    env: Gridworld,
    gamma: float = 1.0,
    tol: float = 1e-6,
    max_iter: int = 1000,
) -> tuple[dict[tuple[int, int], float], dict[tuple[int, int], str]]:
    policy = {s: "U" for s in env.states() if s not in env.terminal_states}
    for _ in range(max_iter):
        V = policy_evaluation(env, policy, gamma=gamma, tol=tol, max_iter=max_iter)
        policy_stable = True
        for s in env.states():
            if s in env.terminal_states:
                continue
            actions = env.actions(s)
            if not actions:
                continue
            best_action = max(actions, key=lambda a: env.step(s, a)[1] + gamma * V[env.step(s, a)[0]])
            if policy.get(s) != best_action:
                policy_stable = False
                policy[s] = best_action
        if policy_stable:
            return V, policy
    return V, policy
