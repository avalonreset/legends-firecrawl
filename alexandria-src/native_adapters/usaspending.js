/**
 * Native Zero-Credit Adapter: USAspending Federal Procurement Data
 * Source: Official US Treasury USAspending API
 * Cost: $0.00 / 0 Firecrawl credits
 * Capabilities: agencies/agency, awards/award_search, awards/award, recipients/recipient
 */

const BASE_URL = 'https://api.usaspending.gov/api/v2';

async function execute(capability, options = {}) {
  const cap = (capability || '').toLowerCase();
  let endpoint = '';
  let method = 'GET';
  let body = null;

  if (cap.includes('agency')) {
    const code = options.toptier_code || '012';
    endpoint = `/agency/${code}/`;
  } else if (cap.includes('recipient')) {
    const uei = options.uei || options.recipient_id;
    if (uei) endpoint = `/recipient/${uei}/`;
    else endpoint = '/references/toptier_agencies/';
  } else if (cap.includes('award') || cap.includes('search')) {
    endpoint = '/search/spending_by_award/';
    method = 'POST';
    body = JSON.stringify({
      filters: {
        award_type_codes: options.award_type_codes || ['A', 'B', 'C', 'D'],
        keywords: options.keywords ? [options.keywords] : ['cloud']
      },
      fields: ['Award ID', 'Recipient Name', 'Award Amount', 'Description', 'Action Date'],
      page: 1,
      limit: options.page_size || 5,
      sort: 'Award Amount',
      order: 'desc'
    });
  } else {
    endpoint = '/references/toptier_agencies/';
  }

  const url = `${BASE_URL}${endpoint}`;
  const headers = {
    'User-Agent': 'LegendsAlexandriaKit/1.0',
    'Accept': 'application/json'
  };
  if (body) headers['Content-Type'] = 'application/json';

  const res = await fetch(url, {
    method,
    headers,
    body,
    signal: AbortSignal.timeout(35000)
  });

  if (!res.ok) {
    throw new Error(`USAspending API error ${res.status}: ${await res.text()}`);
  }

  const json = await res.json();
  return {
    source: 'native-public-api',
    provider: 'usaspending-gov',
    capability: capability,
    creditsUsed: 0,
    data: json.results || json
  };
}

module.exports = { execute };
