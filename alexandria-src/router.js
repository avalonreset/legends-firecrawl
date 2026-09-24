const fs = require('fs');
const path = require('path');

const treasury = require('./native_adapters/treasury');
const espn = require('./native_adapters/espn');
const secEdgar = require('./native_adapters/sec_edgar');
const hackerNews = require('./native_adapters/hacker_news');
const courtListener = require('./native_adapters/courtlistener');
const yahooFinance = require('./native_adapters/yahoo_finance');
const usaSpending = require('./native_adapters/usaspending');
const webArchive = require('./native_adapters/web_archive');

const NATIVE_ADAPTERS = {
  'treasury-fiscal-data': treasury,
  'espn-com': espn,
  'sec-gov': secEdgar,
  'ycombinator-com': hackerNews,
  'courtlistener-com': courtListener,
  'finance-yahoo-com': yahooFinance,
  'usaspending-gov': usaSpending,
  'web-archive-org': webArchive
};

let SAFETY_AUDIT_CACHE = null;

function getSafetyAudit() {
  if (SAFETY_AUDIT_CACHE) return SAFETY_AUDIT_CACHE;
  const auditPath = path.join(__dirname, '..', 'data', 'safety_audit.json');
  if (fs.existsSync(auditPath)) {
    try {
      SAFETY_AUDIT_CACHE = JSON.parse(fs.readFileSync(auditPath, 'utf-8'));
      return SAFETY_AUDIT_CACHE;
    } catch {}
  }
  return null;
}

function getProviderSafety(providerId) {
  const audit = getSafetyAudit();
  if (!audit?.providers) return null;
  return audit.providers.find(p => p.id === providerId) || null;
}

function getCredentials() {
  const credsPath = path.join(process.env.APPDATA || '', 'firecrawl-cli', 'credentials.json');
  if (fs.existsSync(credsPath)) {
    try {
      return JSON.parse(fs.readFileSync(credsPath, 'utf-8'));
    } catch {}
  }
  const envKey = process.env.FIRECRAWL_API_KEY;
  if (envKey) return { apiKey: envKey, apiUrl: 'https://api.firecrawl.dev' };
  return null;
}

async function query(providerId, capability, options = {}, flags = {}) {
  const forceGateway = Boolean(flags.forceGateway || flags.gateway);
  const dangerDirectIp = Boolean(flags.dangerDirectIp || flags['danger-direct-ip']);

  const providerSafety = getProviderSafety(providerId);
  const safetyTier = providerSafety?.ipSafety || 'UNKNOWN';

  // Automated Routing Decision Policy:
  // 1. GREEN_SAFE: Sanctioned open APIs with zero bot mitigation.
  //    Default: Native direct bypass (0 credits burned).
  // 2. YELLOW_SHIELDED: Commercial frontends (Cloudflare / DataDome).
  //    Default: Route via Firecrawl proxy gateway to protect user residential IP.
  //    Override: Only bypass if user explicitly passes --danger-direct-ip.
  // 3. BLUE_LICENSED: Proprietary commercial B2B data brokers.
  //    Default: Route via Firecrawl gateway (credits or enterprise key).

  let routeMode = 'GATEWAY';
  let decisionReason = '';

  if (forceGateway) {
    routeMode = 'GATEWAY';
    decisionReason = 'Manual override: --gateway flag specified by caller.';
  } else if (safetyTier === 'GREEN_SAFE') {
    if (NATIVE_ADAPTERS[providerId]) {
      routeMode = 'NATIVE_DIRECT';
      decisionReason = 'GREEN_SAFE: Sanctioned open API with legal open data mandate and zero bot defenses. Zero credits burned, instant native execution.';
    } else {
      routeMode = 'GATEWAY';
      decisionReason = 'GREEN_SAFE: Sanctioned open API, but no native local adapter written yet. Routing via Alexandria gateway.';
    }
  } else if (safetyTier === 'YELLOW_SHIELDED') {
    if (dangerDirectIp && NATIVE_ADAPTERS[providerId]) {
      routeMode = 'NATIVE_DIRECT';
      decisionReason = 'CAUTION: --danger-direct-ip forced direct execution. Residential IP exposed to commercial anti-bot tracking.';
    } else {
      routeMode = 'GATEWAY';
      decisionReason = 'YELLOW_SHIELDED: Protected commercial frontend (Cloudflare/DataDome/PerimeterX). Auto-routed through Firecrawl residential proxies to shield your home/office IP from blacklists and CAPTCHAs.';
    }
  } else if (safetyTier === 'BLUE_LICENSED') {
    routeMode = 'GATEWAY';
    decisionReason = 'BLUE_LICENSED: Proprietary commercial B2B broker. Routed through Alexandria gateway.';
  } else {
    // Fallback: If native adapter exists and no flags passed, try native adapter
    if (NATIVE_ADAPTERS[providerId]) {
      routeMode = 'NATIVE_DIRECT';
      decisionReason = 'Provider has native adapter available. Executing direct.';
    } else {
      routeMode = 'GATEWAY';
      decisionReason = 'Defaulting to Alexandria gateway.';
    }
  }

  // Execute Direct Native Adapter
  if (routeMode === 'NATIVE_DIRECT') {
    try {
      const adapterResult = await NATIVE_ADAPTERS[providerId].execute(capability, options);
      return {
        ...adapterResult,
        safetyTier,
        routeDecision: 'NATIVE_DIRECT',
        decisionReason
      };
    } catch (err) {
      console.warn(`[WARN] Native adapter failed (${err.message}). Falling back to Alexandria gateway...`);
      routeMode = 'GATEWAY';
      decisionReason = `Native adapter execution error (${err.message}). Safe fallback to Alexandria gateway.`;
    }
  }

  // Execute Alexandria Gateway via Firecrawl API
  const creds = getCredentials();
  if (!creds?.apiKey) {
    throw new Error('No Firecrawl API key available for gateway execution. Check FIRECRAWL_API_KEY or CLI credentials.');
  }

  const res = await fetch(`${creds.apiUrl || 'https://api.firecrawl.dev'}/v2/scrape`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${creds.apiKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      alexandria: {
        provider: providerId,
        capability: capability,
        options: options
      }
    })
  });

  if (!res.ok) {
    const errText = await res.text();
    throw new Error(`Alexandria Gateway error HTTP ${res.status}: ${errText}`);
  }

  const json = await res.json();
  return {
    source: 'firecrawl-alexandria-gateway',
    provider: providerId,
    capability: capability,
    safetyTier,
    routeDecision: 'FIRECRAWL_GATEWAY',
    decisionReason,
    creditsUsed: json?.data?.alexandria?.[0]?.creditsCost || 1,
    data: json?.data?.alexandria?.[0]?.data || json.data
  };
}

module.exports = {
  query,
  getProviderSafety,
  NATIVE_ADAPTERS
};
