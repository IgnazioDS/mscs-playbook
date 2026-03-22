---
summary: Current-state architecture for the static archive platform, including build flow, generated artifacts, and runtime boundaries.
tags:
  - archive
  - architecture
  - platform
status: stable
format: architecture
difficulty: advanced
---

# Archive Architecture

## System Shape

The archive is a derived static platform built from the Markdown corpus.

Source of truth:

- `docs/`
- `modules/`
- `projects/`

Generated layer:

- `docs/archive/content-index.json`
- `docs/archive/search-index.json`
- `docs/archive/relations.json`
- `docs/archive/quality-report.json`

Presentation layer:

- `apps/archive`

## Build Flow

1. `scripts/build_knowledge_archive.py` scans Markdown roots, parses optional front matter, infers archive metadata, and emits the three archive artifacts.
2. `scripts/validate_knowledge_archive.py` verifies uniqueness, hub metadata requirements, relation integrity, track linkage, and artifact freshness.
3. `scripts/archive_quality_report.py` computes quality and budget metrics and writes `docs/archive/quality-report.json`.
4. The Astro app in `apps/archive` reads the generated artifacts and source Markdown files at build time to render static routes.

## Runtime Boundaries

- Markdown remains the only content source of truth.
- The archive app is static and build-time rendered.
- No database or server-side search service is required.
- Search and relation behavior are driven by generated JSON plus client-side filtering/ranking logic.

## Current Validation Surface

- archive artifact build and validation
- archive quality report generation
- search benchmark suite
- Playwright smoke suite
- Pages deployment workflow

## Current Known Limits

- manual visual QA is still a release gate, not an automated guarantee
- client-side search still loads the full search record set into the browse surface
- relation cards are heuristic-derived and should be calibrated as the corpus grows
