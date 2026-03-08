import pytest

from src.patterns.adapter import LegacyGateway, LegacyGatewayAdapter


def test_adapter_success():
    adapter = LegacyGatewayAdapter(LegacyGateway())
    result = adapter.pay(500)
    assert result == "legacy:500"


def test_adapter_translates_error():
    adapter = LegacyGatewayAdapter(LegacyGateway())
    with pytest.raises(RuntimeError):
        adapter.pay(0)
