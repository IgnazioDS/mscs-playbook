# Customer Onboarding Workflow

TL;DR: Rebuild a brittle onboarding flow into a layered workflow service with clear boundaries, integrate KYC providers via adapters, and migrate with a strangler facade.

## Overview
- Problem: onboarding spans multiple systems and fails inconsistently.
- Why it matters: slow or broken onboarding increases drop-off.
- Scope: account creation, identity verification, and initial setup.
- Stakeholders: product, backend, compliance, support, legal.
- Out of scope: long-term lifecycle management and billing.
- Deliverable: predictable onboarding workflow with auditability.
- Success: onboarding can be reconfigured without deploys.
- Constraint: no client app changes during initial rollout.

## Requirements and Constraints
### Functional
- Support multi-step onboarding with pause and resume.
- Integrate external KYC and document verification providers.
- Provide status and error reasons to client applications.
- Maintain audit trail for compliance.

### Non-functional
- SLO: 99.5% onboarding availability.
- Latency: p95 step completion under 2 seconds.
- Cost: per-user KYC cost within budget.
- Safety: no onboarding without required compliance checks.
- Reliability: tolerate provider timeouts and retries.

### Assumptions
- KYC providers have variable latency and rate limits.
- Existing user database remains the source of truth.
- Some customers require manual review before activation.
- Providers can return partial results and require retries.

## System Design
### Components
- Presentation layer: onboarding API and webhooks.
- Application layer: workflow orchestrator and use cases.
- Domain layer: OnboardingAggregate and Policy rules.
- Infrastructure layer: repositories, providers, message bus.
- Anti-corruption layer: adapters for KYC and document APIs.

### Data Flow
1) Client submits onboarding request.
2) Workflow orchestrator creates Onboarding aggregate.
3) KYC adapter sends verification request.
4) Webhook updates step state and triggers next actions.
5) Completion event updates user status.

### Interfaces
- `POST /onboarding/start` with identity and profile data.
- `GET /onboarding/{id}` returns status and next step.
- `POST /onboarding/{id}/documents` uploads required files.

### Data Schemas
- `onboarding_cases`: case_id, user_id, status, started_at.
- `onboarding_steps`: case_id, step, status, updated_at.
- `kyc_results`: case_id, provider_ref, decision, risk_score.

## Data and Modeling Approach
- Aggregate: Onboarding case with step state transitions.
- Patterns:
  - State pattern for step transitions and guard checks.
  - Saga for multi-step orchestration with compensation.
  - Repository for persistence and testability.
  - Anti-corruption layer to isolate provider models.
- Migration strategy:
  - Strangler facade routes new users to the new workflow.
  - Legacy flow remains for existing in-flight cases.

## Evaluation Plan
- Metrics: completion rate, average time to complete, error rate.
- Baselines: current onboarding success and time-to-complete.
- Acceptance gates:
  - Completion rate improves by at least 10%.
  - No increase in compliance violations.
  - p95 latency within 20% of baseline.

## Failure Modes and Mitigations
- Provider outage -> retry with backoff and queue steps.
- Stuck workflows -> watchdog to detect stale steps.
- Data mismatch -> validation layer and strict schema mapping.
- Migration errors -> feature flags and gradual rollout.
- Compliance drift -> automated policy checks and audits.

## Operational Runbook
### Logging
- Log case_id, step transitions, and provider responses.
- Record webhook deliveries and retries.

### Metrics
- Completion rate, step latency, provider error rate.
- Queue depth and retry counts.

### Tracing
- Trace case_id across API, workflow, and provider calls.

### Alerts
- Completion rate drops below 95%.
- Provider error rate > 5% for 10 minutes.
- Stuck workflow count > 50.

### Rollback
- Route traffic back to legacy onboarding via feature flag.
- Keep data mapping to reconcile cases across systems.

### On-call Checklist
- Verify provider status and webhook health.
- Inspect stuck cases and reprocess steps.
- Validate audit logs for missing entries.

## Security, Privacy, and Compliance
- Encrypt PII at rest and in transit.
- Apply least privilege to KYC data access.
- Retain audit logs for regulatory requirements.

## Iteration Plan
- Add risk-based step skipping for low-risk customers.
- Introduce self-serve document reupload flows.
- Support multi-entity onboarding for business accounts.
