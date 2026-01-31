from src.ai.mini_project.route_planning import run_route_planning
from src.ai.mini_project.scheduling import run_schedule
from src.ai.mini_project.diagnosis import run_diagnosis


def test_route_plan_smoke():
    output = run_route_planning(seed=42)
    assert "task: route-plan" in output
    assert "path_len" in output
    assert "cost" in output


def test_schedule_smoke():
    output = run_schedule(seed=42)
    assert "task: schedule" in output
    assert "solved" in output
    assert "assignments" in output


def test_diagnose_smoke():
    output = run_diagnosis(seed=42)
    assert "task: diagnose" in output
    assert "P(Rain=1)" in output
