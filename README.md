# legends-firecrawl

Live web search, page scraping, URL discovery, bounded crawling, data cataloging, credit efficiency, and automated IP safety routing.

Legends Firecrawl is the unified super-module combining official Firecrawl web capabilities with **Legends Alexandria**, the offline data intelligence and credit efficiency engine.

## Agent setup (via `cto-legends`)

Part of the [CTO Legends](https://github.com/avalonreset/cto-legends) ecosystem. `cto-legends` is the only registered skill; this repo vendors a pinned copy at `skills/cto-legends/SKILL.md`.

Install with `cto-legends install legends-firecrawl`, then follow the module recipe the router loads. Do not register this module as its own skill.

---

## Why Legends Firecrawl

1. **Credit Protection & Efficiency**: Firecrawl markets Alexandria as a paid knowledge library for AI agents. Our forensic audit proved that **63.2% of the catalog (72 out of 114 providers) consists of completely free public data**. Legends Firecrawl auto-routes sanctioned government and open endpoints to direct native REST adapters, burning zero credits.
2. **Automated IP Safety Routing**: Protects residential and office IPs from bot bans. Sanctioned open APIs connect directly; commercial frontends with aggressive bot defenses (Zillow, Target, Skyscanner) automatically route through Firecrawl residential proxies.
3. **Bounded & Budget Safe**: Prevents unbounded token and credit exhaustion. Crawls require explicit preview confirmation; page limits and search caps are enforced before HTTP execution.
4. **Vault Encapsulation**: Captures raw API payloads locally and generates structured Obsidian research notes with citations.

---

## 3-Tier IP Safety & Routing Architecture

| Safety Tier | Providers | Characteristics | Router Action |
|---|---|---|---|
| **GREEN_SAFE** | 26 | Official government and international open APIs (US Treasury, SEC EDGAR, USAspending, FRED, CourtListener, World Bank). Legal open access mandate, zero bot defense. | **Auto-routes to Native Direct REST (0 Credits burned)** |
| **YELLOW_SHIELDED** | 32 | Commercial consumer frontends (Zillow, Skyscanner, Target, Amazon, SpotHero). Protected by Cloudflare, DataDome, Akamai. High ban risk on residential IPs. | **Auto-routes via Firecrawl Gateway (Residential proxies shield IP)** |
| **BLUE_LICENSED** | 56 | Proprietary commercial B2B data brokers (Apollo, Benzinga, Fiscal.ai, FullEnrich). Licensed commercial data. | **Auto-routes via Firecrawl Gateway (Paid credits or enterprise key)** |

---

## Quick Reference

### Core Web Operations

```powershell
# Account and credit balance
lfc credits

# Single clean page extraction (ad-blocked markdown)
lfc scrape https://example.com

# Site URL discovery
lfc map https://example.com --limit 100

# Web search without scraping results
lfc search "machine learning benchmarks 2026" --limit 5

# Preview a bounded crawl before spending credits
lfc crawl-preview https://example.com --limit 25 --max-depth 2

# Start reviewed crawl
lfc crawl https://example.com --limit 25 --max-depth 2 --confirm
```

### Alexandria Intelligence Engine

```powershell
# Catalog audit, breakdown, and bypass percentage
lax audit

# Instant offline tool search across all 797 capabilities (0 credits)
lax search "treasury"

# Inspect provider contracts and direct routing details
lax inspect treasury-fiscal-data

# Execute query with automated IP safety routing & vault encapsulation
lax query treasury-fiscal-data debt/to-the-penny

# Preserved captures inventory
lax captures
```

---

## Installation & Setup

```powershell
# 1. Install vendor CLI spine
npm install -g firecrawl-cli@1.23.3

# 2. Configure API key
pwsh -File bin/setup-auth.ps1

# 3. Verify system health
pwsh -File bin/doctor.ps1
```

---

## Multi-Agent Compatibility

Legends Firecrawl ships no per-module skill and requires no ambient MCP daemon. Agents discover and run it through the one registered `cto-legends` router skill (vendored at `skills/cto-legends/SKILL.md`): `cto-legends install legends-firecrawl` previews the install, then the `lfc` / `lax` launchers run intent-level jobs with JSON output.

---

## Verification & Self-Test

```powershell
# Run the 36-test offline contract suite
pytest tests -v

# Run the 12-scenario behavioral benchmark
python scripts/run_behavioral_evals.py

# Run the disposable live canary (costs 1 credit)
pwsh -File bin/canary.ps1 -Confirm
```

---

## License

MIT License. Copyright (c) 2026 Avalon Reset.
