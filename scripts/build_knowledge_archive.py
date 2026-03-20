#!/usr/bin/env python3
"""Build versioned archive artifacts from the Markdown corpus."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ARCHIVE_SCHEMA_VERSION = "1.0.0"
REPO_ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_DIR = REPO_ROOT / "docs" / "archive"
DEFAULT_OUTPUT = ARCHIVE_DIR / "content-index.json"
DEFAULT_SEARCH_OUTPUT = ARCHIVE_DIR / "search-index.json"
DEFAULT_RELATIONS_OUTPUT = ARCHIVE_DIR / "relations.json"
MARKDOWN_ROOTS = ("docs", "modules", "projects")
WORD_RE = re.compile(r"\b[\w'-]+\b")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
FRONT_MATTER_KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")
PROJECT_SOURCE_BASE = "https://github.com/IgnazioDS/mscs-playbook/blob/main"
HUB_TYPES = {"doc", "module-overview", "project", "track"}
CONTENT_TYPE_FORMATS = {
    "case-study": "case-study",
    "cheatsheet": "reference",
    "concept": "reading",
    "doc": "reference",
    "exercise": "exercise",
    "implementation": "runnable",
    "module-document": "reference",
    "module-overview": "module-hub",
    "note": "note",
    "project": "project-brief",
    "project-index": "project-hub",
    "track": "learning-track",
}


def iter_markdown_files() -> list[Path]:
    files: list[Path] = []
    for root_name in MARKDOWN_ROOTS:
        root = REPO_ROOT / root_name
        if not root.exists():
            continue
        for path in root.rglob("*.md"):
            if path.is_file():
                files.append(path)
    return sorted(files)


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "untitled"


def clean_heading(text: str) -> str:
    return text.strip().strip("#").strip()


def parse_scalar(value: str) -> Any:
    normalized = value.strip()
    if not normalized:
        return ""
    if normalized[0] == normalized[-1] and normalized[0] in {'"', "'"}:
        normalized = normalized[1:-1]
    lowered = normalized.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    return normalized


def parse_front_matter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text

    lines = text.splitlines()
    end_index = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end_index = index
            break

    if end_index is None:
        return {}, text

    metadata: dict[str, Any] = {}
    current_list_key: str | None = None

    for raw_line in lines[1:end_index]:
        stripped = raw_line.strip()
        if not stripped:
            continue
        if stripped.startswith("- ") and current_list_key:
            metadata.setdefault(current_list_key, []).append(parse_scalar(stripped[2:]))
            continue

        match = FRONT_MATTER_KEY_RE.match(raw_line)
        if not match:
            current_list_key = None
            continue

        key, value = match.groups()
        key = key.replace("-", "_")
        value = value.strip()
        if not value:
            metadata[key] = []
            current_list_key = key
            continue

        current_list_key = None
        if value.startswith("[") and value.endswith("]"):
            items = [part.strip() for part in value[1:-1].split(",") if part.strip()]
            metadata[key] = [parse_scalar(item) for item in items]
            continue

        metadata[key] = parse_scalar(value)

    body = "\n".join(lines[end_index + 1 :])
    if text.endswith("\n"):
        body += "\n"
    return metadata, body


def listify(value: Any) -> list[str]:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [str(value).strip()]


def first_paragraph(lines: list[str]) -> str:
    buffer: list[str] = []
    in_code_block = False
    for raw_line in lines:
        line = raw_line.rstrip()
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            if buffer:
                break
            continue
        if in_code_block:
            continue
        if not stripped:
            if buffer:
                break
            continue
        if stripped.startswith("#"):
            continue
        if stripped.startswith("- ") or stripped.startswith("* ") or re.match(r"^\d+\.\s+", stripped):
            continue
        buffer.append(stripped)
    return " ".join(buffer)


def infer_content_type(relative_path: Path) -> str:
    parts = relative_path.parts
    if parts[0] == "docs":
        if len(parts) > 1 and parts[1] == "tracks":
            return "track"
        return "doc"

    if parts[0] == "projects":
        if relative_path.name == "README.md" and len(parts) == 2:
            return "project-index"
        return "project"

    if parts[0] != "modules":
        return "document"

    if relative_path.name == "README.md" and len(parts) == 3:
        return "module-overview"
    if len(parts) < 4:
        return "module-document"

    section = parts[2]
    mapping = {
        "01-concepts": "concept",
        "02-cheatsheets": "cheatsheet",
        "03-implementations": "implementation",
        "04-case-studies": "case-study",
        "05-exercises": "exercise",
        "06-notes": "note",
    }
    return mapping.get(section, "module-document")


def infer_module_metadata(relative_path: Path) -> dict[str, str] | None:
    if relative_path.parts[0] != "modules" or len(relative_path.parts) < 2:
        return None
    module_dir = relative_path.parts[1]
    if module_dir == "README.md":
        return None
    prefix, _, slug = module_dir.partition("-")
    return {
        "id": prefix,
        "slug": slug,
        "key": module_dir,
        "path": f"modules/{module_dir}",
    }


def infer_project_metadata(relative_path: Path) -> dict[str, str] | None:
    if relative_path.parts[0] != "projects" or len(relative_path.parts) < 2:
        return None
    project_dir = relative_path.parts[1]
    if project_dir == "README.md":
        return None
    prefix, _, slug = project_dir.partition("-")
    return {
        "id": prefix,
        "slug": slug,
        "key": project_dir,
        "path": f"projects/{project_dir}",
    }


def infer_track_metadata(relative_path: Path) -> dict[str, str] | None:
    if relative_path.parts[:2] != ("docs", "tracks"):
        return None
    return {
        "id": relative_path.stem,
        "slug": relative_path.stem,
        "key": relative_path.stem,
        "path": str(relative_path.parent / relative_path.name),
    }


def infer_section(relative_path: Path) -> str | None:
    if relative_path.parts[0] != "modules" or len(relative_path.parts) < 3:
        return None
    section = relative_path.parts[2]
    return section if re.match(r"^\d{2}-", section) else None


def resolve_local_link(relative_path: Path, target: str) -> str | None:
    link_target = target.split("#", 1)[0].strip()
    if not link_target or link_target.startswith(("http://", "https://", "mailto:", "#")):
        return None
    candidate = (relative_path.parent / link_target).resolve()
    try:
        normalized = candidate.relative_to(REPO_ROOT)
    except ValueError:
        return None
    return str(normalized)


def relative_link_targets(relative_path: Path, text: str) -> list[str]:
    targets: list[str] = []
    seen: set[str] = set()
    for _, target in LINK_RE.findall(text):
        normalized = resolve_local_link(relative_path, target)
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        targets.append(normalized)
    return targets


def extract_headings(lines: list[str]) -> list[dict[str, str | int]]:
    headings: list[dict[str, str | int]] = []
    in_code_block = False
    for raw_line in lines:
        stripped = raw_line.rstrip()
        if stripped.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        match = HEADING_RE.match(stripped)
        if not match:
            continue
        hashes, text = match.groups()
        heading = clean_heading(text)
        headings.append(
            {
                "level": len(hashes),
                "text": heading,
                "slug": slugify(heading),
            }
        )
    return headings


def extract_title(relative_path: Path, headings: list[dict[str, str | int]], metadata: dict[str, Any]) -> str:
    explicit_title = str(metadata.get("title", "")).strip()
    if explicit_title:
        return explicit_title

    for heading in headings:
        if heading["level"] == 1:
            return str(heading["text"])

    if relative_path.name == "README.md" and len(relative_path.parts) >= 2:
        stem = relative_path.parts[-2]
    else:
        stem = relative_path.stem

    stem = re.sub(r"^\d{2,3}[-_]", "", stem)
    stem = stem.replace("-", " ").replace("_", " ").strip()
    return stem.title() if stem else "Untitled"


def strip_markdown(text: str) -> str:
    lines = text.splitlines()
    parts: list[str] = []
    in_code_block = False

    for raw_line in lines:
        stripped = raw_line.rstrip()
        marker = stripped.strip()
        if marker.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        stripped = LINK_RE.sub(r"\1", stripped)
        stripped = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r"\1", stripped)
        stripped = re.sub(r"`([^`]+)`", r"\1", stripped)
        stripped = re.sub(r"^#{1,6}\s+", "", stripped)
        stripped = re.sub(r"^\s*[-*]\s+", "", stripped)
        stripped = re.sub(r"^\s*\d+\.\s+", "", stripped)
        stripped = re.sub(r"\s+", " ", stripped).strip()
        if stripped:
            parts.append(stripped)

    return " ".join(parts)


def build_url(relative_path: Path) -> str:
    if str(relative_path) == "docs/index.md":
        return "/"
    if relative_path.parts[:2] == ("docs", "tracks"):
        return f"/tracks/{relative_path.stem}"

    segments = list(relative_path.with_suffix("").parts)
    if segments and segments[-1] == "README":
        segments = segments[:-1]
    return "/" + "/".join(segments)


def level_from_module_key(module_key: str | None) -> str | None:
    if not module_key:
        return None
    try:
        index = int(module_key.split("-", 1)[0])
    except ValueError:
        return None
    if index <= 2:
        return "foundational"
    if index <= 11:
        return "intermediate"
    return "advanced"


def source_url_for_path(relative_path: Path) -> str:
    return f"{PROJECT_SOURCE_BASE}/{relative_path.as_posix()}"


def normalize_item(path: Path) -> dict[str, Any]:
    relative_path = path.relative_to(REPO_ROOT)
    raw_text = path.read_text(encoding="utf-8")
    front_matter, body = parse_front_matter(raw_text)
    lines = body.splitlines()
    headings = extract_headings(lines)
    title = extract_title(relative_path, headings, front_matter)
    summary = str(front_matter.get("summary") or first_paragraph(lines)).strip()
    content_type = infer_content_type(relative_path)
    module = infer_module_metadata(relative_path)
    project = infer_project_metadata(relative_path)
    track = infer_track_metadata(relative_path)
    url = build_url(relative_path)
    slug = url.strip("/") or "home"

    item: dict[str, Any] = {
        "id": str(relative_path.with_suffix("")).replace("/", ":"),
        "title": title,
        "path": str(relative_path),
        "url": url,
        "slug": slug,
        "collection": relative_path.parts[0],
        "content_type": content_type,
        "section": infer_section(relative_path),
        "summary": summary,
        "word_count": len(WORD_RE.findall(body)),
        "headings": headings,
        "links": relative_link_targets(relative_path, body),
        "source_url": source_url_for_path(relative_path),
        "status": str(front_matter.get("status") or "stable"),
        "format": str(front_matter.get("format") or CONTENT_TYPE_FORMATS.get(content_type, "reference")),
        "difficulty": str(front_matter.get("difficulty") or level_from_module_key(module["key"] if module else None) or ""),
        "tags": listify(front_matter.get("tags")),
        "prerequisites": listify(front_matter.get("prerequisites")),
        "related": listify(front_matter.get("related")),
        "canonical_url": str(front_matter.get("canonical_url") or front_matter.get("canonical") or url),
        "has_front_matter": bool(front_matter),
    }

    if module:
        item["module"] = module
    if project:
        item["project"] = project
    if track:
        item["track"] = track

    plain_text = strip_markdown(body)
    item["_search_body"] = plain_text
    item["_search_terms"] = []
    return item


def concept_sort_key(item: dict[str, Any]) -> tuple[int, str]:
    name = Path(item["path"]).name
    match = re.match(r"^(\d+)[-_]", name)
    order = int(match.group(1)) if match else 9999
    return order, name


def enrich_items(items: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    items_by_id = {item["id"]: item for item in items}
    items_by_path = {item["path"]: item for item in items}
    items_by_url = {item["url"]: item for item in items}

    module_hubs = [item for item in items if item["content_type"] == "module-overview"]
    project_docs = [item for item in items if item["content_type"] == "project"]
    track_docs = [item for item in items if item["content_type"] == "track"]

    module_titles = {
        item["module"]["key"]: {
            "title": item["title"],
            "url": item["url"],
            "id": item["id"],
            "summary": item["summary"],
        }
        for item in module_hubs
        if "module" in item
    }
    project_titles = {
        item["project"]["key"]: {
            "title": item["title"],
            "url": item["url"],
            "id": item["id"],
            "summary": item["summary"],
        }
        for item in project_docs
        if "project" in item
    }
    track_titles = {
        item["track"]["key"]: {
            "title": item["title"],
            "url": item["url"],
            "id": item["id"],
            "summary": item["summary"],
        }
        for item in track_docs
        if "track" in item
    }

    for item in items:
        if "module" in item and item["module"]["key"] in module_titles:
            item["module"] = {**item["module"], **module_titles[item["module"]["key"]]}
        if "project" in item and item["project"]["key"] in project_titles:
            item["project"] = {**item["project"], **project_titles[item["project"]["key"]]}
        if "track" in item and item["track"]["key"] in track_titles:
            item["track"] = {**item["track"], **track_titles[item["track"]["key"]]}

    outgoing_ids: dict[str, list[str]] = {}
    backlinks: dict[str, list[str]] = {item["id"]: [] for item in items}
    filesystem_link_errors: dict[str, list[str]] = {}

    for item in items:
        resolved_ids: list[str] = []
        missing_targets: list[str] = []
        for target_path in item["links"]:
            if target_path in items_by_path:
                resolved_ids.append(items_by_path[target_path]["id"])
                continue
            target_fs_path = REPO_ROOT / target_path
            if target_fs_path.exists():
                continue
            missing_targets.append(target_path)

        unique_resolved = list(dict.fromkeys(resolved_ids))
        outgoing_ids[item["id"]] = unique_resolved
        item["link_ids"] = unique_resolved
        if missing_targets:
            filesystem_link_errors[item["id"]] = sorted(set(missing_targets))
        for target_id in unique_resolved:
            backlinks[target_id].append(item["id"])

    for target_id, refs in backlinks.items():
        backlinks[target_id] = sorted(set(refs))

    track_targets: dict[str, dict[str, list[str]]] = {}
    track_memberships: dict[str, list[str]] = {item["id"]: [] for item in items}

    for track in track_docs:
        module_ids: list[str] = []
        project_ids: list[str] = []
        for target_id in outgoing_ids[track["id"]]:
            target = items_by_id[target_id]
            if target["content_type"] == "module-overview":
                module_ids.append(target_id)
            elif target["content_type"] == "project":
                project_ids.append(target_id)
        track_targets[track["id"]] = {
            "module_ids": list(dict.fromkeys(module_ids)),
            "project_ids": list(dict.fromkeys(project_ids)),
        }

    for track_id, targets in track_targets.items():
        track_slug = items_by_id[track_id]["track"]["slug"]
        for module_id in targets["module_ids"]:
            module_key = items_by_id[module_id]["module"]["key"]
            for item in items:
                if item.get("module", {}).get("key") == module_key:
                    track_memberships[item["id"]].append(track_slug)
        for project_id in targets["project_ids"]:
            track_memberships[project_id].append(track_slug)

    for item in items:
        item["tracks"] = sorted(set(track_memberships[item["id"]]))

    project_modules: dict[str, list[str]] = {}
    module_projects: dict[str, list[str]] = defaultdict(list)

    for project in project_docs:
        module_ids: list[str] = []
        for target_id in outgoing_ids[project["id"]]:
            target = items_by_id[target_id]
            if target["content_type"] == "module-overview":
                module_ids.append(target_id)
        project_modules[project["id"]] = list(dict.fromkeys(module_ids))
        for module_id in project_modules[project["id"]]:
            module_projects[module_id].append(project["id"])

    sequence: dict[str, dict[str, str | None]] = {}
    concepts_by_module: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in items:
        if item["content_type"] == "concept" and "module" in item:
            concepts_by_module[item["module"]["key"]].append(item)

    for concept_items in concepts_by_module.values():
        ordered = sorted(concept_items, key=concept_sort_key)
        for index, item in enumerate(ordered):
            sequence[item["id"]] = {
                "prev": ordered[index - 1]["id"] if index > 0 else None,
                "next": ordered[index + 1]["id"] if index < len(ordered) - 1 else None,
            }

    documents_relations: dict[str, Any] = {}
    orphan_document_ids: list[str] = []

    for item in items:
        same_module_ids: list[str] = []
        if "module" in item:
            module_key = item["module"]["key"]
            same_module_ids = [
                candidate["id"]
                for candidate in items
                if candidate["id"] != item["id"] and candidate.get("module", {}).get("key") == module_key
            ]

        same_track_ids: list[str] = []
        if item["tracks"]:
            for candidate in items:
                if candidate["id"] == item["id"]:
                    continue
                if set(candidate.get("tracks", [])) & set(item["tracks"]):
                    same_track_ids.append(candidate["id"])

        related_candidates: list[dict[str, Any]] = []
        seen_related: set[str] = set()

        def add_related(candidate_id: str, relation_type: str, weight: int) -> None:
            if candidate_id == item["id"] or candidate_id in seen_related:
                return
            seen_related.add(candidate_id)
            related_candidates.append({"id": candidate_id, "type": relation_type, "weight": weight})

        for candidate_id in outgoing_ids[item["id"]]:
            add_related(candidate_id, "authored-link", 100)
        for candidate_id in backlinks[item["id"]]:
            add_related(candidate_id, "backlink", 80)
        for candidate_id in same_module_ids[:6]:
            add_related(candidate_id, "same-module", 60)
        for candidate_id in same_track_ids[:6]:
            add_related(candidate_id, "same-track", 40)
        if item["content_type"] == "module-overview":
            for candidate_id in module_projects.get(item["id"], []):
                add_related(candidate_id, "module-project", 70)
        if item["content_type"] == "project":
            for candidate_id in project_modules.get(item["id"], []):
                add_related(candidate_id, "project-module", 70)

        related_candidates.sort(key=lambda candidate: (-candidate["weight"], candidate["id"]))
        documents_relations[item["id"]] = {
            "outgoing_links": outgoing_ids[item["id"]],
            "backlinks": backlinks[item["id"]],
            "track_memberships": item["tracks"],
            "project_modules": project_modules.get(item["id"], []),
            "module_projects": module_projects.get(item["id"], []),
            "sequence": sequence.get(item["id"], {"prev": None, "next": None}),
            "related": related_candidates[:10],
        }

        if (
            item["content_type"] not in HUB_TYPES
            and not outgoing_ids[item["id"]]
            and not backlinks[item["id"]]
            and not item["tracks"]
        ):
            orphan_document_ids.append(item["id"])

    catalog = {
        "modules": [],
        "projects": [],
        "tracks": [],
        "collections": [{"key": key, "label": key.title(), "count": count} for key, count in sorted(Counter(item["collection"] for item in items).items())],
        "content_types": [
            {"key": key, "label": key.replace("-", " ").title(), "count": count}
            for key, count in sorted(Counter(item["content_type"] for item in items).items())
        ],
    }

    for module in sorted(module_hubs, key=lambda entry: entry["module"]["key"]):
        module_key = module["module"]["key"]
        module_items = [item for item in items if item.get("module", {}).get("key") == module_key]
        catalog["modules"].append(
            {
                "id": module["id"],
                "key": module_key,
                "title": module["title"],
                "url": module["url"],
                "summary": module["summary"],
                "tracks": sorted(set(module["tracks"])),
                "project_ids": sorted(set(module_projects.get(module["id"], []))),
                "content_counts": dict(sorted(Counter(item["content_type"] for item in module_items).items())),
            }
        )

    for project in sorted(project_docs, key=lambda entry: entry["project"]["key"]):
        catalog["projects"].append(
            {
                "id": project["id"],
                "key": project["project"]["key"],
                "title": project["title"],
                "url": project["url"],
                "summary": project["summary"],
                "tracks": sorted(set(project["tracks"])),
                "module_ids": sorted(set(project_modules.get(project["id"], []))),
            }
        )

    for track in sorted(track_docs, key=lambda entry: entry["track"]["key"]):
        targets = track_targets.get(track["id"], {"module_ids": [], "project_ids": []})
        catalog["tracks"].append(
            {
                "id": track["id"],
                "key": track["track"]["key"],
                "title": track["title"],
                "url": track["url"],
                "summary": track["summary"],
                "module_ids": targets["module_ids"],
                "project_ids": targets["project_ids"],
            }
        )

    search_documents = []
    for item in items:
        keywords = sorted(
            {
                *item["tags"],
                item["collection"],
                item["content_type"],
                *(heading["text"] for heading in item["headings"]),
                *(item.get("tracks", [])),
                item.get("module", {}).get("title", ""),
                item.get("project", {}).get("title", ""),
            }
            - {""}
        )
        item["_search_terms"] = keywords
        search_documents.append(
            {
                "id": item["id"],
                "title": item["title"],
                "url": item["url"],
                "summary": item["summary"],
                "collection": item["collection"],
                "content_type": item["content_type"],
                "module": item.get("module", {}).get("key"),
                "project": item.get("project", {}).get("key"),
                "tracks": item.get("tracks", []),
                "tags": item["tags"],
                "keywords": keywords,
                "body": item["_search_body"],
            }
        )

    content_items: list[dict[str, Any]] = []
    for item in items:
        content_items.append(
            {
                key: value
                for key, value in item.items()
                if not key.startswith("_")
            }
        )

    content_index = {
        "schema_version": ARCHIVE_SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_roots": list(MARKDOWN_ROOTS),
        "artifacts": {
            "content_index": str(DEFAULT_OUTPUT.relative_to(REPO_ROOT)),
            "search_index": str(DEFAULT_SEARCH_OUTPUT.relative_to(REPO_ROOT)),
            "relations": str(DEFAULT_RELATIONS_OUTPUT.relative_to(REPO_ROOT)),
        },
        "counts": {
            "documents": len(content_items),
            "collections": dict(sorted(Counter(item["collection"] for item in content_items).items())),
            "content_types": dict(sorted(Counter(item["content_type"] for item in content_items).items())),
        },
        "catalog": catalog,
        "items": content_items,
    }

    search_index = {
        "schema_version": ARCHIVE_SCHEMA_VERSION,
        "generated_at": content_index["generated_at"],
        "documents": search_documents,
        "filters": {
            "collections": catalog["collections"],
            "content_types": catalog["content_types"],
            "modules": [
                {"key": module["key"], "label": module["title"]}
                for module in catalog["modules"]
            ],
            "tracks": [
                {"key": track["key"], "label": track["title"]}
                for track in catalog["tracks"]
            ],
        },
    }

    relations = {
        "schema_version": ARCHIVE_SCHEMA_VERSION,
        "generated_at": content_index["generated_at"],
        "documents": documents_relations,
        "tracks": track_targets,
        "project_modules": project_modules,
        "module_projects": {key: sorted(set(value)) for key, value in module_projects.items()},
        "orphan_document_ids": sorted(orphan_document_ids),
        "filesystem_link_errors": filesystem_link_errors,
    }

    return content_index, search_index, relations


def build_archive_bundle() -> dict[str, Any]:
    files = iter_markdown_files()
    items = [normalize_item(path) for path in files]
    content_index, search_index, relations = enrich_items(items)
    return {
        "content_index": content_index,
        "search_index": search_index,
        "relations": relations,
    }


def write_archive_bundle(output_path: Path, bundle: dict[str, Any]) -> dict[str, Path]:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    search_output = output_path.parent / "search-index.json"
    relations_output = output_path.parent / "relations.json"

    output_path.write_text(json.dumps(bundle["content_index"], indent=2) + "\n", encoding="utf-8")
    search_output.write_text(json.dumps(bundle["search_index"], indent=2) + "\n", encoding="utf-8")
    relations_output.write_text(json.dumps(bundle["relations"], indent=2) + "\n", encoding="utf-8")

    return {
        "content_index": output_path,
        "search_index": search_output,
        "relations": relations_output,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Path to write the generated content index. Default: {DEFAULT_OUTPUT}",
    )
    args = parser.parse_args()

    output_path = args.output
    if not output_path.is_absolute():
        output_path = (REPO_ROOT / output_path).resolve()

    bundle = build_archive_bundle()
    paths = write_archive_bundle(output_path, bundle)
    print(f"Wrote archive bundle to {paths['content_index'].parent}")
    print(f"Indexed {bundle['content_index']['counts']['documents']} Markdown documents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
