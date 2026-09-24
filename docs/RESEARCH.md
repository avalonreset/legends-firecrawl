# Research gate

Verified 2026-08-30 against current official Firecrawl documentation and CLI.

| Surface | Finding |
|---|---|
| Official CLI | `firecrawl-cli` exists and is current; installed/pinned at `1.23.3` on NERV. Machine-readable flags exist for primary commands. |
| Community CLI | Not selected; no need to trust a second implementation. |
| Official API | Hosted HTTPS API v2 with Bearer API key. Current endpoints include search, scrape, map, crawl, account credit usage, and more. |
| Auth | Human-created Firecrawl account and API key; Kit reads `FIRECRAWL_API_KEY`. Secret values never enter repo or receipts. |
| MCP | Vendor offers MCP, but it is excluded from the Empire runtime by Benjamin's direction and house CLI-first doctrine. |
| Spine choice | Official CLI first; thin house launcher and stdlib API compatibility module for stable policy and product consumers. |
| Upgrade | Review current CLI/docs, deliberately change the pin in installer/runtime/docs, then doctor, tests, package, and canary. |

## Important current API facts

- Scrape is `POST /v2/scrape` and can return Markdown and other formats.
- Map is `POST /v2/map` and supports URL limits, sitemap modes, search, and
  subdomain/query-parameter controls.
- Search is `POST /v2/search`; result scraping is optional and increases scope.
- Crawl is asynchronous and returns a job id; it is the broadest initial route.
- Account credit usage is `GET /v2/team/credit-usage` and is the doctor live probe.
- Billing changes across endpoints and features, so the Kit does not freeze
  guessed dollar prices into code.
