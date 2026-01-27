# Health App Data Misuse

## 1. Context
A health tracking app shares analytics data with third-party partners for marketing insights.

## 2. Stakeholders
- Users and patients
- Data partners
- Product and marketing teams
- Regulators and compliance

## 3. System description (what it does, data, model/logic, deployment)
- **Function**: Aggregate health activity and symptom logs for insights.
- **Data**: Self-reported symptoms, geolocation, device IDs.
- **Model**: Analytics segmentation; no direct ML model used.
- **Deployment**: Daily exports to partners via data pipeline.

## 4. What went wrong (or could go wrong)
- Shared data enables re-identification of users.
- Users were not fully informed about data sharing scope.

## 5. Root causes
### Technical
- Weak anonymization; device IDs persist across exports.
- Lack of access controls on data extracts.

### Data
- Sensitive health data combined with location and timestamps.
- No minimization of fields before export.

### Product/UX
- Consent wording unclear; opt-out buried in settings.
- No user-facing data access log.

### Org/process
- Data sharing approved without privacy review.
- No data retention and deletion policy enforcement.

## 6. Harms and severity
### Who is harmed
Users whose health data is exposed; trust in health services.

### Severity rating
High — health data exposure can lead to discrimination and personal harm.

### Likelihood rating
Medium — re-identification risk increases with cross-joins.

## 7. Detection and evidence
- **Signals**: unusual partner queries; complaints about targeted ads.
- **Example metric**: 12% of records contain direct identifiers after export.
- **Monitoring**: access logs, export field audit, partner usage reviews.

## 8. What should have been done (prevent/mitigate)
### Before launch
- Privacy impact assessment and data minimization.
- Remove or hash identifiers; coarse-grain location.

### During launch
- Transparent consent flow with opt-in for sharing.
- Data access monitoring and partner contracts.

### After launch
- Periodic privacy audits; retention enforcement.
- Data sharing inventory and disclosure updates.

## 9. What to do now (incident response)
### Immediate containment
- Pause data exports.
- Revoke partner access tokens.

### User comms/disclosure
- Notify users of the scope and remedial actions.
- Provide opt-out and deletion pathways.

### Short-term fixes (days)
- Strip identifiers; reduce fields to minimal set.
- Update consent screens and privacy policy summaries.

### Medium-term (weeks)
- Implement data access reviews and periodic audits.
- Establish a privacy review gate for new data uses.

## 10. Verification steps
- Confirm 0 direct identifiers in exports.
- Run re-identification risk assessment.
- Track opt-out rates and user complaints.

## 11. If I were the tech lead: next 30 days plan
- Freeze data sharing until privacy audit passes.
- Build a data minimization checklist into pipelines.
- Add automated field validation on exports.
- Require opt-in for sensitive sharing.
- Create a user data access report.
- Implement partner monitoring and renewal reviews.
- Document retention schedules and deletion SLAs.
- Establish a privacy review board.
