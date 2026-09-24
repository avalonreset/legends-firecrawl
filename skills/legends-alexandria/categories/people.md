---
category: "people"
type: reference-card
provider_count: 4
---

# Category: people

> The people at companies: who they are, what they do, and how to reach them.

**Providers in this category:** 4

| Provider ID | Provider Name | Capabilities | Tier | Cost | Bypass Route |
|---|---|---|---|---|---|
| `apollo` | **Apollo** | 4 | Proprietary Commercial B2B Data Brokers | Credits Required or Paid Vendor Key | Use Alexandria credits or direct vendor account |
| `fullenrich` | **FullEnrich** | 10 | Proprietary Commercial B2B Data Brokers | Credits Required or Paid Vendor Key | Use Alexandria credits or direct vendor account |
| `npiregistry-cms-hhs-gov` | **NPI Registry** | 3 | Public Government & Intergovernmental Data | 0 Credits (Public API) | Direct official REST API |
| `particle` | **Particle** | 105 | Proprietary Commercial B2B Data Brokers | Credits Required or Paid Vendor Key | Use Alexandria credits or direct vendor account |

## Capabilities Overview

### Apollo (`apollo`)

Person and company enrichment: find people by title and company, resolve them to verified work emails, and enrich companies from a domain with funding, headcount and technologies.

- **`companies/enrich`** (Company enrichment): Use when you have a domain and need the company behind it. For a company you can only name, search first: this takes a domain and nothing else. [Cost: 5 credit]  
  *Options:* `domain` *(required)*
- **`companies/search`** (Company search): Use to build a list from a shape: size, location, industry, technology. It bills per page, so ask for the page size you need rather than paging through the whole market. [Cost: 5 credit]  
  *Options:* `q_organization_name`, `organization_num_employees_ranges`, `organization_locations`, `currently_using_any_of_technology_uids`, `page`, `per_page`
- **`people/match`** (Person match): Use to resolve one person you have already found. Prefer the id from people/search, then a LinkedIn URL, then email; a bare name needs a domain beside it or it will match the wrong person. [Cost: 5 credit]  
  *Options:* `id`, `linkedin_url`, `email`, `name`, `domain`, `reveal_personal_emails`, `reveal_phone_number`
- **`people/search`** (Person search): Always start here. It is free and it tells you who exists before anything is spent. Never match a list of guesses: search, read the previews, then match only the people worth revealing. [Cost: 0 credit]  
  *Options:* `person_titles`, `q_keywords`, `q_organization_domains_list`, `person_locations`, `page`, `per_page`

### FullEnrich (`fullenrich`)

People and company search, profile lookups, firmographics, and verified contact data.

- **`companies/lookup`** (Company lookup): Resolve one company from its domain, LinkedIn company URL, or LinkedIn company ID. Returns firmographics, technologies, social profiles, and locations. [Cost: 5 credit]  
  *Options:* `domain`, `professional_network_url`, `professional_network_id`
- **`companies/match`** (Company match): Match an exact LinkedIn company URL. Use companies/lookup to resolve a domain, or companies/search to build a shortlist. [Cost: 5 credit]  
  *Options:* `linkedin_url` *(required)*
- **`companies/search`** (Company search): Find companies by industry, size, location, technologies, or founding year. Combine filters and page through the results. Use companies/lookup when you already have a domain or LinkedIn identifier. [Cost: 5 credit]  
  *Options:* `limit`, `offset`, `search_after`, `names`, `domains`, `company_ids`, `professional_network_urls`, `professional_network_ids`, `keywords`, `specialties`, `technologies`, `industries`, `types`, `headquarters_locations`, `founded_years`, `headcounts`
- **`contacts/mobile`** (Mobile number): Find a person's mobile phone number from a LinkedIn URL, or from their name and employer. The most expensive line by far: ask for it only when a phone is what the task needs. To enrich multiple contacts, send up to 10 separate calls in the Firecrawl /v2/scrape alexandria array, each with its own provider, capability and options. Each call accepts one contact, runs as a separate upstream job and is billed only for a result found. Inspect each call for errors; this is not a single bulk job. Concurrent enrichments share poll capacity and can hit rate limits; spread large batches out. Do not pass a contacts array in options. [Cost: 175 credit]  
  *Options:* `first_name`, `last_name`, `domain`, `company_name`, `linkedin_url`
- **`contacts/personal-email`** (Personal email): Find a person's personal email from a LinkedIn URL, or from their name and employer. Schedule A bars marketing to personal addresses; use contacts/work-email for outreach. To enrich multiple contacts, send up to 10 separate calls in the Firecrawl /v2/scrape alexandria array, each with its own provider, capability and options. Each call accepts one contact, runs as a separate upstream job and is billed only for a result found. Inspect each call for errors; this is not a single bulk job. Concurrent enrichments share poll capacity and can hit rate limits; spread large batches out. Do not pass a contacts array in options. [Cost: 55 credit]  
  *Options:* `first_name`, `last_name`, `domain`, `company_name`, `linkedin_url`
