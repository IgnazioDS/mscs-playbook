import { searchRecords } from "../lib/search.js";

function renderCard(record) {
  const tags = [
    record.content_type.replace(/-/g, " "),
    record.collection,
    record.module_title,
    ...(record.track_titles || []).map((track) => `track: ${track}`)
  ].filter(Boolean);

  return `
    <article class="card">
      <div class="badge-row" style="margin-bottom: 0.8rem;">
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

export async function initBrowsePage() {
  let records = [];
  try {
    const response = await fetch("/api/search-records.json");
    if (!response.ok) throw new Error("Network response was not ok");
    records = await response.json();
  } catch (err) {
    console.error("Failed to load search index:", err);
    const countEl = document.getElementById("results-count");
    if (countEl) countEl.textContent = "Failed to load search index. Please refresh.";
    return;
  }
  const queryEl = document.getElementById("query");
  const collectionEl = document.getElementById("collection");
  const typeEl = document.getElementById("content-type");
  const moduleEl = document.getElementById("module");
  const trackEl = document.getElementById("track");
  const resultsEl = document.getElementById("results");
  const countEl = document.getElementById("results-count");

  if (!queryEl || !collectionEl || !typeEl || !moduleEl || !trackEl || !resultsEl || !countEl) {
    return;
  }

  const params = new URLSearchParams(window.location.search);
  if (params.get("collection")) collectionEl.value = params.get("collection");
  if (params.get("content_type")) typeEl.value = params.get("content_type");
  if (params.get("module")) moduleEl.value = params.get("module");
  if (params.get("track")) trackEl.value = params.get("track");
  if (params.get("q")) queryEl.value = params.get("q");

  function applyFilters() {
    const filtered = searchRecords(records, {
      query: queryEl.value,
      collection: collectionEl.value,
      contentType: typeEl.value,
      module: moduleEl.value,
      track: trackEl.value
    }).slice(0, 160);

    resultsEl.innerHTML = filtered.length ? filtered.map(renderCard).join("") : renderEmptyState();
    countEl.textContent = `Showing ${filtered.length} results`;

    writeUrlState({
      query: queryEl.value.trim(),
      collection: collectionEl.value,
      contentType: typeEl.value,
      module: moduleEl.value,
      track: trackEl.value
    });
  }

  [queryEl, collectionEl, typeEl, moduleEl, trackEl].forEach((element) => {
    element.addEventListener("input", applyFilters);
    element.addEventListener("change", applyFilters);
  });

  applyFilters();
}
