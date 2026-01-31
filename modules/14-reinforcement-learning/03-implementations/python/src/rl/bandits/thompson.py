from __future__ import annotations

import numpy as np

from ..utils.rng import make_rng


def run_thompson(bandit, steps: int, seed: int) -> dict:
    rng = make_rng(seed)
    k = len(bandit.probs)
    alpha = np.ones(k)
    beta = np.ones(k)
    counts = np.zeros(k, dtype=int)
    rewards = []
    regrets = []
    optimal = bandit.optimal_prob()

    for _ in range(steps):
        samples = rng.beta(alpha, beta)
        action = int(np.argmax(samples))
        reward = bandit.step(action)
        counts[action] += 1
        alpha[action] += reward
        beta[action] += 1 - reward
        rewards.append(reward)
        regrets.append(optimal - reward)

    return {"counts": counts, "rewards": rewards, "regret": regrets, "alpha": alpha, "beta": beta}
