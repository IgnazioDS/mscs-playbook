---
summary: Reference for the generated archive artifacts, key metadata fields, and which parts of the system are authored versus derived.
tags:
  - archive
  - contract
  - metadata
status: stable
format: reference
difficulty: advanced
---

# Archive Data Contract

## Artifact Inventory

- `docs/archive/content-index.json`
  - full archive item inventory
  - catalog data for modules, projects, tracks, collections, and content types
- `docs/archive/search-index.json`
  - search documents and filter option payloads
- `docs/archive/relations.json`
  - outgoing links, backlinks, track memberships, project/module adjacency, sequence edges, and related candidates
- `docs/archive/quality-report.json`
  - generated quality and budget metrics

## Key Item Fields

Core identity:

- `id`
- `path`
- `url`
- `slug`
- `canonical_url`

Classification:

- `collection`
- `content_type`
- `section`
- `format`
- `status`
- `difficulty`

Discovery metadata:

- `summary`
- `tags`
- `prerequisites`
- `related`
- `headings`
- `links`
- `tracks`

Context:

- `module`
- `project`
- `track`
- `source_url`

## Authored Versus Derived

Authored in Markdown front matter when present:

- `summary`
- `tags`
- `status`
- `format`
- `difficulty`
- `prerequisites`
- `related`
- `canonical_url`

Derived by the generator:

- `id`
- `path`
- `url`
- `slug`
- `collection`
- `content_type`
- `section`
- `word_count`
- `headings`
- `links`
- `module` / `project` / `track` references
- `tracks`
- `source_url`

## Source URL Configuration

The generator respects these environment variables at build time:

- `PUBLIC_ARCHIVE_SOURCE_REPO` or `ARCHIVE_SOURCE_REPO`
- `PUBLIC_ARCHIVE_SOURCE_BRANCH` or `ARCHIVE_SOURCE_BRANCH`

The archive app also uses the public variants for runtime/build-time source-link rendering.

## Schema And Enforcement

- JSON schemas under `docs/archive/schema/` are reference documents.
- The validator script is currently the primary enforcement layer for archive correctness.
