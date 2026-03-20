#!/usr/bin/env python3
"""Validate generated archive artifacts and archive authoring rules."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from build_knowledge_archive import (
    ARCHIVE_SCHEMA_VERSION,
    DEFAULT_OUTPUT,
    DEFAULT_RELATIONS_OUTPUT,
    DEFAULT_SEARCH_OUTPUT,
    build_archive_bundle,
)


REPO_ROOT = Path(__file__).resolve().parent.parent
HUB_TYPES = {"doc", "module-overview", "project", "track"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def strip_generated_at(bundle: dict[str, Any]) -> dict[str, Any]:
    normalized = json.loads(json.dumps(bundle))
    for artifact in normalized.values():
        if isinstance(artifact, dict):
            artifact.pop("generated_at", None)
    return normalized


def validate_bundle(bundle: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    content_index = bundle["content_index"]
    search_index = bundle["search_index"]
    relations = bundle["relations"]

    if content_index.get("schema_version") != ARCHIVE_SCHEMA_VERSION:
        errors.append("content-index schema_version is incorrect")
    if search_index.get("schema_version") != ARCHIVE_SCHEMA_VERSION:
        errors.append("search-index schema_version is incorrect")
    if relations.get("schema_version") != ARCHIVE_SCHEMA_VERSION:
        errors.append("relations schema_version is incorrect")

    items = content_index.get("items", [])
    search_documents = search_index.get("documents", [])
    relation_docs = relations.get("documents", {})

    item_ids = [item["id"] for item in items]
    if len(item_ids) != len(set(item_ids)):
        errors.append("archive item ids are not unique")

    for field in ("path", "url", "slug"):
        values = [item[field] for item in items]
        if len(values) != len(set(values)):
            errors.append(f"archive item {field}s are not unique")

    if len(items) != len(search_documents):
        errors.append("search-index document count does not match content-index")
    if set(item_ids) != set(relation_docs.keys()):
        errors.append("relations documents do not match content-index ids")

    items_by_id = {item["id"]: item for item in items}

    for item in items:
        required = ("id", "title", "path", "url", "slug", "collection", "content_type", "format", "status")
        for field in required:
            value = item.get(field)
            if value is None or value == "":
                errors.append(f"{item['id']} is missing required field {field}")

        if item["content_type"] in HUB_TYPES:
            if not item.get("summary"):
                errors.append(f"{item['path']} must declare a summary")
            if not item.get("has_front_matter"):
                errors.append(f"{item['path']} is missing required front matter")
            if not item.get("tags"):
                errors.append(f"{item['path']} must declare at least one tag")

    filesystem_link_errors = relations.get("filesystem_link_errors", {})
    for item_id, missing in filesystem_link_errors.items():
        for target in missing:
            errors.append(f"{items_by_id[item_id]['path']} contains a broken local link to {target}")

    for item_id, relation_data in relation_docs.items():
        for key in ("outgoing_links", "backlinks", "track_memberships", "project_modules", "module_projects", "related"):
            if key not in relation_data:
                errors.append(f"{item_id} relations entry is missing {key}")

        sequence = relation_data.get("sequence", {})
        for seq_key in ("prev", "next"):
            seq_value = sequence.get(seq_key)
            if seq_value and seq_value not in items_by_id:
                errors.append(f"{item_id} sequence {seq_key} points to unknown id {seq_value}")

        for related in relation_data.get("related", []):
            if related["id"] not in items_by_id:
                errors.append(f"{item_id} related entry points to unknown id {related['id']}")

    for track in content_index.get("catalog", {}).get("tracks", []):
        if not track.get("module_ids"):
            errors.append(f"track {track['key']} must link at least one module")
        if not track.get("project_ids"):
            errors.append(f"track {track['key']} must link at least one project")

    return errors


def compare_to_disk(expected: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    disk_bundle = {
        "content_index": load_json(DEFAULT_OUTPUT),
        "search_index": load_json(DEFAULT_SEARCH_OUTPUT),
        "relations": load_json(DEFAULT_RELATIONS_OUTPUT),
    }
    if strip_generated_at(disk_bundle) != strip_generated_at(expected):
        errors.append("generated archive artifacts are stale; rerun scripts/build_knowledge_archive.py")
    return errors


def main() -> int:
    bundle = build_archive_bundle()
    errors = validate_bundle(bundle)
    for path in (DEFAULT_OUTPUT, DEFAULT_SEARCH_OUTPUT, DEFAULT_RELATIONS_OUTPUT):
        if not path.exists():
            errors.append(f"missing archive artifact: {path.relative_to(REPO_ROOT)}")
    if not errors:
        errors.extend(compare_to_disk(bundle))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Archive bundle is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
