---
type: bypass-guide
title: "ESPN Sports Scores & Rosters Direct Bypass"
provider: "espn-com"
tier: "Tier 3: Public Commercial Web / Frontend JSON"
cost: "0 Credits ($0.00)"
---

# ESPN Sports Scores & Rosters Direct Bypass

- **Provider ID:** `espn-com`
- **Data Tier:** Tier 3: Public Commercial Web / Frontend JSON
- **Official Base URL:** `https://site.api.espn.com/apis/site/v2/sports/`
- **Alexandria Cost:** 1 to 5 Credits | **Native Bypass Cost:** **0 Credits ($0.00)**

## Rationale & Arbitrage Proof

ESPN powers its web apps and mobile apps using unauthenticated JSON endpoints across all major sports leagues (NFL, NBA, MLB, NHL, College Football, Soccer). Alexandria wraps these same endpoints and bills credits.

## Supported Endpoints & Capabilities

| Capability | Official Endpoint | Parameters | Description |
|---|---|---|---|
| **Live Scoreboard** | `{sport}/{league}/scoreboard` | `e.g. football/nfl/scoreboard?dates=20260920` | Real-time scores, clock, possession, down and distance, betting odds, and broadcast networks. |
| **Team Roster** | `{sport}/{league}/teams/{team_id}/roster` | `e.g. basketball/nba/teams/13/roster` | Complete team roster, athlete positions, heights, weights, jersey numbers, and experience. |
| **Player Profile & Stats** | `{sport}/{league}/athletes/{athlete_id}` | `athlete_id` | Player career statistics, bio, draft details, and season splits. |
| **Standings** | `{sport}/{league}/standings` | `season=2026` | Division and conference standings, win/loss records, streak, and tiebreakers. |

## Direct cURL Execution (0 Credits)

```bash
curl -s "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard" | jq .leagues[0].name
```

## CLI Execution via `legends-firecrawl`

```powershell
pwsh -File E:\legends-firecrawl\bin\lax.ps1 query espn-com scoreboard
```

