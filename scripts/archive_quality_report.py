#!/usr/bin/env python3
"""Generate and optionally enforce archive quality and budget metrics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_DIR = REPO_ROOT / "docs" / "archive"
CONTENT_INDEX = ARCHIVE_DIR / "content-index.json"
SEARCH_INDEX = ARCHIVE_DIR / "search-index.json"
RELATIONS_INDEX = ARCHIVE_DIR / "relations.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_report() -> dict:
    content = load_json(CONTENT_INDEX)
    search = load_json(SEARCH_INDEX)
    relations = load_json(RELATIONS_INDEX)
    items = content["items"]
    relation_docs = relations["documents"]

    zero_outgoing = [item["id"] for item in items if not relation_docs[item["id"]]["outgoing_links"]]
    zero_backlinks = [item["id"] for item in items if not relation_docs[item["id"]]["backlinks"]]
    missing_summaries = [item["id"] for item in items if not item.get("summary")]
    untagged_leaf_items = [
        item["id"]
        for item in items
        if item["content_type"] not in {"doc", "module-overview", "project", "track"} and not item.get("tags")
    ]

    return {
        "schema_version": content["schema_version"],
        "generated_at": content["generated_at"],
        "counts": {
            "documents": content["counts"]["documents"],
            "hub_documents_with_front_matter": sum(
                1
                for item in items
                if item["content_type"] in {"doc", "module-overview", "project", "track"} and item.get("has_front_matter")
            ),
            "items_with_summary": sum(1 for item in items if item.get("summary")),
            "items_with_tags": sum(1 for item in items if item.get("tags")),
            "items_with_tracks": sum(1 for item in items if item.get("tracks")),
            "zero_outgoing_links": len(zero_outgoing),
            "zero_backlinks": len(zero_backlinks),
            "orphans": len(relations["orphan_document_ids"]),
        },
        "files": {
            "content_index_bytes": CONTENT_INDEX.stat().st_size,
            "search_index_bytes": SEARCH_INDEX.stat().st_size,
            "relations_index_bytes": RELATIONS_INDEX.stat().st_size,
            "search_documents": len(search["documents"]),
        },
        "issues": {
            "orphan_document_ids": relations["orphan_document_ids"],
            "filesystem_link_errors": relations.get("filesystem_link_errors", {}),
            "missing_summary_ids": missing_summaries[:50],
            "untagged_leaf_ids": untagged_leaf_items[:50],
            "zero_outgoing_link_ids_sample": zero_outgoing[:50],
            "zero_backlink_ids_sample": zero_backlinks[:50],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Optional JSON output path")
    parser.add_argument("--max-search-index-bytes", type=int, default=2_250_000)
    parser.add_argument("--max-content-index-bytes", type=int, default=1_900_000)
    parser.add_argument("--max-relations-index-bytes", type=int, default=1_200_000)
    parser.add_argument("--max-orphans", type=int, default=0)
    args = parser.parse_args()

    report = build_report()
    if args.output:
        output_path = args.output
        if not output_path.is_absolute():
            output_path = (REPO_ROOT / output_path).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(report, indent=2))

    failures: list[str] = []
    files = report["files"]
    if files["search_index_bytes"] > args.max_search_index_bytes:
        failures.append("search-index exceeds configured budget")
    if files["content_index_bytes"] > args.max_content_index_bytes:
        failures.append("content-index exceeds configured budget")
    if files["relations_index_bytes"] > args.max_relations_index_bytes:
        failures.append("relations-index exceeds configured budget")
    if report["counts"]["orphans"] > args.max_orphans:
        failures.append("orphan document count exceeds configured maximum")

    if failures:
        for failure in failures:
            print(f"ERROR: {failure}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
