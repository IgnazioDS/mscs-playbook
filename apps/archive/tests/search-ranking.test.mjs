import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";

import { searchRecords } from "../src/lib/search.js";

const repoRoot = path.resolve(process.cwd(), "..", "..");
const searchIndex = JSON.parse(fs.readFileSync(path.join(repoRoot, "docs/archive/search-index.json"), "utf8"));
const contentIndex = JSON.parse(fs.readFileSync(path.join(repoRoot, "docs/archive/content-index.json"), "utf8"));
const benchmarks = JSON.parse(fs.readFileSync(path.join(process.cwd(), "tests/search-benchmarks.json"), "utf8"));

const itemsById = new Map(contentIndex.items.map((item) => [item.id, item]));
const records = searchIndex.documents.map((doc) => {
  const item = itemsById.get(doc.id);
  return {
    ...doc,
    status: item?.status ?? "",
    format: item?.format ?? "",
    module_title: item?.module?.title ?? "",
    track_titles: item?.tracks ?? []
  };
});

test("search benchmarks return expected archive pages in top N", async (t) => {
  for (const benchmark of benchmarks) {
    await t.test(benchmark.query, () => {
      const results = searchRecords(records, { query: benchmark.query }).slice(0, benchmark.top_n);
      const resultIds = results.map((result) => result.id);
      if (benchmark.expected_first_id) {
        assert.equal(
          resultIds[0],
          benchmark.expected_first_id,
          `expected ${benchmark.expected_first_id} to rank first for query "${benchmark.query}", got ${resultIds[0]}`
        );
      }
      for (const expectedId of benchmark.expected_ids) {
        assert.ok(
          resultIds.includes(expectedId),
          `expected ${expectedId} in top ${benchmark.top_n} for query "${benchmark.query}", got ${resultIds.join(", ")}`
        );
      }
    });
  }
});
