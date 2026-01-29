from __future__ import annotations

from collections import defaultdict

from ..utils.rng import make_rng


def mc_prediction(env, policy: dict, episodes: int, gamma: float, seed: int) -> dict:
    rng = make_rng(seed)
    returns = defaultdict(list)
    V = {s: 0.0 for s in env.states()}

    def choose_action(state):
        actions = env.actions(state)
        if not actions:
            return None
        action_probs = policy.get(state)
        if isinstance(action_probs, str):
            return action_probs
        if action_probs is None:
            return actions[int(rng.randint(0, len(actions)))]
        probs = [action_probs[a] for a in actions]
        return actions[int(rng.choice(len(actions), p=probs))]

    for _ in range(episodes):
        state = env.reset()
        episode = []
        done = False
        while not done:
            action = choose_action(state)
            if action is None:
                break
            next_state, reward, done = env.step(state, action)
            episode.append((state, reward))
            state = next_state
        G = 0.0
        visited = set()
        for t in reversed(range(len(episode))):
            s, r = episode[t]
            G = gamma * G + r
            if s not in visited:
                returns[s].append(G)
                V[s] = sum(returns[s]) / len(returns[s])
                visited.add(s)
    return V
