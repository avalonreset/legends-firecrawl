/**
 * Native Zero-Credit Adapter: ESPN Sports API
 * Source: Official unauthenticated public ESPN web API
 * Cost: $0.00 / 0 Firecrawl credits
 * Capabilities: sports-data/scoreboard, sports-data/teams, sports-data/roster, sports-data/standings, sports-data/event
 */

const BASE_URL = 'https://site.api.espn.com/apis/site/v2/sports';

async function execute(capability, options = {}) {
  const cap = (capability || '').toLowerCase();
  const sport = options.sport || 'football';
  const league = options.league || 'nfl';
  
  let endpoint = 'scoreboard';
  if (cap.includes('team') || cap.includes('roster')) endpoint = 'teams';
  else if (cap.includes('standing')) endpoint = 'standings';
  else if (cap.includes('news')) endpoint = 'news';

  const url = `${BASE_URL}/${sport}/${league}/${endpoint}`;
  const res = await fetch(url, {
    headers: {
      'User-Agent': 'LegendsAlexandriaKit/1.0',
      'Accept': 'application/json'
    },
    signal: AbortSignal.timeout(15000)
  });

  if (!res.ok) {
    throw new Error(`ESPN API error ${res.status}: ${await res.text()}`);
  }

  const json = await res.json();
  return {
    source: 'native-public-api',
    provider: 'espn-com',
    capability: capability,
    creditsUsed: 0,
    data: json
  };
}

module.exports = { execute };
