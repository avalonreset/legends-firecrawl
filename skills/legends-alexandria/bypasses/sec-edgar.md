---
type: bypass-guide
title: "SEC EDGAR Corporate Filings Direct Bypass"
provider: "sec-gov"
tier: "Tier 1: Public Government Data"
cost: "0 Credits ($0.00)"
---

# SEC EDGAR Corporate Filings Direct Bypass

- **Provider ID:** `sec-gov`
- **Data Tier:** Tier 1: Public Government Data
- **Official Base URL:** `https://data.sec.gov/`
- **Alexandria Cost:** 1 to 5 Credits | **Native Bypass Cost:** **0 Credits ($0.00)**

## Rationale & Arbitrage Proof

The US Securities and Exchange Commission (SEC) provides a free public JSON API for all public corporate submissions, XBRL company facts, and financial disclosures. Only a standard User-Agent header is required.

## Supported Endpoints & Capabilities

| Capability | Official Endpoint | Parameters | Description |
|---|---|---|---|
| **Company Submissions** | `submissions/CIK{10-digit-cik}.json` | `None (direct CIK path)` | Complete filing history, insider transactions, addresses, SIC codes, and recent 10-K/10-Q/8-K document links. |
| **Company Facts (XBRL)** | `api/xbrl/companyfacts/CIK{10-digit-cik}.json` | `None (direct CIK path)` | Normalized historical balance sheet, income statement, and cash flow line items across all past filings. |
| **Company Concept** | `api/xbrl/companyconcept/CIK{10-digit-cik}/us-gaap/{concept}.json` | `None` | Single concept series (e.g. Revenues, Assets, NetIncomeLoss) over time. |

## Direct cURL Execution (0 Credits)

```bash
curl -s -H "User-Agent: SampleApp admin@sampleapp.com" "https://data.sec.gov/submissions/CIK0000320193.json" | jq .filings.recent
```

## CLI Execution via `legends-firecrawl`

```powershell
pwsh -File E:\legends-firecrawl\bin\lax.ps1 query sec-gov filings/company
```

