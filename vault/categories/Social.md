---
type: category
id: "social"
title: "Social"
providers_count: 2
---

# Category: Social

> Public social media accounts: profiles, follower counts, posts, hashtags, boards and pins.

Part of [[_Index|Legends Alexandria]] and the [[manifesto/The-Great-AI-Data-Arbitrage|Great AI Data Arbitrage]].

## Cataloged Providers (2)

| Provider | Capabilities | Data Tier | Direct Bypass Available? |
|---|---|---|---|
| `stackexchange-com` (**Stack Exchange**) | 6 | Open Non-Profit, Legal & Community Ecosystems | Yes (Direct community/non-profit REST API) |
| `us-forums-blizzard-com` (**Blizzard US Forums**) | 7 | Proprietary Commercial B2B Data Brokers | No (Proprietary) |

## Tools & Capabilities

### Stack Exchange (`stackexchange-com`)

Stack Exchange public questions, answers and accepted answers with source attribution. Quora is not covered.

- **`questions/accepted_answers`** (Accepted answers): Accepted answers by topic: the top questions on one site carrying every tag in `tagged` (optionally narrowed by `q`), each paired with its accepted answer. One search call plus one batched answers call; `has_more` + `page` paginate. (Cost: 5 credit)
- **`questions/answer`** (Answer): One answer by `answer_id`, or up to 100 answers by `answer_ids`, on one site. Returns the full answer records (bodies, score, is_accepted, owner). Ids that do not exist are simply absent from the result. (Cost: 5 credit)
- **`questions/answers`** (Answers): Answers to one question (by `question_id` + `site` or URL), one page per call, sorted by votes, activity or creation. Each answer carries is_accepted, score, bodies, owner and its canonical URL. (Cost: 5 credit)
- **`questions/question`** (Question): One question identified by `question_id` + `site` or by its URL, with its answers (default: by votes) and the accepted answer surfaced separately. Two API calls. Unknown or deleted questions are an error. (Cost: 5 credit)
- **`questions/search`** (Search): Questions on one Stack Exchange site matching free text (`q`: one term or up to 5 searched together), tags, or title/body text, optionally inside a creation-date window (`fromdate`/`todate`) and score/date bounds (`min`/`max`); `accepted: true` keeps only questions with an accepted answer. Returns question records (bodies only with `include_body: true`) plus per-term counts, total, has_more and quota; `question_id` and `accepted_answer_id` feed `question` and `answer`. (Cost: 5 credit)
- **`questions/sites`** (Sites): Sites in the Stack Exchange network with the `site` parameter every other function takes. Input: page and page size. Returns site name, URL, audience and API parameter. (Cost: 5 credit)

### Blizzard US Forums (`us-forums-blizzard-com`)

Blizzard Entertainment's US community forums (us.forums.blizzard.com, Discourse multisite): categories, latest/top topic listings, topics with their posts, full-text post search, single posts, public user profiles with activity, and the latest-posts feed, for every locale/site forum on the host (WoW, WoW: Forever, Diablo, Hearthstone, Overwatch, StarCraft, ...). Anonymous read-only JSON routes; nothing behind Battle.net login.

- **`forum-discussions/get_post`** (Get post): Fetch a single post found through search_posts, latest_posts or a user's activity. (Cost: 5 credit)
- **`forum-discussions/get_topic`** (Get topic): Read a discussion found through list_topics or search_posts; page through long threads with `page` (and a smaller `page_size` when only the first replies matter). (Cost: 5 credit)
- **`forum-discussions/get_user`** (Get user): Who is behind a post, and what else they wrote on this forum. (Cost: 5 credit)
- **`forum-discussions/latest_posts`** (Latest posts): A firehose of what is being said right now on a forum (news-style monitoring); filter by category_id or topic on the caller's side. (Cost: 5 credit)
- **`forum-discussions/list_categories`** (List categories): Discovery: find the category ids to pass to list_topics (for example the WoW: Forever categories on en/wow) or to read a site's structure. (Cost: 5 credit)
- **`forum-discussions/list_topics`** (List topics): Browse or monitor a forum or category, e.g. WoW: Forever discussions (en/wow category 347) newest first, or the week's top topics. (Cost: 5 credit)
- **`forum-discussions/search_posts`** (Search posts): Find discussions about a subject (e.g. `WoW Forever` newest first, or posts in #housing after a date). Pair with get_topic for the full thread. (Cost: 5 credit)


