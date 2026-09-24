/**
 * Native Zero-Credit Adapter: SEC EDGAR API
 * Source: Official US Securities and Exchange Commission Public EDGAR API
 * Cost: $0.00 / 0 Firecrawl credits
 * Capabilities: filings/company, filings/filings, filings/concept, filings/search
 */

const BASE_URL = 'https://data.sec.gov';

async function execute(capability, options = {}) {
  const cap = (capability || '').toLowerCase();
  const cik = (options.cik || options.CIK || '0000320193').toString().padStart(10, '0'); // Default Apple

  let url = `${BASE_URL}/submissions/CIK${cik}.json`;

  if (cap.includes('concept')) {
    const taxonomy = options.taxonomy || 'us-gaap';
    const tag = options.tag || options.concept || 'Revenues';
    url = `${BASE_URL}/api/xbrl/companyconcept/CIK${cik}/${taxonomy}/${tag}.json`;
  } else if (cap.includes('fact')) {
    url = `${BASE_URL}/api/xbrl/companyfacts/CIK${cik}.json`;
  }

  const res = await fetch(url, {
    headers: {
      'User-Agent': 'LegendsAlexandriaKit/1.0 user@legends.internal',
      'Accept': 'application/json'
    },
    signal: AbortSignal.timeout(20000)
  });

  if (!res.ok) {
    throw new Error(`SEC EDGAR API error ${res.status}: ${await res.text()}`);
  }

  const json = await res.json();
  return {
    source: 'native-public-api',
    provider: 'sec-gov',
    capability: capability,
    creditsUsed: 0,
    data: json
  };
}

module.exports = { execute };
