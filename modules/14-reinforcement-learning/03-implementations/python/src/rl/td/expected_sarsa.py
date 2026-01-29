from __future__ import annotations

from ..utils.rng import make_rng


def expected_sarsa(env, episodes: int, alpha: float, gamma: float, epsilon: float, seed: int) -> dict:
    rng = make_rng(seed)
    states = env.states()
    Q = {s: {a: 0.0 for a in env.actions(s)} for s in states}

    def policy_probs(state):
        actions = env.actions(state)
        if not actions:
            return {}
        best_action = max(actions, key=lambda a: Q[state][a])
        probs = {a: epsilon / len(actions) for a in actions}
        probs[best_action] += 1.0 - epsilon
        return probs

    def choose_action(state):
        actions = env.actions(state)
        if not actions:
            return None
        if rng.rand() < epsilon:
            return actions[int(rng.randint(0, len(actions)))]
        return max(actions, key=lambda a: Q[state][a])

    for _ in range(episodes):
        state = env.reset()
        done = False
        while not done:
            action = choose_action(state)
            if action is None:
                break
            next_state, reward, done = env.step(state, action)
            probs = policy_probs(next_state)
            expected = sum(Q[next_state][a] * p for a, p in probs.items()) if probs else 0.0
            target = reward + (0.0 if done else gamma * expected)
            Q[state][action] += alpha * (target - Q[state][action])
            state = next_state
    return Q
