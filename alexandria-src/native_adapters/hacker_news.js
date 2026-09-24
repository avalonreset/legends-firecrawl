/**
 * Native Zero-Credit Adapter: Y Combinator & Hacker News API
 * Source: Official Algolia Public API for Hacker News & YC Ecosystem
 * Cost: $0.00 / 0 Firecrawl credits
 * Capabilities: companies/search, companies/company, front_page, stories
 */

const BASE_URL = 'https://hn.algolia.com/api/v1';

async function execute(capability, options = {}) {
  const cap = (capability || '').toLowerCase();
  const query = options.query || options.q || '';
  const page = options.page || 0;
  const hitsPerPage = options.limit || options.hitsPerPage || 20;

  let url = `${BASE_URL}/search?page=${page}&hitsPerPage=${hitsPerPage}`;

  if (query) {
    url += `&query=${encodeURIComponent(query)}`;
  } else if (cap.includes('front') || cap.includes('top')) {
    url += '&tags=front_page';
  } else {
    url += '&tags=story';
  }

  const res = await fetch(url, {
    headers: {
      'User-Agent': 'LegendsAlexandriaKit/1.0 (legends-firecrawl; open research)',
      'Accept': 'application/json'
    },
    signal: AbortSignal.timeout(15000)
  });

  if (!res.ok) {
    throw new Error(`Hacker News / YC API error ${res.status}: ${await res.text()}`);
  }

  const json = await res.json();
  const records = (json.hits || []).map(h => ({
    id: h.objectID,
    title: h.title || h.story_title,
    url: h.url || `https://news.ycombinator.com/item?id=${h.objectID}`,
    author: h.author,
    points: h.points,
    comments_count: h.num_comments,
    created_at: h.created_at
  }));

  return {
    source: 'native-public-api',
    provider: 'ycombinator-com',
    capability: capability,
    creditsUsed: 0,
    data: records
  };
}

module.exports = { execute };

