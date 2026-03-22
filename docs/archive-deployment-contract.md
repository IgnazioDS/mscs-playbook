---
summary: Deployment and runtime contract for building and publishing the static archive app outside the local workspace.
tags:
  - archive
  - deployment
  - operations
status: stable
format: guide
difficulty: advanced
---

# Archive Deployment Contract

## Build Inputs

The archive app depends on:

- the Markdown corpus in `docs/`, `modules/`, and `projects/`
- generated archive artifacts in `docs/archive/`
- the Astro app in `apps/archive/`

The app reads the archive artifacts and source Markdown files at build time.

## Environment Variables

These variables parameterize source and filesystem assumptions:

- `ARCHIVE_REPO_ROOT`: absolute path to the repository root when the app build does not run from `apps/archive`
- `PUBLIC_ARCHIVE_SOURCE_REPO` or `ARCHIVE_SOURCE_REPO`: source repository URL, for example `https://github.com/IgnazioDS/mscs-playbook`
- `PUBLIC_ARCHIVE_SOURCE_BRANCH` or `ARCHIVE_SOURCE_BRANCH`: source branch name, defaults to `main`
- `PUBLIC_ARCHIVE_SOURCE_RAW_BASE`: optional override for raw-file delivery if GitHub raw URLs are not appropriate

## Standard Build Sequence

```bash
python3 scripts/build_knowledge_archive.py
python3 scripts/validate_knowledge_archive.py
python3 scripts/archive_quality_report.py --output docs/archive/quality-report.json
cd apps/archive
npm ci
npm run test:search
npx playwright install --with-deps chromium
npm run test:smoke
npm run build
```

## Preview Paths

- PR validation: archive CI uploads a preview artifact for inspection.
- Mainline deployment: the dedicated preview/deploy workflow runs the same archive validation and browser checks before publishing the built static site to GitHub Pages.

## Non-Goals

- No database is required.
- No server-side search service is required.
- The deployed archive should remain a static site derived from Markdown and generated JSON artifacts.
