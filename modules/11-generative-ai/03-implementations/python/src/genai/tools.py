from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import ast
import re

from .schemas import SummaryResult
from .vectorstore import ScoredDoc, TfidfVectorStore


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    input_schema: dict


BUILTIN_TOOL_SPECS = {
    "calc": ToolSpec(
        name="calc",
        description="Evaluate a basic arithmetic expression.",
        input_schema={"type": "object", "properties": {"expression": {"type": "string"}}},
    ),
    "lookup_kb": ToolSpec(
        name="lookup_kb",
        description="Retrieve top matching documents from the local KB.",
        input_schema={
            "type": "object",
            "properties": {"query": {"type": "string"}, "k": {"type": "integer"}},
        },
    ),
    "summarize": ToolSpec(
        name="summarize",
        description="Summarize text into a short summary and bullets.",
        input_schema={"type": "object", "properties": {"text": {"type": "string"}}},
    ),
}


_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.UAdd,
    ast.USub,
    ast.Constant,
)


def _eval_ast(node: ast.AST) -> float:
    if not isinstance(node, _ALLOWED_NODES):
        raise ValueError("Unsafe expression")
    if isinstance(node, ast.Expression):
        return _eval_ast(node.body)
    if isinstance(node, ast.Constant):
        if not isinstance(node.value, (int, float)):
            raise ValueError("Unsupported literal")
        return float(node.value)
    if isinstance(node, ast.UnaryOp):
        value = _eval_ast(node.operand)
        if isinstance(node.op, ast.UAdd):
            return value
        if isinstance(node.op, ast.USub):
            return -value
    if isinstance(node, ast.BinOp):
        left = _eval_ast(node.left)
        right = _eval_ast(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            return left / right
    raise ValueError("Unsupported expression")


def calc(expression: str) -> float:
    parsed = ast.parse(expression, mode="eval")
    return _eval_ast(parsed)


def lookup_kb(query: str, store: TfidfVectorStore, k: int = 3) -> list[ScoredDoc]:
    return store.query(query, k)


def summarize(text: str) -> SummaryResult:
    sentences = [s.strip() for s in re.split(r"[.!?]", text) if s.strip()]
    summary = sentences[0] if sentences else text.strip()
    bullets = sentences[:3] if sentences else ([] if not text.strip() else [text.strip()])
    return SummaryResult(summary=summary, bullets=bullets)


class ToolDispatcher:
    def __init__(self, store: TfidfVectorStore) -> None:
        self._store = store

    def call(self, name: str, **kwargs: Any) -> Any:
        if name == "calc":
            return calc(kwargs["expression"])
        if name == "lookup_kb":
            return lookup_kb(kwargs["query"], self._store, kwargs.get("k", 3))
        if name == "summarize":
            return summarize(kwargs["text"])
        raise KeyError(f"Unknown tool: {name}")
