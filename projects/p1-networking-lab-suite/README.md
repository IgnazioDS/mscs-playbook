# p1-networking-lab-suite

## Purpose
Provide a reproducible networking lab suite for routing, firewall/NAT behavior, and packet diagnostics.

## Scope
- Run containerized and namespace-based networking labs from module assets.
- Validate packet flow behavior with provided verification scripts.
- Capture baseline troubleshooting outputs to support future project automation.

## Modules Used
- 02-network-systems
- 06-big-data-architecture

## How to Run
```bash
bash modules/02-network-systems/03-implementations/lab-03-tcpdump-diagnosis/scripts/setup.sh
bash modules/02-network-systems/03-implementations/lab-03-tcpdump-diagnosis/scripts/verify.sh
bash modules/02-network-systems/03-implementations/lab-03-tcpdump-diagnosis/scripts/teardown.sh
```

## How to Test
```bash
bash modules/02-network-systems/03-implementations/lab-03-tcpdump-diagnosis/scripts/verify.sh
bash modules/02-network-systems/03-implementations/lab-02-nat-firewall/scripts/verify.sh
```

## Expected Output
- Verify scripts complete successfully with non-error exits.
- tcpdump diagnosis lab confirms expected handshake/request traffic.
- NAT/firewall lab shows blocked and allowed behavior per rules.
