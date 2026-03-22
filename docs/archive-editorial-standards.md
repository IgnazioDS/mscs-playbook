---
summary: Minimal authoring and metadata rules for keeping the archive browseable, searchable, and internally consistent.
tags:
  - archive
  - editorial
  - governance
status: stable
format: guide
difficulty: foundational
---

# Archive Editorial Standards

## Purpose

The archive is a derived platform built from Markdown. New content should remain easy to write while still producing reliable search, navigation, and related-content signals.

## Required Metadata For Hub Pages

Add front matter to:

- `docs/*.md`
- `docs/tracks/*.md`
- `modules/*/README.md`
- `projects/*/README.md`

Use this minimum shape:

```yaml
---
summary: One sentence that explains why this page exists in the archive.
tags:
  - archive
status: stable
format: module-hub
difficulty: intermediate
---
```

## Linking Rules

- Prefer explicit Markdown links to modules, projects, and documents instead of plain-text ids.
- Link to the archive-relevant document when a relationship matters for discovery.
- Keep local links relative so the generator can resolve them into archive relations.

## Summary Rules

- Put the most archive-useful one-sentence summary in front matter on hub pages.
- Keep opening paragraphs factual; they are used as fallback summaries when front matter is absent.

## Tagging Rules

- Use a small number of stable tags.
- Prefer curriculum domain tags, artifact tags, and audience/use-case tags over ad hoc keywords.
- Avoid duplicating the full title as a tag.
- Reuse the controlled vocabulary in [Archive Tag Vocabulary](archive-tag-vocabulary.md) before introducing new tags.

## When To Add Explicit Metadata

Add optional `prerequisites` or `related` metadata when path structure and normal links are not enough to represent the relationship cleanly.

## Leaf Content Expectations

Start adding explicit metadata on leaf pages when one of these is true:

- the page is a likely search landing page
- the page is repeatedly surfaced in related-content panels
- the page is a case study or implementation README that should connect to broader archive flows
- the page is otherwise hard to discover through path structure alone

## CI Expectations

Archive validation will fail when:

- generated archive artifacts are stale
- hub pages are missing front matter
- hub pages do not declare tags
- local Markdown links point to missing targets
- archive ids, URLs, or slugs collide
