# ARP, Switching, and L2/L3 Interaction

## Key Ideas

- Ethernet switching and IP routing solve different problems, so a host must decide first whether the destination is local at Layer 2 or remote at Layer 3.
- ARP resolves an IPv4 next-hop address into a link-layer destination address, which is why subnet mistakes often appear as ARP failures rather than routing failures.
- A frame carries link-layer source and destination addresses for one hop, while the IP packet inside it keeps the end-to-end source and destination addresses.
- Broadcast domains, VLAN boundaries, and bridges determine where ARP requests can travel, so they directly shape which hosts can discover one another without a router.
- Many practical outages come from confusing the packet destination with the frame destination, especially when gateways, NAT, or virtual bridges are involved.

## 1. What It Is

Layer 2 and Layer 3 cooperate every time an IP packet leaves a host. Layer 3 decides where the packet should go logically by looking at IP addresses and routes. Layer 2 decides how to deliver the next hop on the local medium by using link-layer addresses such as Ethernet MAC addresses.

### 1.1 Core Definitions

- A **frame** is the Layer 2 unit transmitted on a local link.
- A **packet** is the Layer 3 unit carried inside the frame.
- A **MAC address** is a link-layer identifier used by Ethernet interfaces.
- A **switch** forwards frames inside one broadcast domain based on MAC addresses.
- **ARP**, the Address Resolution Protocol, maps an IPv4 address on the local network to a MAC address.
- A **broadcast domain** is the set of interfaces that receive Layer 2 broadcasts from one another.
- A **default gateway** is the router a host uses when the destination IP is not on a directly connected subnet.

### 1.2 Why This Matters

Troubleshooting gets much faster when the L2/L3 boundary is explicit. If a host cannot reach a peer on the same subnet, the problem may be ARP, switching, VLAN membership, or interface state. If the peer is on another subnet, the host should ARP for the gateway instead of the remote host. Misunderstanding that distinction produces misdiagnoses such as “routing is broken” when the real issue is local neighbor discovery.

## 2. How Local Delivery Works

When a host wants to send to an IP destination on the same subnet, it:

1. compares the destination IP with its connected subnet,
2. decides the destination is directly reachable,
3. resolves the destination IP to a MAC address with ARP if needed,
4. sends an Ethernet frame directly to that MAC address.

In this case, the IP destination and the next hop are the same host.

### 2.1 Switching

An Ethernet switch learns which MAC addresses appear on which ports by observing source addresses on incoming frames. It then forwards later frames to the learned port instead of flooding them everywhere.

Switching is local to the broadcast domain. It does not interpret IP routes or TCP ports. It only moves frames within the L2 segment.

## 3. How Remote Delivery Works

If the destination IP is outside the local subnet, the host does not ARP for the remote destination. It ARPs for the default gateway or another route-selected next hop.

The resulting frame therefore has:

- a **frame destination MAC** equal to the gateway's MAC address,
- an **IP destination address** equal to the remote host's IP address.

At the router:

1. the incoming Ethernet header is removed,
2. the IP packet is inspected,
3. the router selects the next hop,
4. a new frame is built for the next link.

This is the key L2/L3 interaction: the IP packet is end-to-end, but the frame is hop-by-hop.

## 4. Bridges, Broadcast Domains, and Virtual Networks

A Linux bridge behaves like a software switch. It connects multiple interfaces into one Layer 2 segment so that ARP broadcasts and Ethernet frames can move between them.

This is why containers, virtual machines, and namespace labs rely on bridges and `veth` pairs:

- the bridge defines the shared Layer 2 domain,
- ARP discovers neighbors inside that domain,
- routing is still required to leave that domain.

If two namespaces are attached to the same bridge and subnet, they can ARP for one another directly. If they live on different subnets, a router or forwarding host is needed between them.

## 5. Worked Example

Host `A` has:

```text
IP = 10.0.1.10/24
MAC = aa:aa:aa:aa:aa:10
default gateway = 10.0.1.1
```

Router interface on the same LAN has:

```text
IP = 10.0.1.1
MAC = rr:rr:rr:rr:rr:01
```

Remote host `B` has:

```text
IP = 10.0.2.20/24
MAC = bb:bb:bb:bb:bb:20
```

Assume `A` wants to send an IP packet to `10.0.2.20`.

### 5.1 Determine Whether the Destination Is Local

`A` applies subnet mask `/24`:

```text
10.0.1.10 -> network 10.0.1.0/24
10.0.2.20 -> network 10.0.2.0/24
```

