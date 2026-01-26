# Debugging Playbook

## Incident 1: Service unreachable in private subnet
**Symptoms:** clients in a public subnet cannot reach a private service.

**Steps**
1) Confirm route tables (local analog): `ip route show`.
2) Verify NAT path for egress if required: `iptables -t nat -L -n -v`.
3) Check firewall/security group intent: `iptables -L -n -v`.
4) Verify service listener: `ss -tuna | grep <port>`.

**Expected observations**
- Missing route or return path from private subnet.
- NAT not configured for outbound or return traffic.

## Incident 2: DNS resolves but connection fails
**Symptoms:** `dig` resolves, but `curl` hangs or fails.

**Steps**
1) Verify port reachability: `nc -vz <ip> <port>` or `curl -v`.
2) Check listener: `ss -tuna | grep <port>` on target.
3) Inspect firewall rules: `iptables -L -n -v`.
4) Capture traffic: `tcpdump -n -i <iface> host <ip> and port <port>`.

**Expected observations**
- SYN packets with no SYN-ACK (firewall drop).
- RST from host (service not listening).

## Incident 3: Intermittent latency and packet loss
**Symptoms:** sporadic timeouts, jitter, or retransmissions.

**Steps**
1) Measure loss: `ping -c 20 <host>`.
2) Trace path: `traceroute -n <host>`.
3) Inspect retransmissions: `tcpdump -n -i <iface> tcp`.
4) Check MTU: `ip link show`, test with `ping -M do -s <size>`.

**Expected observations**
- High RTT or loss at a hop indicates congestion.
- Repeated retransmits suggest loss or MTU issues.
