---
summary: The docs layer is the lightweight archive hub that routes readers into modules, tracks, projects, and support references.
tags:
  - archive
  - navigation
  - docs-hub
status: stable
format: docs-hub
difficulty: foundational
---

# Docs

This directory is the lightweight documentation hub for the repository and the archive platform.

It does not act as a second full documentation system. Its job is to point contributors toward the primary runtime, data, release, and authoring references for the archive and the underlying repo.

## What This Section Is For

- orienting a new reader to the repository structure
- linking the curriculum layer to the project layer
- keeping repo-level navigation separate from module-level content

## Current Navigation Sources

- [Root README](../README.md): top-level repository positioning and current value
- [Archive Browse Surface](/browse): primary archive search and filtering entrypoint
- [Archive Tracks Hub](/tracks): goal-oriented archive entrypoints
- [Archive Architecture](archive-architecture.md): current-state system overview for the archive platform
- [Archive Frontend Architecture](archive-frontend-architecture.md): architecture overview of the Astro frontend
- [Archive Data Contract](archive-data-contract.md): generated artifacts, key fields, and source-of-truth boundaries
- [Archive Retrieval and Relations](archive-retrieval-and-relations.md): search behavior, relation derivation, and benchmark maintenance
- [Archive Contributor Workflow](archive-contributor-workflow.md): what to run and update when the archive changes
- [Supported Surfaces](supported-surfaces.md): Phase 1 support and deployability matrix
- [Archive Editorial Standards](archive-editorial-standards.md): archive metadata and linking rules
- [Archive QA Checklist](archive-qa-checklist.md): browser, responsive, and accessibility validation matrix
- [Archive Release Checklist](archive-release-checklist.md): release-readiness gates for the archive surface
- [Archive Deployment Contract](archive-deployment-contract.md): environment and build expectations for shipping the Astro app
- [Archive Tag Vocabulary](archive-tag-vocabulary.md): controlled metadata vocabulary for future archive enrichment
- [Repository Structure](../STRUCTURE.md): concise structure reference
- [Modules Index](../modules/README.md): curriculum overview across modules `00` through `17`
- [Projects Index](../projects/README.md): portfolio-oriented project overview

## Current State

The primary archive navigation surface is now the Astro app under [`apps/archive`](../apps/archive/). The `docs/` layer should stay factual about how that archive works, how it is validated, and how contributors keep it healthy.

## Recommended Reading Flow

1. Start with the [Root README](../README.md).
2. Read the [Archive Architecture](archive-architecture.md) if you are changing archive behavior or workflows.
3. Open the archive app in [`apps/archive`](../apps/archive/).
4. Use the [Modules Index](../modules/README.md) and [Projects Index](../projects/README.md) when you need repo-native navigation.
