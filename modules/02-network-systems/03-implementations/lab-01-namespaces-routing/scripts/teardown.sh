#!/usr/bin/env bash
set -euo pipefail

for ns in ns1 ns2 r1; do
  if sudo ip netns list | grep -qw "$ns"; then
    sudo ip netns del "$ns"
  fi

done
