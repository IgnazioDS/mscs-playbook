# Usability Testing and Experiments

## Key Ideas
- Usability testing observes whether people can complete tasks with an interface, while experiments estimate the causal effect of a change on measured outcomes.
- Task design, moderation quality, and success criteria determine whether usability findings are trustworthy.
- Experiments require clear hypotheses, guardrail metrics, and a disciplined stopping rule to avoid noise-driven decisions.
- Qualitative usability findings and quantitative experiment results answer different questions and should not be treated as interchangeable.
- Strong product decisions often combine usability diagnosis before launch with experimentation after launch.

## 1. Why testing and experimentation are different

Usability testing and experimentation are both evaluation tools, but they serve different purposes.

**Usability testing** asks:

- can users complete the task
- where do they hesitate, misunderstand, or recover poorly
- what aspects of the design create friction

**Experiments** ask:

- did variant B outperform variant A on a defined metric
- was the observed difference large enough and credible enough to act on

If a team confuses these methods, it may either over-quantify an interface issue that needs observation or over-generalize from a few observed sessions when a causal measurement is needed.

## 2. Designing a useful usability study

A usability study should define:

- the participant profile
- the tasks to attempt
- the success condition for each task
- what the moderator will and will not say
- what evidence will be recorded

Task realism matters. If the scenario is vague or unnatural, the session mainly measures how well participants interpret the prompt rather than how well the interface supports the real activity.

## 3. Running experiments responsibly

An experiment compares variants under controlled exposure. Important terms:

- **primary metric**: the main outcome the experiment is intended to improve
- **guardrail metric**: a metric watched to prevent hidden regressions
- **sample size**: the number of observations required to detect a meaningful effect with planned confidence

Stopping an experiment early because the graph "looks better" is a common source of false conclusions. The stopping rule should be decided before the test begins.

## 4. Worked example: combining usability testing with an A/B test

A team redesigns a signup flow.

Usability study with 6 participants:

- old flow: 3 of 6 complete signup without moderator clarification
- new flow: 5 of 6 complete signup without clarification

Observed problem in the old flow:

- users do not understand whether the password rules are mandatory before submission

The team fixes the copy and launches an A/B test.

A/B test results:

- Variant A: 1,000 visitors, 420 completed signup
- Variant B: 1,000 visitors, 480 completed signup

Compute conversion rates:

- A: `420 / 1000 = 0.42`
- B: `480 / 1000 = 0.48`

Absolute lift:

- `0.48 - 0.42 = 0.06`, or `6` percentage points

Interpretation:

- usability testing identified the mechanism: unclear password expectations
- the experiment measured the live impact: a `6` point conversion increase

Verification: the conversion calculations are correct and show Variant B outperforming Variant A by `0.06`.

## 5. When to use which method

Use usability testing when the team needs to know why a design is failing. Use experiments when the team needs to know whether a change improved a measured outcome at scale. In many product workflows, the strongest sequence is:

1. diagnose interaction issues through observation
2. refine the design
3. measure the effect in production

This sequence avoids launching weak variants and avoids making high-confidence product decisions from only a few sessions.

## 6. Common Mistakes

1. **Method substitution**: treating an A/B test as if it explains user confusion, or a usability test as if it proves production impact, leads to wrong conclusions; pick the method that matches the question.
2. **Weak task prompts**: vague usability tasks create artificial failure patterns; use realistic prompts with clear success conditions.
3. **Early stopping**: ending an experiment because short-term noise looks promising increases false positives; define the stopping rule before launch.
4. **Metric tunnel vision**: improving the primary metric while harming a key guardrail can degrade the broader experience; monitor both outcome and risk metrics.
5. **Confounded variants**: changing multiple meaningful factors at once makes interpretation hard; isolate the design difference when possible.

## 7. Practical Checklist

- [ ] Decide whether the current question is diagnostic, causal, or both.
- [ ] Write task prompts and success criteria before running usability sessions.
- [ ] Pilot the moderator script to remove ambiguity and accidental coaching.
- [ ] Define primary and guardrail metrics before launching an experiment.
- [ ] Set sample-size assumptions and stopping rules in advance.
- [ ] Combine observed behavior with measured outcomes before making a large product decision.

## References

1. Steve Krug, *Rocket Surgery Made Easy*. [https://sensible.com/rocket-surgery-made-easy/](https://sensible.com/rocket-surgery-made-easy/)
2. Nielsen Norman Group, *Usability Testing*. [https://www.nngroup.com/topic/usability-testing/](https://www.nngroup.com/topic/usability-testing/)
3. Tom Tullis and Bill Albert, *Measuring the User Experience*. [https://www.elsevier.com/books/measuring-the-user-experience/tullis/978-0-12-415781-1](https://www.elsevier.com/books/measuring-the-user-experience/tullis/978-0-12-415781-1)
4. Ron Kohavi, Diane Tang, and Ya Xu, *Trustworthy Online Controlled Experiments*. [https://experimentguide.com/](https://experimentguide.com/)
5. GOV.UK Service Manual, *Usability Testing*. [https://www.gov.uk/service-manual/user-research](https://www.gov.uk/service-manual/user-research)
6. CXL, *A/B Testing Knowledge Base*. [https://cxl.com/institute/programs/ab-testing/](https://cxl.com/institute/programs/ab-testing/)
7. Jakob Nielsen, *Why You Only Need to Test with 5 Users*. [https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/](https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/)
