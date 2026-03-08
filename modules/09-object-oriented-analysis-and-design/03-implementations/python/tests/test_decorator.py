from src.patterns.decorator import CoreService, TimingDecorator


def test_decorator_preserves_behavior_and_adds_timing():
    svc = CoreService()
    wrapped = TimingDecorator(svc)
    result = wrapped.run("hello")
    assert result == "HELLO"
    assert wrapped.last_ms is not None
