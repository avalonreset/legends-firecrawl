---
type: category
id: "news"
title: "News"
providers_count: 4
---

# Category: News

> Reported news: articles, wires and the archives behind them.

Part of [[_Index|Legends Alexandria]] and the [[manifesto/The-Great-AI-Data-Arbitrage|Great AI Data Arbitrage]].

## Cataloged Providers (4)

| Provider | Capabilities | Data Tier | Direct Bypass Available? |
|---|---|---|---|
| `benzinga` (**Benzinga**) | 11 | Proprietary Commercial B2B Data Brokers | No (Proprietary) |
| `nasdaq-com` (**Nasdaq.com news feeds and articles**) | 6 | Proprietary Commercial B2B Data Brokers | No (Proprietary) |
| `substack-com` (**Substack**) | 3 | Proprietary Commercial B2B Data Brokers | No (Proprietary) |
| `us-forums-blizzard-com` (**Blizzard US Forums**) | 7 | Proprietary Commercial B2B Data Brokers | No (Proprietary) |

## Tools & Capabilities

### Benzinga (`benzinga`)

Real-time financial newswire and analyst coverage for US-listed companies: market-moving headlines, why-is-it-moving notes, press releases, ratings changes and consensus, announced deals, and unusual options activity.

- **`calendar/consensus-ratings`** (Consensus ratings): Use for where analysts stand in aggregate right now on one company. For the individual changes that moved the consensus, use calendar/ratings instead. (Cost: 30 credit)
- **`calendar/mergers-acquisitions`** (Mergers and acquisitions): Use for who is buying whom, at what price, and whether the deal is pending or closed. For the coverage and commentary around a deal use news/search. (Cost: 15 credit)
- **`calendar/ratings`** (Analyst ratings): Use for how analysts have moved on a stock: upgrades, downgrades, initiations and target changes. Filter by parameters[analyst_id] or parameters[firm_id] to follow one analyst or firm. It carries the ratings, not the reasoning behind them. (Cost: 30 credit)
- **`calendar/ratings-analysts`** (Analyst roster): Use to resolve an analyst by name, or to judge how accurate a particular analyst has been, and to get the id you then pass to calendar/ratings as parameters[analyst_id]. For the ratings themselves use calendar/ratings; for the list of firms rather than people use calendar/ratings-firms. (Cost: 30 credit)
- **`calendar/ratings-firms`** (Research firms): Use to enumerate the covering firms or to turn a firm name into the id that calendar/ratings filters on as parameters[firm_id]. For an individual analyst and their track record use calendar/ratings-analysts; for the ratings themselves use calendar/ratings. (Cost: 30 credit)
- **`calendar/removed`** (Removed calendar events): Use when you keep a copy of the ratings or M&A calendar and need to know which previously returned events have since been withdrawn, which Schedule C.10 requires you to act on. It answers only what disappeared; for the events themselves use calendar/ratings or calendar/mergers-acquisitions. (Cost: 0 credit)
- **`news/press-releases`** (Press releases): Use this for company-issued announcements distributed over the wires, the primary-source wording behind a story. For Benzinga editorial coverage and the wider newswire use news/search, and for the one-line explanation of a price move use news/wiims. (Cost: 15 credit)
- **`news/removed`** (Removed news): Use this when you keep a copy of Benzinga news and need to know which stories have been withdrawn so you can delete them, which Schedule C.10 requires. It never returns story content; for the stories themselves use news/search. (Cost: 0 credit)
- **`news/search`** (News search): Use for what was reported about a company or subject, and when. Scope it to tickers or a date range: unscoped it returns the whole newswire. For the analyst reaction to a story use calendar/ratings. (Cost: 30 credit)
- **`news/wiims`** (Why Is It Moving): Use this to answer why a stock moved: WIIMs are the short attributed explanations Benzinga files against a ticker's price action. For the underlying coverage use news/search, and for the company's own announcement use news/press-releases. (Cost: 45 credit)
- **`signals/options-activity`** (Unusual options activity): Use for positioning: large directional bets before a catalyst. It reports orders, not outcomes, and a sweep filled at or above the ask (execution_estimate) is a stronger signal than one at the midpoint. (Cost: 45 credit)

