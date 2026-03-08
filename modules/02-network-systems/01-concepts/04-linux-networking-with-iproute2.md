# Linux Networking with iproute2

## What it is

The modern Linux networking suite for interfaces, routes, and neighbors.

## Why it matters

iproute2 is the fastest way to inspect and configure Linux networking.

## Core concepts (with short examples)

- Interfaces: `ip link`, `ip addr`.
- Routes: `ip route add 10.0.2.0/24 via 10.0.1.1`.
- Neighbors/ARP: `ip neigh`.
- Example: bring an interface up: `ip link set eth0 up`.

## Common failure modes

- Interface down or missing IP address.
- Wrong route priority or missing gateway.
- ARP failures due to VLAN or subnet mismatch.

## Debug checklist (commands)

- `ip link show`, `ip addr show`, `ip route show`.
- `ip neigh show`, `arp -n`.
- `ss -tuna` for sockets.

## References

- `man ip`, `man ip-route`
- Linux networking documentation
