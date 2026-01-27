# Addressing, Routing, Subnets

## What it is

IP addressing and subnetting define network boundaries, while routing decides
how packets move between them.

## Why it matters

Most real outages are misconfigured routes, masks, or gateways.

## Core concepts (with short examples)

- CIDR: `/24` means 256 addresses (e.g., `10.0.1.0/24`).
- Default gateway forwards non-local traffic.
- Longest-prefix match selects the most specific route.
- Example: route `10.0.2.0/24` via `10.0.1.1`.

## Common failure modes

- Wrong subnet mask causing ARP for remote hosts.
- Missing default route; traffic never leaves the host.
- Overlapping subnets leading to ambiguous routing.

## Debug checklist (commands)

- `ip addr show`, `ip route show`, `ip neigh show`.
- `ping -c 2 <gateway>` then `ping -c 2 <remote>`.
- `traceroute -n <remote>` to identify routing breaks.

## References

- RFC 4632 (CIDR)
- Linux iproute2 documentation
