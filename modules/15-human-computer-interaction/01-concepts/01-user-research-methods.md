# User Research Methods

## Key Ideas
- User research reduces design risk by replacing assumptions about users with structured evidence about needs, behaviors, and constraints.
- Generative research helps teams discover problems worth solving, while evaluative research checks whether a design actually works.
- Good method choice depends on the decision being made, not on which research technique is fashionable or easiest to run.
- Qualitative methods explain why behavior happens, and quantitative methods estimate how often it happens or how large the effect is.
- Research quality depends on sampling, protocol design, bias control, and how findings are translated into product decisions.

## 1. Why research comes first

Human-computer interaction starts with uncertainty about people, not uncertainty about code. A team may not know what users are trying to accomplish, what constraints shape their behavior, or which parts of the workflow are most costly. User research exists to reduce that uncertainty before the design is locked in.

A research method is a structured way to answer a question about users. The method must match the decision at hand. If the question is "what tasks are currently painful," interviews or contextual inquiry may be appropriate. If the question is "did the redesign improve completion rate," an experiment or instrumentation analysis is more appropriate.

## 2. Generative and evaluative research

**Generative research** is used early to discover opportunities, unmet needs, and real-world constraints. Common methods include:

- semi-structured interviews
- contextual inquiry
- diary studies
- field observation

**Evaluative research** is used later to assess a concept, workflow, or interface. Common methods include:

- usability testing
- heuristic review
- surveys
- A/B testing

The distinction matters because teams often misuse evaluative methods for discovery. A usability test can show where a prototype fails, but it is not a substitute for learning whether the problem itself is worth solving.

## 3. Qualitative and quantitative methods

**Qualitative research** focuses on meanings, motivations, and patterns in language or behavior. It is good for explanation and sense-making. Sample sizes are usually small because the goal is depth.

**Quantitative research** focuses on measurable variables such as completion rate, time on task, error count, or survey score. It is good for estimating prevalence and comparing alternatives. Sample sizes are usually larger because the goal is statistical confidence.

In practice, strong HCI work often combines both. A team might first interview users to understand failure patterns, then run a survey to estimate how widespread those failures are.

## 4. Worked example: choosing methods for a redesign decision

Suppose a team is redesigning appointment booking for a clinic app. Stakeholders ask three questions:

1. Why do users abandon booking?
2. Which prototype is easier to use?
3. Did the final change improve outcomes after launch?

Map each question to a method:

1. "Why do users abandon booking?"
   - best fit: interviews or contextual inquiry
   - reason: the team needs explanations, not just counts
2. "Which prototype is easier to use?"
   - best fit: moderated usability testing
   - reason: direct observation shows where each workflow breaks
3. "Did the final change improve outcomes after launch?"
   - best fit: experiment or product-analytics comparison
   - reason: the team needs a measured effect on behavior

Now suppose the team runs 6 interviews and hears the same booking confusion theme in 5 of them, then runs a usability test on two prototypes:

- Prototype A: 4 of 6 users complete booking
- Prototype B: 6 of 6 users complete booking

The research interpretation is:

- interviews identify the failure mechanism: date selection language is unclear
- usability testing shows Prototype B better supports the task
- the next step is a live measurement plan after launch, not more ideation

Verification: the chosen methods align with the decision type for all three questions: explanation, workflow comparison, and live-outcome measurement.

## 5. Designing a useful study

A research plan should specify:

- the decision the study will inform
- participant criteria
- method and protocol
- how notes or measurements will be captured
- how findings will be translated into action

This matters because research artifacts often fail at the last step. Teams conduct sessions, fill a slide deck with observations, and still cannot explain what should change in the product.

## 6. Common Mistakes

1. **Method mismatch**: using a survey when the real need is explanatory depth produces shallow answers; select methods based on the decision type rather than convenience.
2. **Leading prompts**: asking users to confirm the team's belief biases the data; write neutral questions that invite concrete examples.
3. **Sampling shortcuts**: recruiting only coworkers or highly engaged users distorts the findings; screen for the actual target context and task frequency.
4. **Insight inflation**: treating a few vivid anecdotes as universal truth overstates certainty; report what the data supports and where uncertainty remains.
5. **Action gap**: presenting findings without a product implication wastes the study; tie each key finding to a design, prioritization, or measurement decision.

## 7. Practical Checklist

- [ ] Write the product decision the research is meant to inform before recruiting participants.
- [ ] Choose the method based on whether the goal is discovery, explanation, comparison, or measurement.
- [ ] Define participant criteria around role, context, and task relevance.
- [ ] Pilot the interview guide or study script before running the full study.
- [ ] Record how notes, tags, or metrics will be synthesized into findings.
- [ ] End the study with explicit design implications and open questions.

## References

1. Steve Portigal, *Interviewing Users*. [https://rosenfeldmedia.com/books/interviewing-users/](https://rosenfeldmedia.com/books/interviewing-users/)
2. Erika Hall, *Just Enough Research*. [https://abookapart.com/products/just-enough-research](https://abookapart.com/products/just-enough-research)
3. Indi Young, *Practical Empathy*. [https://rosenfeldmedia.com/books/practical-empathy/](https://rosenfeldmedia.com/books/practical-empathy/)
4. Nielsen Norman Group, *User Research Methods*. [https://www.nngroup.com/topic/user-research/](https://www.nngroup.com/topic/user-research/)
5. Karen Holtzblatt and Hugh Beyer, *Contextual Design*. [https://www.sciencedirect.com/book/9780123540515/contextual-design](https://www.sciencedirect.com/book/9780123540515/contextual-design)
6. GOV.UK Service Manual, *User Research*. [https://www.gov.uk/service-manual/user-research](https://www.gov.uk/service-manual/user-research)
7. IDEO, *The Field Guide to Human-Centered Design*. [https://www.designkit.org/resources/1](https://www.designkit.org/resources/1)
