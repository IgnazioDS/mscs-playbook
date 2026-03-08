# Transport-Layer Behavior, Reliability, and Congestion

## Key Ideas

- The transport layer is responsible for end-to-end delivery behavior such as ordering, retransmission, flow control, and multiplexing between applications.
- TCP reliability comes from sequence numbers, acknowledgments, retransmissions, and in-order delivery rules rather than from any guarantee provided by IP.
- Flow control and congestion control are different mechanisms: flow control protects the receiver, while congestion control protects the network path.
- Latency, loss, and reordering affect transport behavior directly, which is why packet traces and socket metrics often explain application stalls better than logs alone.
- Debugging transport issues requires naming the case precisely, such as handshake failure, retransmission timeout, receive-window exhaustion, or congestion-induced throughput collapse.

## 1. What It Is

The transport layer sits above IP and below application protocols. It provides the communication model applications actually use: byte streams, datagrams, ports, acknowledgments, and connection state.

### 1.1 Core Definitions

- A **segment** is the transport-layer unit used by TCP.
- A **datagram** is the transport-layer unit used by UDP.
- A **port** identifies an application endpoint on a host.
- A **sequence number** identifies the byte position of data in a TCP stream.
- An **acknowledgment** confirms receipt up to a certain byte position.
- A **receive window** limits how much unacknowledged data the receiver is willing to accept.
- A **congestion window** limits how much data the sender may have in flight based on perceived network conditions.

### 1.2 Why This Matters

Most application-visible network failures are transport-layer failures in disguise. “The service is slow” may actually mean excessive retransmissions. “The API timed out” may actually mean the handshake never completed. “The stream stalls after a few megabytes” may actually mean the receiver window or path congestion is limiting the sender.

## 2. Reliability and Ordering

IP is best effort. TCP adds reliability on top of that by tracking which bytes have been sent, acknowledged, or lost.

### 2.1 Sequence Numbers and ACKs

TCP numbers bytes in the stream. The receiver sends a cumulative acknowledgment that says, in effect, “I have received everything up to byte `N - 1`; send me byte `N` next.”

### 2.2 Retransmission

If an acknowledgment does not arrive in time, the sender assumes a loss and retransmits. Retransmission can happen after:

- a **retransmission timeout**, or
- **duplicate ACKs** that strongly suggest a gap in the stream.

### 2.3 In-Order Delivery

TCP exposes an ordered byte stream to the application. Even if later segments arrive first, the receiving TCP stack will not deliver the missing gap to the application until the missing bytes arrive.

## 3. Flow Control and Congestion Control

### 3.1 Flow Control

Flow control protects the receiver. If the receiving application cannot read data quickly enough, the advertised receive window shrinks, and the sender must slow down.

### 3.2 Congestion Control

Congestion control protects the network. The sender uses signals such as loss, delay growth, or explicit congestion marking to infer that the path is overloaded and should carry less traffic.

Two useful limits combine to define how much data can be in flight:

```text
usable_window = min(receive_window, congestion_window)
```

### 3.3 Latency-Throughput Tradeoff

On high-latency paths, a sender needs a sufficiently large in-flight window to keep the link busy. The **bandwidth-delay product** estimates how many bytes must be in flight to fully utilize the path.

## 4. UDP Contrast

UDP provides ports and checksums but not connection setup, retransmission, ordering, or built-in congestion control semantics. That makes it lightweight, but the application must handle any required reliability or timing policy itself.

This is why DNS queries, telemetry bursts, streaming control traffic, and QUIC-based systems can use UDP differently from bulk file transfer over TCP.

## 5. Worked Example

Assume:

```text
MSS = 1000 bytes
receive_window = 6000 bytes
congestion_window = 5000 bytes
usable_window = 5000 bytes
```

A sender wants to transmit bytes `1` through `5000` over TCP as five segments:

```text
S1 = bytes 1-1000
S2 = bytes 1001-2000
S3 = bytes 2001-3000
S4 = bytes 3001-4000
S5 = bytes 4001-5000
```

Assume `S2` is lost in the network, but the others arrive.

### 5.1 Initial Send

