#!/usr/bin/env bash
set -euo pipefail

NS_CLIENT="ns-client"
NS_GW="ns-gw"

set +e
sudo ip netns exec "$NS_CLIENT" curl -s --connect-timeout 2 http://10.0.2.2:8080/ >/dev/null
RESULT=$?
set -e
if [ "$RESULT" -eq 0 ]; then
  echo "Unexpected success: port should be blocked"
  exit 1
fi

echo "Port blocked as expected. Opening port 8080..."
sudo ip netns exec "$NS_GW" iptables -A FORWARD -p tcp -s 10.0.1.0/24 -d 10.0.2.2 --dport 8080 -j ACCEPT

sudo ip netns exec "$NS_CLIENT" curl -s http://10.0.2.2:8080/ >/dev/null
sudo ip netns exec "$NS_GW" iptables -t nat -L POSTROUTING -n -v
