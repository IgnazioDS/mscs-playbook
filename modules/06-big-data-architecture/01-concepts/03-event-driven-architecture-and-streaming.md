# Event-Driven Architecture and Streaming

## Key Ideas

- Event-driven architecture organizes systems around facts that occurred, while streaming systems process ordered event flows under latency and state constraints.
- A durable event log decouples producers from consumers by letting data be written once and consumed many times at different speeds.
- Event time, processing time, partitioning, and consumer offsets are fundamental concepts because they determine ordering, correctness, and recovery behavior.
- Streaming architecture is valuable when low-latency reaction, replay, or many independent consumers matter more than simple scheduled batch processing.
- The main operational challenge is not publishing events; it is handling lag, schema evolution, duplicates, and stateful recovery safely.

## 1. What Event-Driven Streaming Systems Are

An event-driven architecture uses events as the primary interface between components. A streaming system processes those events continuously or near continuously as they arrive.

### 1.1 Core Definitions

- An **event** is a record describing something that happened, such as `order_created`.
- An **event log** is an append-oriented sequence of events stored durably.
- A **partition** is an ordered subset of the log used for scale-out.
- An **offset** is the consumer position within a partition.
- **Event time** is when the event actually occurred.
- **Processing time** is when the system handled the event.

### 1.2 Why This Matters

The event log can become the system's recovery backbone. When consumers fail, logic changes, or new analytical needs appear, replaying the same input stream often matters more than the original low-latency benefit.

## 2. Architectural Mechanics

### 2.1 Producers and Consumers

Producers emit events to the log. Consumers read the log independently, which allows one producer stream to feed many downstream systems without synchronous coupling.

### 2.2 Partitioning and Ordering

Ordering is usually guaranteed only within a partition, not globally. Choosing the partition key therefore determines what sequences can be reconstructed exactly.

### 2.3 Replay and Backfill

Because the log is durable, consumers can reread older events after failure, code changes, or data corrections. This is one of the strongest reasons to adopt an event-driven design.

## 3. When Streaming Is Worth the Complexity

### 3.1 Strong Use Cases

Streaming is attractive when:

- freshness targets are measured in seconds or minutes,
- many consumers need the same input events,
- replay and audit are operationally important,
- stateful alerting or incremental aggregation is required.

### 3.2 Weak Use Cases

If the data is naturally file-based, latency is unimportant, and the pipeline runs once per day, a simpler batch design may be easier to operate.

### 3.3 Stateful Complexity

Stateful streaming introduces windowing, out-of-order handling, checkpointing, and recovery concerns. These are not optional edge cases. They are central design commitments.

## 4. Worked Example: Partitioning and Ordering

Suppose an event log has `3` partitions and uses `customer_id` as the partition key. The partition assignment is:

```text
customer_A -> partition 0
customer_B -> partition 1
customer_C -> partition 2
```

Now consider these events:

```text
e_1 = (customer_A, order_created)
e_2 = (customer_B, order_created)
e_3 = (customer_A, order_paid)
e_4 = (customer_C, order_created)
e_5 = (customer_A, order_shipped)
```

### 4.1 Place Events into Partitions

Using the partition key:

```text
partition 0: e_1, e_3, e_5
partition 1: e_2
partition 2: e_4
```

### 4.2 Reason About Ordering

For `customer_A`, the consumer sees:

```text
order_created -> order_paid -> order_shipped
```

This sequence is reliable within partition `0`.

Across all customers, there is no guaranteed global order between:

```text
e_2 and e_3
e_4 and e_5
```

### 4.3 Interpret the Design Choice

Partitioning by `customer_id` preserves per-customer event order, which is useful for customer-centric state machines. It does not preserve a universal cross-customer timeline.

Verification: because all `customer_A` events map to the same partition, their relative order is preserved, while events for different customers land in different partitions and therefore do not have a strong global ordering guarantee.

## 5. Common Mistakes

1. **Global-order assumption.** Assuming the entire stream has one strict order leads to subtle correctness bugs; most systems guarantee ordering only within a partition.
2. **Event-time neglect.** Treating processing time as if it were the event's real timestamp creates incorrect windows and delayed-data handling; model event time explicitly.
3. **Consumer-coupling drift.** Letting downstream consumers depend on undocumented producer behavior reintroduces tight coupling; use versioned schemas and clear event semantics.
4. **Replay blindness.** Building consumers that cannot safely reread old events defeats one of the main benefits of the log; design for replay from the start.
5. **Streaming-by-default adoption.** Choosing streaming where scheduled batch would satisfy the requirement adds state and recovery complexity without real benefit; justify the latency need explicitly.

## 6. Practical Checklist

- [ ] Define what the event represents and who owns its schema and semantics.
- [ ] Choose a partition key based on the ordering guarantees consumers truly need.
- [ ] Track both event time and processing time when latency and late data matter.
- [ ] Make consumer state and replay behavior explicit before going live.
- [ ] Monitor lag, retries, and schema-compatibility failures continuously.
- [ ] Keep raw events durably retained long enough to support realistic backfills and audits.

## 7. References

- Kleppmann, Martin. 2017. *Designing Data-Intensive Applications*. O'Reilly Media. <https://dataintensive.net/>
- Akidau, Tyler, Slava Chernyak, and Reuven Lax. 2018. *Streaming Systems*. O'Reilly Media.
- Apache Kafka. 2026. *Documentation*. <https://kafka.apache.org/documentation/>
- Confluent. 2026. *Event Streaming Patterns*. <https://developer.confluent.io/patterns/>
- Fowler, Martin. 2017. *What do you mean by Event-Driven?* <https://martinfowler.com/articles/201701-event-driven.html>
- Apache Flink. 2026. *Event Time and Watermarks*. <https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/time/>
- Redpanda. 2026. *Kafka Compatibility and Streaming Basics*. <https://docs.redpanda.com/>
