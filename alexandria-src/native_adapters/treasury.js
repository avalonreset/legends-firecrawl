/**
 * Native Zero-Credit Adapter: US Treasury Fiscal Data
 * Source: Official US Treasury Bureau of the Fiscal Service API
 * Cost: $0.00 / 0 Firecrawl credits
 */

const BASE_URL = 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service';

const CAPABILITY_MAP = {
  'debt/to-the-penny': 'v2/accounting/od/debt_to_penny',
  'debt/average-interest-rates': 'v2/accounting/od/avg_interest_rates',
  'debt/interest-expense': 'v2/accounting/od/interest_expense',
  'debt/historical-outstanding': 'v2/accounting/od/historical_debt',
  'daily-statement/operating-cash-balance': 'v1/accounting/dts/operating_cash_balance',
  'daily-statement/public-debt-transactions': 'v1/accounting/dts/public_debt_transactions',
  'monthly-statement/receipts-and-outlays': 'v1/accounting/mts/mts_table_1',
  'rates/exchange': 'v1/accounting/od/rates_of_exchange',
  'reserves/gold': 'v2/accounting/od/gold_reserve'
};

async function execute(capability, options = {}) {
  const endpoint = CAPABILITY_MAP[capability] || 'v2/accounting/od/debt_to_penny';
  const url = new URL(`${BASE_URL}/${endpoint}`);

  // Passthrough supported query parameters
  if (options.sort) url.searchParams.set('sort', options.sort);
  else url.searchParams.set('sort', '-record_date');

  if (options.page_size) url.searchParams.set('page[size]', options.page_size);
  else if (options['page[size]']) url.searchParams.set('page[size]', options['page[size]']);
  else url.searchParams.set('page[size]', '5');

  if (options.filter) url.searchParams.set('filter', options.filter);

  const res = await fetch(url.toString(), {
    headers: { 'Accept': 'application/json' }
  });

  if (!res.ok) {
    throw new Error(`Treasury API error ${res.status}: ${await res.text()}`);
  }

  const json = await res.json();
  return {
    source: 'native-public-api',
    provider: 'treasury-fiscal-data',
    capability: capability,
    creditsUsed: 0,
    data: json.data,
    meta: json.meta
  };
}

module.exports = { execute, CAPABILITY_MAP };
