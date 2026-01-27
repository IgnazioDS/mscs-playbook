# Toolkit Worked Example

## Scenario
A generative AI customer support assistant that answers billing and account questions, can trigger account actions, and is integrated into a web app chat.

## Risk assessment (top 5 risks)
| Risk | Severity | Likelihood | Mitigation |
| --- | --- | --- | --- |
| Hallucinated billing advice | High | Med | Cite sources, refusal rules, human escalation |
| Unauthorized account actions | High | Low | Strong auth, action confirmation, rate limits |
| Data leakage in responses | High | Med | PII redaction, prompt filtering, logging |
| Bias in handling priority users | Med | Med | Fairness checks, audit queues |
| Prompt injection | Med | Med | Input sanitization, tool isolation |

## Go/No-Go decision
- **Decision**: No-Go for autonomous actions; Go for read-only responses.
- **Rationale**: High-severity risks remain for account actions.

## Incident response (first 24 hours)
- Disable action-triggering tools
- Triage affected users and sessions
- Preserve logs and model versions
- Notify support leadership and compliance
- Publish user-facing correction notice

## Monitoring metrics
- Hallucination rate on policy intents
- Escalation rate to human agents
- User-reported harm rate
- Action error rate for tool calls
