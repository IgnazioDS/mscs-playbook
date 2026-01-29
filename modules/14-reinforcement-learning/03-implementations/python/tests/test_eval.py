from src.rl.eval.metrics import moving_avg
from src.rl.eval.curves import collect_returns


def test_moving_avg():
    values = [1, 2, 3, 4]
    assert moving_avg(values, window=2) == [1.0, 1.5, 2.5, 3.5]


def test_collect_returns_reproducible():
    def run(seed):
        return [seed, seed + 1]

    curves = collect_returns(run, seeds=[1, 1])
    assert curves[0].tolist() == curves[1].tolist()
