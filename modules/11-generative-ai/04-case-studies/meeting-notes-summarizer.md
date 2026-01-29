# Meeting Notes Summarizer

## Problem and constraints
- Convert transcripts into concise, actionable summaries
- Preserve decisions, owners, and deadlines
- Support noisy transcripts and multiple speakers

## Architecture (components and data flow)
- Ingest transcript and speaker labels
- Segment by topic and detect action items
- Generate summary, decisions, and follow-ups
- Store output in a task tracker and shared notes

## Prompting and tool design
- Prompt includes explicit sections: summary, decisions, action items, risks
- Tool: create_tasks(items) posts action items to tracker
- Output schema enforces owners and due dates when available

## Evaluation plan and metrics
- Offline: compare against human-written notes
- Metrics: action item recall, owner accuracy, decision coverage
- Online: user feedback on usefulness and completeness

## Failure modes and mitigations
- Missing action items: add extraction-first pass before summarization
- Hallucinated owners: require explicit mention in transcript
- Overlong summaries: cap bullets and enforce word limits

## Security and privacy considerations
- Mask PII and sensitive project names in logs
- Restrict transcript access by team and project
- Apply retention policies aligned to HR and legal requirements

## Cost and latency levers
- Chunk long transcripts and summarize hierarchically
- Cache speaker metadata and meeting templates
- Use smaller models for extraction, larger for final polish

## What I would ship checklist
- [ ] JSON schema with strict validation
- [ ] Action item extraction benchmark
- [ ] Human review flow for low-confidence outputs
- [ ] Integration tests with the task tracker
- [ ] Documentation for retention and access controls
