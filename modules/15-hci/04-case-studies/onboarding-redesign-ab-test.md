# Onboarding Redesign A/B Test

## Context
A consumer SaaS product sees high drop-off during onboarding and wants to
improve activation without increasing support load.

## Users and jobs-to-be-done
- New users trying to connect their first data source
- Admins validating security requirements
- Analysts wanting a quick first report

## Constraints
- Limited engineering bandwidth for new flows
- Legal requirements for consent and data usage
- Must keep time-to-first-value under five minutes

## Hypotheses
- A guided checklist will reduce confusion and increase activation.
- Inline validation will reduce errors during setup.

## Prototype approach
- Two low-fidelity prototypes to test navigation
- High-fidelity variant with a stepper and inline tips
- Copy updated for clarity and trust cues

## Evaluation plan
- Usability test with eight participants
- A/B test with 10 percent traffic for two weeks

## Metrics
- Activation rate
- Time-to-first-value
- Support ticket rate during onboarding
- SUS score

## Results
- Activation increased by 12 percent
- Median time-to-first-value decreased by 18 percent
- Support tickets flat

## Tradeoffs
- Additional steps created more screens to maintain
- Inline tips increased content load on mobile

## Shipping checklist
- Success metrics and guardrails reviewed
- Accessibility checks passed
- Localization updates complete
- Analytics events validated
