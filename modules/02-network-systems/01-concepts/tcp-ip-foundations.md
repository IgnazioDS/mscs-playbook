# TCP/IP Foundations

## What it is
The layered model that moves data across networks: IP for routing, TCP/UDP for transport,
and application protocols on top.

## Why it matters
Understanding layers and responsibilities prevents misdiagnosis and speeds debugging.

## Core concepts (with short examples)
- IP delivers packets best-effort across hops; routers forward based on routes.
- TCP: connection-oriented, reliable stream (3-way handshake, retransmission).
- UDP: connectionless, best-effort datagrams (DNS queries, streaming).
- Example: HTTP over TCP vs DNS over UDP.

## Common failure modes
- MTU/fragmentation issues causing stalls.
- TCP SYN blocked by firewall; UDP silently dropped.
- Misrouted traffic due to incorrect default route.

## Debug checklist (commands)
- `ip addr`, `ip route` to verify local config.
- `ss -tuna` to confirm listening sockets.
- `tcpdump -n -i <iface>` to observe handshake and retransmits.

## References
- TCP/IP Illustrated, Vol. 1
- RFC 793 (TCP), RFC 768 (UDP)
