from __future__ import annotations

from ..utils.rng import make_rng


def mc_control(env, episodes: int, gamma: float, epsilon: float, seed: int) -> dict:
    rng = make_rng(seed)
    Q = {s: {a: 0.0 for a in env.actions(s)} for s in env.states()}
    returns = {s: {a: [] for a in env.actions(s)} for s in env.states()}

    def choose_action(state):
        actions = env.actions(state)
        if not actions:
            return None
        if rng.rand() < epsilon:
            return actions[int(rng.randint(0, len(actions)))]
        return max(actions, key=lambda a: Q[state][a])

    for _ in range(episodes):
        episode = []
        state = env.reset()
        done = False
        while not done:
            action = choose_action(state)
            if action is None:
                break
            next_state, reward, done = env.step(state, action)
            episode.append((state, action, reward))
            state = next_state
        G = 0.0
        visited = set()
        for t in reversed(range(len(episode))):
            s, a, r = episode[t]
            G = gamma * G + r
            if (s, a) not in visited:
                returns[s][a].append(G)
                Q[s][a] = sum(returns[s][a]) / len(returns[s][a])
                visited.add((s, a))
    return Q
