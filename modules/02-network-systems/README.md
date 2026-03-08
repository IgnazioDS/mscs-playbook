# Network Systems

## Status

- Concepts, cheat sheet, case study, and labs are complete.
- Labs are Docker-first with Linux namespace and iptables notes plus local troubleshooting workflows.

## Overview

This module focuses on practical network systems: protocol layering, Layer 2 and Layer 3
interaction, transport behavior, sockets, Linux networking primitives, packet inspection,
firewalling, balancing, cloud abstractions, and performance-oriented troubleshooting.
It emphasizes reproducible local labs and tool-driven debugging with `iproute2`,
`iptables`, and `tcpdump`.

## Recommended learning path

1. Build the packet-delivery model with TCP/IP, ARP, addressing, and DNS.
2. Learn how transport reliability and socket lifecycle expose network behavior to applications.
3. Use Linux host and packet-level tools to inspect real traffic and route decisions.
4. Move into isolated Linux topologies, then firewalling and NAT.
5. Finish with balancing, cloud abstractions, and performance-oriented troubleshooting.

## Prerequisites

- Docker installed (Docker Desktop or Engine)
- Linux host recommended for namespace/iptables labs

## OS constraints

- Lab 01 and Lab 02 require Linux kernel features (network namespaces, iptables).
  On macOS, run them inside a privileged Linux container or a Linux VM.
- Lab 03 is Docker-only and runs on macOS and Linux.

## Quickstart

From the repo root (Docker-only lab that works on macOS/Linux):

- `bash modules/02-network-systems/03-implementations/lab-03-tcpdump-diagnosis/scripts/setup.sh`
- `bash modules/02-network-systems/03-implementations/lab-03-tcpdump-diagnosis/scripts/verify.sh`
- `bash modules/02-network-systems/03-implementations/lab-03-tcpdump-diagnosis/scripts/teardown.sh`

## Concepts (reading order)

- [01 TCP/IP Foundations](01-concepts/01-tcp-ip-foundations.md)
- [02 ARP, Switching, and L2/L3 Interaction](01-concepts/02-arp-switching-and-l2-l3-interaction.md)
- [03 Addressing, Routing, and Subnets](01-concepts/03-addressing-routing-and-subnets.md)
- [04 DNS and Name Resolution](01-concepts/04-dns-and-name-resolution.md)
- [05 Transport-Layer Behavior, Reliability, and Congestion](01-concepts/05-transport-layer-behavior-reliability-and-congestion.md)
- [06 Sockets and Connection Lifecycle](01-concepts/06-sockets-and-connection-lifecycle.md)
- [07 Linux Networking with iproute2](01-concepts/07-linux-networking-with-iproute2.md)
- [08 Packet Capture with tcpdump](01-concepts/08-packet-capture-with-tcpdump.md)
- [09 Namespaces, veth, and Bridges](01-concepts/09-namespaces-veth-and-bridges.md)
- [10 Firewalling and NAT with iptables](01-concepts/10-firewalling-and-nat-with-iptables.md)
- [11 Load Balancers and Reverse Proxies](01-concepts/11-load-balancers-and-reverse-proxies.md)
- [12 Cloud Networking Mental Models](01-concepts/12-cloud-networking-mental-models.md)
- [13 Network Performance and Troubleshooting Workflow](01-concepts/13-network-performance-and-troubleshooting-workflow.md)

## Concept-to-lab bridge

- Use the concept numbers as the default reading order even if you jump into labs selectively.
- Read `07` and `09` before Lab 01 on namespaces and routing.
- Read `10` before Lab 02 on NAT and firewall behavior.
- Read `08` and `13` before Lab 03 on packet capture and diagnosis.

## Cheat sheet

- [Networking Cheat Sheet](02-cheatsheets/networking-cheatsheet.md)

## Case study

- [Debugging Playbook](04-case-studies/debugging-playbook.md)

## Mini-project

- [Network Troubleshooting Runbook](05-exercises/network-troubleshooting-mini-project.md)

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
