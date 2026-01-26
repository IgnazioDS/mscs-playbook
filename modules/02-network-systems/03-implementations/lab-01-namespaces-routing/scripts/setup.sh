#!/usr/bin/env bash
set -euo pipefail

NS1="ns1"
NS2="ns2"
R1="r1"

for ns in "$NS1" "$NS2" "$R1"; do
  if sudo ip netns list | grep -qw "$ns"; then
    sudo ip netns del "$ns"
  fi
  sudo ip netns add "$ns"
done

sudo ip link add veth-ns1 type veth peer name veth-r1-1
sudo ip link add veth-ns2 type veth peer name veth-r1-2

sudo ip link set veth-ns1 netns "$NS1"
sudo ip link set veth-r1-1 netns "$R1"
sudo ip link set veth-ns2 netns "$NS2"
sudo ip link set veth-r1-2 netns "$R1"

sudo ip -n "$NS1" link set lo up
sudo ip -n "$NS2" link set lo up
sudo ip -n "$R1" link set lo up

sudo ip -n "$NS1" addr add 10.0.1.2/24 dev veth-ns1
sudo ip -n "$R1" addr add 10.0.1.1/24 dev veth-r1-1
sudo ip -n "$NS2" addr add 10.0.2.2/24 dev veth-ns2
sudo ip -n "$R1" addr add 10.0.2.1/24 dev veth-r1-2

sudo ip -n "$NS1" link set veth-ns1 up
sudo ip -n "$NS2" link set veth-ns2 up
sudo ip -n "$R1" link set veth-r1-1 up
sudo ip -n "$R1" link set veth-r1-2 up

sudo ip -n "$NS1" route add default via 10.0.1.1
sudo ip -n "$NS2" route add default via 10.0.2.1

sudo ip netns exec "$R1" sysctl -w net.ipv4.ip_forward=1 >/dev/null
