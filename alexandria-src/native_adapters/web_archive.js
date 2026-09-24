/**
 * Native Zero-Credit Adapter: Internet Archive Wayback Machine
 * Source: Official Internet Archive Wayback API
 * Cost: $0.00 / 0 Firecrawl credits
 * Capabilities: captures/oldest, captures/history, captures/content
 */

const BASE_URL = 'https://archive.org/wayback/available';

async function execute(capability, options = {}) {
  const targetUrl = options.url || 'wikipedia.org';
  const timestamp = options.timestamp || options.date || '';

  let url = `${BASE_URL}?url=${encodeURIComponent(targetUrl)}`;
  if (timestamp) url += `&timestamp=${timestamp}`;

  const res = await fetch(url, {
    headers: {
      'User-Agent': 'LegendsAlexandriaKit/1.0',
      'Accept': 'application/json'
    },
    signal: AbortSignal.timeout(15000)
  });

  if (!res.ok) {
    throw new Error(`Wayback API error ${res.status}: ${await res.text()}`);
  }

  const json = await res.json();
  return {
    source: 'native-public-api',
    provider: 'web-archive-org',
    capability: capability,
    creditsUsed: 0,
    data: json.archived_snapshots?.closest || json
  };
}

module.exports = { execute };
