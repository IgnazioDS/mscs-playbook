from __future__ import annotations

from typing import Dict

from .mdp import MDP


def policy_evaluation(
    mdp: MDP,
    policy: dict[str, str],
    theta: float = 1e-6,
    max_iterations: int = 1000,
) -> dict[str, float]:
    V = {state: 0.0 for state in mdp.states}
    for _ in range(max_iterations):
        delta = 0.0
        for state in mdp.states:
            action = policy.get(state)
            if action is None:
                continue
            total = 0.0
            for next_state in mdp.next_states(state, action):
                prob = mdp.transition_prob(state, action, next_state)
                reward = mdp.reward(state, action, next_state)
                total += prob * (reward + mdp.gamma * V[next_state])
            delta = max(delta, abs(total - V[state]))
            V[state] = total
        if delta < theta:
            break
    return V
