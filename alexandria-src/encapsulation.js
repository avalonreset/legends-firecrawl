const fs = require('fs');
const path = require('path');

/**
 * Legends Alexandria: Data Encapsulation Engine
 * Adheres to Legends Empire Vault principles:
 * 1. Provenance & Raw Immutability (var/captures/)
 * 2. Synthesized Readable Knowledge Cards (vault/captures/)
 * 3. Provincial Routing (Work vs Money)
 * Zero em dashes (Unicode U+2014) enforced.
 */

function sanitizeSlug(str) {
  return (str || 'unknown').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
}

function determineProvince(providerId, capability) {
  const p = (providerId || '').toLowerCase();
  const c = (capability || '').toLowerCase();

  if (
    p.includes('treasury') ||
    p.includes('sec-gov') ||
    p.includes('fred') ||
    p.includes('yahoo') ||
    p.includes('benzinga') ||
    p.includes('fiscal') ||
    p.includes('imf') ||
    p.includes('worldbank') ||
    c.includes('debt') ||
    c.includes('quote') ||
    c.includes('filing') ||
    c.includes('balance') ||
    c.includes('spending')
  ) {
    return 'Money';
  }

  return 'Work';
}

function formatDataPreviewTable(data) {
  if (!data) return '*No data returned.*';

  if (Array.isArray(data) && data.length > 0 && typeof data[0] === 'object' && data[0] !== null) {
    const keys = Object.keys(data[0]).slice(0, 6);
    let md = '| ' + keys.join(' | ') + ' |\n';
    md += '| ' + keys.map(() => '---').join(' | ') + ' |\n';

    const rows = data.slice(0, 5);
    for (const r of rows) {
      md += '| ' + keys.map(k => {
        const val = r[k];
        if (val === null || val === undefined) return '';
        if (typeof val === 'object') return '[Object]';
        return String(val).replace(/\|/g, '\\|').slice(0, 40);
      }).join(' | ') + ' |\n';
    }

    if (data.length > 5) {
      md += `\n*Showing first 5 of ${data.length} records. See raw JSON for complete payload.*\n`;
    }
    return md;
  }

  if (typeof data === 'object') {
    const keys = Object.keys(data).slice(0, 10);
    let md = '| Field | Value |\n|---|---|\n';
    for (const k of keys) {
      const val = data[k];
      let display = '';
      if (val === null || val === undefined) display = 'null';
      else if (typeof val === 'object') display = Array.isArray(val) ? `[Array of ${val.length} items]` : '{Object}';
      else display = String(val).replace(/\|/g, '\\|').slice(0, 80);
      md += `| **${k}** | ${display} |\n`;
    }
    return md;
  }

  return '```text\n' + String(data).slice(0, 1000) + '\n```';
}

function encapsulate(queryResult, customBaseDir = null) {
  const baseDir = customBaseDir || path.resolve(__dirname, '..');
  const now = new Date();
  const dateStr = now.toISOString().slice(0, 10);
  const timeStr = now.toISOString().replace(/[:.]/g, '-');

  const providerSlug = sanitizeSlug(queryResult.provider);
  const capSlug = sanitizeSlug(queryResult.capability);
  const province = determineProvince(queryResult.provider, queryResult.capability);

  // 1. Raw Immutability: var/captures/<provider>/
  const rawDir = path.join(baseDir, 'var', 'captures', providerSlug);
  if (!fs.existsSync(rawDir)) {
    fs.mkdirSync(rawDir, { recursive: true });
  }

  const rawFileName = `${timeStr}_${capSlug}.raw.json`;
  const rawFilePath = path.join(rawDir, rawFileName);

  const rawPayload = {
    metadata: {
      timestamp: now.toISOString(),
      provider: queryResult.provider,
      capability: queryResult.capability,
      source: queryResult.source,
      routeDecision: queryResult.routeDecision || 'UNKNOWN',
      safetyTier: queryResult.safetyTier || 'UNKNOWN',
      creditsBurned: queryResult.creditsUsed || 0,
      decisionReason: queryResult.decisionReason || ''
    },
    data: queryResult.data
  };

  fs.writeFileSync(rawFilePath, JSON.stringify(rawPayload, null, 2), 'utf-8');

  // 2. Synthesized Knowledge Card: vault/captures/<provider>/
  const vaultCardDir = path.join(baseDir, 'vault', 'captures', providerSlug);
  if (!fs.existsSync(vaultCardDir)) {
    fs.mkdirSync(vaultCardDir, { recursive: true });
  }

  const cardFileName = `${dateStr}_${capSlug}.md`;
  const cardFilePath = path.join(vaultCardDir, cardFileName);

  const recordCount = Array.isArray(queryResult.data) 
    ? queryResult.data.length 
    : (queryResult.data && typeof queryResult.data === 'object' ? Object.keys(queryResult.data).length : 1);

  const previewTable = formatDataPreviewTable(queryResult.data);

  const mdContent = `---
type: data-capture
title: "${queryResult.provider} / ${queryResult.capability} Capture"
created: ${dateStr}
timestamp: "${now.toISOString()}"
provider: "${queryResult.provider}"
capability: "${queryResult.capability}"
safety_tier: "${queryResult.safetyTier || 'UNKNOWN'}"
route_decision: "${queryResult.routeDecision || 'UNKNOWN'}"
credits_burned: ${queryResult.creditsUsed || 0}
record_count: ${recordCount}
province: "${province}"
tags:
  - data-capture
  - alexandria
  - ${providerSlug}
  - ${province.toLowerCase()}
related:
  - "[[wiki/${province.toLowerCase()}/${province}]]"
  - "[[_Index]]"
---

# Data Capture: ${queryResult.provider} (${queryResult.capability})

Captured on **${now.toISOString()}** via **${queryResult.source}**.

## Capture Provenance

| Property | Value |
|---|---|
| **Provider** | \`${queryResult.provider}\` |
| **Capability** | \`${queryResult.capability}\` |
| **Safety Tier** | **${queryResult.safetyTier || 'UNKNOWN'}** |
| **Route Decision** | **${queryResult.routeDecision || 'UNKNOWN'}** |
| **Credits Burned** | **${queryResult.creditsUsed || 0}** |
| **Records** | ${recordCount} |
| **Primary Province** | [[wiki/${province.toLowerCase()}/${province}|${province}]] |
| **Immutable Raw** | \`${rawFilePath}\` |

### Router Rationale
> ${queryResult.decisionReason || 'Direct execution completed.'}

## Synthesized Data Preview

${previewTable}

## Integration & Use
- Re-querying this capability with identical parameters is unnecessary; data is preserved locally.
- Link to this card from research notes, client reports, or portfolio ledgers.
`;

  fs.writeFileSync(cardFilePath, mdContent, 'utf-8');

  return {
    rawFilePath,
    cardFilePath,
    province,
    recordCount
  };
}

module.exports = {
  encapsulate,
  determineProvince
};

