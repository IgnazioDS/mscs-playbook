# Reliability, Idempotency, and the Exactly-Once Myth

## What it is
A practical view of reliability in distributed data systems, focusing on
idempotent processing, deduplication, and replay rather than strict
"exactly-once" guarantees.

## Why it matters
Failures are inevitable. Systems that rely on exactly-once semantics often
fail in production when retries and partial writes occur.

## Architecture patterns
- At-least-once delivery with idempotent consumers
- Deduplication tables keyed by event_id
- Transactional outbox for producer reliability

## Failure modes
- Duplicate processing due to retries
- Lost updates when idempotency is missing
- Inconsistent state across OLTP and analytics stores

## Operability checklist
- Define idempotency keys and retention windows
- Track retry rates and DLQ volume
- Document replay procedures and limits
- Test with forced duplicate inputs

## References
- Exactly-Once Semantics Are Overrated — https://www.confluent.io/blog/exactly-once-semantics-are-overrated/
- Transactional Outbox Pattern — https://microservices.io/patterns/data/transactional-outbox.html
