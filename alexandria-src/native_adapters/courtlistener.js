/**
 * Native Zero-Credit Adapter: CourtListener / Free Law Project
 * Source: Free Law Project open legal search API
 * Cost: $0.00 / 0 Firecrawl credits
 * Capabilities: opinions/search_opinions, dockets/search_dockets, courts/courts, dockets/docket_entries
 */

const BASE_URL = 'https://www.courtlistener.com/api/rest/v4';

async function execute(capability, options = {}) {
  const cap = (capability || '').toLowerCase();
  const query = options.query || options.q || 'copyright';

  let endpoint = `/search/?q=${encodeURIComponent(query)}&type=o`;
  if (cap.includes('docket')) {
    endpoint = `/search/?q=${encodeURIComponent(query)}&type=r`;
  } else if (cap.includes('court')) {
    endpoint = '/courts/';
  }

  const url = `${BASE_URL}${endpoint}`;

  const res = await fetch(url, {
    headers: {
      'User-Agent': 'LegendsAlexandriaKit/1.0 (legends-firecrawl; open research)',
      'Accept': 'application/json'
    },
    signal: AbortSignal.timeout(45000)
  });

  if (!res.ok) {
    throw new Error(`CourtListener API error ${res.status}: ${await res.text()}`);
  }

  const json = await res.json();
  return {
    source: 'native-public-api',
    provider: 'courtlistener-com',
    capability: capability,
    creditsUsed: 0,
    data: json.results || json
  };
}

module.exports = { execute };

