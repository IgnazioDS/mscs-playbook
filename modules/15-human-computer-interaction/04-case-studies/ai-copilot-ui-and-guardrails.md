# AI Copilot UI and Guardrails

## Context
A productivity app is adding an AI copilot for drafting and summarization. The
team needs an interface that supports trust, correction, and safe use.

## Users and Jobs-to-Be-Done
- Knowledge workers who want drafts they can quickly edit.
- Managers who need consistent tone and compliant outputs.

## Constraints
- Outputs must be reviewable before sharing.
- Sensitive data cannot be sent to external services.
- The copilot must work within existing editor layouts.

## Hypotheses
- Showing sources and rationale will improve trust and adoption.
- Inline revision tools will reduce time to acceptable output.
- Guardrails on risky actions will reduce policy violations.

## Prototype Approach
- Wizard-of-oz prototype with staged responses and citations.
- Variants for inline suggestions versus side-panel previews.
- Error and refusal states to test transparency language.

## Evaluation Plan
- Think-aloud sessions with realistic drafting tasks.
- A/B test of inline edits versus side-panel preview.
- Logging of correction rate and user overrides.

## Metrics
- Task success: draft accepted or edited to completion.
- Time-on-task: drafting and editing time.
- Correction rate: percentage of output edited by users.
- Trust score: post-task survey on confidence and clarity.

## Results
- Side-panel preview reduced accidental sends by 40 percent.
- Inline edits were faster but increased unnoticed errors.
- Trust scores improved with source previews and disclaimers.

## Tradeoffs
- Transparency UI increased cognitive load on small screens.
- Stricter guardrails reduced speed for expert users.
- Source previews required additional space and interaction steps.

## Shipping Checklist
- Clear review step before share or send.
- Guardrails implemented for sensitive topics and actions.
- Audit logging for prompts, outputs, and user edits.
- Accessibility review for screen readers and keyboard navigation.
- Human fallback guidance for refusals or low confidence.
