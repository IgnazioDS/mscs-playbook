# RAG Support Assistant

## Problem and constraints
- Answer customer support questions using internal knowledge base
- Cite sources and avoid unsupported claims
- Handle product updates weekly and multiple languages

## Architecture (components and data flow)
- Ingest documentation, tickets, and release notes into a document store
- Chunk, embed, and index into a vector database with metadata
- Retrieve top-k passages with hybrid search and re-ranking
- Generate a response with citations and a confidence score

## Prompting and tool design
- System prompt enforces citation and refusal rules
- Tool: retrieve_passages(query, filters) returns passages with source IDs
- Post-processor validates citations against retrieved source IDs

## Evaluation plan and metrics
- Offline: labeled Q/A set with expected citations
- Metrics: answer correctness, citation accuracy, refusal rate, latency
- Online: thumbs up/down with escalation for low confidence

## Failure modes and mitigations
- Hallucinated answers when retrieval fails: add fallback to ask clarifying questions
- Stale answers after product updates: schedule re-indexing and freshness checks
- Overly long answers: enforce response length caps

## Security and privacy considerations
- Filter by tenant and access level before retrieval
- Redact PII from logs and prompts
- Store audit logs for answers and citations

## Cost and latency levers
- Cache embeddings and frequent Q/A pairs
- Reduce top-k and re-ranker depth for low-value queries
- Use smaller models for first-pass drafts

## What I would ship checklist
- [ ] Golden eval set with 50 to 100 questions
- [ ] Citation validation and refusal policy
- [ ] Retrieval logs with query and passage IDs
- [ ] Freshness SLA with automated re-indexing
- [ ] On-call dashboard for failure monitoring
