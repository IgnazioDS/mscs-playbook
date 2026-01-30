# AI Copilot UI and Guardrails

## Context
A productivity app adds an AI copilot to draft responses and summarize threads.
The team needs a UI that supports trust and safe use.

## Users and jobs-to-be-done
- Operators drafting messages quickly
- Reviewers verifying content accuracy
- Managers tracking compliance

## Constraints
- High risk of hallucination and policy violations
- Human review required before sending
- Latency budget under three seconds

## Hypotheses
- Showing source highlights improves trust calibration.
- Explicit review gates reduce policy violations.

## Prototype approach
- Wizard flow with step-by-step review
- Inline citations and confidence indicators
- Editable drafts with required confirmation

## Evaluation plan
- Usability tests with error-spotting tasks
- Offline evaluation using curated risk scenarios

## Metrics
- Rate of detected errors in draft review
- Time to approve and send
- Policy violation rate
- Trust calibration survey

## Results
- Error detection improved by 20 percent
- Approval time increased by 10 percent but within SLA

## Tradeoffs
- More friction for expert users
- Some users over-trust confidence labels

## Shipping checklist
- Guardrails and escalation paths validated
- Audit logging enabled
- Clear disclaimers and limitations shown
- Feedback loop to improve prompts and tools
