---
name: legends-firecrawl
description: >
  Legends Firecrawl is the unified ultimate super-module for live web search, page scraping, URL discovery, bounded crawling, data cataloging, credit efficiency, and IP safety routing. It combines all core Firecrawl operations with Legends Alexandria, the internal intelligence engine. Use when the user wants to search the web, scrape, map, crawl, or run Alexandria commands. Run doctor first.
---

# Legends Firecrawl

**Disk:** E:\legends-firecrawl  
**House launcher:** pwsh -File E:\legends-firecrawl\bin\lfc.ps1 and pwsh -File E:\legends-firecrawl\bin\lax.ps1
**Vendor spine:** official firecrawl CLI 1.23.3 + native REST adapters

## Hard gate

```powershell
pwsh -File E:\legends-firecrawl\bin\doctor.ps1
```

If doctor fails, use its exact remediation. Do not install or fall back to
Firecrawl MCP. A missing API key requires the one-time path in `docs/AUTH.md`.

## Quick reference

| Intent | Command |
|---|---|
| Account and credits | `lfc.ps1 credits` |
| One clean page | `lfc.ps1 scrape <url>` |
| Discover site URLs | `lfc.ps1 map <url> --limit 100` |
| Search the web | `lfc.ps1 search "<query>" --limit 5` |
| Preview a site crawl | `lfc.ps1 crawl-preview <url> --limit 25 --max-depth 2` |
| Start reviewed crawl | `lfc.ps1 crawl <url> --limit 25 --max-depth 2 --confirm` |
| Check crawl | `lfc.ps1 crawl-status <job-id>` |
| Route inventory | `lfc.ps1 routes` / `lfc.ps1 route <intent>` |
| Scope estimate | `lfc.ps1 estimate <intent> --limit N` |
| Usage ledger | `lfc.ps1 cost` |
| Alexandria Catalog Audit | `lax.ps1 audit` |
| Search Alexandria Tools | `lax.ps1 search "<query>"` |
| Inspect Provider Contract | `lax.ps1 inspect <provider-id>` |
| Query Tool / Safe Route | `lax.ps1 query <provider> <tool>` |
| Preserved Captures Inventory | `lax.ps1 captures` |
| Vendor escape hatch | `lfc.ps1 vendor <safe firecrawl args>` |

## Routing

1. Need one known page: `scrape`.
2. Need to learn which pages exist: `map`, optionally with `--search`.
3. Need sources outside a known domain: `search`; do not scrape results by
   default.
4. Need multiple pages from one site: `crawl-preview`; show the bounded plan;
   start only after explicit confirmation.
5. Need Firecrawl inside Python: import `legends_firecrawl.packet_compat` or
   `FirecrawlClient`; do not shell an MCP server.
6. Need an unsupported advanced feature: use `vendor` only after checking the
   current official CLI. The house wrapper blocks vendor integration installers.

## Quality and safety

- Public HTTP(S) only. Reject localhost, private IPs, credential-bearing URLs,
  and non-web schemes before HTTP.
- Scrape defaults to Markdown, main content, clean content, ad blocking, and a
  24-hour maximum cache age.
- Search is capped at 20 house results and does not scrape results unless asked.
- Map is capped at 1,000 URLs and excludes subdomains by default.
- Crawl is capped at 100 pages and depth 5; ordinary defaults are 25 and 2.
- Never claim an exact dollar cost from a local guess. Use `credits`, bounded
  scope, and the provider-reported ledger.
- Never print `FIRECRAWL_API_KEY` or pass it as a command argument.
- Never use Firecrawl to bypass authentication, CAPTCHA, robots policy, or
  access controls.

## References

- Load `docs/RECIPES.md` for daily jobs.
- Load `docs/AUTH.md` for first-run authentication.
- Load `docs/OPERATION-MAP.md` for capability boundaries.
- Load `docs/PYTHON.md` for Packet/programmatic use.
- Load `docs/VERIFY.md` for qualification and canary commands.
- Load `docs/MCP-TO-CLI.md` only when replacing an old MCP-shaped workflow.



