---
type: bypass-guide
title: "US Treasury Fiscal Data Direct Bypass"
provider: "treasury-fiscal-data"
tier: "Tier 1: Public Government Data"
cost: "0 Credits ($0.00)"
---

# US Treasury Fiscal Data Direct Bypass

- **Provider ID:** `treasury-fiscal-data`
- **Data Tier:** Tier 1: Public Government Data
- **Official Base URL:** `https://api.fiscaldata.treasury.gov/services/api/fiscal_service/`
- **Alexandria Cost:** 1 to 5 Credits | **Native Bypass Cost:** **0 Credits ($0.00)**

## Rationale & Arbitrage Proof

The US Department of the Treasury Bureau of the Fiscal Service operates a completely public, taxpayer-funded REST API. Firecrawl charges 1 credit per query while passing through identical query parameters.

## Supported Endpoints & Capabilities

| Capability | Official Endpoint | Parameters | Description |
|---|---|---|---|
| **Debt to the Penny** | `v2/accounting/od/debt_to_penny` | `sort=-record_date&page[size]=5` | Daily total public debt outstanding, debt held by public, intragovernmental holdings. |
| **Operating Cash Balance** | `v1/accounting/dts/operating_cash_balance` | `sort=-record_date&page[size]=5` | Daily Treasury General Account (TGA) cash balance. |
| **Average Interest Rates** | `v2/accounting/od/avg_interest_rates` | `sort=-record_date&page[size]=5` | Average interest rates on marketable and non-marketable Treasury securities. |
| **Interest Expense** | `v2/accounting/od/interest_expense` | `sort=-record_date&page[size]=5` | Monthly interest expense on the public debt. |
| **Historical Debt Outstanding** | `v2/accounting/od/historical_debt` | `sort=-record_date&page[size]=5` | Historical annual national debt dating back to 1790. |
| **Gold Reserve** | `v2/accounting/od/gold_reserve` | `sort=-record_date&page[size]=5` | Official US government book-value gold reserve holdings. |

## Direct cURL Execution (0 Credits)

```bash
curl -s "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_to_penny?sort=-record_date&page\[size\]=1" | jq .
```

## CLI Execution via `legends-firecrawl`

```powershell
pwsh -File E:\legends-firecrawl\bin\lax.ps1 query treasury-fiscal-data debt/to-the-penny
```

