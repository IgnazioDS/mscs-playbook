from __future__ import annotations

import numpy as np

from ..utils.rng import make_rng


def sarsa(env, episodes: int, alpha: float, gamma: float, epsilon: float, seed: int) -> dict:
    rng = make_rng(seed)
    states = env.states()
    Q = {s: {a: 0.0 for a in env.actions(s)} for s in states}

    def choose_action(state):
        actions = env.actions(state)
        if not actions:
            return None
        if rng.rand() < epsilon:
            return actions[int(rng.randint(0, len(actions)))]
        return max(actions, key=lambda a: Q[state][a])

    for _ in range(episodes):
        state = env.reset()
        action = choose_action(state)
        done = False
        while not done and action is not None:
            next_state, reward, done = env.step(state, action)
            next_action = choose_action(next_state)
            target = reward
            if not done and next_action is not None:
                target += gamma * Q[next_state][next_action]
            Q[state][action] += alpha * (target - Q[state][action])
            state, action = next_state, next_action
    return Q
