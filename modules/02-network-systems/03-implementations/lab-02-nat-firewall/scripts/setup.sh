#!/usr/bin/env bash
set -euo pipefail

NS_CLIENT="ns-client"
NS_SERVER="ns-server"
NS_GW="ns-gw"

for ns in "$NS_CLIENT" "$NS_SERVER" "$NS_GW"; do
  if sudo ip netns list | grep -qw "$ns"; then
    sudo ip netns del "$ns"
  fi
  sudo ip netns add "$ns"
done

sudo ip link add veth-client type veth peer name veth-gw-1
sudo ip link add veth-server type veth peer name veth-gw-2

sudo ip link set veth-client netns "$NS_CLIENT"
sudo ip link set veth-gw-1 netns "$NS_GW"
sudo ip link set veth-server netns "$NS_SERVER"
sudo ip link set veth-gw-2 netns "$NS_GW"

sudo ip -n "$NS_CLIENT" link set lo up
sudo ip -n "$NS_SERVER" link set lo up
sudo ip -n "$NS_GW" link set lo up

sudo ip -n "$NS_CLIENT" addr add 10.0.1.2/24 dev veth-client
sudo ip -n "$NS_GW" addr add 10.0.1.1/24 dev veth-gw-1
sudo ip -n "$NS_SERVER" addr add 10.0.2.2/24 dev veth-server
sudo ip -n "$NS_GW" addr add 10.0.2.1/24 dev veth-gw-2

sudo ip -n "$NS_CLIENT" link set veth-client up
sudo ip -n "$NS_SERVER" link set veth-server up
sudo ip -n "$NS_GW" link set veth-gw-1 up
sudo ip -n "$NS_GW" link set veth-gw-2 up

sudo ip -n "$NS_CLIENT" route add default via 10.0.1.1
sudo ip -n "$NS_SERVER" route add default via 10.0.2.1

sudo ip netns exec "$NS_GW" sysctl -w net.ipv4.ip_forward=1 >/dev/null

sudo ip netns exec "$NS_GW" iptables -F
sudo ip netns exec "$NS_GW" iptables -t nat -F
sudo ip netns exec "$NS_GW" iptables -P FORWARD DROP
sudo ip netns exec "$NS_GW" iptables -A FORWARD -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
sudo ip netns exec "$NS_GW" iptables -t nat -A POSTROUTING -s 10.0.1.0/24 -o veth-gw-2 -j MASQUERADE

sudo ip netns exec "$NS_SERVER" bash -c "python3 -m http.server 8080 --bind 10.0.2.2 >/tmp/ns-http.log 2>&1 & echo \$! > /tmp/ns-http.pid"
