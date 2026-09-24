---
type: bypass-guide
title: "Internet Archive Wayback Machine Direct Bypass"
provider: "web-archive-org"
tier: "Tier 2: Open Non-Profit & Academic"
cost: "0 Credits ($0.00)"
---

# Internet Archive Wayback Machine Direct Bypass

- **Provider ID:** `web-archive-org`
- **Data Tier:** Tier 2: Open Non-Profit & Academic
- **Official Base URL:** `https://archive.org/wayback/available`
- **Alexandria Cost:** 1 to 5 Credits | **Native Bypass Cost:** **0 Credits ($0.00)**

## Rationale & Arbitrage Proof

The Internet Archive Wayback Machine offers open availability and capture APIs to look up historical snapshots of any public web page without authentication or credits.

## Supported Endpoints & Capabilities

| Capability | Official Endpoint | Parameters | Description |
|---|---|---|---|
| **Available Snapshot Check** | `wayback/available` | `url={target_url}&timestamp={optional_date}` | Find the closest snapshot timestamp and permanent playback URL for any target website. |
| **Raw Capture Content** | `https://web.archive.org/web/{timestamp}id_/{url}` | `timestamp, url` | Retrieve the unmodified raw HTML capture without Wayback toolbar injection. |

## Direct cURL Execution (0 Credits)

```bash
curl -s "https://archive.org/wayback/available?url=google.com" | jq .archived_snapshots.closest
```

## CLI Execution via `legends-firecrawl`

```powershell
pwsh -File E:\legends-firecrawl\bin\lax.ps1 query web-archive-org oldest
```

