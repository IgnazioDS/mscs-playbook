from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Iterable

from ..datasets import load_tiny_kb
from ..tools import ToolDispatcher
from ..vectorstore import ScoredDoc, TfidfVectorStore
from .reporting import write_markdown_report


@dataclass(frozen=True)
class AnalystResult:
    question: str
    plan_steps: list[str]
    tool_name: str
    tool_input: dict[str, Any]
    tool_output: Any
    final_answer: str


_PLAN_STEPS = [
    "1. Parse the question",
    "2. Select the best tool",
    "3. Execute the tool",
    "4. Provide a final answer",
]


def _format_retrieved(retrieved: Iterable[ScoredDoc]) -> str:
    lines = []
    for doc in retrieved:
        lines.append(f"- {doc.id} ({doc.score:.3f})")
    return "\n".join(lines) if lines else "- (none)"


def _choose_tool(question: str) -> str:
    lowered = question.lower()
    if re.search(r"[\d)][\s]*[+\-*/]", lowered) or re.search(r"\d", lowered) and any(
        op in lowered for op in ["+", "-", "*", "/", "(", ")"]
    ):
        return "calc"
    if any(keyword in lowered for keyword in ["policy", "kb", "knowledge", "handbook", "refund", "billing", "retention"]):
        return "lookup_kb"
    if len(lowered) > 140:
        return "summarize"
    return "summarize"


def run_agentic_analyst(question: str, out: str | None = None) -> str:
    store = TfidfVectorStore()
    store.fit(load_tiny_kb())
    dispatcher = ToolDispatcher(store)

    tool_name = _choose_tool(question)
    tool_input: dict[str, Any]
    tool_output: Any
    if tool_name == "calc":
        expression = re.sub(r"[^0-9+\-*/(). ]", "", question)
        tool_input = {"expression": expression.strip()}
        tool_output = dispatcher.call("calc", **tool_input)
        final_answer = f"Computed result: {tool_output:.3f}"
    elif tool_name == "lookup_kb":
        tool_input = {"query": question, "k": 2}
        tool_output = dispatcher.call("lookup_kb", **tool_input)
        retrieved = _format_retrieved(tool_output)
        final_answer = f"Found KB references:\n{retrieved}"
    else:
        tool_input = {"text": question}
        tool_output = dispatcher.call("summarize", **tool_input)
        final_answer = f"Summary: {tool_output.summary}"

    output_lines = [
        "task: agentic-analyst",
        "plan:",
        "\n".join(_PLAN_STEPS),
        "tool_call:",
        f"- name: {tool_name}",
        f"- input: {tool_input}",
        "tool_output:",
        _format_tool_output(tool_output),
        "final_answer:",
        final_answer,
    ]
    output = "\n".join(output_lines)

    if out:
        sections = [
            ("Question", question),
            ("Plan", "\n".join(_PLAN_STEPS)),
            ("Tool Call", f"name: {tool_name}\ninput: {tool_input}"),
            ("Tool Output", _format_tool_output(tool_output)),
            ("Final Answer", final_answer),
        ]
        write_markdown_report(out, "Agentic Data Analyst", sections)

    return output


def _format_tool_output(value: Any) -> str:
    if isinstance(value, list) and value and isinstance(value[0], ScoredDoc):
        return _format_retrieved(value)
    if hasattr(value, "model_dump"):
        return str(value.model_dump())
    if isinstance(value, float):
        return f"{value:.3f}"
    return str(value)
