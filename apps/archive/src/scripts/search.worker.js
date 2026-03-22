import { searchRecords } from "../lib/search.js";

let records = [];

self.onmessage = async (e) => {
  const { type, payload } = e.data;
  
  if (type === "INIT") {
    try {
      const response = await fetch("/api/search-records.json");
      if (!response.ok) throw new Error("Network error loading search index");
      records = await response.json();
      self.postMessage({ type: "READY" });
    } catch (err) {
      self.postMessage({ type: "ERROR", error: err.message });
    }
  } else if (type === "SEARCH") {
    const filtered = searchRecords(records, payload).slice(0, 160);
    self.postMessage({ type: "RESULTS", results: filtered });
  }
};