Because the usable window is `5000` bytes, the sender may send all five segments without waiting.

### 5.2 Receiver Behavior

The receiver gets `S1` and sends:

```text
ACK 1001
```

Then `S3` arrives, but `S2` is missing. TCP cannot advance the cumulative acknowledgment, so the receiver sends:

```text
duplicate ACK 1001
```

`S4` arrives:

```text
duplicate ACK 1001
```

`S5` arrives:

```text
duplicate ACK 1001
```

At this point the sender has seen three duplicate ACKs for the same missing byte position.

### 5.3 Fast Retransmit

The sender infers that bytes starting at `1001` were lost and retransmits `S2` without waiting for a full timeout.

### 5.4 Recovery

When `S2` finally arrives, the receiver now has a contiguous byte range from `1` through `5000`, so it sends:

```text
ACK 5001
```

That cumulative ACK confirms that all five segments are now received in order.

Verification: the receiver keeps acknowledging `1001` until the missing bytes `1001-2000` arrive, and once retransmitted `S2` fills the gap, the acknowledgment jumps to `5001`, confirming the full `1-5000` byte range.

## 6. Pseudocode Pattern

```text
procedure usable_in_flight_limit(receive_window, congestion_window):
    if receive_window < congestion_window:
        return receive_window
    return congestion_window
```

Time: `Theta(1)` worst case. Space: `Theta(1)` auxiliary space.

## 7. Common Mistakes

1. **Flow-control versus congestion-control confusion.** Treating the receive window and congestion window as the same mechanism obscures whether the bottleneck is the receiver or the network path; inspect both separately.
2. **IP-reliability assumption.** Expecting IP to guarantee ordered delivery or retransmission leads to the wrong mental model; those guarantees are transport-layer behavior, not network-layer behavior.
3. **Timeout-only thinking.** Assuming every loss is recovered only after a timeout ignores duplicate-ACK-driven recovery; packet traces often show fast retransmit long before a timer fires.
4. **Throughput-without-latency analysis.** Looking only at bandwidth ignores the window needed to fill a high-latency path; long RTTs can limit throughput even when raw capacity is high.
5. **UDP-as-broken-TCP framing.** Describing UDP only as “unreliable TCP” misses its actual design tradeoff; it provides a different service model that some applications want explicitly.

## 8. Practical Checklist

- [ ] Separate handshake failures, retransmission behavior, and application timeouts when diagnosing a transport problem.
- [ ] Inspect both receive-window and congestion-window signals before concluding why throughput is low.
- [ ] Use packet captures or socket metrics to confirm whether losses trigger duplicate ACKs or retransmission timeouts.
- [ ] Estimate the bandwidth-delay product when evaluating high-latency links.
- [ ] Treat UDP applications as responsible for any reliability or ordering semantics they need.
- [ ] Name complexity claims as worst, average, or expected whenever discussing transport algorithms or implementations.

## 9. References

- Stevens, W. Richard, Kevin R. Fall, and Gary R. Wright. 2011. *TCP/IP Illustrated, Volume 1* (2nd ed.). Addison-Wesley.
- Allman, Mark, Vern Paxson, and Ethan Blanton. 2009. *TCP Congestion Control*. RFC 5681. <https://datatracker.ietf.org/doc/html/rfc5681>
- Postel, Jon. 1981. *Transmission Control Protocol*. RFC 793. <https://datatracker.ietf.org/doc/html/rfc793>
- Eddy, Wesley. 2011. *TCP Extensions for High Performance*. RFC 7323. <https://datatracker.ietf.org/doc/html/rfc7323>
- Jacobson, Van. 1988. Congestion Avoidance and Control. *ACM SIGCOMM Computer Communication Review* 18(4). <https://doi.org/10.1145/52325.52356>
- Kurose, James F., and Keith W. Ross. 2021. *Computer Networking: A Top-Down Approach* (8th ed.). Pearson.
- Arpaci-Dusseau, Remzi H., and Andrea C. Arpaci-Dusseau. 2018. *Computer Networks: A Systems Approach*. <https://book.systemsapproach.org/>
