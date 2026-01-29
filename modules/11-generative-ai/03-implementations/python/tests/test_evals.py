from src.genai.datasets import load_goldens
from src.genai.evals import run_goldens


def test_run_goldens_pass():
    cases = load_goldens()
    report = run_goldens(cases)
    assert report["failed"] == 0
