from __future__ import annotations

import numpy as np

from ..utils.rng import make_rng


def run_epsilon_greedy(bandit, steps: int, epsilon: float, seed: int) -> dict:
    rng = make_rng(seed)
    k = len(bandit.probs)
    counts = np.zeros(k, dtype=int)
    values = np.zeros(k, dtype=float)
    rewards = []
    regrets = []
    optimal = bandit.optimal_prob()

    for _ in range(steps):
        if rng.rand() < epsilon:
            action = int(rng.randint(0, k))
        else:
            action = int(np.argmax(values))
        reward = bandit.step(action)
        counts[action] += 1
        values[action] += (reward - values[action]) / counts[action]
        rewards.append(reward)
        regrets.append(optimal - reward)

    return {"counts": counts, "rewards": rewards, "regret": regrets}
