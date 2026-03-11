# Interaction Design and Information Architecture

## Key Ideas
- Interaction design defines how a user moves through a task, while information architecture defines how content and options are organized.
- Task structure should be designed before surface-level UI details because layout cannot rescue a broken flow.
- Good information architecture reduces search cost by using clear grouping, labels, and navigation paths that match user mental models.
- Interaction design must account for normal paths, edge cases, errors, and recovery states.
- Architecture decisions are best validated through task-based testing such as card sorting, tree testing, and first-click evaluation.

## 1. Why structure matters before screens

Interfaces fail most often because the product's structure does not match how users think about their tasks. A beautiful visual layer on top of a broken flow only hides the problem temporarily. Interaction design and information architecture exist to make the underlying structure usable.

**Interaction design** answers questions like:

- what steps must happen, and in what order
- what feedback should appear after each action
- how can users undo or recover from mistakes

**Information architecture** answers questions like:

- where should information live
- how should categories be named
- how do users move between sections

## 2. Task flows and mental models

A **task flow** is the sequence of user actions and system responses needed to achieve a goal. A **mental model** is the user's internal expectation about how the system is organized and behaves.

Good structure aligns with mental models closely enough that the user can predict what will happen next. When alignment is poor, users hesitate, backtrack, or search inefficiently.

This is why teams should map:

- entry points
- decision points
- branches and exceptions
- completion and recovery paths

before debating visual detail.

## 3. Labeling, hierarchy, and navigation

Labels are part of the interaction, not just content. Vague or internally framed labels force users to translate product jargon into their own goals.

Useful architecture choices often include:

- shallow hierarchies when tasks are frequent
- progressive disclosure when complexity is necessary
- search-first navigation when the content space is large and known-item retrieval dominates

No navigation model is universally correct. The right structure depends on task frequency, predictability, and user vocabulary.

## 4. Worked example: restructuring a support portal

Suppose a support portal currently has these top-level sections:

- Resources
- Account Services
- Plans
- General

User research shows people mainly come to do three tasks:

1. change billing details
2. troubleshoot login
3. compare plan limits

The team proposes a new architecture:

- Billing and Payments
- Login and Account Access
- Plans and Limits
- Contact Support

Why this is better:

- the new labels map directly to user tasks
- "General" and "Resources" were internally convenient but not task oriented
- the portal now supports known-item retrieval more directly

Now consider a first-click test with 8 users trying to "change billing details":

- old IA: 3 of 8 choose the correct first section
- new IA: 7 of 8 choose the correct first section

The new architecture reduces ambiguity at the first navigation step.

Verification: the redesigned labels are task-aligned and improve first-click success from `3/8` to `7/8` in the stated test.

## 5. Designing for edge cases and recovery

A complete interaction model includes more than the happy path. It should also cover:

- missing data
- validation errors
- interrupted sessions
- permission limits
- empty states

Many products appear usable in demos because only ideal paths are designed. Real usability depends on how gracefully the structure handles partial progress and confusion.

## 6. Common Mistakes

1. **Screen-first design**: starting from page layouts instead of task structure creates beautiful dead ends; map flows and architecture before styling.
2. **Internal labeling**: using team vocabulary instead of user vocabulary makes navigation harder to predict; test labels with representative users.
3. **Hidden recovery paths**: failing to design for errors and backtracking turns minor mistakes into blocked tasks; define recovery states explicitly.
4. **Overdeep hierarchies**: nesting content too many levels down increases search cost and abandonment; flatten the structure where frequent tasks allow it.
5. **Untested architecture**: shipping a new IA without tree or first-click testing makes navigation quality guesswork; validate structure before full implementation.

## 7. Practical Checklist

- [ ] Identify the top user tasks before defining sections and navigation.
- [ ] Write labels in user language rather than internal organizational language.
- [ ] Map the main task flow, exceptions, and recovery states end to end.
- [ ] Choose a navigation model that matches task frequency and content size.
- [ ] Validate structure with tree tests, card sorting, or first-click studies.
- [ ] Review whether empty, error, and permission states still make the architecture understandable.

## References

1. Peter Morville and Louis Rosenfeld, *Information Architecture for the World Wide Web*. [https://www.oreilly.com/library/view/information-architecture-for/0596527349/](https://www.oreilly.com/library/view/information-architecture-for/0596527349/)
2. Alan Cooper et al., *About Face: The Essentials of Interaction Design*. [https://www.wiley.com/en-us/About+Face%3A+The+Essentials+of+Interaction+Design%2C+4th+Edition-p-9781118766576](https://www.wiley.com/en-us/About+Face%3A+The+Essentials+of+Interaction+Design%2C+4th+Edition-p-9781118766576)
3. Donna Spencer, *Card Sorting*. [https://abookapart.com/products/card-sorting](https://abookapart.com/products/card-sorting)
4. Nielsen Norman Group, *Information Architecture*. [https://www.nngroup.com/topic/information-architecture/](https://www.nngroup.com/topic/information-architecture/)
5. Jesse James Garrett, *The Elements of User Experience*. [https://www.oreilly.com/library/view/the-elements-of/9780134034317/](https://www.oreilly.com/library/view/the-elements-of/9780134034317/)
6. GOV.UK Service Manual, *Structuring Pages and Navigation*. [https://www.gov.uk/service-manual/design](https://www.gov.uk/service-manual/design)
7. Rosenfeld Media, *Enterprise Experience*. [https://rosenfeldmedia.com/books/enterprise-experience/](https://rosenfeldmedia.com/books/enterprise-experience/)
