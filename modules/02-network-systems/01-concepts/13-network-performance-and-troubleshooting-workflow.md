# Network Performance and Troubleshooting Workflow

## Key Ideas

- Network performance is multi-dimensional, so latency, throughput, loss, jitter, and availability must be separated rather than treated as one generic “network health” signal.
- A good troubleshooting workflow narrows the problem layer by layer and measurement by measurement, which is why disciplined evidence gathering outperforms ad hoc command execution.
- Throughput is often constrained by windows, RTT, or queueing behavior rather than by raw link bandwidth alone.
- Packet captures, socket state, route tables, and DNS data answer different diagnostic questions, so each tool should be used for a specific hypothesis.
- The fastest way to prolong an incident is to change multiple variables before establishing a baseline and a reproduction path.

## 1. What It Is

Network troubleshooting is the process of locating and explaining a communication failure or performance regression by collecting evidence across layers. Performance analysis is the related task of explaining why a path delivers the latency, loss, and throughput it does.

### 1.1 Core Definitions

- **Latency** is the time required for data or a request to travel and be processed.
- **Round-trip time (RTT)** is the time for a signal to go from sender to receiver and back.
- **Throughput** is the rate of successful data delivery over time.
- **Bandwidth** is the path's capacity ceiling, not the observed delivered rate.
- **Jitter** is variation in latency across packets or requests.
- **Loss** is the fraction of packets that fail to arrive.
- The **bandwidth-delay product (BDP)** is the amount of data needed in flight to fully use a path with a given bandwidth and RTT.

### 1.2 Why This Matters

Many incidents look similar from the outside. “The system is slow” could mean:

- DNS delay before the first connection,
- a SYN blocked by a firewall,
- a small receive window on a high-RTT path,
- packet loss causing retransmissions,
- or an overloaded proxy queue.

Without a structured workflow, teams collect lots of data but answer none of the key questions.

## 2. A Diagnostic Workflow

### 2.1 Define the Symptom Precisely

Start by naming the exact failure mode:

- no connection,
- slow handshake,
- low throughput,
- intermittent timeout,
- name-resolution failure,
- or one-way traffic.

Precision changes which tools are appropriate.

### 2.2 Move from Outside In

A useful sequence is:

1. confirm name resolution,
2. confirm routing and reachability,
3. confirm socket and port state,
4. inspect packets,
5. inspect policy devices such as firewalls, NAT, or proxies,
6. measure performance variables such as RTT, loss, and windows.

### 2.3 Change One Variable at a Time

If the incident is reproducible, keep one baseline path and adjust only one factor at a time, such as DNS resolver, MTU, firewall rule, or backend target. That prevents false conclusions from overlapping changes.

## 3. Latency, Throughput, and Queueing

### 3.1 Bandwidth Is Not Throughput

A path can have high bandwidth but poor throughput if:

- RTT is large,
- receive or congestion windows are small,
- losses trigger retransmissions,
- or queueing delays make the sender back off.

### 3.2 Bandwidth-Delay Product

The bandwidth-delay product is:

```text
BDP = bandwidth * RTT
```

It estimates how much unacknowledged data must be in flight to keep the path full.

### 3.3 Queueing and Jitter

If a device queue grows under load, packets wait longer before transmission. That increases latency and often jitter. In real systems, queue buildup may appear before packet loss, so latency growth can be an earlier warning sign than dropped packets.

## 4. Tool Selection by Hypothesis

Use tools according to the question:

- `dig` for name-resolution behavior,
- `ip route` and `ip addr` for path selection and interface state,
- `ss -tuna` for socket state,
- `tcpdump` for packet-level truth,
- `ping` or similar probes for RTT and reachability,
- application logs for timeout boundaries and retry behavior.

The question should drive the tool, not the other way around.

## 5. Worked Example

A team reports that a file download is unexpectedly capped around `13 Mb/s` over a WAN link.

Measured facts:

```text
link bandwidth = 100 Mb/s
RTT = 40 ms = 0.04 s
receiver window = 64 KiB = 65,536 bytes
loss = negligible
```

### 5.1 Compute the Bandwidth-Delay Product

First convert bandwidth to bytes per second:

```text
100 Mb/s = 100,000,000 bits/s
100,000,000 / 8 = 12,500,000 bytes/s
```

