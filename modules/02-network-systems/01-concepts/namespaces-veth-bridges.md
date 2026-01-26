# Namespaces, veth, Bridges

## What it is
Namespaces isolate network stacks; veth pairs connect namespaces; bridges
join multiple interfaces at L2.

## Why it matters
These primitives underpin containers, labs, and multi-tenant systems.

## Core concepts (with short examples)
- Create namespace: `ip netns add ns1`.
- Connect with veth: `ip link add veth1 type veth peer name veth2`.
- Bridge interfaces: `ip link add br0 type bridge`.
- Example: attach veth to bridge and assign IPs.

## Common failure modes
- Missing IP forwarding between namespaces.
- Interfaces not set `up`.
- Bridge without ports or incorrect VLAN tagging.

## Debug checklist (commands)
- `ip netns list`, `ip -n <ns> addr`, `ip -n <ns> route`.
- `ip link show type veth`, `bridge link`.
- `tcpdump -n -i <veth>`.

## References
- Linux network namespaces documentation
- `man ip-netns`, `man bridge`
