---
summary: Reference for how search ranking, filters, benchmark fixtures, and relation derivation currently work in the archive platform.
tags:
  - archive
  - retrieval
  - search
status: stable
format: reference
difficulty: advanced
---

# Archive Retrieval And Relations

## Search Model

The archive uses precomputed search documents from `docs/archive/search-index.json` and client-side ranking in `apps/archive/src/lib/search.js`.

Current ranked fields:

- exact title match
- title substring match
- summary match
- keyword match
- module title match
- track match
- body match

Current browse filters:

- collection
- content type
- module
- track

## Search Benchmarks

Benchmark fixtures live in:

- `apps/archive/tests/search-benchmarks.json`
- `apps/archive/tests/search-ranking.test.mjs`

Current benchmark scope is representative but still intentionally lightweight. When changing ranking behavior:

1. update or extend benchmark fixtures
2. verify top-ranked expectations still reflect user-intent queries
3. add benchmark cases for any new filter behavior or ranking dimension

## Relation Derivation

The relations bundle currently combines:

- authored outgoing links
- backlinks
- same-module adjacency
- same-track adjacency
- module-to-project edges
- project-to-module edges
- sequence neighbors for ordered concept pages

Related-content cards are a derived convenience layer, not editorial truth. If related panels become noisy, prefer tightening derivation rules before adding more relation types.

## Current Quality Caveats

- search relevance evidence is stronger than before but still narrower than a production search program
- relation cards can saturate on structurally similar pages
- leaf metadata depth still constrains richer ranking and faceting
