---
summary: Architecture overview of the Astro frontend for the archive.
tags:
  - archive
  - architecture
  - frontend
status: stable
---

# Archive Frontend Architecture

## Component Map

- `BaseLayout.astro`: Provides the global shell, accessibility wrappers (skip link, main landmark).
- Routing pages (`pages/`):
  - `index.astro`: Entry point.
  - `browse.astro`: Renders search results and filter logic.
  - `docs/`, `tracks/`, `modules/`, `projects/`: Map physical folders to URL routes dynamically using generated JSON artifacts.
- Search logic (`src/lib/search.js`):
  - In-browser client-side fuzzy and exact field matches.

## State Management
- Currently stateless outside `localStorage` usage if any. 
- Filters are passed via URL query parameters (`?q=...&module=...`).
