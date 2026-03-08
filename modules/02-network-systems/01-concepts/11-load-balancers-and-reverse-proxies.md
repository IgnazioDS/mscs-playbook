# Load Balancers and Reverse Proxies

## Key Ideas

- A reverse proxy sits in front of backend services and accepts client requests on their behalf, while a load balancer adds a policy for distributing traffic across multiple backends.
- Layer 4 and Layer 7 balancing solve different problems: Layer 4 focuses on connection forwarding, while Layer 7 can route based on protocol details such as hostnames, paths, or headers.
- Health checks, connection draining, and retry policy matter as much as the balancing algorithm because production failures are usually partial rather than absolute.
- TLS termination, header forwarding, and source-address preservation change what the backend can observe, so debugging requires knowing where the connection is actually being terminated.
- Reverse proxies and load balancers are core cloud and platform primitives, not optional extras, because they shape availability, rollout safety, and failure isolation.

## 1. What It Is

A **reverse proxy** is an intermediary that receives requests from clients and forwards them to one or more backend services. A **load balancer** is a reverse proxy or forwarding device that also decides which backend instance should receive each connection or request.

### 1.1 Core Definitions

- A **backend** is the service instance that ultimately handles the request.
- A **virtual IP** or **frontend listener** is the client-facing address and port.
- A **health check** tests whether a backend should receive traffic.
- **Connection draining** allows existing connections to finish while new ones stop being routed to a backend.
- **TLS termination** means the proxy decrypts TLS traffic before forwarding it onward.
- **Sticky sessions** send related requests from one client to the same backend.

### 1.2 Why This Matters

Many systems appear simple from the client side because the balancing layer hides replication and failure. That abstraction is powerful, but it also creates new failure modes:

- a backend is healthy at TCP but broken at HTTP,
- retries amplify overload,
- source IP information disappears,
- or a deployment drains traffic incorrectly.

Without a clear proxy model, these issues are misread as generic application bugs.

## 2. Layer 4 and Layer 7 Behavior

### 2.1 Layer 4 Balancing

Layer 4 balancing uses transport-layer information such as IP addresses and ports. It forwards TCP or UDP traffic without interpreting application semantics.

This is efficient and general, but it cannot route based on URL path, HTTP header, or cookie content.

### 2.2 Layer 7 Balancing

Layer 7 balancing understands application protocol structure, usually HTTP or gRPC. It can:

- route `/api` and `/static` differently,
- apply per-host policies,
- terminate TLS,
- add forwarding headers,
- or retry certain request classes selectively.

That flexibility is useful, but it also means the proxy becomes part of the application path rather than a pure transport relay.

## 3. Distribution, Health, and Failover

Common balancing policies include:

- **round robin**
- **least connections**
- **weighted distribution**
- **hash-based affinity**

The policy alone is not enough. The system also needs a rule for removing unhealthy nodes and reintroducing them safely. A backend that is merely slow may be more dangerous than one that is hard down because it can trigger retries, queue buildup, and timeout cascades.

## 4. Observability and Correctness

When a proxy sits in front of a service, the backend may no longer see the original client tuple directly. Instead, it may observe:

- the proxy as the TCP peer,
- forwarded metadata such as `X-Forwarded-For`,
- or the original source only if a protocol such as Proxy Protocol is used.

This matters when correlating logs, packet captures, firewall rules, and rate limits. A packet capture on the backend may show proxy-to-backend traffic even when the client thinks it is connected directly to `service.example.com`.

## 5. Worked Example

Suppose a reverse proxy listens on:

```text
203.0.113.10:443
```

and forwards HTTP requests to three backends:

```text
app1 = 10.0.0.11:8080
app2 = 10.0.0.12:8080
app3 = 10.0.0.13:8080
```

Assume a round-robin policy with all backends initially healthy.

### 5.1 Initial Request Distribution

Requests arrive in this order:

```text
R1, R2, R3, R4, R5
```

Round robin assigns:

```text
R1 -> app1
R2 -> app2
R3 -> app3
R4 -> app1
R5 -> app2
```

### 5.2 Health Failure

Before `R6`, the health checker marks `app2` unhealthy because its `/healthz` endpoint returns HTTP `500`.

The healthy backend set becomes:

```text
{app1, app3}
```

### 5.3 Continued Routing

Requests `R6`, `R7`, and `R8` are distributed only across the healthy backends:

```text
R6 -> app3
R7 -> app1
R8 -> app3
```

No new requests should be sent to `app2` until health recovery is confirmed.

### 5.4 Connection Perspective

From the client's perspective, every request still targets:

```text
203.0.113.10:443
```

From the backend's perspective, the TCP peer may be the proxy rather than the original client unless source-preservation mechanisms are configured.

Verification: once `app2` is marked unhealthy, new requests stop being assigned to it, while the client-facing endpoint remains `203.0.113.10:443` throughout the entire trace.

## 6. Pseudocode Pattern

```text
procedure choose_backend_round_robin(backends, next_index):
    checked = 0

    while checked < length(backends):
        candidate = backends[next_index]
        next_index = (next_index + 1) mod length(backends)
        checked = checked + 1

        if candidate.is_healthy:
            return candidate, next_index

    return nil, next_index
```

Time: `O(n)` worst case when all or most backends are unhealthy and the balancer must scan the set of `n` backends. Space: `Theta(1)` auxiliary space.

## 7. Common Mistakes

1. **Proxy-versus-backend confusion.** Debugging the backend as if it were the client-facing endpoint hides where TLS, retries, and headers are actually handled; identify the real termination point first.
2. **Algorithm-only focus.** Debating round robin versus least connections while ignoring health checks and draining misses the larger reliability problem; failure handling is part of the balancing design.
3. **Source-IP assumption.** Assuming the backend always sees the original client IP can break logging, ACLs, and rate limits; confirm what metadata or transport mechanism preserves client identity.
4. **Retry amplification.** Adding aggressive proxy retries without checking backend capacity can magnify overload; treat retries as extra traffic, not free resilience.
5. **Layer-mismatch debugging.** Expecting an L4 balancer to make path-based HTTP decisions, or expecting an L7 proxy to behave like a transparent TCP relay, applies the wrong abstraction to the problem.

## 8. Practical Checklist

- [ ] Decide whether the workload needs Layer 4 forwarding or Layer 7 request-aware routing.
- [ ] Define health-check semantics that match real service readiness rather than just port openness.
- [ ] Confirm where TLS terminates and what the backend can actually observe about the client.
- [ ] Use connection draining during deployments so active requests do not fail abruptly.
- [ ] Check whether retries, sticky sessions, or header forwarding change application correctness.
- [ ] Correlate proxy logs with backend logs before concluding where a failure originated.

## 9. References

- NGINX. *Reverse Proxy*. <https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/>
- HAProxy Technologies. *HAProxy Configuration Tutorials*. <https://www.haproxy.com/documentation/haproxy-configuration-tutorials/>
- Envoy Proxy. *Overview*. <https://www.envoyproxy.io/docs/envoy/latest/intro/what_is_envoy>
- Google. 2024. *Cloud Load Balancing Overview*. <https://cloud.google.com/load-balancing/docs/load-balancing-overview>
- Amazon Web Services. 2024. *Elastic Load Balancing User Guide*. <https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/what-is-load-balancing.html>
- Beyer, Betsy, et al., eds. 2016. *Site Reliability Engineering*. O'Reilly Media. <https://sre.google/sre-book/table-of-contents/>
- Kurose, James F., and Keith W. Ross. 2021. *Computer Networking: A Top-Down Approach* (8th ed.). Pearson.
