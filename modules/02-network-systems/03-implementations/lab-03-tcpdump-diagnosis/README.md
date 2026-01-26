# Lab 03: Packet Capture and Diagnosis

## Goal
Capture a simple HTTP exchange between a client and server using tcpdump.

## Requirements
- Docker with `docker compose`.

## Run
```
bash scripts/setup.sh
bash scripts/verify.sh
bash scripts/teardown.sh
```

## Alternative (manual)
```
docker compose up --build
# then
docker compose down
```

## Verification
- tcpdump output includes SYN/SYN-ACK/ACK and HTTP request/response.
- Client exits with HTTP 200.
