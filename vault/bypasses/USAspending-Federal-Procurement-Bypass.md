---
type: bypass-guide
title: "USAspending Federal Procurement Direct Bypass"
provider: "usaspending-gov"
tier: "Tier 1: Public Government Data"
cost: "0 Credits ($0.00)"
---

# USAspending Federal Procurement Direct Bypass

- **Provider ID:** `usaspending-gov`
- **Data Tier:** Tier 1: Public Government Data
- **Official Base URL:** `https://api.usaspending.gov/api/v2/`
- **Alexandria Cost:** 1 to 5 Credits | **Native Bypass Cost:** **0 Credits ($0.00)**

## Rationale & Arbitrage Proof

USAspending.gov is the official open data source for federal spending information mandated by the DATA Act. It offers a completely open REST API covering prime contract awards, subawards, agency outlays, and recipient tracking.

## Supported Endpoints & Capabilities

| Capability | Official Endpoint | Parameters | Description |
|---|---|---|---|
| **Agency Outlays & Profile** | `agency/{toptier_code}/` | `e.g. 012 for USDA, 097 for DoD` | Agency budget authority, gross outlays, obligations, and subtier agency counts. |
| **Top-tier Agencies Reference** | `references/toptier_agencies/` | `None` | Directory of all 111 federal executive and independent agencies. |
| **Spending by Award Search** | `search/spending_by_award/` | `POST JSON with award filters` | Search prime awards by keyword, NAICS code, PSC code, date range, or recipient. |

## Direct cURL Execution (0 Credits)

```bash
curl -s "https://api.usaspending.gov/api/v2/agency/012/" | jq .
```

## CLI Execution via `legends-firecrawl`

```powershell
pwsh -File E:\legends-firecrawl\bin\lax.ps1 query usaspending-gov agency
```

