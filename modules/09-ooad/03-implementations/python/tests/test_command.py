from src.patterns.command import Counter, IncrementCommand


def test_command_execute_and_undo():
    counter = Counter()
    cmd = IncrementCommand(counter, amount=3)
    cmd.execute()
    assert counter.value == 3
    cmd.undo()
    assert counter.value == 0
