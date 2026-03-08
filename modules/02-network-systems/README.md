# Network Systems

## Status

- Concepts, cheat sheet, case study, and labs are complete.
- Labs are Docker-first with Linux namespace and iptables notes plus local troubleshooting workflows.

## Overview

This module focuses on practical network systems: protocol layering, addressing, routing,
DNS, Linux networking primitives, packet inspection, firewalling, and the cloud-networking
mental models that build on those foundations. It emphasizes reproducible local labs and
tool-driven debugging with `iproute2`, `iptables`, and `tcpdump`.

## Recommended learning path

1. Build the protocol and naming model with TCP/IP, addressing, and DNS.
2. Learn the Linux host and packet-level tools used to inspect real traffic.
3. Move into isolated Linux network topologies, then firewalling and NAT.
4. Finish with cloud networking as an abstraction layer over the same local ideas.

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

## Concepts

- [01 TCP/IP Foundations](01-concepts/01-tcp-ip-foundations.md)
- [02 Addressing, Routing, and Subnets](01-concepts/02-addressing-routing-and-subnets.md)
- [03 DNS and Name Resolution](01-concepts/03-dns-and-name-resolution.md)
- [04 Linux Networking with iproute2](01-concepts/04-linux-networking-with-iproute2.md)
- [05 Packet Capture with tcpdump](01-concepts/05-packet-capture-with-tcpdump.md)
- [06 Namespaces, veth, and Bridges](01-concepts/06-namespaces-veth-and-bridges.md)
- [07 Firewalling and NAT with iptables](01-concepts/07-firewalling-and-nat-with-iptables.md)
- [08 Cloud Networking Mental Models](01-concepts/08-cloud-networking-mental-models.md)

## Concept-to-lab bridge

- Read `04` and `06` before Lab 01 on namespaces and routing.
- Read `07` before Lab 02 on NAT and firewall behavior.
- Read `05` before Lab 03 on packet capture and diagnosis.

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
