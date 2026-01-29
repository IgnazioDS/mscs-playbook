from __future__ import annotations

from typing import Dict

from .mdp import MDP


def value_iteration(mdp: MDP, theta: float = 1e-6, max_iterations: int = 1000) -> tuple[dict[str, float], dict[str, str]]:
    V = {state: 0.0 for state in mdp.states}
    for _ in range(max_iterations):
        delta = 0.0
        for state in mdp.states:
            action_values = []
            for action in mdp.actions.get(state, []):
                total = 0.0
                for next_state in mdp.next_states(state, action):
                    prob = mdp.transition_prob(state, action, next_state)
                    reward = mdp.reward(state, action, next_state)
                    total += prob * (reward + mdp.gamma * V[next_state])
                action_values.append(total)
            best = max(action_values) if action_values else 0.0
            delta = max(delta, abs(best - V[state]))
            V[state] = best
        if delta < theta:
            break

    policy: dict[str, str] = {}
    for state in mdp.states:
        best_action = None
        best_value = float("-inf")
        for action in mdp.actions.get(state, []):
            total = 0.0
            for next_state in mdp.next_states(state, action):
                prob = mdp.transition_prob(state, action, next_state)
                reward = mdp.reward(state, action, next_state)
                total += prob * (reward + mdp.gamma * V[next_state])
            if total > best_value:
                best_value = total
                best_action = action
        if best_action is not None:
            policy[state] = best_action
    return V, policy
