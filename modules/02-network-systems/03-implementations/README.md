---
summary: Overview and references for 02 network systems 03 implementations.
status: stable
tags:
  - archive
  - 03-implementations
---

# Network Systems Labs

## Lab 01: Namespaces + Routing
- Linux-only (network namespaces). macOS: run in a privileged Linux container or VM.
- `bash lab-01-namespaces-routing/scripts/setup.sh`
- `bash lab-01-namespaces-routing/scripts/verify.sh`
- `bash lab-01-namespaces-routing/scripts/teardown.sh`

## Lab 02: NAT + Firewall
- Linux-only (iptables). macOS: run in a privileged Linux container or VM.
- `bash lab-02-nat-firewall/scripts/setup.sh`
- `bash lab-02-nat-firewall/scripts/verify.sh`
- `bash lab-02-nat-firewall/scripts/teardown.sh`

## Lab 03: tcpdump Diagnosis (Docker)
- Docker-only; works on macOS and Linux.
- `bash lab-03-tcpdump-diagnosis/scripts/setup.sh`
- `bash lab-03-tcpdump-diagnosis/scripts/verify.sh`
- `bash lab-03-tcpdump-diagnosis/scripts/teardown.sh`


## Related Concepts

- [TCP/IP Foundations](../01-concepts/01-tcp-ip-foundations.md)
- [ARP, Switching, and L2/L3 Interaction](../01-concepts/02-arp-switching-and-l2-l3-interaction.md)
- [Addressing, Routing, and Subnets](../01-concepts/03-addressing-routing-and-subnets.md)
