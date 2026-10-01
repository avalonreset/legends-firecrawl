---
type: category
id: "skills"
title: "Skills"
providers_count: 1
---

# Category: Skills

> Website instructions and source files for agents and browser interactions.

Part of [[_Index|Legends Alexandria]] and the [[manifesto/The-Great-AI-Data-Arbitrage|Direct access and managed data]].

> Historical catalog snapshot. Provider descriptions and prices are cached discovery data, not verified native implementations. All native substitutions are retired; see [release scope](../../docs/RELEASE-SCOPE.md).

## Cataloged Providers (1)

| Provider | Capabilities | Data Tier | Execution route |
|---|---|---|---|
| `web-archive-org` (**Wayback Machine**) | 3 | Open Non-Profit, Legal & Community Ecosystems | Official Firecrawl; preview required |

## Tools & Capabilities

### Wayback Machine (`web-archive-org`)

Find archived website snapshots and read text from archived HTML pages.

- **`captures/content`** (Content): Retrieve readable static text and title from an exact archived HTML or plain-text capture. Use a timestamp from history. Reports the actual timestamp and URL after archive-only redirects. Does not execute JavaScript or load assets; maximum response 2 MiB. (Cost: 5 credit)
- **`captures/history`** (History): Oldest indexed snapshots (default 5, maximum 20), or the snapshot closest to midnight UTC on date YYYYMMDD; earlier wins ties. One page, not a domain crawl. Replay may redirect. (Cost: 5 credit)
- **`captures/oldest`** (Oldest): Find when a website first appeared in the Internet Archive, or get its oldest archived page. (Cost: 5 credit)