The networks differ, so `B` is remote.

### 5.2 Resolve the Next Hop

Because the destination is remote, `A` must send to the gateway `10.0.1.1`.

If `A` lacks an ARP entry, it broadcasts:

```text
Who has 10.0.1.1? Tell 10.0.1.10
```

The router replies:

```text
10.0.1.1 is at rr:rr:rr:rr:rr:01
```

### 5.3 Build the First-Hop Frame

`A` now sends:

```text
Ethernet source MAC = aa:aa:aa:aa:aa:10
Ethernet destination MAC = rr:rr:rr:rr:rr:01
IP source = 10.0.1.10
IP destination = 10.0.2.20
```

Notice the difference:

- the frame goes to the router,
- the packet still targets host `B`.

### 5.4 Router Forwards to the Next Link

The router strips the incoming frame, checks its route for `10.0.2.20`, and decides the destination network `10.0.2.0/24` is directly connected on another interface.

If needed, it ARPs for `10.0.2.20`, learns:

```text
10.0.2.20 is at bb:bb:bb:bb:bb:20
```

Then it sends a new frame:

```text
Ethernet source MAC = router's MAC on 10.0.2.0/24
Ethernet destination MAC = bb:bb:bb:bb:bb:20
IP source = 10.0.1.10
IP destination = 10.0.2.20
```

Verification: host `A` correctly ARPs for the gateway rather than for `10.0.2.20`, the first-hop frame is addressed to the router's MAC, and the IP destination remains `10.0.2.20` end to end.

## 6. Pseudocode Pattern

```text
procedure choose_next_hop(local_ip, prefix_length, destination_ip, default_gateway):
    local_network = apply_mask(local_ip, prefix_length)
    destination_network = apply_mask(destination_ip, prefix_length)

    if local_network == destination_network:
        return destination_ip
    return default_gateway
```

Time: `Theta(1)` worst case for one local-subnet decision with fixed-width IPv4 addresses. Space: `Theta(1)` auxiliary space.

## 7. Common Mistakes

1. **Packet-frame confusion.** Treating the remote host's MAC as the frame destination for off-subnet traffic breaks delivery; send the frame to the next hop and keep the packet addressed to the remote IP.
2. **Same-subnet assumption.** Assuming every reachable IP should answer local ARP ignores subnet boundaries; only directly connected next hops should be resolved with ARP from the host.
3. **Bridge-versus-router blur.** Expecting a bridge to route between subnets leads to silent failure; bridges forward L2 frames, while routers move packets between L3 networks.
4. **Mask mismatch.** Configuring inconsistent subnet masks on peers can make one side ARP for a host that the other side treats as remote; verify prefix lengths on every participant.
5. **Neighbor-cache neglect.** Ignoring stale or incomplete ARP entries can hide the real failure mode; inspect neighbor state explicitly with `ip neigh`.

## 8. Practical Checklist

- [ ] Confirm whether the destination IP is on a directly connected subnet before debugging anything else.
- [ ] Inspect `ip route` to see which next hop the host actually chose.
- [ ] Check `ip neigh` for incomplete, stale, or missing ARP entries.
- [ ] Distinguish bridge problems from router problems by identifying the broadcast-domain boundary.
- [ ] Capture ARP traffic with `tcpdump -n -e arp` when neighbor discovery is suspicious.
- [ ] Verify VLAN or bridge membership before assuming two interfaces share one Layer 2 segment.

## 9. References

- Stevens, W. Richard, Kevin R. Fall, and Gary R. Wright. 2011. *TCP/IP Illustrated, Volume 1* (2nd ed.). Addison-Wesley.
- Perlman, Radia. 1999. *Interconnections* (2nd ed.). Addison-Wesley.
- RFC 826. 1982. *An Ethernet Address Resolution Protocol*. <https://datatracker.ietf.org/doc/html/rfc826>
- RFC 1122. 1989. *Requirements for Internet Hosts*. <https://datatracker.ietf.org/doc/html/rfc1122>
- Linux Foundation. *bridge(8) manual page*. <https://man7.org/linux/man-pages/man8/bridge.8.html>
- Linux Foundation. *ip-neighbour(8) manual page*. <https://man7.org/linux/man-pages/man8/ip-neighbour.8.html>
- Arpaci-Dusseau, Remzi H., and Andrea C. Arpaci-Dusseau. 2018. *Computer Networks: A Systems Approach*. <https://book.systemsapproach.org/>
