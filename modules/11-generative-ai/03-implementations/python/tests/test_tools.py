import pytest

from src.genai.tools import ToolDispatcher, calc, summarize
from src.genai.datasets import load_tiny_kb
from src.genai.vectorstore import TfidfVectorStore


def test_calc_basic():
    assert calc("2+2*2") == 6.0


def test_calc_rejects_unsafe():
    with pytest.raises(ValueError):
        calc("__import__('os').system('echo hi')")


def test_summarize_output():
    result = summarize("First sentence. Second sentence.")
    assert result.summary == "First sentence"
    assert "Second sentence" in result.bullets


def test_tool_dispatcher_lookup():
    store = TfidfVectorStore()
    store.fit(load_tiny_kb())
    dispatcher = ToolDispatcher(store)
    results = dispatcher.call("lookup_kb", query="invoices", k=1)
    assert results[0].id == "kb-03"
