---
category: "skills"
type: reference-card
provider_count: 1
---

# Category: skills

> Website instructions and source files for agents and browser interactions.

**Providers in this category:** 1

| Provider ID | Provider Name | Capabilities | Tier | Cost | Bypass Route |
|---|---|---|---|---|---|
| `web-archive-org` | **Wayback Machine** | 3 | Open Non-Profit, Legal & Community Ecosystems | 0 Credits (Public API) | Direct community/non-profit REST API |

## Capabilities Overview

### Wayback Machine (`web-archive-org`)

Find archived website snapshots and read text from archived HTML pages.

- **`captures/content`** (Content): Retrieve readable static text and title from an exact archived HTML or plain-text capture. Use a timestamp from history. Reports the actual timestamp and URL after archive-only redirects. Does not execute JavaScript or load assets; maximum response 2 MiB. [Cost: 5 credit]  
  *Options:* `timestamp` *(required)*, `url` *(required)*
- **`captures/history`** (History): Oldest indexed snapshots (default 5, maximum 20), or the snapshot closest to midnight UTC on date YYYYMMDD; earlier wins ties. One page, not a domain crawl. Replay may redirect. [Cost: 5 credit]  
  *Options:* `date`, `limit`, `url` *(required)*
- **`captures/oldest`** (Oldest): Find when a website first appeared in the Internet Archive, or get its oldest archived page. [Cost: 5 credit]  
  *Options:* `url` *(required)*

