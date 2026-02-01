from src.ns02.addresses import summarize_subnet


def test_summarize_subnet_ipv4():
    info = summarize_subnet("10.0.0.0/24")
    assert info["network"] == "10.0.0.0"
    assert info["broadcast"] == "10.0.0.255"
    assert info["prefix"] == 24
    assert info["hosts"] == 254


def test_summarize_subnet_handles_host_bits():
    info = summarize_subnet("192.168.1.10/24")
    assert info["network"] == "192.168.1.0"
