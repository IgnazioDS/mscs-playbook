# Mini-Project: Network Troubleshooting Runbook

## Goal
Create a repeatable diagnosis workflow for a flaky internal API reachable only
through a Docker lab environment (Lab 03).

## Deliverables
- A short troubleshooting runbook (bulleted steps).
- Evidence captures: command outputs or screenshots.
- A one-page postmortem summary with root cause and fixes.

## Steps
1. Run Lab 03 setup and verify you can reproduce the failure condition.
2. Capture traffic with tcpdump and identify the TCP handshake and HTTP request.
3. Confirm DNS resolution and routing inside the container.
4. Apply a minimal fix (e.g., correct port or routing rule).
5. Re-run verification and document the delta.

## Suggested Commands
- `docker compose -f modules/02-network-systems/03-implementations/lab-03-tcpdump-diagnosis/docker-compose.yml up -d`
- `bash modules/02-network-systems/03-implementations/lab-03-tcpdump-diagnosis/scripts/verify.sh`
- `docker compose -f modules/02-network-systems/03-implementations/lab-03-tcpdump-diagnosis/docker-compose.yml down -v`

## Success Criteria
- You can point to the exact packet sequence that proves the failure.
- The root cause is stated in one sentence.
- The verify script passes after applying the fix.
