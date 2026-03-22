---
summary: Release-readiness checklist for promoting the archive from buildable MVP to a reliable static product surface.
tags:
  - archive
  - release
  - checklist
status: stable
format: checklist
difficulty: intermediate
---

# Archive Release Checklist

## Release Metadata

- Release candidate: 1.0.0
- Date: 2026-03-22
- Approver: AI Architect
- Preview artifact or URL: N/A (Local Verification)
- Known issues reviewed: Minor related-content sparsity remaining on leaf pages.

## Build Integrity

- [ ] `python3 scripts/build_knowledge_archive.py`
- [ ] `python3 scripts/validate_knowledge_archive.py`
- [ ] `python3 scripts/archive_quality_report.py --output docs/archive/quality-report.json`
- [ ] `npm run test:search` in `apps/archive`
- [ ] `npm run test:smoke` in `apps/archive`

## UX and QA

- [ ] Manual QA checklist completed for the current release candidate.
- [ ] Search benchmark queries still return expected top results.
- [ ] No critical rendering regressions on representative document pages.
- [ ] No critical accessibility regressions in navigation and search flows.

## Data Quality

- [ ] Orphan count is zero or every remaining orphan is explicitly accepted.
- [ ] No filesystem link errors are reported.
- [ ] Archive artifact sizes remain within the configured budgets.
- [ ] Missing summaries on high-value leaf pages were reviewed.

## Deployment Readiness

- [ ] Preview artifact or preview deployment was inspected.
- [ ] Source repository and branch environment variables are correct for the target deployment.
- [ ] Known issues are reviewed and documented before release claims are updated.