Now compute BDP:

```text
BDP = 12,500,000 bytes/s * 0.04 s = 500,000 bytes
```

So the path needs about `500,000` bytes in flight to fully utilize `100 Mb/s` at `40 ms` RTT.

### 5.2 Compare with the Receive Window

The receive window is only:

```text
65,536 bytes
```

This is much smaller than the `500,000` byte BDP, so the sender cannot keep enough data in flight to fill the path.

### 5.3 Estimate the Maximum Window-Limited Throughput

Approximate maximum throughput:

```text
throughput <= receive_window / RTT
throughput <= 65,536 / 0.04
throughput <= 1,638,400 bytes/s
```

Convert back to bits per second:

```text
1,638,400 * 8 = 13,107,200 bits/s
```

So the expected ceiling is about:

```text
13.1 Mb/s
```

### 5.4 Interpret the Result

The observed `13 Mb/s` is consistent with a window-limited transfer, not with a saturated `100 Mb/s` link or a loss-driven collapse.

Verification: the `500,000` byte BDP is far larger than the `65,536` byte receive window, and `65,536 / 0.04 * 8 ≈ 13.1 Mb/s`, matching the reported throughput cap.

## 6. Pseudocode Pattern

```text
procedure estimate_window_limited_throughput(window_bytes, rtt_seconds):
    if rtt_seconds == 0:
        return infinity
    return window_bytes / rtt_seconds
```

Time: `Theta(1)` worst case. Space: `Theta(1)` auxiliary space.

## 7. Common Mistakes

1. **Bandwidth-equals-performance thinking.** Assuming a `100 Mb/s` link should always deliver near `100 Mb/s` hides latency, window, loss, and queueing constraints; evaluate the whole transport path.
2. **Tool-before-hypothesis debugging.** Running commands without a specific question produces noise rather than evidence; decide whether the problem is naming, reachability, transport, policy, or throughput first.
3. **Multi-change incidents.** Adjusting DNS, firewall rules, routes, and application settings at once destroys causal evidence; preserve a baseline and change one variable at a time.
4. **Packet-capture overreach.** Using packet capture for every problem can waste time when the failure is already visible in route or socket state; start with the lowest-cost evidence that can falsify the current hypothesis.
5. **One-metric diagnosis.** Looking only at loss or only at RTT can miss the actual bottleneck; performance pathologies often require combining latency, throughput, window, and queueing signals.

## 8. Practical Checklist

- [ ] State the symptom in one precise sentence before collecting data.
- [ ] Verify DNS, route selection, and listening socket state before jumping to packet capture.
- [ ] Measure RTT and compare observed throughput against the bandwidth-delay product.
- [ ] Check whether receive-window or congestion-window limits explain throughput before blaming raw bandwidth.
- [ ] Capture packets only after naming what the capture should confirm or disprove.
- [ ] Record one reproducible baseline path before making changes during an incident.

## 9. References

- Stevens, W. Richard, Kevin R. Fall, and Gary R. Wright. 2011. *TCP/IP Illustrated, Volume 1* (2nd ed.). Addison-Wesley.
- Paxson, Vern. 1997. End-to-End Internet Packet Dynamics. *ACM SIGCOMM Computer Communication Review* 27(4). <https://dl.acm.org/doi/10.1145/263109.263155>
- Beyer, Betsy, et al., eds. 2016. *Site Reliability Engineering*. O'Reilly Media. <https://sre.google/sre-book/table-of-contents/>
- Jacobson, Van. 1988. Congestion Avoidance and Control. *ACM SIGCOMM Computer Communication Review* 18(4). <https://doi.org/10.1145/52325.52356>
- Allman, Mark, Vern Paxson, and Ethan Blanton. 2009. *TCP Congestion Control*. RFC 5681. <https://datatracker.ietf.org/doc/html/rfc5681>
- Arpaci-Dusseau, Remzi H., and Andrea C. Arpaci-Dusseau. 2018. *Computer Networks: A Systems Approach*. <https://book.systemsapproach.org/>
- Morton, Al, et al. 2011. *Framework for TCP Throughput Testing*. RFC 6349. <https://datatracker.ietf.org/doc/html/rfc6349>
