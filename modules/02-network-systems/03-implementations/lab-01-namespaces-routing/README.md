# Lab 01: Network Namespaces + veth + Routing

## Goal
Create two isolated namespaces and route traffic between them through a router namespace.

## Requirements
- Linux host with `iproute2` and `iputils-ping`.
- macOS: run inside a privileged Linux container.

## macOS Docker fallback
From `modules/02-network-systems/03-implementations/lab-01-namespaces-routing/`:
```
docker run --rm -it --privileged -v "$PWD":/lab -w /lab ubuntu:24.04 bash
apt-get update && apt-get install -y iproute2 iputils-ping traceroute
```
Then run the scripts inside the container shell.

## Run
```
bash scripts/setup.sh
bash scripts/verify.sh
bash scripts/teardown.sh
```

## Verification
- `ns1` can ping `10.0.2.2`.
- Routes in `ns1` and `ns2` show a default gateway via the router namespace.
