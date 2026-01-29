from __future__ import annotations

import numpy as np


def td0_linear(env, feature_fn, alpha: float, gamma: float, episodes: int, seed: int) -> np.ndarray:
    rng = np.random.RandomState(seed)
    states = env.states()
    w = np.zeros(len(feature_fn(states[0])), dtype=np.float32)

    for _ in range(episodes):
        state = env.reset()
        done = False
        while not done:
            actions = env.actions(state)
            if not actions:
                break
            action = actions[int(rng.randint(0, len(actions)))]
            next_state, reward, done = env.step(state, action)
            phi = feature_fn(state)
            phi_next = feature_fn(next_state)
            td_target = reward + (0.0 if done else gamma * float(w @ phi_next))
            td_error = td_target - float(w @ phi)
            w += alpha * td_error * phi
            state = next_state
    return w


def value_from_weights(w: np.ndarray, feature_fn, state) -> float:
    return float(w @ feature_fn(state))
