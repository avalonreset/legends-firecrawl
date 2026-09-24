---
type: hot-cache
title: "Legends Alexandria Hot Cache"
status: living
created: 2026-09-24
updated: 2026-09-24
tags: [hot-cache, alexandria, firecrawl, routing]
---

# Legends Alexandria Hot Cache

Current status: **0.1.0 Operational** · 114 providers · 797 capabilities · 21 categories · automated IP safety routing live.

## Quick Routing Policy

The router automatically makes the safety decision for the user:

1. **GREEN_SAFE (26 Providers):** Sanctioned public government and international open APIs (US Treasury, SEC EDGAR, USAspending, FRED, CourtListener, World Bank). Legal open data mandate with zero bot mitigation. Auto-routes to direct native adapter (0 credits burned).
2. **YELLOW_SHIELDED (32 Providers):** Commercial consumer frontends (Zillow, Skyscanner, Target, Amazon, SpotHero). Protected by Cloudflare, DataDome, Akamai, or PerimeterX. Auto-routes through Firecrawl residential proxies to shield residential and office IPs from blacklisting and CAPTCHAs.
3. **BLUE_LICENSED (56 Providers):** Proprietary commercial B2B data brokers (Apollo, Benzinga, Fiscal.ai). Requires Firecrawl credits or enterprise keys.

## Quick CLI Reference

```powershell
lax audit                             # Catalog tiers and free percentage
lax search <keyword>                  # Offline instant tool discovery
lax inspect <provider>                # Tool contracts, pricing, and safety tier
lax query treasury-fiscal-data debt/to-the-penny  # 0-credit direct execution
lax query zillow-com properties/locations --options '{"query":"Miami"}'  # Proxy-shielded
```

## Hot State

- Local catalog cached at `data/alexandria_catalog.json`.
- Credentials live in your local environment and the Firecrawl CLI credential store; never commit them.
- Check your current credit balance in the Firecrawl dashboard before large runs.
- Empire shelf: file this module under your Empire vault library when you adopt it.