### Nasdaq.com news feeds and articles (`nasdaq-com`)

Nasdaq.com's public news surfaces: ticker news, press releases, market-wide and topic feeds (JSON), the RSS feeds that carry publish times, and the full text and exact publish instant of a Nasdaq article or press release page.

- **`news/article`** (Article): Full text and the exact publish time of a story listed by any feed function. Costs one ~180 KB page fetch. (Cost: 1 credit)
- **`news/feed`** (Feed): Publish times for the newest stories on a ticker or topic in one request. For older stories or more than 15 rows use `ticker_news` / `topic_news` and `article`. (Cost: 1 credit)
- **`news/latest_headlines`** (Latest headlines): What is being published right now across the market, with no ticker or topic filter. (Cost: 1 credit)
- **`news/press_releases`** (Press releases): Company announcements for one ticker (earnings dates, product launches, filings) rather than third-party coverage. (Cost: 1 credit)
- **`news/ticker_news`** (Ticker news): Latest third-party coverage of one stock or ETF. Official company announcements (deals, partnerships, earnings, launches) are press releases, which this feed omits: pass `include_press_releases: true` or call `press_releases`. For the exact publish time of any row pass its `url` to `article`; for only the 15 newest with times in one request use `feed`. (Cost: 1 credit)
- **`news/topic_news`** (Topic news): Coverage of a theme (Markets, Stocks, Technology, Investing) rather than a ticker. (Cost: 1 credit)

### Substack (`substack-com`)

Public Substack archives, search and free posts or paid previews.

- **`newsletters/archive`** (Archive): One page of a Substack publication's archive, newest, top or pinned first. Each entry carries title, subtitle, URL, publish time, audience (free or paid), word count, engagement counts, section, tags and bylines. Page with offset and limit. (Cost: 5 credit)
- **`newsletters/post`** (Post): One Substack post by URL, or by publication and slug: metadata plus body_html and body_text. Free posts (audience everyone) are complete; paid posts return the publicly served preview with paywalled true, full_text_available false and text_coverage showing how much of the author's word count is visible. (Cost: 5 credit)
- **`newsletters/search`** (Search): Search a Substack publication's archive for posts matching a query, using Substack's own archive search. Returns the same post entries as archive, with the query echoed. (Cost: 5 credit)

### Blizzard US Forums (`us-forums-blizzard-com`)

Blizzard Entertainment's US community forums (us.forums.blizzard.com, Discourse multisite): categories, latest/top topic listings, topics with their posts, full-text post search, single posts, public user profiles with activity, and the latest-posts feed, for every locale/site forum on the host (WoW, WoW: Forever, Diablo, Hearthstone, Overwatch, StarCraft, ...). Anonymous read-only JSON routes; nothing behind Battle.net login.

- **`forum-discussions/get_post`** (Get post): Fetch a single post found through search_posts, latest_posts or a user's activity. (Cost: 5 credit)
- **`forum-discussions/get_topic`** (Get topic): Read a discussion found through list_topics or search_posts; page through long threads with `page` (and a smaller `page_size` when only the first replies matter). (Cost: 5 credit)
- **`forum-discussions/get_user`** (Get user): Who is behind a post, and what else they wrote on this forum. (Cost: 5 credit)
- **`forum-discussions/latest_posts`** (Latest posts): A firehose of what is being said right now on a forum (news-style monitoring); filter by category_id or topic on the caller's side. (Cost: 5 credit)
- **`forum-discussions/list_categories`** (List categories): Discovery: find the category ids to pass to list_topics (for example the WoW: Forever categories on en/wow) or to read a site's structure. (Cost: 5 credit)
- **`forum-discussions/list_topics`** (List topics): Browse or monitor a forum or category, e.g. WoW: Forever discussions (en/wow category 347) newest first, or the week's top topics. (Cost: 5 credit)
- **`forum-discussions/search_posts`** (Search posts): Find discussions about a subject (e.g. `WoW Forever` newest first, or posts in #housing after a date). Pair with get_topic for the full thread. (Cost: 5 credit)


