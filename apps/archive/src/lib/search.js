export const SEARCH_WEIGHTS = {
  exactTitle: 20,
  title: 12,
  summary: 7,
  keywords: 5,
  module: 4,
  tracks: 3,
  body: 1
};

export function normalizeSearchValue(value) {
  return (value || "").toString().toLowerCase().trim();
}

export function tokenizeQuery(query) {
  return normalizeSearchValue(query).split(/\s+/).filter(Boolean);
}

function includesToken(haystack, token) {
  return haystack.includes(token);
}

export function scoreSearchRecord(record, tokens, weights = SEARCH_WEIGHTS) {
  if (!tokens.length) {
    return 1;
  }

  const title = normalizeSearchValue(record.title);
  const summary = normalizeSearchValue(record.summary);
  const keywords = normalizeSearchValue((record.keywords || []).join(" "));
  const moduleTitle = normalizeSearchValue(record.module_title || "");
  const tracks = normalizeSearchValue((record.track_titles || record.tracks || []).join(" "));
  const body = normalizeSearchValue(record.body);

  let score = 0;

  for (const token of tokens) {
    let matched = false;

    if (title === token) {
      score += weights.exactTitle;
      matched = true;
    }
    if (includesToken(title, token)) {
      score += weights.title;
      matched = true;
    }
    if (includesToken(summary, token)) {
      score += weights.summary;
      matched = true;
    }
    if (includesToken(keywords, token)) {
      score += weights.keywords;
      matched = true;
    }
    if (includesToken(moduleTitle, token)) {
      score += weights.module;
      matched = true;
    }
    if (includesToken(tracks, token)) {
      score += weights.tracks;
      matched = true;
    }
    if (includesToken(body, token)) {
      score += weights.body;
      matched = true;
    }

    if (!matched) {
      return 0;
    }
  }

  return score;
}

export function searchRecords(records, options = {}) {
  const tokens = tokenizeQuery(options.query || "");
  const collections = Array.isArray(options.collection) ? options.collection : (options.collection ? [options.collection] : []);
  const contentTypes = Array.isArray(options.contentType) ? options.contentType : (options.contentType ? [options.contentType] : []);
  const modules = Array.isArray(options.module) ? options.module : (options.module ? [options.module] : []);
  const tracks = Array.isArray(options.track) ? options.track : (options.track ? [options.track] : []);

  return records
    .map((record) => ({ record, score: scoreSearchRecord(record, tokens) }))
    .filter(({ record, score }) => {
      if (score <= 0) {
        return false;
      }
      if (collections.length > 0 && !collections.includes(record.collection)) {
        return false;
      }
      if (contentTypes.length > 0 && !contentTypes.includes(record.content_type)) {
        return false;
      }
      if (modules.length > 0 && !modules.includes(record.module)) {
        return false;
      }
      if (tracks.length > 0 && !tracks.some(t => (record.tracks || []).includes(t))) {
        return false;
      }
      return true;
    })
    .sort((left, right) => right.score - left.score || left.record.title.localeCompare(right.record.title))
    .map(({ record }) => record);
}
