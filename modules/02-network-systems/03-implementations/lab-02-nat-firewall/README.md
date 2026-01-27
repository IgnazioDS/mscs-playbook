# Lab 02: NAT + Firewall Rules

## Goal
Use iptables inside a router namespace to block a port, open it, and apply NAT.

## Requirements
- Linux host with `iproute2`, `iptables`, `curl`, `python3` (iptables is Linux-only).
- macOS: run inside a privileged Linux container or a Linux VM.
Note: `nftables` is the modern replacement for `iptables`; this lab sticks to
`iptables` for portability.

## macOS Docker fallback
From `modules/02-network-systems/03-implementations/lab-02-nat-firewall/`:
```
docker run --rm -it --privileged -v "$PWD":/lab -w /lab ubuntu:24.04 bash
apt-get update && apt-get install -y iproute2 iptables iputils-ping curl python3
```
Then run the scripts inside the container shell.

## Run
```
bash scripts/setup.sh
bash scripts/verify.sh
bash scripts/teardown.sh
```

## Verification
- First `curl` from client fails (DROP).
- After ACCEPT, `curl` succeeds and NAT counters increment.
