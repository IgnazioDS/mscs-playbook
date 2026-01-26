# Cloud Networking Mental Models

## What it is
Portable patterns to reason about VPC/VNet networks, security, and routing
without tying to a specific cloud provider.

## Why it matters
Cloud designs map cleanly to local Linux networking concepts, enabling fast
learning and safer changes.

## Core concepts (with short examples)
- VPC/VNet contains subnets and route tables.
- Security groups/firewalls allow or block traffic by port/protocol.
- Load balancers sit at L4 or L7 with health checks.
- Connectivity via peering or VPN.

## Local analogs
- VPC subnet -> Docker bridge network / Linux bridge
- Security group -> iptables filter rules
- Route table -> `ip route`
- NAT gateway -> MASQUERADE on egress
- Load balancer -> reverse proxy (nginx) concept

## Common failure modes
- Route tables missing return paths.
- Security group blocks ephemeral return traffic.
- NAT or load balancer misconfigured for private subnets.

## Debug checklist (commands)
- `ip route show`, `iptables -L -n -v`.
- `curl -v`, `ss -tuna`, `tcpdump -n -i <iface>`.

## References
- AWS VPC, Azure VNet, GCP VPC docs (concept pages)
- Site Reliability Engineering (networking chapters)
