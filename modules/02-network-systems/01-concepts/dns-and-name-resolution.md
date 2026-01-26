# DNS and Name Resolution

## What it is
DNS maps names to addresses; resolvers, caches, and authoritative servers
implement the lookup chain.

## Why it matters
Most applications start with DNS. If it fails, everything else looks down.

## Core concepts (with short examples)
- Recursive resolver vs authoritative server.
- A/AAAA, CNAME, TXT records.
- Caching with TTLs.
- Example: `dig example.com A +trace`.

## Common failure modes
- Stale cache (TTL too high), or negative caching.
- Resolver unreachable or blocked by firewall.
- Incorrect CNAME chains or split-horizon DNS.

## Debug checklist (commands)
- `dig <name>`, `dig @<resolver> <name>`.
- `cat /etc/resolv.conf`, `scutil --dns` (macOS).
- `tcpdump -n -i <iface> port 53`.

## References
- DNS and BIND (O'Reilly)
- RFC 1034/1035
