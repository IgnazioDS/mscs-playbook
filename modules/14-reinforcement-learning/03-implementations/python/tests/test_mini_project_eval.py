from src.rl.mini_project.evaluate import run_evaluate


def test_run_evaluate_passes():
    passed, report = run_evaluate()
    assert passed is True
    assert "task: evaluate" in report
    assert "failed: 0" in report
