# Ideation and Prototyping

## Key Ideas
- Ideation expands the solution space so teams do not commit too early to the first plausible interface idea.
- Prototypes make assumptions testable by turning abstract concepts into concrete artifacts that users and stakeholders can react to.
- Fidelity should match the decision being made: low fidelity is best for structure and concept testing, while higher fidelity is useful for interaction detail.
- Good prototypes isolate the riskiest assumptions rather than trying to simulate an entire finished product.
- The value of prototyping lies in learning speed, not in visual polish.

## 1. Why ideation should stay broad at first

After user research identifies a meaningful problem, teams are tempted to converge immediately on one solution. That is usually a mistake. Early commitment narrows thinking before the tradeoffs are visible. Ideation creates deliberate variation so the team can compare different approaches to the same task.

Useful ideation techniques include:

- sketching multiple concepts
- storyboarding user journeys
- mapping assumptions and risks
- generating alternative task flows

The point is not novelty for its own sake. It is to avoid treating one initial concept as inevitable.

## 2. What prototypes are for

A **prototype** is a deliberately incomplete representation of a design idea. It exists to answer a question. Examples:

- paper sketches can test layout and task order
- clickable wireframes can test navigation and screen transitions
- high-fidelity mocks can test visual clarity and stakeholder alignment

Prototype fidelity should be chosen by the type of uncertainty:

- if the uncertainty is about core flow, low fidelity is enough
- if the uncertainty is about timing, motion, or microcopy, higher fidelity may be necessary

## 3. Assumptions, risk, and iteration

Strong prototyping starts by naming the assumptions being tested. For example:

- users will notice the reschedule option
- users will trust the AI-generated summary enough to edit it rather than rewrite it
- users can complete the task without training

Each prototype iteration should update at least one assumption. Otherwise the team may be polishing an artifact without learning anything meaningful.

## 4. Worked example: fidelity choice for a dashboard redesign

A team wants to redesign an operations dashboard. They have three open questions:

1. Should alerts be grouped by severity or by system?
2. Will users notice the new "Investigate" action?
3. Is the visual styling readable in low-light control-room conditions?

Choose prototype types:

1. Grouping by severity vs system
   - low-fidelity wireframe is enough because the issue is information structure
2. Visibility of "Investigate" action
   - clickable prototype is appropriate because the issue is task flow and interaction
3. Readability in low light
   - high-fidelity mock is needed because color, contrast, and typography matter

Now suppose the team uses:

- 2 low-fidelity layout variants for grouping
- 1 clickable flow prototype for navigation
- 1 high-fidelity visual sample for readability

This is better than building one polished prototype for everything because each artifact is matched to the question it must answer.

Verification: each prototype format corresponds to the uncertainty being tested: structure, interaction, or visual readability.

## 5. When prototypes fail

Prototypes fail when teams forget that they are learning instruments. A polished artifact can create false confidence, especially if stakeholders mistake it for an implementation commitment. The opposite also happens: a crude prototype may trigger feedback about aesthetics when the real question is task logic.

A prototype should therefore be framed clearly:

- what question it is testing
- what parts are intentionally incomplete
- what decision will follow from the results

## 6. Common Mistakes

1. **Premature fidelity**: jumping to polished mocks too early burns time and hides structural issues; use the lowest fidelity that can answer the question.
2. **Single-concept bias**: prototyping only one idea prevents meaningful comparison; generate several alternatives before narrowing.
3. **Undefined assumptions**: building artifacts without naming the hypothesis makes feedback noisy and hard to interpret; write down what must be learned from the prototype.
4. **Stakeholder confusion**: presenting a prototype as if it were a final commitment distorts review behavior; explain what is provisional and what is under test.
5. **Feedback overload**: asking for reactions to every aspect of a prototype at once produces scattered input; focus the review on the targeted risk.

## 7. Practical Checklist

- [ ] List the core assumptions behind the design concept before sketching solutions.
- [ ] Generate multiple concept directions before choosing one to prototype.
- [ ] Match prototype fidelity to the specific design question.
- [ ] Tell reviewers what the prototype is intended to test and what is intentionally incomplete.
- [ ] Capture findings in terms of decisions, not only comments.
- [ ] Revise the prototype or concept based on the highest-risk unresolved assumption.

## References

1. Bill Buxton, *Sketching User Experiences*. [https://www.sciencedirect.com/book/9780123740373/sketching-user-experiences](https://www.sciencedirect.com/book/9780123740373/sketching-user-experiences)
2. Jake Knapp, John Zeratsky, and Braden Kowitz, *Sprint*. [https://www.thesprintbook.com/](https://www.thesprintbook.com/)
3. Jeff Gothelf and Josh Seiden, *Lean UX*. [https://www.oreilly.com/library/view/lean-ux/9781098116293/](https://www.oreilly.com/library/view/lean-ux/9781098116293/)
4. IDEO, *Design Kit Methods*. [https://www.designkit.org/methods](https://www.designkit.org/methods)
5. Nielsen Norman Group, *Prototyping*. [https://www.nngroup.com/topic/prototyping/](https://www.nngroup.com/topic/prototyping/)
6. Stanford d.school, *Bootcamp Bootleg*. [https://dschool.stanford.edu/resources/the-bootcamp-bootleg](https://dschool.stanford.edu/resources/the-bootcamp-bootleg)
7. Martin Tomitsch et al., *Design. Think. Make. Break. Repeat.* [https://www.bloomsbury.com/us/design-think-make-break-repeat-9781474279598/](https://www.bloomsbury.com/us/design-think-make-break-repeat-9781474279598/)
