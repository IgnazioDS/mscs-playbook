#!/usr/bin/env bash
set -euo pipefail

# Create two namespaces and a router namespace, then wire them with veth pairs.
NS1="ns1"
NS2="ns2"
R1="r1"

for ns in "$NS1" "$NS2" "$R1"; do
  if sudo ip netns list | grep -qw "$ns"; then
    sudo ip netns del "$ns"
  fi
  sudo ip netns add "$ns"
done

# Create veth pairs to connect each namespace to the router namespace.
sudo ip link add veth-ns1 type veth peer name veth-r1-1
sudo ip link add veth-ns2 type veth peer name veth-r1-2

# Move veth endpoints into their respective namespaces.
sudo ip link set veth-ns1 netns "$NS1"
sudo ip link set veth-r1-1 netns "$R1"
sudo ip link set veth-ns2 netns "$NS2"
sudo ip link set veth-r1-2 netns "$R1"

# Bring loopback interfaces up so local services work inside namespaces.
sudo ip -n "$NS1" link set lo up
sudo ip -n "$NS2" link set lo up
sudo ip -n "$R1" link set lo up

# Assign IP addresses for two /24 subnets on each veth.
sudo ip -n "$NS1" addr add 10.0.1.2/24 dev veth-ns1
sudo ip -n "$R1" addr add 10.0.1.1/24 dev veth-r1-1
sudo ip -n "$NS2" addr add 10.0.2.2/24 dev veth-ns2
sudo ip -n "$R1" addr add 10.0.2.1/24 dev veth-r1-2

# Bring veth interfaces up to carry traffic.
sudo ip -n "$NS1" link set veth-ns1 up
sudo ip -n "$NS2" link set veth-ns2 up
sudo ip -n "$R1" link set veth-r1-1 up
sudo ip -n "$R1" link set veth-r1-2 up

# Route each namespace's default traffic through the router namespace.
sudo ip -n "$NS1" route add default via 10.0.1.1
sudo ip -n "$NS2" route add default via 10.0.2.1

# Enable IP forwarding in the router namespace to allow routing.
sudo ip netns exec "$R1" sysctl -w net.ipv4.ip_forward=1 >/dev/null
