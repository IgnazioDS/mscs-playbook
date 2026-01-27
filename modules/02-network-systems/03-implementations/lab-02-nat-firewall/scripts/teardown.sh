#!/usr/bin/env bash
set -euo pipefail

NS_SERVER="ns-server"

# Stop the HTTP server if it is running.
if sudo ip netns list | grep -qw "$NS_SERVER"; then
  sudo ip netns exec "$NS_SERVER" bash -c "if [ -f /tmp/ns-http.pid ]; then kill \$(cat /tmp/ns-http.pid) || true; rm -f /tmp/ns-http.pid; fi"
fi

# Remove namespaces to clean all links and routes.
for ns in ns-client ns-server ns-gw; do
  if sudo ip netns list | grep -qw "$ns"; then
    sudo ip netns del "$ns"
  fi

done
