from __future__ import annotations

import numpy as np

from ..utils.rng import make_rng


def run_ucb1(bandit, steps: int, seed: int) -> dict:
    rng = make_rng(seed)
    k = len(bandit.probs)
    counts = np.zeros(k, dtype=int)
    values = np.zeros(k, dtype=float)
    rewards = []
    regrets = []
    optimal = bandit.optimal_prob()

    for t in range(1, steps + 1):
        if 0 in counts:
            action = int(np.argmin(counts))
        else:
            ucb = values + np.sqrt(2 * np.log(t) / counts)
            action = int(np.argmax(ucb))
        reward = bandit.step(action)
        counts[action] += 1
        values[action] += (reward - values[action]) / counts[action]
        rewards.append(reward)
        regrets.append(optimal - reward)

    return {"counts": counts, "rewards": rewards, "regret": regrets}
