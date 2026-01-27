# 02-network-systems

## Status

- Concepts, cheat sheet, case study, and labs are complete.
- Labs are Docker-first with Linux namespace/iptables notes and fallbacks.

## Overview

This module focuses on practical network systems: addressing, routing, DNS, TCP/UDP,
and reproducible Linux networking labs. It emphasizes tooling (iproute2, iptables,
tcpdump) and a troubleshooting workflow you can run locally and repeat.

## Prerequisites

- Docker installed (Docker Desktop or Engine)
- Linux host recommended for namespace/iptables labs

## OS constraints

- Lab 01 and Lab 02 require Linux kernel features (network namespaces, iptables).
  On macOS, run them inside a privileged Linux container or a Linux VM.
- Lab 03 is Docker-only and runs on macOS and Linux.

## Concepts

- [TCP/IP Foundations](01-concepts/tcp-ip-foundations.md)
- [Addressing, Routing, Subnets](01-concepts/addressing-routing-subnets.md)
- [DNS and Name Resolution](01-concepts/dns-and-name-resolution.md)
- [Linux Networking with iproute2](01-concepts/linux-networking-iproute2.md)
- [Namespaces, veth, Bridges](01-concepts/namespaces-veth-bridges.md)
- [Firewalling and NAT (iptables)](01-concepts/firewalling-nat-iptables.md)
- [Packet Capture with tcpdump](01-concepts/packet-capture-tcpdump.md)
- [Cloud Networking Mental Models](01-concepts/cloud-networking-mental-models.md)

## Cheat sheet

- [Networking Cheat Sheet](02-cheatsheets/networking-cheatsheet.md)

## Case study

- [Debugging Playbook](04-case-studies/debugging-playbook.md)

## Labs

- Lab 01: Namespaces + Routing
  - `bash modules/02-network-systems/03-implementations/lab-01-namespaces-routing/scripts/setup.sh`
  - `bash modules/02-network-systems/03-implementations/lab-01-namespaces-routing/scripts/verify.sh`
  - `bash modules/02-network-systems/03-implementations/lab-01-namespaces-routing/scripts/teardown.sh`
- Lab 02: NAT + Firewall
  - `bash modules/02-network-systems/03-implementations/lab-02-nat-firewall/scripts/setup.sh`
  - `bash modules/02-network-systems/03-implementations/lab-02-nat-firewall/scripts/verify.sh`
  - `bash modules/02-network-systems/03-implementations/lab-02-nat-firewall/scripts/teardown.sh`
- Lab 03: tcpdump Diagnosis (Docker)
  - `bash modules/02-network-systems/03-implementations/lab-03-tcpdump-diagnosis/scripts/setup.sh`
  - `bash modules/02-network-systems/03-implementations/lab-03-tcpdump-diagnosis/scripts/verify.sh`
  - `bash modules/02-network-systems/03-implementations/lab-03-tcpdump-diagnosis/scripts/teardown.sh`

## How to verify

- Lab 01: ping succeeds between namespaces and routes show expected gateways.
- Lab 02: blocked port fails, then succeeds after ACCEPT; NAT rule present.
- Lab 03: tcpdump logs show TCP handshake and HTTP request/response.
