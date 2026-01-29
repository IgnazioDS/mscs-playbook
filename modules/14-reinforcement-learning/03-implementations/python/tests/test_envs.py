from src.rl.envs.gridworld import Gridworld
from src.rl.envs.chain import ChainEnv
from src.rl.envs.bandit import BernoulliBandit


def test_gridworld_step():
    env = Gridworld(width=2, height=2, terminal_states={(1, 1): 0.0}, step_cost=-1.0, start_state=(0, 0))
    s2, r, done = env.step((0, 0), "R")
    assert s2 == (0, 1)
    assert r == -1.0
    assert done is False


def test_chain_terminal():
    env = ChainEnv(length=3, start=1, reward_right=1.0)
    s2, r, done = env.step(1, "R")
    assert s2 == 2
    assert done is True
    assert r == 1.0


def test_bandit_step_deterministic():
    bandit = BernoulliBandit([0.0, 1.0], seed=0)
    assert bandit.step(0) == 0.0
    assert bandit.step(1) == 1.0
