# HCI for AI: Explainability and Trust

## Key Ideas
- Human-AI interaction design is about helping people form accurate mental models of what the system can do, cannot do, and is currently doing.
- Trustworthy AI interfaces support appropriate trust calibration, which means neither blind acceptance nor blanket rejection.
- Explanations are useful only when they help users predict behavior, verify outputs, or decide when to intervene.
- Confidence and uncertainty cues must be designed carefully because users often mistake probability-like signals for correctness guarantees.
- Human override, verification, and feedback loops are core interaction features in AI systems, not optional extras.

## 1. Why AI changes the HCI problem

Traditional interfaces usually expose deterministic system behavior. AI systems often produce variable outputs, uncertain predictions, and errors that are difficult for users to anticipate. This shifts the design problem from simple command-and-response interaction to **mental model management**.

Users need to know:

- what the AI is trying to do
- how reliable it is in this context
- how to inspect or correct the result
- when to ignore it

Without that clarity, the interface can create overtrust or undertrust.

## 2. Explainability, transparency, and verification

An **explanation** is a representation that helps a user understand why the system produced an output. A useful explanation is matched to a user goal, such as:

- verifying a recommendation
- debugging an incorrect answer
- understanding which source influenced the result

A **transparency cue** may include provenance, confidence, cited evidence, or model limitations. These do not automatically increase trustworthiness. They increase trustworthiness only if they improve user judgment.

## 3. Trust calibration and uncertainty

**Trust calibration** means users rely on the system to the degree that its actual capability warrants. Poor calibration has two forms:

- **overtrust**: users accept wrong outputs too easily
- **undertrust**: users ignore useful outputs even when they are reliable

Uncertainty communication helps, but only if it is understandable. A system that labels an answer "92% confident" may still mislead users if they interpret that as a probability of truth rather than a model-internal score.

## 4. Worked example: redesigning an AI writing assistant

An AI writing assistant suggests edits to an email draft. The current interface shows:

- one-click "Apply Suggestion"
- no explanation of what changed
- no indication of source or confidence

Observed problem:

- users accept awkward rewrites because the UI implies the output is authoritative

Redesign elements:

1. show inline diff between original and suggested text
2. add short rationale such as "shortened for clarity"
3. allow accept, reject, or edit
4. show a warning for low-confidence or high-risk suggestions

Interpretation:

- the redesign improves verification
- the user stays in control of the final text
- trust becomes conditional on visible evidence rather than on interface authority

Verification: the redesigned interface adds comparison, rationale, and user override, which directly address the overtrust problem described in the original flow.

## 5. Human control and fallback design

AI features should be designed with:

- clear override paths
- graceful failure states
- visible limitations
- feedback channels for correction

This matters most in high-stakes settings such as healthcare, hiring, finance, and education. In those contexts, the interface must help people notice when the AI should not be the final decision-maker.

## 6. Common Mistakes

1. **Authority signaling**: presenting AI output with overly certain language or visual prominence encourages overtrust; communicate limits and make verification easy.
2. **Explanation theater**: showing generic explanations that do not help user judgment creates false transparency; tie explanations to concrete user decisions.
3. **Opaque confidence cues**: using scores or labels without interpretation support confuses users; explain what the signal means and what it does not mean.
4. **No correction path**: forcing users to accept or abandon AI output without editable control breaks collaboration; include reject, revise, and fallback actions.
5. **Trust-by-default assumptions**: assuming users will naturally calibrate trust correctly ignores observed misuse; test how users actually respond to AI cues in realistic tasks.

## 7. Practical Checklist

- [ ] Define what users need to understand, verify, or override in the AI-assisted workflow.
- [ ] Add explanations only when they improve prediction, verification, or correction.
- [ ] Make confidence or uncertainty cues interpretable, not merely visible.
- [ ] Provide clear paths to reject, edit, or escalate beyond the AI output.
- [ ] Test for both overtrust and undertrust during usability studies.
- [ ] Expose limitations and failure cases in the interface where they are relevant to action.

## References

1. Microsoft, *Guidelines for Human-AI Interaction*. [https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/](https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/)
2. Saleema Amershi et al., *Guidelines for Human-AI Interaction*. [https://dl.acm.org/doi/10.1145/3290605.3300233](https://dl.acm.org/doi/10.1145/3290605.3300233)
3. Jakob Nielsen and Maria Rosala, *AI User Experience*. [https://www.nngroup.com/topic/ai-ux/](https://www.nngroup.com/topic/ai-ux/)
4. Tim Miller, *Explanation in Artificial Intelligence: Insights from the Social Sciences*. [https://arxiv.org/abs/1706.07269](https://arxiv.org/abs/1706.07269)
5. Ben Shneiderman, *Human-Centered AI*. [https://global.oup.com/academic/product/human-centered-ai-9780192845290](https://global.oup.com/academic/product/human-centered-ai-9780192845290)
6. Google PAIR, *People + AI Guidebook*. [https://pair.withgoogle.com/guidebook/](https://pair.withgoogle.com/guidebook/)
7. ACM Digital Library, *Human-AI Interaction Research*. [https://dl.acm.org/topic/human-centered-computing/human-computer-interaction](https://dl.acm.org/topic/human-centered-computing/human-computer-interaction)
