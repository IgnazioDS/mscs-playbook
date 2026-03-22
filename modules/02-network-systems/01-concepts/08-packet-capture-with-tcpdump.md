---
tags:
  - archive
  - 01-concepts
status: stable
---

# Packet Capture with tcpdump

## What it is

tcpdump captures packets for low-level inspection and verification.

## Why it matters

It reveals what is actually on the wire, beyond assumptions and logs.

## Core concepts (with short examples)

- Capture interface: `tcpdump -i eth0 -n`.
- Filter by port: `tcpdump -n -i eth0 port 443`.
- Follow handshake: SYN/SYN-ACK/ACK sequence.
- Example: capture DNS: `tcpdump -n -i eth0 port 53`.

## Common failure modes

- Capturing on the wrong interface.
- Packet drops due to buffer limits.
- Misreading directionality without `-n` or `-vv`.

## Debug checklist (commands)

- `tcpdump -D` to list interfaces.
- `tcpdump -n -i <iface> -c 20` for quick samples.
- `ss -tuna` to map sockets to ports.

## References

- tcpdump and libpcap documentation
- The TCPdump Workshop (training notes)


## Related Concepts

- [TCP/IP Foundations](01-tcp-ip-foundations.md)
- [ARP, Switching, and L2/L3 Interaction](02-arp-switching-and-l2-l3-interaction.md)
- [Addressing, Routing, and Subnets](03-addressing-routing-and-subnets.md)
