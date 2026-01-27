# Biased Hiring Model

## 1. Context
A company deploys a model to rank candidates for recruiter review. The system is used for high-volume roles and influences interview invitations.

## 2. Stakeholders
- Applicants
- Recruiters and hiring managers
- Legal and compliance teams
- The company’s customers and workforce

## 3. System description (what it does, data, model/logic, deployment)
- **Function**: Score candidates based on resume features and prior hiring outcomes.
- **Data**: Historical hiring decisions, resume text embeddings, education and experience fields.
- **Model**: Gradient-boosted classifier; threshold used to decide auto-advance vs manual review.
- **Deployment**: Weekly batch scoring feeding ATS; recruiters see ranked list.

## 4. What went wrong (or could go wrong)
- The model under-ranks candidates from underrepresented groups.
- A fairness audit shows a large false negative rate (FNR) gap across gender groups.

## 5. Root causes
### Technical
- Feature leakage from past hiring outcomes (target proxy) amplifies historical bias.
- Threshold chosen to optimize overall accuracy without fairness constraints.

### Data
- Historical labels reflect biased hiring practices.
- Imbalanced representation in training data.

### Product/UX
- Recruiter UI does not show model confidence or uncertainty.
- No override workflow or justification capture.

### Org/process
- No fairness gate in model review.
- Lack of cross-functional sign-off before deployment.

## 6. Harms and severity
### Who is harmed
Applicants from underrepresented groups and the company’s workforce diversity.

### Severity rating
High — hiring decisions materially affect livelihoods and long-term opportunity.

### Likelihood rating
Medium — bias is evident in historical data and likely to persist without intervention.

## 7. Detection and evidence
- **Signals**: FNR parity gap, selection rate by group, disparate impact ratio.
- **Example metric**: FNR gap of 18 percentage points between groups.
- **Monitoring**: Weekly fairness dashboard; audit sampling of rejected candidates.

## 8. What should have been done (prevent/mitigate)
### Before launch
- Remove or de-emphasize target proxies; re-label outcomes with bias review.
- Evaluate fairness metrics by group; set thresholds with constraints.

### During launch
- Shadow mode with human review; log overrides and outcomes.
- Add UI disclosure and uncertainty indicators.

### After launch
- Continuous fairness monitoring; periodic bias audits.
- Create appeal and review process for applicants.

## 9. What to do now (incident response)
### Immediate containment
- Pause automated ranking for affected roles.
- Require human review for all candidates.

### User comms/disclosure
- Notify recruiting leadership and compliance.
- Prepare applicant-facing disclosure if required by policy.

### Short-term fixes (days)
- Remove high-risk features; re-train with balanced sampling.
- Adjust thresholds to reduce FNR disparity.

### Medium-term (weeks)
- Implement bias-aware evaluation in CI.
- Establish governance review and periodic audits.

## 10. Verification steps
- Re-run fairness metrics on holdout and recent data.
- Confirm FNR gap < 5 percentage points.
- Track selection rate parity and recruiter override rates.

## 11. If I were the tech lead: next 30 days plan
- Freeze automated ranking for high-risk roles until fairness goals met.
- Deploy shadow evaluation with strict fairness gates.
- Build model cards with group metrics and thresholds rationale.
- Run a data audit and remove proxy features.
- Add opt-in applicant disclosure in ATS.
- Create retraining schedule with bias checks.
- Add human-in-the-loop review for borderline scores.
- Measure recruiter override outcomes and adjust UI.
- Set quarterly fairness audits with compliance.
