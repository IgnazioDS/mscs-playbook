from src.nlp.mini_project.cli import run_cli


def test_cli_ticket_triage(capsys):
    run_cli(["ticket-triage", "--seed", "42"])
    out = capsys.readouterr().out
    assert "task: ticket-triage" in out
    assert "Results" in out


def test_cli_kb_search(capsys):
    run_cli(["kb-search", "--k", "3"])
    out = capsys.readouterr().out
    assert "task: kb-search" in out
    assert "query:" in out


def test_cli_evaluate(capsys):
    run_cli(["evaluate", "--seed", "42", "--k", "3"])
    out = capsys.readouterr().out
    assert "task: evaluate" in out
    assert "Retrieval metrics" in out
