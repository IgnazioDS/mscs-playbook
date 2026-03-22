import { searchRecords } from "../lib/search.js";

function renderCard(record) {
  let isRead = false;
  try {
    const dict = JSON.parse(localStorage.getItem('archive_read') || '{}');
    const cleanUrl = record.url.replace(/\/$/, '');
    isRead = !!dict[cleanUrl];
  } catch (e) {}

  const readTag = isRead ? '<span class="badge" style="background: var(--accent); color: white; border-color: var(--accent);">✓ Read</span>' : '';

  const tags = [
    record.content_type.replace(/-/g, " "),
    record.collection,
    record.module_title,
    ...(record.track_titles || []).map((track) => `track: ${track}`)
  ].filter(Boolean);

  return `
    <article class="card">
      <div class="badge-row" style="margin-bottom: 0.8rem;">
        ${readTag}
        ${tags.slice(0, 4).map((tag) => `<span class="badge">${tag}</span>`).join("")}
      </div>
      <h3 style="font-size: 1.25rem; margin-bottom: 0.5rem;"><a href="${record.url}">${record.title}</a></h3>
      <p>${record.summary || "No summary available yet."}</p>
      <div class="meta-list" style="margin-top: 0.9rem;">
        <span>${record.status}</span>
        <span>${record.format}</span>
      </div>
    </article>
  `;
}

function renderEmptyState() {
  return `
    <article class="card" style="grid-column: 1 / -1;">
      <div class="eyebrow">No Results</div>
      <h3 style="font-size: 1.4rem; margin: 0.7rem 0 0.4rem;">No archive pages matched this filter set.</h3>
      <p>Try a broader query, remove one filter, or start from a track or module hub instead of searching for a leaf page title.</p>
    </article>
  `;
}

function writeUrlState(state) {
  const params = new URLSearchParams();
  if (state.query) params.set("q", state.query);
  if (state.collection) params.set("collection", state.collection);
  if (state.contentType) params.set("content_type", state.contentType);
  if (state.module) params.set("module", state.module);
  if (state.track) params.set("track", state.track);
  const url = `${window.location.pathname}${params.toString() ? `?${params.toString()}` : ""}`;
  window.history.replaceState({}, "", url);
}

export function initBrowsePage() {
  const queryEl = document.getElementById("query");
  const resultsEl = document.getElementById("results");
  const countEl = document.getElementById("results-count");

  if (!queryEl || !resultsEl || !countEl) {
    return;
  }
  
  const worker = new Worker(new URL("./search.worker.js", import.meta.url), { type: "module" });
  worker.postMessage({ type: "INIT" });

  worker.onmessage = (e) => {
    const data = e.data;
    if (data.type === "READY") {
      applyFilters();
    } else if (data.type === "RESULTS") {
      const results = data.results;
      resultsEl.innerHTML = results.length ? results.map(renderCard).join("") : renderEmptyState();
      countEl.textContent = `Showing ${results.length} results`;
    } else if (data.type === "ERROR") {
      console.error(data.error);
      countEl.textContent = "Failed to load search index. Please refresh.";
    }
  };

  const params = new URLSearchParams(window.location.search);
  if (params.get("q")) queryEl.value = params.get("q");

  ["collection", "content_type", "module", "track"].forEach(name => {
    const val = params.get(name);
    if (val) {
      val.split(",").forEach(v => {
        const el = document.querySelector(`input[name="${name}"][value="${v}"]`);
        if (el) el.checked = true;
      });
    }
  });

  function getChecked(name) {
    return Array.from(document.querySelectorAll(`input[name="${name}"]:checked`)).map(el => el.value);
  }

  function applyFilters() {
    const collections = getChecked("collection");
    const contentTypes = getChecked("content_type");
    const modules = getChecked("module");
    const tracks = getChecked("track");

    worker.postMessage({
      type: "SEARCH",
      payload: {
        query: queryEl.value,
        collection: collections,
        contentType: contentTypes,
        module: modules,
        track: tracks
      }
    });

    writeUrlState({
      query: queryEl.value.trim(),
      collection: collections.join(","),
      contentType: contentTypes.join(","),
      module: modules.join(","),
      track: tracks.join(",")
    });
  }

  queryEl.addEventListener("input", applyFilters);
  document.querySelectorAll('input[type="checkbox"]').forEach(el => {
    el.addEventListener("change", applyFilters);
  });
}
