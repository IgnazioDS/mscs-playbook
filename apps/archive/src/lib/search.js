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
  const collection = options.collection || "";
  const contentType = options.contentType || "";
  const moduleKey = options.module || "";
  const trackKey = options.track || "";

  return records
    .map((record) => ({ record, score: scoreSearchRecord(record, tokens) }))
    .filter(({ record, score }) => {
      if (score <= 0) {
        return false;
      }
      if (collection && record.collection !== collection) {
        return false;
      }
      if (contentType && record.content_type !== contentType) {
        return false;
      }
      if (moduleKey && record.module !== moduleKey) {
        return false;
      }
      if (trackKey && !(record.tracks || []).includes(trackKey)) {
        return false;
      }
      return true;
    })
    .sort((left, right) => right.score - left.score || left.record.title.localeCompare(right.record.title))
    .map(({ record }) => record);
}
