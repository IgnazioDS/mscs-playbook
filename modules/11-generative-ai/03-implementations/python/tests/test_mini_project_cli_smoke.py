from src.genai.mini_project.support_assistant import run_support_assistant
from src.genai.mini_project.meeting_summarizer import run_meeting_summarize
from src.genai.mini_project.agentic_analyst import run_agentic_analyst


def test_support_assistant_smoke():
    output = run_support_assistant("reset password", 2)
    assert "task: support-assistant" in output
    assert "retrieved:" in output
    assert "kb-02:0" in output
    assert "chunk:kb-02:0" in output


def test_meeting_summarize_smoke():
    output = run_meeting_summarize()
    assert "task: meeting-summarize" in output
    assert "summary:" in output
    assert "bullets:" in output


def test_agentic_analyst_smoke():
    output = run_agentic_analyst("What is (12*7) + 5?")
    assert "task: agentic-analyst" in output
    assert "tool_call:" in output
    assert "Computed result" in output
