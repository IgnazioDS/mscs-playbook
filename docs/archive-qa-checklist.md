---
summary: Manual and automated QA matrix for validating the archive UI across browsers, devices, and critical user flows.
tags:
  - archive
  - qa
  - checklist
status: stable
format: checklist
difficulty: intermediate
---

# Archive QA Checklist

## Run Metadata

- Release candidate:
- Date:
- Reviewer:
- Preview artifact or URL:
- Notes / defect log:

## Core Journeys

- [ ] Home page loads and primary navigation is visible.
- [ ] Browse page returns results for known-good queries.
- [ ] Module hubs load and expose linked content counts.
- [ ] Project hubs load and expose linked modules.
- [ ] Track hubs load and expose linked modules and projects.
- [ ] Representative document pages render headings, TOC, breadcrumbs, source links, backlinks, and sequence navigation.

## Responsive Checks

- [ ] Desktop layout is readable on home, browse, hub, and document pages.
- [ ] Mobile layout remains usable on browse and long document pages.
- [ ] Sticky TOC does not overlap or hide content on smaller screens.
- [ ] Long code blocks and tables remain horizontally scrollable rather than breaking layout.

## Rendering Edge Cases

- [ ] Internal Markdown links resolve to archive routes where possible.
- [ ] External links open correctly and remain visibly distinguishable.
- [ ] Heading anchors navigate to the correct section.
- [ ] Images, tables, and blockquotes render cleanly.
- [ ] Placeholder or sparse README pages do not create broken UI states.

## Accessibility Baseline

- [ ] Page titles reflect the active route.
- [ ] Landmark structure is present (`header`, `nav`, `main`).
- [ ] Keyboard users can reach primary navigation, search controls, and source links.
- [ ] Focus indicators are visible on interactive controls.
- [ ] Heading order stays logical on representative pages.
- [ ] Search result count updates are announced.

## Current Automation Coverage

- Playwright smoke suite: `npm run test:smoke` in `apps/archive`
- Search benchmark suite: `npm run test:search` in `apps/archive`
- Archive build and data validation: `python3 scripts/build_knowledge_archive.py` and `python3 scripts/validate_knowledge_archive.py`