- **`contacts/reverse-email`** (Reverse email lookup): Identify the person and company behind a work or personal email address. Returns a professional profile; use people/lookup when a name or LinkedIn URL is already known. To enrich multiple contacts, send up to 10 separate calls in the Firecrawl /v2/scrape alexandria array, each with its own provider, capability and options. Each call accepts one contact, runs as a separate upstream job and is billed only for a result found. Inspect each call for errors; this is not a single bulk job. Concurrent enrichments share poll capacity and can hit rate limits; spread large batches out. Do not pass a contacts array in options. [Cost: 20 credit]  
  *Options:* `email` *(required)*
- **`contacts/work-email`** (Work email): Find a person's verified work email from a LinkedIn URL, or from their name and employer. Use contacts/mobile for a phone number and people/lookup when only the profile is needed. To enrich multiple contacts, send up to 10 separate calls in the Firecrawl /v2/scrape alexandria array, each with its own provider, capability and options. Each call accepts one contact, runs as a separate upstream job and is billed only for a result found. Inspect each call for errors; this is not a single bulk job. Concurrent enrichments share poll capacity and can hit rate limits; spread large batches out. Do not pass a contacts array in options. [Cost: 20 credit]  
  *Options:* `first_name`, `last_name`, `domain`, `company_name`, `linkedin_url`
- **`people/lookup`** (Person lookup): Resolve a person from a LinkedIn URL or ID, or a full name combined with a company domain, LinkedIn URL, or ID. Returns a profile, not verified email addresses or phone numbers. [Cost: 5 credit]  
  *Options:* `person_name`, `person_professional_network_url`, `person_professional_network_id`, `company_domain`, `company_professional_network_url`, `company_professional_network_id`
- **`people/match`** (Person match): Match an exact LinkedIn profile URL. Use people/lookup for additional identifiers, or people/search to build a shortlist. [Cost: 5 credit]  
  *Options:* `linkedin_url` *(required)*
- **`people/search`** (People search): Find people by role, employer, location, skills, or work history. Combine filters and page through the results. Use people/lookup when you already know a person's identifiers; contact enrichment retrieves emails and phones separately. [Cost: 5 credit]  
  *Options:* `limit`, `offset`, `search_after`, `person_names`, `person_ids`, `person_professional_network_urls`, `person_professional_network_ids`, `person_locations`, `person_languages`, `person_skills`, `person_universities`, `current_position_titles`, `past_position_titles`, `current_position_seniority_level`, `current_position_job_functions`, `current_position_sub_functions`, `current_position_years_in`, `current_company_names`, `current_company_domains`, `current_company_ids`, `current_company_professional_network_urls`, `current_company_professional_network_ids`, `current_company_specialties`, `current_company_industries`, `current_company_technologies`, `current_company_types`, `current_company_headquarters`, `current_company_headcounts`, `current_company_founded_years`, `current_company_years_at`, `current_company_days_since_last_job_change`, `past_company_names`, `past_company_domains`

### NPI Registry (`npiregistry-cms-hhs-gov`)

Public CMS healthcare provider business identities, taxonomy and practice locations.

- **`providers/locations`** (Locations): Practice locations for one 10-digit NPI: the primary practice location plus every secondary practice location NPPES lists, with phone/fax, and the mailing address separately. Same source record as provider, shaped for where-does-this-provider-practise questions. [Cost: 5 credit]  
  *Options:* `npi` *(required)*
- **`providers/provider`** (Provider): Full NPPES record for one 10-digit NPI: entity type, name, credential, status, enumeration and update dates, all taxonomies (specialties) with the primary flagged, mailing and practice addresses, secondary practice locations, other/DBA names, Medicaid and payer identifiers, and health-information-exchange endpoints. An unknown NPI is a not_found error. [Cost: 5 credit]  
  *Options:* `npi` *(required)*
- **`providers/search`** (Search): Search the CMS NPPES NPI Registry for healthcare providers (individuals or organizations) by name, organization, taxonomy/specialty, city, state, postal code or country. Returns one page (limit 1-200, skip up to 1200) of full provider records: NPI, taxonomies with licenses, mailing and practice addresses, other names, payer identifiers and endpoints. Requires at least one of first_name, last_name, organization_name, taxonomy_description or postal_code. [Cost: 5 credit]  
  *Options:* `address_purpose`, `city`, `country_code`, `enumeration_type`, `first_name`, `last_name`, `limit`, `organization_name`, `postal_code`, `skip`, `state`, `taxonomy_description`, `use_first_name_alias`

### Particle (`particle`)

Podcast intelligence: speaker-labelled transcripts, episode and show search, the people who appear, the sponsors and companies advertising, chart rankings, and bias and brand-suitability analysis.

- **`advertising/co-occurrence`** (Sponsors that appear together): Use for who a sponsor shares ad breaks with: the advertisers that buy the same inventory. [Cost: 25 credit]  
  *Options:* `sponsor_id`, `company_id`, `limit`, `cursor`
- **`advertising/company`** (Company profile): Use for the company record behind a sponsor, an entity or a companies/search hit. For its podcast advertising footprint use advertising/company/overview; for firmographics or funding, a company data provider is the better source. [Cost: 5 credit]  
  *Options:* `id` *(required)*
