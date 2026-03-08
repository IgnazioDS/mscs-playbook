# Concepts

Read these pages in numerical order. Later pages assume the mental model built by the earlier ones.

- [01 TCP/IP Foundations](01-tcp-ip-foundations.md): layered responsibilities, transport behavior, and the baseline packet-delivery model.
- [02 ARP, Switching, and L2/L3 Interaction](02-arp-switching-and-l2-l3-interaction.md): frame delivery, neighbor discovery, and the handoff between local switching and routed forwarding.
- [03 Addressing, Routing, and Subnets](03-addressing-routing-and-subnets.md): CIDR, gateways, and route selection for moving between networks.
- [04 DNS and Name Resolution](04-dns-and-name-resolution.md): recursive lookup, authoritative data, caching, and common resolver failures.
- [05 Transport-Layer Behavior, Reliability, and Congestion](05-transport-layer-behavior-reliability-and-congestion.md): retransmission, windows, congestion, and transport-level failure modes.
- [06 Sockets and Connection Lifecycle](06-sockets-and-connection-lifecycle.md): the OS socket model that ties transport behavior to processes, ports, and state transitions.
- [07 Linux Networking with iproute2](07-linux-networking-with-iproute2.md): the core Linux commands for interfaces, routes, and neighbors.
- [08 Packet Capture with tcpdump](08-packet-capture-with-tcpdump.md): how to observe traffic directly and confirm what is on the wire.
- [09 Namespaces, veth, and Bridges](09-namespaces-veth-and-bridges.md): Linux isolation and L2 connectivity for containers and local labs.
- [10 Firewalling and NAT with iptables](10-firewalling-and-nat-with-iptables.md): filtering, translation, forwarding, and stateful return traffic.
- [11 Load Balancers and Reverse Proxies](11-load-balancers-and-reverse-proxies.md): frontend traffic distribution, health checking, and client-to-backend request flow.
- [12 Cloud Networking Mental Models](12-cloud-networking-mental-models.md): the provider-neutral abstraction layer that maps cloud constructs back to local networking concepts.
- [13 Network Performance and Troubleshooting Workflow](13-network-performance-and-troubleshooting-workflow.md): a capstone workflow for diagnosing latency, loss, and throughput problems systematically.
