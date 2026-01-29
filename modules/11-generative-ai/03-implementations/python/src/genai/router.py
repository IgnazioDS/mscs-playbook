from __future__ import annotations

import re
from typing import Any

from .datasets import load_tiny_kb
from .rag import RAGPipeline
from .schemas import ClassificationResult, ExtractionResult
from .tools import ToolDispatcher
from .vectorstore import ScoredDoc, TfidfVectorStore


_DOCS = load_tiny_kb()
_DOC_STORE = TfidfVectorStore()
_DOC_STORE.fit(_DOCS)
_RAG = RAGPipeline(_DOCS)
_TOOLS = ToolDispatcher(_DOC_STORE)


def _serialize(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        return value.model_dump()
    if isinstance(value, list) and value and isinstance(value[0], ScoredDoc):
        return [
            {"id": doc.id, "score": doc.score, "text": doc.text, "meta": doc.meta}
            for doc in value
        ]
    return value


def _classify(text: str) -> ClassificationResult:
    lowered = text.lower()
    if any(word in lowered for word in ["invoice", "payment", "refund"]):
        return ClassificationResult(label="billing", confidence=0.9)
    if any(word in lowered for word in ["error", "bug", "issue", "crash"]):
        return ClassificationResult(label="support", confidence=0.9)
    if any(word in lowered for word in ["price", "plan", "pricing"]):
        return ClassificationResult(label="sales", confidence=0.8)
    return ClassificationResult(label="general", confidence=0.6)


def _extract(text: str) -> ExtractionResult:
    items: list[dict[str, str]] = []
    emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    amounts = re.findall(r"\$\s?\d+(?:\.\d{2})?", text)
    for email in emails:
        items.append({"type": "email", "value": email})
    for amount in amounts:
        items.append({"type": "amount", "value": amount})
    return ExtractionResult(items=items)


def route(task: str, payload: dict[str, Any]) -> dict[str, Any]:
    if task == "classify":
        result = _classify(payload["text"])
        return result.model_dump()
    if task == "extract":
        result = _extract(payload["text"])
        return result.model_dump()
    if task == "rag_answer":
        query = payload["query"]
        k = payload.get("k", 3)
        contexts = _RAG.retrieve(query, k)
        answer = _RAG.synthesize(query, contexts)
        return {
            "answer": answer,
            "sources": [doc.id for doc in contexts],
        }
    if task == "tool_call":
        name = payload["name"]
        args = payload.get("args", {})
        result = _TOOLS.call(name, **args)
        return {"result": _serialize(result)}
    raise KeyError(f"Unknown task: {task}")