- **`advertising/company/overview`** (Company advertising profile): Use for a company's podcast advertising footprint in one call, across all its brands. For the show list use advertising/company/shows. [Cost: 25 credit]  
  *Options:* `id` *(required)*, `since`, `until`
- **`advertising/company/placements`** (Company ad placements): Use for the feed of a company's actual ad reads, episode by episode, to read or audit them. [Cost: 25 credit]  
  *Options:* `id` *(required)*, `sponsor_id`, `podcast_id`, `since`, `until`, `limit`, `cursor`
- **`advertising/company/prospects`** (Shows a company could advertise on): Use as a buy-side prospect list: where an advertiser could go next, with the shows it already buys as the reason. [Cost: 25 credit]  
  *Options:* `id` *(required)*, `include`, `min_score`, `language`, `limit`, `cursor`
- **`advertising/company/shows`** (Shows carrying a company's ads): Use for where a company advertises, ranked by volume, with the reads to sample. Pages are at most 24 rows. [Cost: 25 credit]  
  *Options:* `id` *(required)*, `sponsor_id`, `podcast_id`, `publisher_id`, `include_facets`, `include_sponsors`, `include_previews`, `preview_limit`, `since`, `until`, `limit`, `cursor`
- **`advertising/episode`** (Ads in an episode): Use for exactly who advertised in one episode, with the offer and where in the episode the read sits. [Cost: 25 credit]  
  *Options:* `id` *(required)*
- **`advertising/leaderboard`** (Sponsor leaderboard): Use for the biggest podcast advertisers overall, in a period, or on one network. For the free top-ten snapshot use advertising/leaderboard/preview. [Cost: 25 credit]  
  *Options:* `metric`, `since`, `until`, `company_id`, `publisher_id`, `limit`, `cursor`
- **`advertising/leaderboard/preview`** (Sponsor leaderboard, top ten): Use for a quick read of who is spending most on podcasts this week and who is climbing. For deeper pages, other windows or filters use advertising/leaderboard. [Cost: 25 credit]  
  *Options:* `metric`
- **`advertising/publisher`** (Publisher advertising profile): Use for how a network is monetised and who buys across it. For its shows ranked by ad volume use advertising/publisher/shows. [Cost: 25 credit]  
  *Options:* `id` *(required)*
- **`advertising/publisher/shows`** (Shows of a publisher by ad volume): Use for which of a network's shows carry the advertising. For the same catalogue by popularity use podcasts/publisher/shows. [Cost: 25 credit]  
  *Options:* `id` *(required)*, `limit`, `cursor`
- **`advertising/publisher/sponsors`** (Sponsors of a publisher): Use for who buys a network, and which of them buy it as a bundle: sort by podcast_coverage with a minimum. [Cost: 25 credit]  
  *Options:* `id` *(required)*, `q`, `sort`, `min_podcast_coverage`, `limit`, `cursor`
- **`advertising/publishers/leaderboard`** (Publisher advertising leaderboard): Use for which networks carry the most advertising, or monetise their catalogue most densely. [Cost: 25 credit]  
  *Options:* `metric`, `min_active_podcasts`, `limit`, `cursor`
- **`advertising/show`** (Show advertising profile): Use for who sponsors a show and how heavily it is monetised. For the full per-sponsor list use advertising/show/sponsors. [Cost: 25 credit]  
  *Options:* `id` *(required)*
- **`advertising/show/prospects`** (Sponsors a show could pitch): Use as a prospecting list for a show selling its own inventory: who buys shows like mine and has not bought me. [Cost: 25 credit]  
  *Options:* `id` *(required)*, `include`, `min_score`, `active_since`, `exclude_top_advertisers`, `limit`, `cursor`
- **`advertising/show/sponsors`** (Sponsors of a show): Use for every advertiser on one show with counts and recency, or one company's brands on it. [Cost: 25 credit]  
  *Options:* `id` *(required)*, `company_id`, `since`, `until`, `limit`, `cursor`
- **`advertising/sponsor`** (Sponsor profile): Use to find who is buying advertising, or to go from a sponsor back to the company paying for it. For where it runs use advertising/sponsor/shows. [Cost: 25 credit]  
  *Options:* `id` *(required)*, `since`, `until`
- **`advertising/sponsor/publishers`** (Publishers a sponsor buys across): Use to tell network buys from per-show buys: a sponsor at 60 to 100 percent coverage of several publishers is buying bundles. [Cost: 25 credit]  
  *Options:* `id` *(required)*, `limit`, `cursor`
- **`advertising/sponsor/segments`** (Ad reads of a sponsor): Use to read the actual ad reads for a sponsor, then podcasts/segment/transcript for the words of one. [Cost: 25 credit]  
  *Options:* `id` *(required)*, `podcast_id`, `since`, `until`, `limit`, `cursor`
- **`advertising/sponsor/shows`** (Shows a sponsor buys): Use for where an advertiser buys: the canonical footprint of one sponsor, or of a whole company across its brands. [Cost: 25 credit]  
  *Options:* `id` *(required)*, `since`, `until`, `limit`, `cursor`
- **`advertising/sponsors`** (Sponsor directory): Use to find a sponsor by name or by company and pick up its id. For the biggest spenders use advertising/leaderboard. [Cost: 25 credit]  
  *Options:* `q`, `company_id`, `since`, `until`, `limit`, `cursor`
- **`advertising/sponsors/trending`** (Trending sponsors): Use for which advertisers are ramping podcast spend right now, by airdate. [Cost: 25 credit]  
  *Options:* `window_days`, `min_podcast_reach`, `limit`, `cursor`
- **`advertising/timeseries`** (Ad placements over time): Use for how an advertiser's podcast spend trends by week or month, optionally on one show or network, and its host-read mix. [Cost: 25 credit]  
  *Options:* `sponsor_id`, `company_id`, `podcast_id`, `publisher_id`, `published_after`, `published_before`, `interval`
- **`bias/publisher`** (Publisher bias profile): Use for a network's political profile as a whole: how political its catalogue is and which way it leans. [Cost: 25 credit]  
  *Options:* `id` *(required)*
- **`bias/publisher/shows`** (Analysed shows of a publisher): Use to list a network's shows by political lean, or only the ones in a bucket. [Cost: 25 credit]  
  *Options:* `id` *(required)*, `bias`, `political_context`, `include_non_political`, `sort`, `order`, `limit`, `cursor`
- **`bias/publishers-by-bucket`** (Publishers with shows in a bias bucket): Use for which publishers carry the most shows of one lean: the flip of a publisher's own bias profile. [Cost: 25 credit]  
  *Options:* `result` *(required)*, `political_context`, `min_count`, `sort`, `limit`, `cursor`
- **`bias/publishers/leaderboard`** (Publisher bias leaderboard): Use for which networks lean furthest left or right, are most political, or most ideologically diverse. [Cost: 25 credit]  
  *Options:* `metric` *(required)*, `political_context`, `min_analyzed_podcasts`, `min_political_podcasts`, `since`, `until`, `limit`, `cursor`
- **`bias/show`** (Show bias analysis): Use for where a show sits politically and why, with the evidence to quote. The bucket alone rides on every show record as bias. [Cost: 25 credit]  
  *Options:* `id` *(required)*
- **`charts/chart`** (Entity chart edition): Use for what podcasts are talking about most this week in one domain: the most-mentioned shows, films, games, teams or players, or the most-booked guests, with movement since last edition. [Cost: 50 credit]  
  *Options:* `category` *(required)*, `window`, `limit`, `sort`, `include`
- **`charts/list`** (Entity charts): Use to see which charts exist (all, tv-series, movies, video-games, nfl, nba, guests and so on) and who leads each, before fetching one with charts/chart. [Cost: 50 credit]  
  *Options:* `window`
- **`companies/competitors`** (Company competitors): Use for a company's competitive set with the reason each one is on it, before comparing their podcast presence or advertising. [Cost: 25 credit]  
  *Options:* `id` *(required)*, `limit`, `cursor`
- **`companies/external-links`** (Company profile links): Use to get a company's handles, domain, CIK or ticker. The reverse, identifier to company, is entities/lookup. [Cost: 15 credit]  
  *Options:* `id` *(required)*, `limit`, `cursor`
- **`companies/people`** (People at a company): Use to find executives and role holders at a company, or the marketing, brand and partnerships contacts a sponsorship conversation would go to. [Cost: 25 credit]  
  *Options:* `id` *(required)*, `current_only`, `title`, `role`, `limit`, `cursor`
- **`companies/products`** (Company products): Use to see what a company sells, structured by segment and product line, for example to match an ad read's offer to a product. [Cost: 25 credit]  
  *Options:* `id` *(required)*, `status`
- **`companies/search`** (Company directory): Use to resolve a company by name, ticker, domain, CIK or Wikidata QID to the slug every company capability takes. The record itself is advertising/company. [Cost: 5 credit]  
  *Options:* `q`, `ids`, `ticker`, `domain`, `cik`, `qid`, `entity_id`, `updated_after`, `limit`, `cursor`
- **`entities/list`** (Entity directory): Use for the most-discussed entities overall, in one show, or of one kind, or to fetch several entities by slug at once. Takes no free text; for a name use entities/search. [Cost: 5 credit]  
  *Options:* `ids`, `podcast_id`, `type`, `limit`, `cursor`
- **`entities/lookup`** (Entity lookup by external identifier): Use when you hold a LinkedIn slug, a handle, a domain, a ticker or a CIK and need the Particle person or company: the reverse of the external-links capabilities. [Cost: 5 credit]  
  *Options:* `identifier` *(required)*, `platform`, `type`
- **`entities/mentions`** (Entity record): Use to resolve an entity slug to its record and its linked company or person. For where it was mentioned use podcasts/mentions (dialogue lines) or podcasts/episodes/list with entity_id (episodes). [Cost: 5 credit]  
  *Options:* `id` *(required)*
- **`entities/search`** (Entity search): Use to turn what someone typed into a specific person, company or entity and its slug, before asking what was said about it with podcasts/mentions or filtering episodes by it. Searching episodes directly is better when the topic, not a name, is the question. [Cost: 5 credit]  
  *Options:* `q` *(required)*, `type`, `limit`, `cursor`
- **`entities/topic`** (Topic profile): Use to place a topic in the taxonomy and see its neighbours. For the shows in it use podcasts/list with topic_id; for episodes, podcasts/episodes/list. This returns classification, not passages. [Cost: 5 credit]  
  *Options:* `id` *(required)*
- **`entities/topics`** (Topics): Use to find the topic_id that podcasts/search, podcasts/list and the guest capabilities filter on. Walk down from the roots by passing parent_id. [Cost: 15 credit]  
  *Options:* `parent_id`, `ancestry_path`, `ancestry_path_prefix`, `limit`, `cursor`
- **`entities/types`** (Types): Use to see what the type filter on entities/list can take. Skip it when listing without a filter. [Cost: 15 credit]  
  *Options:* `limit`, `cursor`
- **`people/external-links`** (Person profile links): Use to get a person's LinkedIn or social handles. The reverse, handle to person, is entities/lookup. [Cost: 15 credit]  
  *Options:* `id` *(required)*, `limit`, `cursor`
- **`people/guest`** (Guest profile): Use when the question is about someone as a podcast guest: how often they appear, where, and since when. For the episode list use people/guest/appearances. [Cost: 15 credit]  
  *Options:* `id` *(required)*
- **`people/guest/appearances`** (Guest appearances): Use for where someone has appeared, episode by episode, to read what they said: take episode.id to podcasts/transcript with speaker set to their name. [Cost: 15 credit]  
  *Options:* `id` *(required)*, `podcast_id`, `topic_id`, `published_after`, `published_before`, `suitability_tier_max`, `min_speaking_seconds`, `limit`, `cursor`
- **`people/guest/pitch-list`** (Shows a guest could appear on): Use to build a pitch list for a guest: the shows most like the ones that already booked them, with the venues to cite. [Cost: 25 credit]  
  *Options:* `id` *(required)*, `include`, `limit`, `cursor`
- **`people/guest/shows`** (Shows a guest has appeared on): Use for the set of shows behind a guest rather than the episodes: which shows book them and how often. [Cost: 15 credit]  
  *Options:* `id` *(required)*, `limit`, `cursor`
- **`people/guests`** (Guest directory): Use to find guests by name, by show, by topic or by how often they appear, and pick up the person slug. For who is currently making the rounds use people/guests/trending. [Cost: 15 credit]  
  *Options:* `q`, `min_appearances`, `podcast_id`, `topic_id`, `appeared_since`, `suitability_tier_max`, `sort`, `limit`, `cursor`
- **`people/guests/trending`** (Trending guests): Use for who is doing the podcast circuit right now: a book launch, a product unveil, a news moment, or someone new. For a steady-state directory use people/guests. [Cost: 25 credit]  
  *Options:* `since`, `min_distinct_podcasts`, `first_appearance_since`, `topic_id`, `suitability_tier_max`, `limit`, `cursor`
- **`people/profile`** (Person profile): Use to go from a name on an episode to the person: who they are, where they work and worked, and their profile links. For their podcast appearances use people/guest. [Cost: 5 credit]  
  *Options:* `id` *(required)*
- **`people/show-guests`** (Guest roster of a show): Use for who has been on a show and how often. For who it could book next use people/show-recommended-guests. [Cost: 15 credit]  
  *Options:* `id` *(required)*, `limit`, `cursor`
- **`people/show-recommended-guests`** (Guests a show could book): Use as a booking pipeline for a show: guests its peers chose that it has not had yet. [Cost: 25 credit]  
  *Options:* `id` *(required)*, `include`, `limit`, `cursor`
- **`podcasts/clip`** (Episode clip): Use when a segment needs to be cited as a playable range rather than as text. For its words call podcasts/clip/transcript. [Cost: 15 credit]  
  *Options:* `id` *(required)*
- **`podcasts/clip/transcript`** (Clip transcript): Use to quote a clip verbatim with speaker labels, or export it as subtitles with format srt. [Cost: 15 credit]  
  *Options:* `id` *(required)*, `format`
- **`podcasts/clips`** (Clip directory): Use to browse quotable moments by show, speaker or kind. For clips about a subject, search episodes: matching clips ride inside each search result. [Cost: 15 credit]  
  *Options:* `episode_id`, `podcast_id`, `speaker`, `type`, `min_engagement`, `limit`, `cursor`
- **`podcasts/episode`** (Podcast episode): Use episode.id from a search match to get the full record and, when available, its web URL or direct audio stream. Neither link is guaranteed. For what was said, fetch podcasts/transcript. [Cost: 5 credit]  
  *Options:* `id` *(required)*
- **`podcasts/episode/clips`** (Episode clips): Use for the quotable moments of an episode as bounded, playable ranges with a kind and a speaker. [Cost: 5 credit]  
  *Options:* `id` *(required)*, `limit`, `cursor`
- **`podcasts/episode/entities`** (Entities in an episode): Use for what an episode was about in named things: the companies, people and products it discussed, ranked by salience. For where each one came up in the dialogue use podcasts/transcript/mentions. [Cost: 15 credit]  
  *Options:* `id` *(required)*, `limit`, `cursor`
- **`podcasts/episode/related`** (Related episodes): Use for who else covered this: the same story or subject on other shows, optionally within a week of the episode. [Cost: 15 credit]  
  *Options:* `id` *(required)*, `same_podcast`, `published_within_days`, `include`, `limit`, `cursor`
- **`podcasts/episode/segments`** (Episode segments): Use to see the structure of an episode and pick the section to read: which time ranges are ads to skip, where the interview starts, what each discussion covers. Then podcasts/segment/transcript for the words. [Cost: 15 credit]  
  *Options:* `id` *(required)*, `limit`, `cursor`
- **`podcasts/episode/speakers`** (Episode speakers): Use to find who was on an episode and in what role, with the person slug to follow into people/profile or people/guest. Ask for the advertiser role to see who voiced the sponsor reads. [Cost: 15 credit]  
  *Options:* `id` *(required)*, `role`, `limit`, `cursor`
- **`podcasts/episode/topics`** (Episode topics): Use to classify an episode by subject area, or to pick up a topic_id for filtering shows and episodes. [Cost: 15 credit]  
  *Options:* `id` *(required)*, `limit`, `cursor`
- **`podcasts/episodes/feed`** (Episode feed): Use to poll for new episodes of a set of shows or topics as they are transcribed: a resumable, strictly ordered pull. A filter is required. For a one-off list by date use podcasts/episodes/list. [Cost: 5 credit]  
  *Options:* `milestone`, `podcast_ids`, `topic_ids`, `popularity_threshold`, `since`, `include`, `limit`, `cursor`
- **`podcasts/episodes/list`** (Episode directory): Use for episode-level filtering without dialogue: every episode a person spoke on, every episode featuring a company, a show's episodes in a date range, episodes in a language. When the question is about what was said, search episodes instead. [Cost: 5 credit]  
  *Options:* `podcast_id`, `entity_id`, `person_id`, `company_id`, `role`, `published_after`, `published_before`, `language`, `has_transcript`, `fully_ingested`, `min_duration`, `max_duration`, `limit`, `cursor`
- **`podcasts/episodes/lookup`** (Episode lookup by platform id): Use when you hold an Apple Podcasts episode URL or id, a YouTube video id, or an RSS guid and need the Particle episode id to read its transcript. Guids match exactly as supplied. [Cost: 5 credit]  
  *Options:* `platform` *(required)*, `identifier` *(required)*
- **`podcasts/episodes/search`** (Episode search): Use to find episodes that discussed something. This is the entry point: it returns ids the other podcast capabilities take. For every line about one person or company use podcasts/mentions instead. [Cost: 15 credit]  
  *Options:* `semantic_search`, `keyword_search`, `keyword_match`, `entity_id`, `entity_type`, `company_id`, `episode_id`, `podcast_id`, `type`, `role`, `language`, `since`, `until`, `sort`, `context`, `limit`, `cursor`
- **`podcasts/episodes/timeseries`** (Episode counts over time): Use for a trend rather than a list: how often a person appeared by month, how a show's output changed, how many episodes discussed a term each week. One call replaces paging the episode list per period. [Cost: 5 credit]  
  *Options:* `podcast_id`, `entity_id`, `person_id`, `company_id`, `role`, `keyword_search`, `semantic_search`, `published_after`, `published_before`, `interval`, `language`, `has_transcript`, `fully_ingested`, `min_duration`, `max_duration`
- **`podcasts/list`** (Show directory): Use to browse shows by attribute rather than by name: a topic, a language, a brand-suitability tier, a length band, a cadence, an ad-free or interview format. For a name, podcasts/search is the canonical search. [Cost: 5 credit]  
  *Options:* `slug`, `topic_id`, `language`, `sort`, `suitability_tier`, `popularity_threshold`, `guest_frequency`, `format_signal`, `has_ads`, `has_video`, `min_avg_episode_minutes`, `max_avg_episode_minutes`, `min_episodes_per_week`, `max_episodes_per_week`, `publishing_status`, `limit`, `cursor`
- **`podcasts/lookup`** (Show lookup by platform id): Use when you already hold an Apple collection id, Spotify show id, YouTube channel id or RSS feed URL and need the Particle podcast deterministically. For a name, use podcasts/search. [Cost: 5 credit]  
  *Options:* `platform` *(required)*, `identifier` *(required)*
- **`podcasts/mentions`** (Dialogue mentions of an entity): Use for every line of dialogue about one person or company across podcasts: the read-everything-about-X call. Resolve the subject with entities/search first. For dialogue by topic or exact phrase use podcasts/episodes/search. [Cost: 15 credit]  
  *Options:* `entity_id`, `company_id`, `podcast_id`, `publisher_id`, `episode_id`, `role`, `sort`, `include_ads`, `language`, `since`, `until`, `context_lines`, `limit`, `cursor`
- **`podcasts/mentions/timeseries`** (Mention counts over time): Use for how mentions of a person or company trend by day, week or month, optionally within one show or network. One call instead of paging podcasts/mentions per period. [Cost: 15 credit]  
  *Options:* `entity_id`, `company_id`, `podcast_id`, `publisher_id`, `role`, `include_ads`, `language`, `published_after`, `published_before`, `interval`
- **`podcasts/publisher`** (Publisher profile): Use to go from a show's publisher reference to the network record. For the network's shows call podcasts/publisher/shows; for its advertising, bias or suitability roll-ups use the capabilities under those concepts. [Cost: 15 credit]  
  *Options:* `id` *(required)*
- **`podcasts/publisher/shows`** (Shows of a publisher): Use to walk a network's catalogue by audience. For the same catalogue ranked by ad volume use advertising/publisher/shows. [Cost: 15 credit]  
  *Options:* `id` *(required)*, `limit`, `cursor`
- **`podcasts/publishers`** (Publisher directory): Use to find a network's slug by name before asking about its shows, advertising, bias or suitability. [Cost: 15 credit]  
  *Options:* `q`, `sort`, `limit`, `cursor`
- **`podcasts/search`** (Show search): Use to turn a show name into its slug and record. To find what was said inside one, search episodes instead: this matches show metadata, not transcripts. For an Apple, Spotify or YouTube id use podcasts/lookup. [Cost: 5 credit]  
  *Options:* `q` *(required)*, `topic_id`, `language`, `sort`, `suitability_tier`, `popularity_threshold`, `guest_frequency`, `format_signal`, `has_ads`, `has_video`, `min_avg_episode_minutes`, `max_avg_episode_minutes`, `min_episodes_per_week`, `max_episodes_per_week`, `publishing_status`, `limit`, `cursor`
- **`podcasts/segment`** (Episode segment): Use to see what a matched segment is (an interview, a topic discussion, an ad) and its time range. For its text call podcasts/segment/transcript. [Cost: 5 credit]  
  *Options:* `id` *(required)*
- **`podcasts/segment/transcript`** (Segment transcript): Use to read the words of one segment in full and in order, at the price of a segment rather than an episode. [Cost: 15 credit]  
  *Options:* `id` *(required)*, `format`
- **`podcasts/segments`** (Segment directory): Use to pull one kind of section across a show: every interview, every ad read, every topic discussion in a date range. For one episode's structure use podcasts/episode/segments. [Cost: 5 credit]  
  *Options:* `episode_id`, `podcast_id`, `type`, `since`, `until`, `limit`, `cursor`
- **`podcasts/show`** (Show profile): Use when a search or an episode record gave you a podcast id and the full show record is needed, including the publisher to go up to and the slug every other show capability takes. [Cost: 5 credit]  
  *Options:* `id` *(required)*, `topic_limit`, `include`
- **`podcasts/show/episodes`** (Episodes of a show): Use to get from a show to its episodes and their ids: the latest episode, an episode by title, or the run of episodes in a date range. A podcast slug is never an episode id; this is how you get one. [Cost: 15 credit]  
  *Options:* `id` *(required)*, `q`, `published_after`, `published_before`, `limit`, `cursor`
- **`podcasts/show/external-links`** (Show platform links): Use to get a show's Apple, Spotify or YouTube ids and links, its social handles, or its website. The reverse direction, platform id to show, is podcasts/lookup. [Cost: 15 credit]  
  *Options:* `id` *(required)*, `limit`, `cursor`
- **`podcasts/show/format`** (Show format profile): Use for the exact rates and distributions behind a show's format: how often it has guests, how long episodes run, how often it publishes and on which days. The compact form rides on every show record as format. [Cost: 15 credit]  
  *Options:* `id` *(required)*
- **`podcasts/show/mentions`** (Entity mentions in a show): Use for how much one show talks about a person or company: an episode-level roll-up inside one podcast. For the dialogue lines themselves, across shows, use podcasts/mentions. [Cost: 15 credit]  
  *Options:* `id` *(required)*, `entity_id`, `company_id`, `role`, `published_after`, `published_before`, `limit`, `cursor`
- **`podcasts/show/ratings`** (Show ratings): Use to read what listeners wrote about a show. For the averages and histogram use podcasts/show/ratings-summary. [Cost: 5 credit]  
  *Options:* `id` *(required)*, `platform_slug`, `locale`, `min_stars`, `since`, `until`, `limit`, `cursor`
- **`podcasts/show/ratings-summary`** (Show ratings summary): Use for a show's average rating and count per storefront, plus the combined figure and what recent reviews say in aggregate. [Cost: 15 credit]  
  *Options:* `id` *(required)*
- **`podcasts/show/related`** (Related shows): Use for shows like this one: competitive sets, a listener's next show, or the peer set a sponsor or guest pitch cites. Branch on band rather than on the raw score. [Cost: 15 credit]  
  *Options:* `id` *(required)*, `include`, `min_score`, `language`, `publishing_status`, `suitability_tier`, `min_popularity`, `exclude_same_publisher`, `limit`, `cursor`
- **`podcasts/topics`** (Top-level topics by show count): Use to see which subject areas have the most shows. For the full taxonomy tree use entities/topics; for the shows in one topic use podcasts/list with topic_id. [Cost: 15 credit]  
  *Options:* `limit`, `cursor`
- **`podcasts/transcript`** (Episode transcript): Use to read a whole episode rather than the excerpt a search returned. For one passage, podcasts/segment/transcript is smaller and cheaper; for a moment, podcasts/transcript/preview. [Cost: 15 credit]  
  *Options:* `id` *(required)*, `format`, `speaker`, `start`, `end`
- **`podcasts/transcript/mentions`** (Entity mentions in a transcript): Use to see exactly where and how a company, person or product was discussed within one episode, with the dialogue around each mention. Across episodes, use podcasts/mentions. [Cost: 15 credit]  
  *Options:* `id` *(required)*, `entity_id`, `context_lines`, `limit`, `cursor`
- **`podcasts/transcript/preview`** (Transcript excerpt at a moment): Use to read what was being said at a timestamp, or the opening of an episode, at a fifth of the full transcript's price. For a whole episode use podcasts/transcript. [Cost: 15 credit]  
  *Options:* `id` *(required)*, `at`, `format`
- **`rankings/categories`** (Ranking categories): Use to find the category_slug the chart capabilities take. [Cost: 15 credit]  
  *Options:* `source`, `limit`, `cursor`
- **`rankings/charts`** (Chart entries): Use for today's chart: the US Apple overall top podcasts with no arguments, or a country and category. Use rankings/categories and rankings/countries for the valid slugs. [Cost: 25 credit]  
  *Options:* `source`, `chart_type`, `country`, `category_slug`, `podcast_id`, `min_rank`, `max_rank`, `limit`, `cursor`
- **`rankings/countries`** (Ranking countries): Use to find the country codes the chart capabilities take. [Cost: 15 credit]  
  *Options:* `source`, `limit`, `cursor`
- **`rankings/history`** (Chart slot history): Use for how a chart looked on past days, or how one show moved within it. For one show across every chart use rankings/show/history. [Cost: 25 credit]  
  *Options:* `source`, `chart_type`, `country`, `category_slug`, `podcast_id`, `since`, `until`, `limit`, `cursor`
- **`rankings/movers`** (Chart movers): Use for what debuted, climbed, fell or dropped off a chart since yesterday or over a window. [Cost: 25 credit]  
  *Options:* `source`, `chart_type`, `country`, `category_slug`, `window_days`, `change`, `limit`
- **`rankings/show`** (Current rankings of a show): Use for where a show charts today, everywhere it charts. For a one-number summary use rankings/show/summary. [Cost: 25 credit]  
  *Options:* `id` *(required)*, `limit`, `cursor`
- **`rankings/show/history`** (Ranking history of a show): Use for a show's chart trajectory over time. [Cost: 25 credit]  
  *Options:* `id` *(required)*, `source`, `chart_type`, `country`, `category_slug`, `since`, `until`, `limit`, `cursor`
- **`rankings/show/summary`** (Chart presence summary): Use for how big a show is on the charts in one call: its best rank and how widely it charts. [Cost: 25 credit]  
  *Options:* `id` *(required)*
- **`rankings/sources`** (Ranking sources): Use to check which chart sources exist and how fresh the snapshot is. [Cost: 15 credit]  
  *Options:* `limit`, `cursor`
- **`suitability/category-publishers`** (Publishers by exposure to a category): Use to pivot on one category for a regulated or family brand: which networks carry the most, or least, alcohol, weapons, adult or hate-speech exposure. [Cost: 25 credit]  
  *Options:* `code` *(required)*, `direction`, `min_prevalence`, `treatment`, `min_analyzed_podcasts`, `limit`, `cursor`
- **`suitability/guest`** (Guest suitability exposure): Use for what kind of shows a guest tends to appear on, in brand-safety terms. [Cost: 25 credit]  
  *Options:* `id` *(required)*
- **`suitability/publisher`** (Publisher suitability profile): Use for how brand-safe a network's catalogue is as a whole and where its exposure sits. [Cost: 25 credit]  
  *Options:* `id` *(required)*
- **`suitability/publisher/shows`** (Assessed shows of a publisher): Use to build an inclusion or exclusion list inside one network: its shows by tier, or the ones exposed in a category. [Cost: 25 credit]  
  *Options:* `id` *(required)*, `tier`, `category`, `min_prevalence`, `treatment`, `sort`, `limit`, `cursor`
- **`suitability/publishers/leaderboard`** (Publisher suitability leaderboard): Use for the safest or riskiest networks to buy, or the most broadly placeable. [Cost: 25 credit]  
  *Options:* `metric`, `min_analyzed_podcasts`, `limit`, `cursor`
- **`suitability/show`** (Show suitability assessment): Use for whether a show is safe to advertise on and in which categories it is exposed, with the evidence. The tier alone rides on every show record as suitability_tier. [Cost: 25 credit]  
  *Options:* `id` *(required)*, `include`

