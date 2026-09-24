/**
 * Native Zero-Credit Adapter: Yahoo Finance
 * Source: Public Yahoo Finance Query Endpoints
 * Cost: $0.00 / 0 Firecrawl credits
 * Capabilities: equities/quote, equities/search, equities/dividends, equities/earnings
 */

const BASE_URL = 'https://query1.finance.yahoo.com';

async function execute(capability, options = {}) {
  const cap = (capability || '').toLowerCase();
  const symbol = (options.symbol || options.ticker || 'AAPL').toUpperCase();

  let url = '';

  if (cap.includes('search')) {
    const q = options.query || options.q || symbol;
    url = `${BASE_URL}/v1/finance/search?q=${encodeURIComponent(q)}&quotesCount=10&newsCount=0`;
  } else if (cap.includes('dividends')) {
    url = `${BASE_URL}/v8/finance/chart/${symbol}?range=5y&interval=1mo&events=div`;
  } else if (cap.includes('earnings')) {
    url = `${BASE_URL}/v10/finance/quoteSummary/${symbol}?modules=earnings,earningsHistory,earningsTrend`;
  } else {
    // equities/quote or chart
    url = `${BASE_URL}/v8/finance/chart/${symbol}?range=1d&interval=1d&indicators=quote&includeTimestamps=true`;
  }

  const res = await fetch(url, {
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      'Accept': 'application/json'
    },
    signal: AbortSignal.timeout(15000)
  });

  if (!res.ok) {
    throw new Error(`Yahoo Finance API error ${res.status}: ${await res.text()}`);
  }

  const json = await res.json();
  let data = json;

  if (json?.chart?.result?.[0]) {
    data = json.chart.result[0];
  } else if (json?.quoteSummary?.result?.[0]) {
    data = json.quoteSummary.result[0];
  } else if (json?.quotes) {
    data = json.quotes;
  }

  return {
    source: 'native-public-api',
    provider: 'finance-yahoo-com',
    capability: capability,
    creditsUsed: 0,
    data: data
  };
}

module.exports = { execute };
