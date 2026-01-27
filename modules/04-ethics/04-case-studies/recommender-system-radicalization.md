# Recommender System Radicalization

## 1. Context
A content platform deploys a recommender system to increase engagement through personalized feeds.

## 2. Stakeholders
- Users
- Content creators
- Trust and safety teams
- Advertisers

## 3. System description (what it does, data, model/logic, deployment)
- **Function**: Rank content per user based on predicted engagement.
- **Data**: Watch time, clicks, shares, user follow graph.
- **Model**: Two-stage retrieval + ranking; objective optimized for watch time.
- **Deployment**: Real-time ranking; A/B experiments daily.

## 4. What went wrong (or could go wrong)
- The system progressively surfaces more extreme content to maximize engagement.
- Users report exposure to polarizing content after repeated recommendations.

## 5. Root causes
### Technical
- Objective ignores safety signals; no penalty for harmful content.
- Feedback loops amplify engagement bias.

### Data
- Historical engagement data already skewed toward sensational content.
- Missing labels for harmful content categories.

### Product/UX
- Limited user controls to reset or tune recommendations.
- No visibility into why content is recommended.

### Org/process
- Growth goals dominate safety requirements.
- Safety metrics not in primary launch gates.

## 6. Harms and severity
### Who is harmed
Users exposed to harmful content; platform reputation; societal discourse.

### Severity rating
High — exposure can drive radicalization and real-world harm.

### Likelihood rating
Medium — depends on user cohort and content availability.

## 7. Detection and evidence
- **Signals**: growth in harmful content impressions; user complaints.
- **Example metric**: harmful content exposure rate increases from 0.7% to 2.1% of feed impressions.
- **Monitoring**: safety classifier scores, complaint rate per 1k sessions, cohort drift.

## 8. What should have been done (prevent/mitigate)
### Before launch
- Incorporate safety constraints or penalties into ranking objective.
- Audit recommendation paths for high-risk content clusters.

### During launch
- Run safety-aware A/B tests with explicit harm metrics.
- Provide user controls for topic filtering and reset.

### After launch
- Retrain with safety labels; add diversity constraints.
- Enforce thresholds for harmful content exposure.

## 9. What to do now (incident response)
### Immediate containment
- Downrank flagged categories and reduce amplification.
- Disable auto-play on sensitive topics.

### User comms/disclosure
- Publish transparency update on mitigation steps.
- Provide users with content control options.

### Short-term fixes (days)
- Add hard constraints on safety score in ranking.
- Increase moderation coverage in high-risk clusters.

### Medium-term (weeks)
- Build safety-aware objective; include long-term engagement.
- Launch periodic audits of recommendation paths.

## 10. Verification steps
- Measure reduction in harmful exposure rate to < 1%.
- Track user reports per 1k sessions; target 30% reduction.
- Validate that engagement drop is bounded (tradeoff tracking).

## 11. If I were the tech lead: next 30 days plan
- Add safety constraints to ranking objective.
- Launch a user control panel for feed tuning.
- Implement path-based audits for content clusters.
- Increase review of borderline content by moderators.
- Instrument exposure metrics by cohort.
- Document tradeoff: safety vs engagement with leadership sign-off.
- Set release gates using safety KPIs.
- Schedule quarterly external red-team reviews.
