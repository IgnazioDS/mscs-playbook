"""Deterministic address parsing helpers."""

from __future__ import annotations

from ipaddress import ip_network


def summarize_subnet(cidr: str) -> dict:
    """Return basic subnet metadata for a CIDR string."""
    net = ip_network(cidr, strict=False)
    hosts = max(net.num_addresses - 2, 0)
    return {
        "network": str(net.network_address),
        "broadcast": str(net.broadcast_address),
        "prefix": net.prefixlen,
        "hosts": hosts,
    }
