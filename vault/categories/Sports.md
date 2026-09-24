---
type: category
id: "sports"
title: "Sports"
providers_count: 3
---

# Category: Sports

> Sports federations and circuits: tournament calendars, match results and player rankings.

Part of [[_Index|Legends Alexandria]] and the [[manifesto/The-Great-AI-Data-Arbitrage|Great AI Data Arbitrage]].

## Cataloged Providers (3)

| Provider | Capabilities | Data Tier | Direct Bypass Available? |
|---|---|---|---|
| `espn-com` (**ESPN**) | 10 | Public Commercial Web / Frontend JSON Endpoints | Yes (Direct unauthenticated web fetch or lightweight house scraper) |
| `tickpick-com` (**TickPick**) | 7 | Public Commercial Web / Frontend JSON Endpoints | Yes (Direct unauthenticated web fetch or lightweight house scraper) |
| `worldtabletennis-com` (**World Table Tennis**) | 5 | Proprietary Commercial B2B Data Brokers | No (Proprietary) |

## Tools & Capabilities

### ESPN (`espn-com`)

ESPN public sports data from the anonymous site and core JSON APIs: sport/league discovery, scoreboards by date or week (schedules, live and final scores with explicit status), event summaries, teams, team records and schedules, rosters, standings, player bios with career statistics, and site search. US and international coverage as ESPN exposes it (NFL, NBA, MLB, NHL, college sports, Premier League and ~219 soccer competitions incl. UEFA and FIFA tournaments).

- **`sports-data/event`** (Event): Read a specific game/match after finding its event_id in scoreboard or team_schedule. (Cost: 5 credit)
- **`sports-data/leagues`** (Leagues): Start here to discover `sport` and `league` slugs before calling scoreboard, teams, standings or search. (Cost: 5 credit)
- **`sports-data/player`** (Player): Read a player's bio and season-by-season statistics after finding the athlete_id in roster or search. (Cost: 5 credit)
- **`sports-data/roster`** (Roster): Get athlete_id values and roster details for a team; feed athlete_id to `player`. (Cost: 5 credit)
- **`sports-data/scoreboard`** (Scoreboard): Find schedules, live and completed scores for a league and day, and the event_id for `event`. (Cost: 5 credit)
- **`sports-data/search`** (Search): Resolve a team or player name to ESPN ids and the league slug to use with team, roster, player. (Cost: 5 credit)
- **`sports-data/standings`** (Standings): Read a league table or conference/division standings for a season. (Cost: 5 credit)
- **`sports-data/team`** (Team): Read a team's record, standing and next fixture by team_id. (Cost: 5 credit)
- **`sports-data/team_schedule`** (Team schedule): List a team's fixtures and results with event_ids for `event`. (Cost: 5 credit)
- **`sports-data/teams`** (Teams): Get team_id values for team, team_schedule, roster. (Cost: 5 credit)

### TickPick (`tickpick-com`)

TickPick (US resale ticket marketplace, all-in pricing): discover sports, concert, theater and comedy events by free text, performer, venue or location, and read event details with event-level listing statistics (count, min/max/average all-in per-ticket price) and daily/hourly price history from TickPick's own web API. Per-listing offers are not available (DataDome-protected).

- **`events/categories`** (Categories): Browse without a query: list leagues, teams, genres and shows and get performer slugs. Cached daily by the site. (Cost: 5 credit)
- **`events/event`** (Event): After search, performer_events or venue_events returned an event_id, or when the user pastes a tickpick.com/buy-... URL. (Cost: 5 credit)
- **`events/event_price_history`** (Event price history): To see how the cheapest ticket and the listing count moved over time for an event_id from search, performer_events or venue_events. (Cost: 5 credit)
- **`events/nearby_events`** (Nearby events): Location-first discovery: 'what is happening in Chicago'. Pass latitude/longitude; add the TickPick market slug (dma, for example washington-dc-md or chicago-il) for venues and just-announced lists. (Cost: 5 credit)
- **`events/performer_events`** (Performer events): Events for a performer whose slug and url_category came from search (performers[]) or categories (items[]). (Cost: 5 credit)
- **`events/search`** (Search): Start here to resolve a team, artist, show, venue or event name to TickPick identifiers. For a full event list use performer_events or venue_events; for one event use event. (Cost: 5 credit)
- **`events/venue_events`** (Venue events): Everything at a venue whose slug came from search or an event's venue. Page with offset = next_offset until it is null. (Cost: 5 credit)

### World Table Tennis (`worldtabletennis-com`)

Public WTT table tennis events, official match results and cards, and senior/youth ITTF ranking lists.

- **`table-tennis/event_results`** (Event results): Official match results for one completed WTT/ITTF event, identified by its numeric event id (from `events`). Returns every official match with round, start time and, by default, the full match card (competitors, game scores, winner). Filter by sub-event (MS, WS, MD, WD, XD, MT, WT, XT) and round (FNL, SFNL, QFNL, 8FNL, R32, R64, RND1.., GP). Events still in progress or not yet archived return an upstream not-found error. (Cost: 5 credit)
- **`table-tennis/events`** (Events): Search the WTT/ITTF tournament calendar (2022 to date, including scheduled events). Input optionally narrows by season year, free-text name/city/country and three-letter association code; returns event ids (needed by event_results and match), names, tier, dates, venue and sub-events, latest first. (Cost: 5 credit)
- **`table-tennis/match`** (Match): One match card by event id and WTT document code (as listed by `event_results`): competitors with ITTF ids and associations, best-of, per-game points, overall score, status, venue, table, local/UTC start and duration. Unknown document codes return an upstream not-found error. (Cost: 5 credit)
- **`table-tennis/ranking_weeks`** (Ranking weeks): Published ITTF senior ranking weeks (year, week number, publication date), newest first. Input is just an optional limit; useful to learn which week the `rankings` list reflects and how often it updates. (Cost: 5 credit)
- **`table-tennis/rankings`** (Rankings): Current ITTF world ranking list. Input selects senior (SEN, default) or youth (YOU) category, the list (MS/WS singles, MD/WD/XD doubles pairs, MDI/WDI/XDI doubles individual; default MS), an optional youth age group (U19, U17, U15, U13, U11) and an optional association filter. Returns rank, previous rank, points, player or pair identity and the publication date of the week in force. (Cost: 5 credit)


