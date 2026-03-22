---
tags:
  - archive
  - 03-implementations
status: stable
---

# Lab 03: Packet Capture and Diagnosis

## Goal
Capture a simple HTTP exchange between a client and server using tcpdump.

## Requirements
- Docker with `docker compose` (works on macOS and Linux).

## Run
```
bash scripts/setup.sh
bash scripts/verify.sh
bash scripts/teardown.sh
```

## Alternative (manual)
```
docker compose up --build
# then
docker compose down
```

## Verification
- tcpdump output includes SYN/SYN-ACK/ACK and HTTP request/response.
- Client exits with HTTP 200.


## Related Concepts

- [TCP/IP Foundations](../../01-concepts/01-tcp-ip-foundations.md)
- [ARP, Switching, and L2/L3 Interaction](../../01-concepts/02-arp-switching-and-l2-l3-interaction.md)
- [Addressing, Routing, and Subnets](../../01-concepts/03-addressing-routing-and-subnets.md)
