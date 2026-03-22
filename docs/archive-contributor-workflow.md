---
summary: Contributor workflow for making archive-related changes safely across content, generator logic, frontend behavior, tests, and docs.
tags:
  - archive
  - workflow
  - contributor
status: stable
format: guide
difficulty: intermediate
---

# Archive Contributor Workflow

## When You Need This Workflow

Use this workflow when you change any of:

- archive generator or validator scripts
- archive artifacts or schemas
- search logic or benchmark fixtures
- relation derivation behavior
- archive UI or rendering logic
- archive templates, editorial rules, or deployment workflows

## Standard Validation Sequence

```bash
python3 scripts/build_knowledge_archive.py
python3 scripts/validate_knowledge_archive.py
python3 scripts/archive_quality_report.py --output docs/archive/quality-report.json
cd apps/archive
npm ci
npm run test:search
npm run test:smoke
npm run build
```

## Required Documentation Touchpoints

Update at least one adjacent reference doc when changing:

- generator or artifact behavior
  - update `archive-data-contract.md`
- search or relation logic
  - update `archive-retrieval-and-relations.md`
- deploy or release workflows
  - update `archive-deployment-contract.md` and `archive-release-checklist.md`
- editorial rules or templates
  - update `archive-editorial-standards.md`

## Manual QA Expectations

When archive UI behavior, rendering, or layout changes:

1. complete the archive QA checklist on a current build or preview
2. note critical defects before claiming release readiness
3. confirm the release checklist still matches the current workflow

## Template And Metadata Discipline

- keep Markdown as the source of truth
- prefer explicit Markdown links over prose references
- do not add leaf metadata everywhere by default; add it where it improves discovery or curation
- keep tags aligned with the current vocabulary
