from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from ..datasets import load_tiny_kb
from ..rag import RAGPipeline
from ..vectorstore import ScoredDoc
from .reporting import write_markdown_report


@dataclass(frozen=True)
class SupportResult:
    query: str
    k: int
    retrieved: list[ScoredDoc]
    answer: str


def _format_retrieved(retrieved: Iterable[ScoredDoc]) -> str:
    lines = []
    for doc in retrieved:
        lines.append(f"- {doc.id} ({doc.score:.3f})")
    return "\n".join(lines) if lines else "- (none)"


def _format_answer(query: str, contexts: list[ScoredDoc]) -> str:
    if not contexts:
        return f"Answer: No sources found for '{query}'."
    citations = ", ".join(f"chunk:{doc.id}" for doc in contexts)
    return f"Answer: Use retrieved context to respond to '{query}'. Sources: [{citations}]"


def run_support_assistant(query: str, k: int = 3, out: str | None = None) -> str:
    rag = RAGPipeline(load_tiny_kb())
    retrieved = rag.retrieve(query, k)
    answer = _format_answer(query, retrieved)
    output_lines = [
        "task: support-assistant",
        f"k: {k}",
        f"query: {query}",
        "retrieved:",
        _format_retrieved(retrieved),
        f"answer: {answer}",
    ]
    output = "\n".join(output_lines)
    if out:
        sections = [
            ("Input", f"- query: {query}\n- k: {k}"),
            ("Retrieved", _format_retrieved(retrieved)),
            ("Answer", answer),
        ]
        write_markdown_report(out, "RAG Support Assistant", sections)
    return output
