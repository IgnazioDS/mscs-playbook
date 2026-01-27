#!/usr/bin/env bash
set -euo pipefail

NS1="ns1"
NS2="ns2"

# Verify connectivity across namespaces via the router namespace.
sudo ip netns exec "$NS1" ping -c 2 10.0.2.2
# Show routing tables to confirm default gateways are set.
sudo ip -n "$NS1" route
sudo ip -n "$NS2" route
