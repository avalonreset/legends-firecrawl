---
name: legends-firecrawl
description: |
  Strategic data catalog, zero-credit circumvention engine, automated IP safety router,
  and vault encapsulation system for Firecrawl Alexandria. Provides instant offline discovery
  across 114 providers and 797 capabilities, with direct native bypass routes for 63.2%
  of catalog endpoints that are taxpayer-funded government APIs or open databases.
---

# Legends Alexandria Skill

Use this skill when you need structured external data (financial macro indicators, corporate SEC filings, federal procurement awards, legal cases, sports, package registries, commercial product details, or local places).

## Why This Skill Exists

Firecrawl sells access to Alexandria for vendor metering credits. However, empirical analysis proves:
- **63.2% of Alexandria (72 of 114 providers) is free public information.**
- Official government APIs (US Treasury, SEC EDGAR, USAspending, USPTO, World Bank, IMF) require zero authentication and zero credits.
- Firecrawl wraps these exact APIs, preserves identical parameter names, and bills credits for them.

This skill provides an **automated IP safety routing engine and markdown-driven alternative to MCP**:
1. **Automated Safety Routing**: The router decides on behalf of the user. Open government APIs (GREEN_SAFE) auto-route directly to native zero-credit REST endpoints. Commercial frontends (YELLOW_SHIELDED like Zillow or Target) auto-route through Firecrawl residential proxies to shield home and office IPs from bot blacklisting, CAPTCHAs, and bans.
2. **Instant Offline Discovery**: Search all 797 capabilities offline in under 5 milliseconds with zero credit cost and zero token bloat.
3. **Vault Encapsulation**: Every query result is automatically archived under Empire Vault principles: immutable raw JSON in `var/captures/` and synthesized Markdown knowledge cards in `vault/captures/` linked to Work or Money provinces.

---

## Architecture: Why Markdown Beats MCP for Agents

Firecrawl's MCP server (`https://mcp.firecrawl.dev/v2/mcp`) exposes only 3 generic RPC tools (`firecrawl_scrape`, `firecrawl_search`, `firecrawl_parse`). To query an Alexandria capability via MCP, an agent must take 2 to 3 sequential LLM round-trips:
1. Call `firecrawl_search` to find tools.
2. Call `firecrawl_scrape` or an internal command to inspect the schema.
3. Call `firecrawl_scrape` with the full JSON payload.

With `legends-firecrawl`, an agent:
- Reads the markdown card for the target category or provider in `references/`.
- Immediately obtains the endpoint URL, query parameters, and cURL / PowerShell command.
- Queries the public endpoint directly for **$0.00 / 0 credits**, with **zero extra LLM hops**.

For the complete technical breakdown, see:
- [MCP Dissection and Architectural Analysis](references/mcp-dissection.md)
- [Providers Directory (All 114 Providers)](references/providers-index.md)

---

## The 21 Alexandria Categories

Every provider in Alexandria belongs to one of 21 verified categories. Each category has its own reference card in `references/categories/`:

| Category | Providers | Reference Card |
|---|---|---|
| **ai-models** | 2 | [ai-models.md](references/categories/ai-models.md) |
| **apps** | 3 | [apps.md](references/categories/apps.md) |
| **companies** | 25 | [companies.md](references/categories/companies.md) |
| **developer** | 1 | [developer.md](references/categories/developer.md) |
| **finance** | 17 | [finance.md](references/categories/finance.md) |
| **government** | 32 | [government.md](references/categories/government.md) |
| **health** | 1 | [health.md](references/categories/health.md) |
| **jobs** | 7 | [jobs.md](references/categories/jobs.md) |
| **news** | 4 | [news.md](references/categories/news.md) |
| **people** | 4 | [people.md](references/categories/people.md) |
| **places** | 18 | [places.md](references/categories/places.md) |
| **podcasts** | 1 | [podcasts.md](references/categories/podcasts.md) |
| **real-estate** | 3 | [real-estate.md](references/categories/real-estate.md) |
| **research** | 1 | [research.md](references/categories/research.md) |
| **restaurants** | 6 | [restaurants.md](references/categories/restaurants.md) |
| **shopping** | 20 | [shopping.md](references/categories/shopping.md) |
| **skills** | 1 | [skills.md](references/categories/skills.md) |
| **social** | 2 | [social.md](references/categories/social.md) |
| **software** | 1 | [software.md](references/categories/software.md) |
| **sports** | 3 | [sports.md](references/categories/sports.md) |
| **travel** | 15 | [travel.md](references/categories/travel.md) |

---

## Direct Public API Roster (Top 8 Zero-Credit Targets)

Detailed reference cards for the top circumvention targets are located in `references/bypasses/`:

1. **US Treasury Fiscal Data (`treasury-fiscal-data` - 12 tools)**
   - [US Treasury Bypass Guide](references/bypasses/us-treasury.md)
   - Official API: `https://api.fiscaldata.treasury.gov/services/api/fiscal_service/`
   - Cost: $0.00 / 0 credits.
