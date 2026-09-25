# Product plan

## Outcome

Create a Tier-2 Legends Kit that gives Grok, Codex, Claude, Gemini, and house
products a predictable Firecrawl capability without an ambient MCP server.

## Users and jobs

- Agents: discover and run live-web collection through one skill and launcher.
- Legends Packet: call a shared Python client for page and site evidence.
- Benjamin/Katherine: inspect bounded scope and credit state before broad jobs.

## Architecture

1. Official `firecrawl` CLI is the vendor spine and stays pinned.
2. `bin/lfc.ps1` is the house launcher with stable JSON and policy gates.
3. `python/legends_firecrawl` is a small direct-API compatibility layer.
4. `skills/cto-legends` (pinned router copy) is the multi-agent discovery surface.
5. `var/usage-ledger.jsonl` is local runtime evidence, never a secret store.

## Initial first-class jobs

- credit usage
- one-page scrape
- website URL map
- bounded web search
- previewed/confirmed crawl and status
- route discovery, scope estimate, and usage summary

Advanced Firecrawl agent, interact, monitor, parse, and browser jobs remain
vendor escape-hatch territory until a real house workflow justifies a policy
recipe. This avoids a 1:1 endpoint dump.

