# Event-Driven Architecture and Streaming

## What it is
A design where systems publish events to a durable log and consumers process
those events asynchronously, often in near real time.

## Why it matters
Streaming enables low-latency analytics, decouples services, and supports
replays and backfills.

## Architecture patterns
- Append-only event log with retention
- Consumer groups for scale-out processing
- Idempotent consumers with deduplication
- Schema registry and versioned events

## Failure modes
- Consumer lag and growing backlog
- Poison messages stalling processing
- Schema changes breaking downstream jobs

## Operability checklist
- Monitor lag, throughput, and consumer errors
- Set retention and compaction policies
- Implement dead-letter handling
- Test replay and backfill procedures

## References
- Kafka: A Distributed Messaging System for Log Processing — https://kafka.apache.org/
- Event-Driven Architecture — https://martinfowler.com/articles/201701-event-driven.html
