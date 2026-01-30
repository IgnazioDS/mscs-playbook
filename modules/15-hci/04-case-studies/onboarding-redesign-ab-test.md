# Onboarding Redesign A/B Test

## Context
A SaaS analytics product has high signup completion but low activation. The team
wants to redesign onboarding to guide new users to a first successful report.

## Users and Jobs-to-Be-Done
- Data analysts who need a quick way to connect a data source and build a report.
- Team leads who want a clear path to value within the first session.

## Constraints
- Cannot change backend data connectors in this release.
- Must keep time-to-first-report under five minutes.
- Legal requires explicit consent before importing data.

## Hypotheses
- A guided checklist will increase first-report completion rate.
- Inline examples will reduce drop-off during data connection.
- A simplified step count will reduce perceived effort.

## Prototype Approach
- Clickable prototype for the new checklist and step flow.
- High-fidelity mock for the data connection screen.
- Variant with progressive disclosure for advanced settings.

## Evaluation Plan
- Conduct five moderated usability tests for qualitative feedback.
- Run an A/B test for two weeks on new signups.
- Monitor support tickets tagged to onboarding.

## Metrics
- Activation rate: first report created within 24 hours.
- Time-on-task: duration from signup to first report.
- Task success: percent completing onboarding without errors.
- Drop-off rate at each step.

## Results
- Activation increased from 32 percent to 44 percent in the test group.
- Median time-to-first-report decreased by 18 percent.
- Largest drop-off moved from data connection to permissions.

## Tradeoffs
- Added checklist increased page length on small screens.
- Progressive disclosure reduced clutter but hid advanced settings.
- Consent step improved compliance but slightly increased completion time.

## Shipping Checklist
- Analytics events verified for each onboarding step.
- Error states documented with recovery guidance.
- Copy reviewed for clarity and consent language.
- Accessibility audit completed for keyboard and screen readers.
- Rollback plan and guardrails agreed with stakeholders.