2. **SEC EDGAR Corporate Filings (`sec-gov` - 7 tools)**
   - [SEC EDGAR Bypass Guide](references/bypasses/sec-edgar.md)
   - Official API: `https://data.sec.gov/`
   - Cost: $0.00 / 0 credits.
3. **USAspending Federal Procurement (`usaspending-gov` - 7 tools)**
   - [USAspending Bypass Guide](references/bypasses/usaspending.md)
   - Official API: `https://api.usaspending.gov/api/v2/`
   - Cost: $0.00 / 0 credits.
4. **CourtListener Case Law & Dockets (`courtlistener-com` - 4 tools)**
   - [CourtListener Bypass Guide](references/bypasses/courtlistener.md)
   - Official API: `https://www.courtlistener.com/api/rest/v4/`
   - Cost: $0.00 / 0 credits.
5. **ESPN Sports Scores & Rosters (`espn-com` - 10 tools)**
   - [ESPN Sports Bypass Guide](references/bypasses/espn.md)
   - Official API: `https://site.api.espn.com/apis/site/v2/sports/`
   - Cost: $0.00 / 0 credits.
6. **Yahoo Finance Market Rates (`finance-yahoo-com` - 4 tools)**
   - [Yahoo Finance Bypass Guide](references/bypasses/yahoo-finance.md)
   - Official API: `https://query1.finance.yahoo.com/v8/finance/chart/`
   - Cost: $0.00 / 0 credits.
7. **Wayback Machine Historical Captures (`web-archive-org` - 3 tools)**
   - [Wayback Machine Bypass Guide](references/bypasses/wayback-machine.md)
   - Official API: `https://archive.org/wayback/available`
   - Cost: $0.00 / 0 credits.
8. **Y Combinator & Hacker News Ecosystem (`ycombinator-com` - 4 tools)**
   - Public Algolia Search API for YC companies and tech discussions.
   - Cost: $0.00 / 0 credits.

---

## CLI Usage (`bin/lax.ps1` / `bin/lax.cmd`)

From PowerShell or any terminal:

### 1. Offline Search (Zero Network, Zero Credits)
```powershell
pwsh -File E:\legends-firecrawl\bin\lax.ps1 search "treasury"
pwsh -File E:\legends-firecrawl\bin\lax.ps1 search "filings"
pwsh -File E:\legends-firecrawl\bin\lax.ps1 search "scores"
```

### 2. Inspect Provider Contract & Safety Tier
```powershell
pwsh -File E:\legends-firecrawl\bin\lax.ps1 inspect treasury-fiscal-data
pwsh -File E:\legends-firecrawl\bin\lax.ps1 inspect zillow-com
pwsh -File E:\legends-firecrawl\bin\lax.ps1 inspect sec-gov
```

### 3. Execute Query (With Automated Safety & Vault Encapsulation)
```powershell
# Direct zero-credit open government execution (auto-encapsulated into vault)
pwsh -File E:\legends-firecrawl\bin\lax.ps1 query treasury-fiscal-data debt/to-the-penny
pwsh -File E:\legends-firecrawl\bin\lax.ps1 query sec-gov filings/company --options '{"cik":"0000320193"}'
pwsh -File E:\legends-firecrawl\bin\lax.ps1 query usaspending-gov agencies/agency --options '{"toptier_code":"012"}'

# Commercial frontend execution (automatically routed through Firecrawl residential proxies)
pwsh -File E:\legends-firecrawl\bin\lax.ps1 query zillow-com properties/locations --options '{"query":"Miami"}'
pwsh -File E:\legends-firecrawl\bin\lax.ps1 query skyscanner-net flights/search --options '{"origin":"JFK"}'

# Force direct connection or bypass encapsulation
pwsh -File E:\legends-firecrawl\bin\lax.ps1 query <provider> <tool> --danger-direct-ip
pwsh -File E:\legends-firecrawl\bin\lax.ps1 query <provider> <tool> --no-save
```

### 4. Review Preserved Captures
```powershell
pwsh -File E:\legends-firecrawl\bin\lax.ps1 captures
```

---

## Obsidian Knowledge Vault Integration

The knowledge base in `E:\legends-firecrawl\vault\` adheres to the Legends Obsidian Wiki standard and slots seamlessly into `E:\empire`:
- `vault/_Index.md` & `vault/index.md`: Master table of contents and MOC.
- `vault/hot.md`: Short current-context cache (under 500 words).
- `vault/log.md`: Chronological structural changelog.
- `vault/captures/`: Auto-generated synthesized research cards.
- `vault/manifesto/The-Great-AI-Data-Arbitrage.md`: Full empirical manifesto.
- `vault/manifesto/IP-Risk-And-Proxy-Shielding.md`: Proxy defense doctrine.
- `vault/tiers/`: Tiers 1 through 4 architectural notes.
- `vault/categories/`: 21 Obsidian-linked category files.
- `vault/bypasses/`: Production circumvention guides for the top public APIs.

