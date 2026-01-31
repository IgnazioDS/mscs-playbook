import numpy as np

from src.rl.envs.bandit import BernoulliBandit
from src.rl.bandits.epsilon_greedy import run_epsilon_greedy
from src.rl.bandits.ucb1 import run_ucb1
from src.rl.bandits.thompson import run_thompson


def test_bandits_choose_best_arm():
    bandit = BernoulliBandit([0.2, 0.8], seed=0)
    result = run_epsilon_greedy(bandit, steps=200, epsilon=0.1, seed=0)
    assert result["counts"][1] > result["counts"][0]

    bandit = BernoulliBandit([0.2, 0.8], seed=0)
    result = run_ucb1(bandit, steps=200, seed=0)
    assert result["counts"][1] > result["counts"][0]

    bandit = BernoulliBandit([0.2, 0.8], seed=0)
    result = run_thompson(bandit, steps=200, seed=0)
    assert result["counts"][1] > result["counts"][0]


def test_thompson_posterior_update():
    bandit = BernoulliBandit([1.0], seed=0)
    result = run_thompson(bandit, steps=5, seed=0)
    assert np.all(result["alpha"] >= 1.0)
    assert np.all(result["beta"] >= 1.0)
