---
type: bypass-guide
title: "CourtListener Legal Decisions & Dockets Direct Bypass"
provider: "courtlistener-com"
tier: "Tier 2: Open Non-Profit & Academic"
cost: "0 Credits ($0.00)"
---

# CourtListener Legal Decisions & Dockets Direct Bypass

- **Provider ID:** `courtlistener-com`
- **Data Tier:** Tier 2: Open Non-Profit & Academic
- **Official Base URL:** `https://www.courtlistener.com/api/rest/v4/`
- **Alexandria Cost:** 1 to 5 Credits | **Native Bypass Cost:** **0 Credits ($0.00)**

## Rationale & Arbitrage Proof

CourtListener is maintained by the non-profit Free Law Project, providing millions of legal opinions, federal court dockets, oral arguments, and judicial profiles via an open REST API.

## Supported Endpoints & Capabilities

| Capability | Official Endpoint | Parameters | Description |
|---|---|---|---|
| **Opinion Search** | `search/?q={query}&type=o` | `q=keyword, order_by=score desc` | Search federal and state legal opinions with full text, citations, and download links. |
| **Docket Search** | `dockets/` | `court=dcd, docket_number=...` | Search federal district, appellate, and bankruptcy court dockets. |
| **Courts Directory** | `courts/` | `None` | Directory of all federal and state court jurisdictions and metadata. |

## Direct cURL Execution (0 Credits)

```bash
curl -s "https://www.courtlistener.com/api/rest/v4/search/?q=artificial+intelligence&type=o" | jq .results[0]
```

## CLI Execution via `legends-firecrawl`

```powershell
pwsh -File E:\legends-firecrawl\bin\lax.ps1 query courtlistener-com opinions
```

