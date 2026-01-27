# GenAI Customer Support Hallucinations

## 1. Context
A company deploys a generative AI assistant to answer customer support questions.

## 2. Stakeholders
- Customers
- Support agents
- Product and engineering teams
- Legal and compliance teams

## 3. System description (what it does, data, model/logic, deployment)
- **Function**: Answer FAQs and triage support requests.
- **Data**: Product docs, help articles, ticket history.
- **Model**: LLM with retrieval-augmented generation (RAG).
- **Deployment**: Chat widget with autonomous responses.

## 4. What went wrong (or could go wrong)
- The model hallucinates refund policies and provides incorrect instructions.
- Customers follow wrong advice, increasing churn and costs.

## 5. Root causes
### Technical
- Retrieval index out of date; missing latest policy changes.
- No calibrated confidence or refusal mechanism.

### Data
- Inconsistent documentation and multiple policy versions.
- No provenance metadata for retrieved passages.

### Product/UX
- UI presents answers as authoritative without citations.
- No escalation path to human agents for high-risk queries.

### Org/process
- Lack of eval suite for hallucination rate.
- No rollback plan for unsafe responses.

## 6. Harms and severity
### Who is harmed
Customers who receive incorrect guidance; support teams handling escalations.

### Severity rating
Medium — financial impact and trust loss, but not typically life-critical.

### Likelihood rating
High — hallucinations occur with ambiguous or novel queries.

## 7. Detection and evidence
- **Signals**: complaint rate, escalation rate, refund overrides.
- **Example metric**: hallucination rate 6% on policy queries; P95 response latency +120ms after safety filters.
- **Monitoring**: response audits, sampling, and citation coverage.

## 8. What should have been done (prevent/mitigate)
### Before launch
- Build eval set with policy questions; measure hallucination rate.
- Require citations and implement refusal threshold.

### During launch
- Roll out with human review for policy-sensitive intents.
- Add user feedback buttons and escalation paths.

### After launch
- Continuous retrieval refresh and doc governance.
- Track hallucination rate and enforce go/no-go thresholds.

## 9. What to do now (incident response)
### Immediate containment
- Disable autonomous responses for policy topics.
- Route high-risk intents to human agents.

### User comms/disclosure
- Notify customers of incorrect guidance and provide corrections.
- Publish a transparency note in the help center.

### Short-term fixes (days)
- Rebuild index and add policy versioning.
- Add refusal rules and fallback to articles.

### Medium-term (weeks)
- Build a policy QA benchmark and monitor weekly.
- Add response logging for safety review.

## 10. Verification steps
- Reduce hallucination rate below 1% for policy intents.
- Validate citation coverage > 95%.
- Measure customer complaint rate drop by 50%.

## 11. If I were the tech lead: next 30 days plan
- Define high-risk intents and block auto-responses.
- Deploy citation-required responses for policy queries.
- Implement weekly retrieval refresh and doc governance.
- Add automated evals to CI for hallucination rate.
- Instrument escalation rates and outcomes.
- Create a customer correction protocol.
- Document tradeoff: safety vs latency and UX.
- Prepare rollback playbook and on-call rotation.
