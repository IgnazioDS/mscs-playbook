# Batch vs Streaming Tradeoffs

## What it is
A comparison of two execution models:
- Batch: process data in large chunks on a schedule
- Streaming: process events continuously as they arrive

## Why it matters
The right choice depends on latency, cost, and consistency requirements.

## Architecture patterns
- Lambda architecture (batch + stream)
- Kappa architecture (stream-first)
- Micro-batching for cost control

## Failure modes
- Batch windows missing late-arriving data
- Streaming pipelines with complex state recovery
- Dual-pipeline drift in Lambda architectures

## Operability checklist
- Define freshness SLOs and late data handling
- Monitor end-to-end lag and processing time
- Document backfill and replay procedures
- Validate correctness under duplicates

## References
- The Log: What every software engineer should know — https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know
- Streaming Systems (Akidau et al.) — https://www.oreilly.com/library/view/streaming-systems/9781491983874/
