---
type: bypass-guide
title: "Yahoo Finance Market Data Direct Bypass"
provider: "finance-yahoo-com"
tier: "Tier 3: Public Commercial Web / Frontend JSON"
cost: "0 Credits ($0.00)"
---

# Yahoo Finance Market Data Direct Bypass

- **Provider ID:** `finance-yahoo-com`
- **Data Tier:** Tier 3: Public Commercial Web / Frontend JSON
- **Official Base URL:** `https://query1.finance.yahoo.com/`
- **Alexandria Cost:** 1 to 5 Credits | **Native Bypass Cost:** **0 Credits ($0.00)**

## Rationale & Arbitrage Proof

Yahoo Finance provides high-speed, unauthenticated JSON chart and quote endpoints used by quantitative developers worldwide. Firecrawl Alexandria charges 5 credits per quote query.

## Supported Endpoints & Capabilities

| Capability | Official Endpoint | Parameters | Description |
|---|---|---|---|
| **Quote & Chart Series** | `v8/finance/chart/{symbol}` | `range=1d&interval=1d&indicators=quote` | Real-time prices, 52-week ranges, market cap, previous close, volume, and trading periods. |
| **Ticker & Equity Search** | `v1/finance/search` | `q={query}&quotesCount=5` | Fuzzy search ticker symbols, company names, ETFs, and indices. |
| **Historical Dividends & Splits** | `v8/finance/chart/{symbol}` | `events=div%7Csplit&range=5y` | Historical dividend payouts and stock split dates/ratios. |

## Direct cURL Execution (0 Credits)

```bash
curl -s -H "User-Agent: Mozilla/5.0" "https://query1.finance.yahoo.com/v8/finance/chart/AAPL?range=1d" | jq .chart.result[0].meta
```

## CLI Execution via `legends-firecrawl`

```powershell
pwsh -File E:\legends-firecrawl\bin\lax.ps1 query finance-yahoo-com quote
```

