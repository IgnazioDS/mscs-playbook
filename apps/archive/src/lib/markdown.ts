import fs from "node:fs";
import path from "node:path";
import { Marked } from "marked";

import { itemsByPath, sourceBlobBase, sourceRawBase } from "./archive";

const REPO_ROOT = path.resolve(process.cwd(), "../..");

function slugify(text: string): string {
  return text.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "") || "section";
}

function stripFrontMatter(text: string): string {
  if (!text.startsWith("---\n")) {
    return text;
  }
  const end = text.indexOf("\n---\n", 4);
  if (end === -1) {
    return text;
  }
  return text.slice(end + 5);
}

function resolveLocalHref(sourcePath: string, href: string): string {
  if (!href || href.startsWith("#") || href.startsWith("http://") || href.startsWith("https://") || href.startsWith("mailto:")) {
    return href;
  }

  const [target, anchor] = href.split("#", 2);
  const resolved = path.resolve(path.dirname(path.join(REPO_ROOT, sourcePath)), target);
  const relative = path.relative(REPO_ROOT, resolved).split(path.sep).join("/");
  const archiveItem = itemsByPath.get(relative);
  if (archiveItem) {
    return anchor ? `${archiveItem.url}#${slugify(anchor)}` : archiveItem.url;
  }
  if (fs.existsSync(resolved)) {
    const stat = fs.statSync(resolved);
    const base = stat.isDirectory() ? `${sourceBlobBase.replace("/blob/", "/tree/")}` : sourceBlobBase;
    return `${base}/${relative}`;
  }
  return href;
}

function resolveImageHref(sourcePath: string, href: string): string {
  if (!href || href.startsWith("http://") || href.startsWith("https://") || href.startsWith("data:")) {
    return href;
  }
  const resolved = path.resolve(path.dirname(path.join(REPO_ROOT, sourcePath)), href);
  const relative = path.relative(REPO_ROOT, resolved).split(path.sep).join("/");
  return `${sourceRawBase}/${relative}`;
}

export function renderMarkdown(sourcePath: string): string {
  const filePath = path.join(REPO_ROOT, sourcePath);
  const body = stripFrontMatter(fs.readFileSync(filePath, "utf8"));
  const renderer = {
    heading(this: any, token: { depth: number; text: string; tokens: unknown[] }) {
      const text = this.parser.parseInline(token.tokens);
      const id = slugify(token.text);
      return `<h${token.depth} id="${id}">${text}</h${token.depth}>`;
    },
    link(this: any, token: { href: string; title: string | null; tokens: unknown[] }) {
      const text = this.parser.parseInline(token.tokens);
      const href = resolveLocalHref(sourcePath, token.href);
      const title = token.title ? ` title="${token.title}"` : "";
      const external = href.startsWith("http://") || href.startsWith("https://");
      const extra = external ? ' target="_blank" rel="noreferrer"' : "";
      return `<a href="${href}"${title}${extra}>${text}</a>`;
    },
    image(token: { href: string; text: string; title: string | null }) {
      const src = resolveImageHref(sourcePath, token.href);
      const title = token.title ? ` title="${token.title}"` : "";
      return `<img src="${src}" alt="${token.text}" loading="lazy"${title} />`;
    }
  };

  const marked = new Marked({ gfm: true, breaks: false });
  marked.use({ renderer });
  return marked.parse(body) as string;
}
