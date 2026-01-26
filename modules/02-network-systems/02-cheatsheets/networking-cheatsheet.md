# Networking Cheat Sheet

## Must-know commands
- `ip addr`, `ip link`, `ip route`, `ip neigh`
- `ss -tuna` (list sockets)
- `ping -c 2 <host>`
- `traceroute -n <host>`
- `dig <name>`, `dig @<resolver> <name>`
- `tcpdump -n -i <iface> [port <p>]`

## Common debugging flows
**Connectivity**
1) `ip addr`, `ip route` (local config)
2) `ping <gateway>` then `ping <remote>`
3) `traceroute -n <remote>`
4) `tcpdump -n -i <iface>`

**DNS**
1) `cat /etc/resolv.conf`
2) `dig <name>` and `dig @<resolver> <name>`
3) `tcpdump -n -i <iface> port 53`

**Routing**
1) `ip route show`
2) Check default route and specific prefixes
3) Verify reverse path / return route

**Firewall**
1) `iptables -L -n -v`
2) `iptables -t nat -L -n -v`
3) Confirm RELATED,ESTABLISHED

## NAT and iptables quick reference
- Allow inbound TCP: `iptables -A INPUT -p tcp --dport 8080 -j ACCEPT`
- Default drop: `iptables -P INPUT DROP`
- Allow return traffic: `iptables -A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT`
- SNAT/MASQUERADE: `iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE`

## Interpreting outputs
- `ip route`: longest prefix wins; `default via <gw>` for external.
- `ss -tuna`: LISTEN vs ESTAB; verify local port is bound.
- TCP states: SYN-SENT (no response), ESTAB (connected), TIME-WAIT (recent close).
