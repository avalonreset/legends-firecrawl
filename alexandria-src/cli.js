#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const CATALOG_PATH = path.join(__dirname, '..', 'data', 'alexandria_catalog.json');
const AUDIT_PATH = path.join(__dirname, '..', 'data', 'refined_audit.json');
const SAFETY_AUDIT_PATH = path.join(__dirname, '..', 'data', 'safety_audit.json');

function getCatalog() {
  if (!fs.existsSync(CATALOG_PATH)) {
    console.error('Error: Alexandria catalog not found. Run extract_all.js first.');
    process.exit(1);
  }
  return JSON.parse(fs.readFileSync(CATALOG_PATH, 'utf-8'));
}

function getAudit() {
  if (!fs.existsSync(AUDIT_PATH)) {
    return null;
  }
  return JSON.parse(fs.readFileSync(AUDIT_PATH, 'utf-8'));
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

const args = process.argv.slice(2);
const command = args[0] || 'help';

switch (command) {
  case 'audit':
  case 'stats': {
    const audit = getAudit();
    if (!audit) {
      console.log('Run refine_audit.js to generate audit data.');
      break;
    }
    console.log('\n======================================================');
    console.log('       Legends Alexandria: CATALOG AUDIT');
    console.log('======================================================');
    console.log(`Total Providers:            ${audit.totalProviders}`);
    console.log(`Total Capabilities (Tools): ${audit.totalCapabilities}`);
    console.log(`Free / Public Providers:    ${audit.freeOrPublicProviders} (${audit.freeOrPublicPercent})`);
    console.log('\nBreakdown by Tier:');
    for (const [tier, count] of Object.entries(audit.tierCounts)) {
      const pct = ((count / audit.totalProviders) * 100).toFixed(1);
      console.log(`  - ${tier.padEnd(46)}: ${count} (${pct}%)`);
    }
    console.log('\nIP Safety & Proxy Shielding Breakdown:');
    console.log('  • \x1b[32mGREEN_SAFE (Official Open APIs)\x1b[0m     : 26 providers (Direct connection safe at scale)');
    console.log('  • \x1b[33mYELLOW_SHIELDED (Scraped Frontends)\x1b[0m : 32 providers (High IP ban risk; use Firecrawl proxies)');
    console.log('  • \x1b[34mBLUE_LICENSED (Proprietary B2B)\x1b[0m    : 56 providers (Requires credits or partner key)');
    console.log('======================================================\n');
    break;
  }

  case 'providers':
  case 'list': {
    const catalog = getCatalog();
    const audit = getAudit();
    const filterTier = args[1]?.toLowerCase();

    console.log(`\nCatalog Providers (${catalog.providers.length}):\n`);
    for (const p of catalog.providers) {
      const auditEntry = audit?.providers?.find(ap => ap.id === p.id);
      const tier = auditEntry?.classification?.tier || 'Unclassified';
      const cost = auditEntry?.classification?.cost || 'Credits';

      if (filterTier && !tier.toLowerCase().includes(filterTier)) {
        continue;
      }

      console.log(`• \x1b[36m${p.id.padEnd(28)}\x1b[0m | ${(p.tools?.length || 0).toString().padStart(2)} tools | \x1b[32m${cost.padEnd(16)}\x1b[0m | ${p.name}`);
    }
    console.log('');
    break;
  }

  case 'search': {
    const term = args[1]?.toLowerCase();
    if (!term) {
      console.log('Usage: lax search <query>');
      process.exit(1);
    }
    const catalog = getCatalog();
    const audit = getAudit();
    console.log(`\nSearching catalog for "${term}"...\n`);

    let matchCount = 0;
    for (const p of catalog.providers) {
      const auditEntry = audit?.providers?.find(ap => ap.id === p.id);
      const pMatch = p.id.includes(term) || (p.name || '').toLowerCase().includes(term) || (p.description || '').toLowerCase().includes(term);
      const matchingTools = (p.tools || []).filter(t => 
        t.capability.includes(term) || (t.name || '').toLowerCase().includes(term) || (t.description || '').toLowerCase().includes(term)
      );

      if (pMatch || matchingTools.length > 0) {
        matchCount++;
        const cost = auditEntry?.classification?.cost || 'Credits';
        console.log(`\x1b[33m[Provider]\x1b[0m \x1b[1m${p.name}\x1b[0m (\x1b[36m${p.id}\x1b[0m) - \x1b[32m${cost}\x1b[0m`);
        console.log(`  Description: ${p.description || 'N/A'}`);
        if (matchingTools.length > 0) {
          console.log(`  Matching Capabilities (${matchingTools.length}):`);
          for (const t of matchingTools) {
            console.log(`    - \x1b[35m${t.capability}\x1b[0m: ${t.name} (${t.creditsCost} credit)`);
          }
        }
        console.log('');
      }
    }
    console.log(`Found ${matchCount} matching providers.\n`);
    break;
  }

  case 'inspect': {
    const providerId = args[1];
    if (!providerId) {
      console.log('Usage: lax inspect <provider-id>');
      process.exit(1);
    }
    const catalog = getCatalog();
    const p = catalog.providers.find(x => x.id === providerId);
    if (!p) {
      console.error(`Provider "${providerId}" not found in catalog.`);
      process.exit(1);
    }
    const audit = getAudit();
    let safetyEntry = null;
    if (fs.existsSync(SAFETY_AUDIT_PATH)) {
      try {
        const sAudit = JSON.parse(fs.readFileSync(SAFETY_AUDIT_PATH, 'utf-8'));
        safetyEntry = sAudit.providers.find(x => x.id === p.id);
      } catch {}
    }
    const auditEntry = audit?.providers?.find(ap => ap.id === p.id);

    console.log('\n======================================================');
    console.log(`Provider:        ${p.name} (${p.id})`);
    console.log(`Tier:            ${auditEntry?.classification?.tier || 'Standard'}`);
    console.log(`Cost:            ${auditEntry?.classification?.cost || 'Standard'}`);
    console.log(`IP Safety:       ${safetyEntry?.ipSafety || 'STANDARD'}`);
    console.log(`IP Risk Factor:  ${safetyEntry?.ipRisk || 'Check host terms before high-volume requests'}`);
    console.log(`Recommended:     ${safetyEntry?.recommendedRoute || auditEntry?.classification?.bypassPossibility || 'Alexandria'}`);
    console.log(`Description:     ${p.description || 'N/A'}`);
    console.log(`Capabilities (${p.tools?.length || 0}):`);
    console.log('======================================================');

    for (const t of (p.tools || [])) {
      console.log(`\n• \x1b[36m${t.capability}\x1b[0m (\x1b[32m${t.name}\x1b[0m)`);
      console.log(`  Credits Cost: ${t.creditsCost || 1} credit`);
      console.log(`  Description:  ${t.description || 'N/A'}`);
    }
    console.log('\n');
    break;
  }

  case 'query': {
    const providerId = args[1];
    const capability = args[2];
    const forceGateway = args.includes('--gateway');
    const dangerDirectIp = args.includes('--danger-direct-ip');
    const noSave = args.includes('--no-save');
    
    let options = {};
    const optIdx = args.indexOf('--options');
    if (optIdx !== -1 && args[optIdx + 1]) {
      try {
        options = JSON.parse(args[optIdx + 1]);
      } catch (e) {
        console.error('Invalid JSON passed to --options:', e.message);
        process.exit(1);
      }
    }

    if (!providerId || !capability) {
      console.log('Usage: lax query <provider-id> <capability> [--gateway] [--danger-direct-ip] [--no-save] [--options \'{"key":"val"}\']');
      process.exit(1);
    }

    const { query } = require('./router');
    console.log(`\nEvaluating route for ${providerId} / ${capability}...`);

    query(providerId, capability, options, { gateway: forceGateway, dangerDirectIp })
      .then(res => {
        console.log('\n======================================================');
        console.log(`  ROUTER DECISION: \x1b[1m${res.routeDecision}\x1b[0m (Safety Tier: \x1b[36m${res.safetyTier}\x1b[0m)`);
        console.log('======================================================');
        console.log(`Rationale:       ${res.decisionReason}`);
        console.log(`Execution Path:  \x1b[32m${res.source}\x1b[0m`);
        console.log(`Credits Burned:  \x1b[33m${res.creditsUsed}\x1b[0m`);

        // Encapsulation under Empire Vault principles
        if (!noSave) {
          const { encapsulate } = require('./encapsulation');
          const capInfo = encapsulate(res);
          console.log(`Raw Capture:     \x1b[32m${capInfo.rawFilePath}\x1b[0m`);
          console.log(`Vault Card:      \x1b[36m${capInfo.cardFilePath}\x1b[0m (Province: ${capInfo.province})`);
        }

        console.log('======================================================\n');
        console.log('Data Preview:');
        console.log(JSON.stringify(res.data, null, 2).slice(0, 1500));
        console.log('\n');
      })
      .catch(err => {
        console.error(`\x1b[31m[ERROR]\x1b[0m ${err.message}`);
        process.exit(1);
      });
    break;
  }

  case 'captures': {
    const capturesDir = path.join(__dirname, '..', 'var', 'captures');
    if (!fs.existsSync(capturesDir)) {
      console.log('No captures archived yet. Run `lax query <provider> <capability>` to capture data.');
      break;
    }

    console.log('\n======================================================');
    console.log('       Legends Alexandria: ARCHIVED CAPTURES');
    console.log('======================================================\n');

    const providers = fs.readdirSync(capturesDir).filter(f => fs.statSync(path.join(capturesDir, f)).isDirectory());
    let totalCaptures = 0;

    for (const p of providers) {
      const pDir = path.join(capturesDir, p);
      const files = fs.readdirSync(pDir).filter(f => f.endsWith('.raw.json'));
      totalCaptures += files.length;
      console.log(`• \x1b[36m${p}\x1b[0m (${files.length} captures)`);
      for (const f of files.slice(-3)) {
        try {
          const raw = JSON.parse(fs.readFileSync(path.join(pDir, f), 'utf-8'));
          const ts = raw.metadata?.timestamp?.slice(0, 19).replace('T', ' ') || f;
          const credits = raw.metadata?.creditsBurned || 0;
          console.log(`    - ${ts} | \x1b[33m${credits} creds\x1b[0m | \x1b[35m${raw.metadata?.capability || 'cap'}\x1b[0m`);
        } catch {
          console.log(`    - ${f}`);
        }
      }
    }

    console.log(`\nTotal Captures Preserved: ${totalCaptures}\n`);
    break;
  }

  case 'help':
  default: {
    console.log(`
Legends Alexandria (lax) - Strategic Data Catalog, Credit Circumvention & Vault Encapsulation

Commands:
  lax audit                             Display catalog breakdown, tiers, and free percentage
  lax providers [tier]                  List catalog providers (optionally filtered by tier)
  lax search <keyword>                  Search providers and capabilities offline
  lax inspect <provider-id>             Inspect detailed tool contracts and direct route
  lax query <provider> <tool> [flags]   Execute query with automated IP safety routing & vault encapsulation
  lax captures                          List all archived raw captures and knowledge cards

Query Flags:
  --gateway           Force routing through Firecrawl Alexandria Gateway
  --danger-direct-ip  Bypass Firecrawl proxy shielding on commercial frontends (Risks IP bans)
  --no-save           Skip automatic vault and raw data encapsulation
  --options <json>    Pass JSON payload parameters to the capability
    `);
    break;
  }
}

