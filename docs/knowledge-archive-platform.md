---
summary: Blueprint for turning the indexed Markdown corpus into a real archive surface with search, relations, and governance.
tags:
  - archive
  - blueprint
  - strategy
status: stable
format: blueprint
difficulty: advanced
---

# Knowledge Archive Platform

## Current State

The repository is already a valid archive corpus:

- content is Markdown-first and versioned in Git
- the top-level collections in `docs/`, `modules/`, and `projects/` are stable
- module internals follow repeatable section buckets
- the corpus is large enough to justify dedicated retrieval and browsing surfaces

The archive is no longer theoretical. The repo now ships a working generator at [`scripts/build_knowledge_archive.py`](../scripts/build_knowledge_archive.py) and generated artifacts under [`docs/archive/`](archive/).

## What Exists Today

The current archive contract now includes:

- a versioned content index in [`docs/archive/content-index.json`](archive/content-index.json)
- a full-text search payload in [`docs/archive/search-index.json`](archive/search-index.json)
- a relations bundle in [`docs/archive/relations.json`](archive/relations.json)
- schema documents under [`docs/archive/schema/`](archive/schema/)

Those artifacts are derived from the Markdown corpus and keep Markdown as the source of truth.

## What The Platform Still Needs

The next step is not more corpus writing. The next step is making the indexed corpus usable as a platform.

### Archive Contract

The archive contract should stay stable enough that the frontend and CI can depend on it:

- canonical archive URLs
- schema-versioned JSON artifacts
- hub metadata on docs, tracks, modules, and projects
- explicit relation edges where prose currently implies them

### Retrieval

The retrieval layer needs to expose:

- full-text search across the full corpus
- faceted filtering by collection, content type, module, and track
- backlinks and authored-link discovery
- module and project adjacency driven by relation data

### Presentation

The archive frontend should provide:

- a home surface that feels like an archive, not a file tree
- browse and search pages
- rendered document pages with source links, breadcrumbs, and sequence navigation
- track, module, and project hubs that connect the curriculum and proof-of-work layers

### Editorial Governance

The archive must also stay healthy as the corpus grows:

- optional front matter for explicit archive metadata
- CI validation for stale artifacts, duplicate URLs, and broken local links
- authoring standards for new hub pages and templates

## Delivery Shape

The preferred technical shape remains incremental:

1. keep Markdown as the source of truth
2. generate structured JSON from the repo
3. feed that JSON into a static-first archive frontend
4. deepen metadata and related-content logic without introducing a database

## Immediate Build Priorities

The immediate build sequence is:

1. harden the archive contract and validation
2. normalize hub metadata and cross-links
3. ship the archive UI on top of the generated artifacts
4. improve related-content intelligence after the MVP is live

That sequencing keeps the project incremental and avoids building a UI whose taxonomy is still too weak to trust.
