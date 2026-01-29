from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np

from ..envs.gridworld import Gridworld
from ..envs.bandit import BernoulliBandit
from ..bandits.epsilon_greedy import run_epsilon_greedy
from ..bandits.ucb1 import run_ucb1
from ..bandits.thompson import run_thompson
from ..utils.rng import make_rng


def _round(value: float) -> float:
    return float(f"{value:.3f}")


def _mean(values: list[float]) -> float:
    if not values:
        return 0.0
    return float(np.mean(values))


def _epsilon_greedy(Q: dict, state, actions: list[str], epsilon: float, rng) -> str:
    if rng.rand() < epsilon:
        return actions[int(rng.randint(0, len(actions)))]
    return max(actions, key=lambda a: Q[state][a])


def _init_q(env: Gridworld) -> dict:
    return {s: {a: 0.0 for a in env.actions(s)} for s in env.states()}


def _train_td(
    env: Gridworld,
    algo: str,
    episodes: int,
    alpha: float,
    gamma: float,
    epsilon: float,
    seed: int,
    reward_shaping: Callable[[tuple[int, int], tuple[int, int], float], float] | None = None,
) -> tuple[dict, list[float]]:
    rng = make_rng(seed)
    Q = _init_q(env)
    returns: list[float] = []
    max_steps = env.width * env.height * 4

    for _ in range(episodes):
        state = env.reset()
        total = 0.0
        done = False
        steps = 0
        if algo == "sarsa":
            action = _epsilon_greedy(Q, state, env.actions(state), epsilon, rng)
        else:
            action = None
        while not done and steps < max_steps:
            if action is None:
                action = _epsilon_greedy(Q, state, env.actions(state), epsilon, rng)
            next_state, reward, done = env.step(state, action)
            if reward_shaping is not None:
                reward = reward_shaping(state, next_state, reward)
            total += reward
            if algo == "q_learning":
                next_actions = env.actions(next_state)
                next_val = max([Q[next_state][a] for a in next_actions], default=0.0)
                target = reward + (0.0 if done else gamma * next_val)
                Q[state][action] += alpha * (target - Q[state][action])
                action = None
            elif algo == "expected_sarsa":
                next_actions = env.actions(next_state)
                if next_actions:
                    best = max(next_actions, key=lambda a: Q[next_state][a])
                    probs = {a: epsilon / len(next_actions) for a in next_actions}
                    probs[best] += 1.0 - epsilon
                    expected = sum(Q[next_state][a] * p for a, p in probs.items())
                else:
                    expected = 0.0
                target = reward + (0.0 if done else gamma * expected)
                Q[state][action] += alpha * (target - Q[state][action])
                action = None
            else:  # sarsa
                next_actions = env.actions(next_state)
                next_action = _epsilon_greedy(Q, next_state, next_actions, epsilon, rng) if next_actions else None
                target = reward
                if not done and next_action is not None:
                    target += gamma * Q[next_state][next_action]
                Q[state][action] += alpha * (target - Q[state][action])
                action = next_action
            state = next_state
            steps += 1
        returns.append(total)
    return Q, returns


def run_gridworld_control(
    algo: str = "q_learning",
    episodes: int = 200,
    seed: int = 42,
    epsilon: float = 0.1,
    alpha: float = 0.5,
    gamma: float = 0.99,
) -> dict:
    env = Gridworld(width=4, height=4, terminal_states={(3, 3): 0.0}, step_cost=-1.0, start_state=(0, 0))
    Q, returns = _train_td(env, algo, episodes, alpha, gamma, epsilon, seed)

    window = min(10, len(returns))
    final_avg = _mean(returns[-window:])
    first_avg = _mean(returns[:window])

    # Evaluate greedy policy
    successes = 0
    eval_episodes = 50
    for _ in range(eval_episodes):
        state = env.reset()
        done = False
        steps = 0
        while not done and steps < env.width * env.height * 4:
            actions = env.actions(state)
            if not actions:
                break
            action = max(actions, key=lambda a: Q[state][a])
            next_state, _, done = env.step(state, action)
            state = next_state
            steps += 1
        if state in env.terminal_states:
            successes += 1

    success_rate = successes / eval_episodes

    policy_preview = []
    for state in sorted(env.states())[:5]:
        actions = env.actions(state)
        if not actions:
            continue
        action = max(actions, key=lambda a: Q[state][a])
        policy_preview.append((state, action))

    return {
        "task": "gridworld-control",
        "algo": algo,
        "seed": seed,
        "episodes": episodes,
        "final_avg_return": _round(final_avg),
        "success_rate": _round(success_rate),
        "policy_preview": policy_preview,
        "curve_summary": {"first": _round(first_avg), "last": _round(final_avg)},
    }


def run_bandit_compare(steps: int = 500, seed: int = 42) -> dict:
    probs = [0.2, 0.8, 0.5]
    results = {}
    for name, runner in [
        ("epsilon_greedy", lambda: run_epsilon_greedy(BernoulliBandit(probs, seed=seed), steps, 0.1, seed)),
        ("ucb1", lambda: run_ucb1(BernoulliBandit(probs, seed=seed), steps, seed)),
        ("thompson", lambda: run_thompson(BernoulliBandit(probs, seed=seed), steps, seed)),
    ]:
        output = runner()
        counts = output["counts"]
        total_reward = float(np.sum(output["rewards"]))
        total_regret = float(np.sum(output["regret"]))
        best_arm = int(np.argmax(probs))
        best_pick_rate = float(counts[best_arm] / steps)
        results[name] = {
            "total_reward": _round(total_reward),
            "regret": _round(total_regret),
            "best_pick_rate": _round(best_pick_rate),
        }

    return {
        "task": "bandit-compare",
        "seed": seed,
        "steps": steps,
        "probs": probs,
        "results": results,
    }


def run_reward_shaping(episodes: int = 200, seed: int = 42) -> dict:
    env = Gridworld(width=4, height=4, terminal_states={(3, 3): 0.0}, step_cost=-1.0, start_state=(0, 0))

    goal = (env.height - 1, env.width - 1)

    def potential(state):
        return -abs(state[0] - goal[0]) - abs(state[1] - goal[1])

    def shaping(s, s2, reward):
        return reward + 0.99 * potential(s2) - potential(s)

    Q_base, returns_base = _train_td(env, "q_learning", episodes, 0.5, 0.99, 0.1, seed)
    Q_shape, returns_shape = _train_td(env, "q_learning", episodes, 0.5, 0.99, 0.1, seed, reward_shaping=shaping)

    window = min(10, episodes)
    base_final = _mean(returns_base[-window:])
    shaped_final = _mean(returns_shape[-window:])

    return {
        "task": "reward-shaping",
        "seed": seed,
        "episodes": episodes,
        "baseline_final_avg_return": _round(base_final),
        "shaped_final_avg_return": _round(shaped_final),
        "delta": _round(shaped_final - base_final),
    }
