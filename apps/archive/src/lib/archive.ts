import fs from "node:fs";
import path from "node:path";

export type ArchiveHeading = {
  level: number;
  text: string;
  slug: string;
};

export type ArchiveEntityRef = {
  id: string;
  key: string;
  title: string;
  url: string;
  summary: string;
  slug: string;
  path: string;
};

export type ArchiveItem = {
  id: string;
  title: string;
  path: string;
  url: string;
  slug: string;
  collection: string;
  content_type: string;
  section?: string | null;
  summary: string;
  word_count: number;
  headings: ArchiveHeading[];
  links: string[];
  link_ids?: string[];
  source_url: string;
  status: string;
  format: string;
  difficulty?: string;
  tags: string[];
  prerequisites: string[];
  related: string[];
  canonical_url: string;
  has_front_matter: boolean;
  tracks?: string[];
  module?: ArchiveEntityRef;
  project?: ArchiveEntityRef;
  track?: ArchiveEntityRef;
};

export type CatalogEntry = {
  id: string;
  key: string;
  title: string;
  url: string;
  summary: string;
  tracks?: string[];
  project_ids?: string[];
  module_ids?: string[];
  content_counts?: Record<string, number>;
};

export type ContentIndex = {
  schema_version: string;
  generated_at: string;
  counts: {
    documents: number;
    collections: Record<string, number>;
    content_types: Record<string, number>;
  };
  catalog: {
    modules: CatalogEntry[];
    projects: CatalogEntry[];
    tracks: CatalogEntry[];
    collections: Array<{ key: string; label: string; count: number }>;
    content_types: Array<{ key: string; label: string; count: number }>;
  };
  items: ArchiveItem[];
};

export type SearchDocument = {
  id: string;
  title: string;
  url: string;
  summary: string;
  collection: string;
  content_type: string;
  module?: string | null;
  project?: string | null;
  tracks: string[];
  tags: string[];
  keywords: string[];
  body: string;
};

export type SearchIndex = {
  schema_version: string;
  generated_at: string;
  documents: SearchDocument[];
  filters: {
    collections: Array<{ key: string; label: string }>;
    content_types: Array<{ key: string; label: string }>;
    modules: Array<{ key: string; label: string }>;
    tracks: Array<{ key: string; label: string }>;
  };
};

export type RelationDocument = {
  outgoing_links: string[];
  backlinks: string[];
  track_memberships: string[];
  project_modules: string[];
  module_projects: string[];
  sequence: {
    prev: string | null;
    next: string | null;
  };
  related: Array<{
    id: string;
    type: string;
    weight: number;
  }>;
};

export type RelationsIndex = {
  schema_version: string;
  generated_at: string;
  documents: Record<string, RelationDocument>;
  tracks: Record<string, { module_ids: string[]; project_ids: string[] }>;
  project_modules: Record<string, string[]>;
  module_projects: Record<string, string[]>;
  orphan_document_ids: string[];
};

const REPO_ROOT = path.resolve(process.cwd(), "../..");
const ARCHIVE_DIR = path.join(REPO_ROOT, "docs", "archive");

function readJson<T>(filename: string): T {
  return JSON.parse(fs.readFileSync(path.join(ARCHIVE_DIR, filename), "utf8")) as T;
}

export const contentIndex = readJson<ContentIndex>("content-index.json");
export const searchIndex = readJson<SearchIndex>("search-index.json");
export const relationsIndex = readJson<RelationsIndex>("relations.json");

export const archiveItems = contentIndex.items;
export const moduleCatalog = contentIndex.catalog.modules;
export const projectCatalog = contentIndex.catalog.projects;
export const trackCatalog = contentIndex.catalog.tracks;
export const itemsById = new Map(archiveItems.map((item) => [item.id, item]));
export const itemsByUrl = new Map(archiveItems.map((item) => [item.url, item]));
export const itemsByPath = new Map(archiveItems.map((item) => [item.path, item]));
export const moduleCatalogByKey = new Map(moduleCatalog.map((entry) => [entry.key, entry]));
export const projectCatalogByKey = new Map(projectCatalog.map((entry) => [entry.key, entry]));
export const trackCatalogByKey = new Map(trackCatalog.map((entry) => [entry.key, entry]));

export const sourceRepoBase = "https://github.com/IgnazioDS/mscs-playbook";
export const sourceBlobBase = `${sourceRepoBase}/blob/main`;
export const sourceRawBase = "https://raw.githubusercontent.com/IgnazioDS/mscs-playbook/main";

export function getItemById(id: string | null | undefined): ArchiveItem | undefined {
  return id ? itemsById.get(id) : undefined;
}

export function getItemByUrl(url: string): ArchiveItem | undefined {
  return itemsByUrl.get(url);
}

export function humanizeContentType(value: string): string {
  return value.replace(/-/g, " ");
}

export function formatWordCount(wordCount: number): string {
  if (wordCount < 1000) {
    return `${wordCount} words`;
  }
  return `${(wordCount / 1000).toFixed(1)}k words`;
}

export function sectionLabel(section?: string | null): string | null {
  if (!section) {
    return null;
  }
  const label = section.replace(/^\d+-/, "").replace(/-/g, " ");
  return label.charAt(0).toUpperCase() + label.slice(1);
}

export function getBreadcrumbs(item: ArchiveItem): Array<{ label: string; url?: string }> {
  const crumbs: Array<{ label: string; url?: string }> = [{ label: "Archive", url: "/" }];

  if (item.collection === "modules") {
    crumbs.push({ label: "Modules", url: "/modules" });
    if (item.module) {
      crumbs.push({ label: item.module.title, url: item.module.url });
    }
    const label = sectionLabel(item.section);
    if (label && item.content_type !== "module-overview") {
      crumbs.push({ label });
    }
  } else if (item.collection === "projects") {
    crumbs.push({ label: "Projects", url: "/projects" });
  } else if (item.content_type === "track") {
    crumbs.push({ label: "Tracks", url: "/tracks" });
  } else if (item.collection === "docs") {
    crumbs.push({ label: "Docs", url: "/docs" });
  }

  if (crumbs[crumbs.length - 1]?.label !== item.title) {
    crumbs.push({ label: item.title });
  }

  return crumbs;
}

export function relatedItemsFor(item: ArchiveItem): RelationDocument {
  return relationsIndex.documents[item.id] ?? {
    outgoing_links: [],
    backlinks: [],
    track_memberships: [],
    project_modules: [],
    module_projects: [],
    sequence: { prev: null, next: null },
    related: []
  };
}

export function readSourceFile(relativePath: string): string {
  return fs.readFileSync(path.join(REPO_ROOT, relativePath), "utf8");
}
