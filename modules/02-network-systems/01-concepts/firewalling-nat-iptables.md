# Firewalling and NAT (iptables)

## What it is
iptables programs netfilter tables to filter, NAT, and mangle traffic.

## Why it matters
Firewall rules and NAT are common sources of connectivity issues and are core
to cloud security group behavior.

## Core concepts (with short examples)
- Tables: `filter`, `nat`.
- Chains: `INPUT`, `OUTPUT`, `FORWARD`, `PREROUTING`, `POSTROUTING`.
- Example: allow SSH: `iptables -A INPUT -p tcp --dport 22 -j ACCEPT`.
- Example SNAT: `iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE`.

## Common failure modes
- Default DROP without explicit ACCEPT.
- NAT rules applied on wrong interface.
- Forgetting related/established return traffic.

## Debug checklist (commands)
- `iptables -L -n -v`, `iptables -t nat -L -n -v`.
- `sysctl net.ipv4.ip_forward` for routing/NAT.
- `tcpdump -n -i <iface> port <port>`.

## References
- iptables tutorial (netfilter.org)
- `man iptables`
