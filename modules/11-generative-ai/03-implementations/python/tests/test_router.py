from src.genai.router import route


def test_route_classify():
    result = route("classify", {"text": "Invoice for last month"})
    assert result["label"] == "billing"


def test_route_extract():
    result = route("extract", {"text": "Email alice@example.com about $50.00"})
    values = {item["value"] for item in result["items"]}
    assert "alice@example.com" in values
    assert "$50.00" in values


def test_route_rag_answer():
    result = route("rag_answer", {"query": "reset password", "k": 1})
    assert result["sources"] == ["kb-02:0"]


def test_route_tool_call():
    result = route("tool_call", {"name": "calc", "args": {"expression": "3+3"}})
    assert result["result"] == 6.0
