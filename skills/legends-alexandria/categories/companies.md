---
category: "companies"
type: reference-card
provider_count: 25
---

# Category: companies

> Company records, filings, funding and firmographics.

**Providers in this category:** 25

| Provider ID | Provider Name | Capabilities | Tier | Cost | Bypass Route |
|---|---|---|---|---|---|
| `apollo` | **Apollo** | 4 | Proprietary Commercial B2B Data Brokers | Credits Required or Paid Vendor Key | Use Alexandria credits or direct vendor account |
| `b3-com-br` | **B3 listed companies and indices** | 9 | Proprietary Commercial B2B Data Brokers | Credits Required or Paid Vendor Key | Use Alexandria credits or direct vendor account |
| `bbb-business-profiles-ratings-complaint` | **BBB business profiles** | 4 | Public Commercial Web / Frontend JSON Endpoints | 0 Credits (Direct Web / Scraping Bypass) | Direct unauthenticated web fetch or lightweight house scraper |
| `bbb-org` | **Better Business Bureau** | 4 | Public Commercial Web / Frontend JSON Endpoints | 0 Credits (Direct Web / Scraping Bypass) | Direct unauthenticated web fetch or lightweight house scraper |
| `benzinga` | **Benzinga** | 11 | Proprietary Commercial B2B Data Brokers | Credits Required or Paid Vendor Key | Use Alexandria credits or direct vendor account |
| `bing-com` | **Bing Maps** | 2 | Public Commercial Web / Frontend JSON Endpoints | 0 Credits (Direct Web / Scraping Bypass) | Direct unauthenticated web fetch or lightweight house scraper |
| `builtin-com` | **Built In** | 3 | Public Commercial Web / Frontend JSON Endpoints | 0 Credits (Direct Web / Scraping Bypass) | Direct unauthenticated web fetch or lightweight house scraper |
| `finance-yahoo-com` | **Yahoo Finance** | 4 | Public Commercial Web / Frontend JSON Endpoints | 0 Credits (Direct Web / Scraping Bypass) | Direct unauthenticated web fetch or lightweight house scraper |
| `find-and-update-company-information-service-gov-uk` | **Companies House** | 15 | Public Government & Intergovernmental Data | 0 Credits (Public API) | Direct official REST API |
| `fiscal-ai` | **Fiscal.ai** | 34 | Proprietary Commercial B2B Data Brokers | Credits Required or Paid Vendor Key | Use Alexandria credits or direct vendor account |
| `fullenrich` | **FullEnrich** | 10 | Proprietary Commercial B2B Data Brokers | Credits Required or Paid Vendor Key | Use Alexandria credits or direct vendor account |
| `gartner-com` | **Gartner** | 4 | Proprietary Commercial B2B Data Brokers | Credits Required or Paid Vendor Key | Use Alexandria credits or direct vendor account |
| `gleif-org` | **GLEIF** | 6 | Open Non-Profit, Legal & Community Ecosystems | 0 Credits (Public API) | Direct community/non-profit REST API |
| `houzz-com` | **Houzz** | 3 | Proprietary Commercial B2B Data Brokers | Credits Required or Paid Vendor Key | Use Alexandria credits or direct vendor account |
| `indeed-com` | **Indeed US** | 3 | Proprietary Commercial B2B Data Brokers | Credits Required or Paid Vendor Key | Use Alexandria credits or direct vendor account |
| `maps-google-com` | **Google Maps** | 4 | Proprietary Commercial B2B Data Brokers | Credits Required or Paid Vendor Key | Use Alexandria credits or direct vendor account |
| `particle` | **Particle** | 105 | Proprietary Commercial B2B Data Brokers | Credits Required or Paid Vendor Key | Use Alexandria credits or direct vendor account |
| `peerspot-com` | **PeerSpot** | 4 | Proprietary Commercial B2B Data Brokers | Credits Required or Paid Vendor Key | Use Alexandria credits or direct vendor account |
| `reclameaqui-com-br` | **Reclame Aqui** | 7 | Proprietary Commercial B2B Data Brokers | Credits Required or Paid Vendor Key | Use Alexandria credits or direct vendor account |
| `search-sunbiz-org` | **Florida Sunbiz** | 2 | Public Government & Intergovernmental Data | 0 Credits (Public API) | Direct official REST API |
| `sos-state-co-us` | **Colorado Secretary of State business database** | 3 | Public Government & Intergovernmental Data | 0 Credits (Public API) | Direct official REST API |
| `trademarks-ipo-gov-uk` | **UK IPO trade mark register** | 4 | Public Government & Intergovernmental Data | 0 Credits (Public API) | Direct official REST API |
| `usaspending-gov` | **USAspending** | 7 | Public Government & Intergovernmental Data | 0 Credits (Public API) | Direct official REST API |
| `uspto-gov` | **USPTO patents, trademarks and assignments** | 5 | Public Government & Intergovernmental Data | 0 Credits (Public API) | Direct official REST API |
| `ycombinator-com` | **Y Combinator** | 4 | Open Non-Profit, Legal & Community Ecosystems | 0 Credits (Public API) | Direct community/non-profit REST API |

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

### B3 listed companies and indices (`b3-com-br`)

B3 (Brasil, Bolsa, Balcão), the São Paulo exchange: listed-company registry search and enumeration, company detail with sector classification and financial summary, corporate actions, cash dividend history, CVM filings, index portfolios (IBOV, IBRX, SMLL, IDIV, IFIX...), stock-to-index membership, delayed quotes and the sector taxonomy. Public data, no credentials; Portuguese labels as B3 publishes them.

- **`companies/cash_dividends`** (Cash dividends): When the `trading_name` (e.g. PETROBRAS) is known from `search_companies` or `company`. [Cost: 5 credit]  
  *Options:* `page`, `page_size`, `trading_name` *(required)*
- **`companies/company`** (Company): After `search_companies` returned a `code_cvm`, or when the CVM code is known. [Cost: 5 credit]  
  *Options:* `code_cvm` *(required)*, `include_financials`
- **`companies/company_filings`** (Company filings): For a company's regulatory disclosures; filter by `category` id (1 Assembleia, 2 Reunião da Administração, 3 Aviso aos Acionistas, 4 Fato Relevante, 6 Comunicado ao Mercado, 7 Dados Econômico-Financeiros, 8 Valores Mobiliários Negociados e Detidos, ...). [Cost: 5 credit]  
  *Options:* `category`, `code_cvm` *(required)*, `page`, `page_size`, `year`
- **`companies/corporate_actions`** (Corporate actions): When the four-letter issuer code (`issuing_company`, e.g. PETR) is known, typically from `search_companies` or `company`. [Cost: 5 credit]  
  *Options:* `issuing_company` *(required)*
- **`companies/index_portfolio`** (Index portfolio): To get an index's composition; page through with `page` (default 120 rows covers IBOV in one call). [Cost: 5 credit]  
  *Options:* `index` *(required)*, `page`, `page_size`, `portfolio`
- **`companies/industry_classification`** (Industry classification): To interpret or filter the `segment` and classification labels returned by the company functions. [Cost: 5 credit]  
  *Options:* `language`
- **`companies/quote`** (Quote): For a ticker such as PETR4, VALE3, BOVA11. Quotes are delayed per B3 policy. [Cost: 5 credit]  
  *Options:* `symbol` *(required)*
- **`companies/search_companies`** (Search companies): First step to find a company's CVM code (`code_cvm`), issuer code and trading name for the detail functions. [Cost: 5 credit]  
  *Options:* `listing_year`, `page`, `page_size`, `query`
- **`companies/stock_indices`** (Stock indices): To learn the indices a company (e.g. PETR) is a member of. [Cost: 5 credit]  
  *Options:* `keyword`, `page`, `page_size`

### BBB business profiles (`bbb-business-profiles-ratings-complaint`)

Better Business Bureau (bbb.org) business search, profiles with BBB letter grade and accreditation, complaint histories and customer reviews for the US and Canada.

- **`businesses/complaints`** (Complaint history): One page (10) of the public complaint history for a BBB business identified by profile URL or bbb_id + business_id: complaint type, status, date, redacted text and business/consumer responses, with per-type and per-status counts, optional type/status filters, and the profile's complaint totals (all, closed in 3 years, closed in 12 months). [Cost: 1 credit]  
  *Options:* `url`, `bbb_id`, `business_id`, `country`, `page`, `complaint_type`, `status`
- **`businesses/profile`** (Business profile): One BBB business profile identified by its bbb.org profile URL or by bbb_id + business_id (from search): BBB letter grade with reasons, accreditation status and dates, file-opened/start/incorporation dates, years in business, entity type, categories, address, coordinates, contacts, websites, social links, local BBB office, alerts, and complaint and customer-review totals. [Cost: 1 credit]  
  *Options:* `url`, `bbb_id`, `business_id`, `country`
- **`businesses/reviews`** (Customer reviews): One page (10) of BBB customer reviews for a business identified by profile URL or bbb_id + business_id: star rating, reviewer display name, date, text and business/customer follow-up responses, plus the profile's review total and average star rating. [Cost: 1 credit]  
  *Options:* `url`, `bbb_id`, `business_id`, `country`, `page`
- **`businesses/search`** (Business search): Find BBB business profiles by business name or category near a place (US or Canada). Returns one page of 15 results with each business's BBB letter grade, accreditation flag, categories, address, phones, coordinates and profile URL, plus totals for pagination. BBB's matching is fuzzy: check the returned name. [Cost: 1 credit]  
  *Options:* `query` *(required)*, `location`, `country`, `page`, `sort`

### Better Business Bureau (`bbb-org`)

bbb.org business directory: search businesses by name/category and location across the US and Canada with rating and accreditation filters; read a full business profile with BBB letter grade, accreditation status and dates, complaint and review summaries, alerts and licences; list published complaints with business responses; resolve a pasted bbb.org URL or id to its canonical identity. Reads the server-rendered page state live on every call; bbb.org sits behind a Cloudflare managed challenge which the runner's solver clears.

- **`businesses/complaints`** (Complaints): You need the complaint detail behind a business's complaint counts, filtered by status (answered, resolved, unanswered) or type. [Cost: 5 credit]  
  *Options:* `complaint_type`, `id`, `page`, `status`, `url`
- **`businesses/profile`** (Profile): You have a BBB `id` (from search or resolve) or a pasted bbb.org profile URL and need ratings, accreditation and complaint summary figures. [Cost: 5 credit]  
  *Options:* `id`, `url`
- **`businesses/resolve`** (Resolve): Normalise a bbb.org link an agent found elsewhere, or confirm an `id` exists, before calling profile or complaints. [Cost: 5 credit]  
  *Options:* `id`, `url`
- **`businesses/search`** (Search): Start here to find a business and its `id` for profile / complaints / resolve, or to list businesses in a category and place. [Cost: 5 credit]  
  *Options:* `accredited_only`, `category_id`, `country`, `distance_miles`, `location`, `min_rating`, `page`, `query`, `sort`, `state`

### Benzinga (`benzinga`)

Real-time financial newswire and analyst coverage for US-listed companies: market-moving headlines, why-is-it-moving notes, press releases, ratings changes and consensus, announced deals, and unusual options activity.

- **`calendar/consensus-ratings`** (Consensus ratings): Use for where analysts stand in aggregate right now on one company. For the individual changes that moved the consensus, use calendar/ratings instead. [Cost: 30 credit]  
  *Options:* `parameters[tickers]`, `parameters[date_from]`, `parameters[date_to]`, `simplify`, `aggregate_type`, `pagesize`
- **`calendar/mergers-acquisitions`** (Mergers and acquisitions): Use for who is buying whom, at what price, and whether the deal is pending or closed. For the coverage and commentary around a deal use news/search. [Cost: 15 credit]  
  *Options:* `parameters[tickers]`, `parameters[date]`, `parameters[date_from]`, `parameters[date_to]`, `parameters[date_sort]`, `parameters[importance]`, `parameters[updated]`, `page`, `pagesize`
- **`calendar/ratings`** (Analyst ratings): Use for how analysts have moved on a stock: upgrades, downgrades, initiations and target changes. Filter by parameters[analyst_id] or parameters[firm_id] to follow one analyst or firm. It carries the ratings, not the reasoning behind them. [Cost: 30 credit]  
  *Options:* `fields`, `parameters[tickers]`, `parameters[analyst_id]`, `parameters[firm_id]`, `parameters[action]`, `parameters[date]`, `parameters[date_from]`, `parameters[date_to]`, `parameters[importance]`, `simplify`, `parameters[updated]`, `page`, `pagesize`
- **`calendar/ratings-analysts`** (Analyst roster): Use to resolve an analyst by name, or to judge how accurate a particular analyst has been, and to get the id you then pass to calendar/ratings as parameters[analyst_id]. For the ratings themselves use calendar/ratings; for the list of firms rather than people use calendar/ratings-firms. [Cost: 30 credit]  
  *Options:* `page`, `pageSize`, `fields`, `analyst`, `analyst_name`, `firm`, `firm_name`, `updated`
- **`calendar/ratings-firms`** (Research firms): Use to enumerate the covering firms or to turn a firm name into the id that calendar/ratings filters on as parameters[firm_id]. For an individual analyst and their track record use calendar/ratings-analysts; for the ratings themselves use calendar/ratings. [Cost: 30 credit]  
  *Options:* `page`, `pageSize`, `fields`, `firm`, `updated`
- **`calendar/removed`** (Removed calendar events): Use when you keep a copy of the ratings or M&A calendar and need to know which previously returned events have since been withdrawn, which Schedule C.10 requires you to act on. It answers only what disappeared; for the events themselves use calendar/ratings or calendar/mergers-acquisitions. [Cost: 0 credit]  
  *Options:* `page`, `pageSize`, `type`, `updated`
- **`news/press-releases`** (Press releases): Use this for company-issued announcements distributed over the wires, the primary-source wording behind a story. For Benzinga editorial coverage and the wider newswire use news/search, and for the one-line explanation of a price move use news/wiims. [Cost: 15 credit]  
  *Options:* `page`, `pageSize`, `displayOutput`, `date`, `dateFrom`, `dateTo`, `updatedSince`, `publishedSince`, `sort`, `isin`, `cusips`, `tickers`, `primaryTickers`, `topics`, `topic_group_by`, `authors`, `format`, `importance`, `region`
- **`news/removed`** (Removed news): Use this when you keep a copy of Benzinga news and need to know which stories have been withdrawn so you can delete them, which Schedule C.10 requires. It never returns story content; for the stories themselves use news/search. [Cost: 0 credit]  
  *Options:* `page`, `pageSize`, `updatedSince`
- **`news/search`** (News search): Use for what was reported about a company or subject, and when. Scope it to tickers or a date range: unscoped it returns the whole newswire. For the analyst reaction to a story use calendar/ratings. [Cost: 30 credit]  
  *Options:* `page`, `pageSize`, `displayOutput`, `date`, `dateFrom`, `dateTo`, `updatedSince`, `publishedSince`, `sort`, `isin`, `cusips`, `tickers`, `primaryTickers`, `channels`, `topics`, `topic_group_by`, `authors`, `content_types`, `format`, `importance`, `importanceRank`, `region`
- **`news/wiims`** (Why Is It Moving): Use this to answer why a stock moved: WIIMs are the short attributed explanations Benzinga files against a ticker's price action. For the underlying coverage use news/search, and for the company's own announcement use news/press-releases. [Cost: 45 credit]  
  *Options:* `page`, `pageSize`, `displayOutput`, `date`, `dateFrom`, `dateTo`, `updatedSince`, `publishedSince`, `sort`, `isin`, `cusips`, `tickers`, `primaryTickers`, `topics`, `topic_group_by`, `authors`, `content_types`, `format`, `importance`, `importanceRank`, `region`
- **`signals/options-activity`** (Unusual options activity): Use for positioning: large directional bets before a catalyst. It reports orders, not outcomes, and a sweep filled at or above the ask (execution_estimate) is a stronger signal than one at the midpoint. [Cost: 45 credit]  
  *Options:* `parameters[tickers]`, `parameters[id]`, `parameters[date]`, `parameters[date_from]`, `parameters[date_to]`, `parameters[date_sort]`, `parameters[updated]`, `page`, `pagesize`

### Bing Maps (`bing-com`)

Public Bing Maps local business search and structured business details.

- **`businesses/business`** (Business): One local business by its Bing ypid (from `search`): name, structured address, display and E.164 phone, website, coordinates, categories, aggregate rating with review count and source, current open-status sentence, and structured weekly opening hours (per day, 24h HH:MM ranges, all-day flag, closed days). Missing values are null; hours are null when Bing publishes none. [Cost: 5 credit]  
  *Options:* `ypid` *(required)*
- **`businesses/search`** (Search): Local businesses matching a category or a business name near a street address, city/state or postal code (US and other Bing Maps markets). One page of up to 30 results with Bing ypid, name, street address, phone, website, coordinates, category, aggregate rating with review count and source (Yelp/Tripadvisor/...), and current open status. Use the ypid with `business` for structured weekly hours. [Cost: 5 credit]  
  *Options:* `count`, `latitude`, `location`, `longitude`, `page`, `query` *(required)*

### Built In (`builtin-com`)

Technology job search, public role details and company profiles from Built In.

- **`jobs/company`** (Company): Read one company profile by returned slug: description, website, logo, source employee count and industries. Headcount is a public source observation; founding year omitted because source metadata is unreliable. [Cost: 5 credit]  
  *Options:* `slug` *(required)*
- **`jobs/job`** (Job): Read one canonical Built In job URL: description, employer, source salary range/currency/unit, posting/expiry dates, locations, benefits and industry. Missing values remain unknown; a listing is not a current hiring guarantee. [Cost: 5 credit]  
  *Options:* `url` *(required)*
- **`jobs/search`** (Search): Search Built In public technology jobs by keyword, with pages1-100 and source ordering. Returns job URLs and company slugs for detail lookups. No location or remote filters in this initial contract. [Cost: 5 credit]  
  *Options:* `page`, `query`

### Yahoo Finance (`finance-yahoo-com`)

Yahoo Finance public quotes, earnings estimates, ticker discovery and dividend history.

- **`equities/dividends`** (Dividends): Cash dividend history for one ticker over a range (default 10y): each payout's ex-dividend date and per-share amount, newest first, plus any stock splits in the range with their ratio. A stock that pays no dividend returns count 0. [Cost: 5 credit]  
  *Options:* `range`, `symbol` *(required)*
- **`equities/earnings`** (Earnings): Earnings calendar and estimates for one ticker: the next earnings date (with an is_estimate flag and, when Yahoo gives a window, its end), consensus EPS and revenue estimates for that quarter, the last four quarters of EPS actual vs estimate with surprise, and the analyst estimate trend by period (0q, +1q, 0y, +1y). [Cost: 5 credit]  
  *Options:* `symbol` *(required)*
- **`equities/quote`** (Quote): Live quote and key fundamentals for one ticker: last price, change, day range, volume, pre/post-market, market cap, shares outstanding, 52-week range, valuation ratios (P/E, PEG, P/B, EV/EBITDA), margins, cash/debt, analyst targets, dividend rate/yield with ex-dividend date, the next earnings date, and company profile. Unknown values are null. [Cost: 5 credit]  
  *Options:* `symbol` *(required)*
- **`equities/search`** (Search): Resolve a company name or partial ticker to Yahoo Finance symbols. Returns up to `count` matches with symbol, name, quote type (EQUITY, ETF, ...), exchange, sector and industry; feed a `symbol` into quote, earnings or dividends. [Cost: 5 credit]  
  *Options:* `count`, `query` *(required)*, `quote_types`

### Companies House (`find-and-update-company-information-service-gov-uk`)

Public UK company searches, profiles, filings, officers, ownership, charges and historic records from the Companies House website.

- **`companies/advanced_search`** (Advanced search): Search companies by name, free-text registered-office address, dates, status, type and one SIC code. Returns one page; source limits access to 10,000 results and dissolved coverage to 2010 onward. [Cost: 5 credit]  
  *Options:* `dissolved_from`, `dissolved_to`, `incorporated_from`, `incorporated_to`, `name_excludes`, `name_includes`, `page`, `registered_office_contains`, `sic_code`, `statuses`, `subtypes`, `types`
- **`companies/alphabetical_search`** (Alphabetical search): Read an alphabetical window of company names with opaque previous/next cursors. This is not a substring search. [Cost: 5 credit]  
  *Options:* `company_name` *(required)*, `search_after`, `search_before`
- **`companies/charge`** (Charge): Read a returned charge identifier, dates, status, entitled parties, particulars and filing links. [Cost: 5 credit]  
  *Options:* `charge_id` *(required)*, `company_number` *(required)*
- **`companies/charges`** (Charges): Read one company-charge page, optionally outstanding charges only. [Cost: 5 credit]  
  *Options:* `company_number` *(required)*, `outstanding_only`, `page`
- **`companies/company`** (Company): Read a company overview, deadlines, SICs, former names and available sections. Preserve different date/address meanings and partial profiles for special company types. [Cost: 5 credit]  
  *Options:* `company_number` *(required)*
- **`companies/disqualification`** (Disqualification): Read a returned natural-person or corporate disqualification record, preserving the published sanction/order/undertaking classification. [Cost: 5 credit]  
  *Options:* `id` *(required)*, `kind` *(required)*
- **`companies/dissolved_search`** (Dissolved search): Search the historic 1989-2009 dissolved-company index by name, previous name or alphabetical window. Report downloads can be unavailable or require sign-in. [Cost: 5 credit]  
  *Options:* `mode`, `page`, `query` *(required)*, `search_after`, `search_before`
- **`companies/filing_document`** (Filing document): Return a stable public PDF filing link; optionally retrieve PDF bytes through validated redirects, capped at 5 MiB. Signed URLs are not returned. [Cost: 5 credit]  
  *Options:* `company_number` *(required)*, `download`, `transaction_id` *(required)*
- **`companies/filings`** (Filings): Read one filing-history page, optionally filtered by category, with annotations and stable document links. [Cost: 5 credit]  
  *Options:* `categories`, `company_number` *(required)*, `page`
- **`companies/insolvency`** (Insolvency): Read published insolvency cases for a company with an available insolvency page. An unavailable route is not evidence of no cases. [Cost: 5 credit]  
  *Options:* `company_number` *(required)*
- **`companies/name_availability`** (Name availability): Read the source name-conflict check. No exact match does not guarantee registration. [Cost: 5 credit]  
  *Options:* `name` *(required)*
- **`companies/officer_appointments`** (Officer appointments): Read one page of appointments for an officer identifier returned by the website, optionally current appointments only. [Cost: 5 credit]  
  *Options:* `current_only`, `officer_id` *(required)*, `page`
- **`companies/officers`** (Officers): Read one company-officer page, including public appointment details; optionally current officers only. [Cost: 5 credit]  
  *Options:* `company_number` *(required)*, `current_only`, `page`
- **`companies/persons_with_significant_control`** (Persons with significant control): Read public PSC records, statements or explicit exemption information for a company. [Cost: 5 credit]  
  *Options:* `company_number` *(required)*
- **`companies/search`** (Search): Search one page of public company, officer or disqualification results. Defaults to companies. [Cost: 5 credit]  
  *Options:* `kind`, `page`, `query` *(required)*

### Fiscal.ai (`fiscal-ai`)

Company fundamentals with the record around them: standardized and as-reported statements, ratios, ownership, prices, earnings call transcripts, and what fund letters say about a company.

- **`company/list`** (Company directory): Call to discover what is covered, or to resolve names to identifiers when you do not already have a ticker. Check the per-company dataset list before assuming a costlier capability will answer for it. [Cost: 0 credit]  
  *Options:* `pageNumber`, `compact`
- **`company/profile`** (Company profile): Call first when starting from a company name or ticker: it returns every other identifier, so one call here makes the rest of this provider addressable. Also the only place peers and secondary listings are published. [Cost: 30 credit]  
  *Options:* `fscl`, `companyKey`, `ticker`, `exchange`, `cusip`, `isin`, `figi`, `cik`
- **`company/segments-and-kpis`** (Segments and KPIs): Call for the numbers a business is actually run on - segment revenue, units, subscribers - which never reach the three statements. Coverage is narrower than for financials, and varies by company. [Cost: 30 credit]  
  *Options:* `fscl`, `companyKey`, `ticker`, `exchange`, `cusip`, `isin`, `figi`, `cik`, `periodType`, `currency`
- **`company/shares-outstanding`** (Shares outstanding): Call when a per-share figure has to be computed, or when a dual-class structure means the headline share count is misleading. Point-in-time, not a series. [Cost: 30 credit]  
  *Options:* `fscl`, `companyKey`, `ticker`, `exchange`, `cusip`, `isin`, `figi`, `cik`
- **`events/calendar`** (Earnings calendar): Call to answer who reports when. Omit every company identifier for the whole calendar, which is what makes this the one capability here that answers a question not about a specific company. Read `eventStatus` before relying on a date - an estimated one moves. [Cost: 15 credit]  
  *Options:* `fscl`, `companyKey`, `ticker`, `exchange`, `cusip`, `isin`, `figi`, `cik`, `country`, `sector`, `startDate`, `endDate`, `status`, `page`, `pageSize`
- **`events/ir-events`** (IR event resources): Call to find what exists for a quarter before asking for any of it - the deck, the release, the report, the transcript. Rows sharing a fiscal year and quarter are one event, so group on that pair rather than on the date. [Cost: 30 credit]  
  *Options:* `fscl`, `companyKey`, `ticker`, `exchange`, `cusip`, `isin`, `figi`, `cik`
- **`events/transcript`** (Earnings call transcript): Call for what was said on the call, attributed and timed. The speaker mapping is what makes it worth more than the raw text: management's prepared remarks and an analyst's question can be told apart, and the Q&A boundary is given rather than guessed. [Cost: 30 credit]  
  *Options:* `fscl`, `companyKey`, `ticker`, `exchange`, `cusip`, `isin`, `figi`, `cik`, `eventKey` *(required)*
- **`filings/list`** (Company filings): Call to find out what exists and when it was filed, and to get the document links. The filing bytes themselves are not retrievable through this provider - see its page for why - so treat `pdfUrl` as a handoff. [Cost: 15 credit]  
  *Options:* `fscl`, `companyKey`, `ticker`, `exchange`, `cusip`, `isin`, `figi`, `cik`
- **`financials/adjusted-metrics`** (Adjusted metrics): Call when comparing against analyst estimates or consensus, which are quoted on an adjusted basis rather than a GAAP one. Not a substitute for the statements: these are management's adjustments, and the exclusions are theirs. [Cost: 30 credit]  
  *Options:* `fscl`, `companyKey`, `ticker`, `exchange`, `cusip`, `isin`, `figi`, `cik`, `periodType`, `currency`
- **`financials/balance-sheet`** (Balance sheet): Call when comparing companies, screening, or computing anything that has to mean the same thing across two filers. The mapping is visible: each standardized metric names the as-reported lines behind it, so a surprising figure can be traced rather than trusted. [Cost: 15 credit]  
  *Options:* `fscl`, `companyKey`, `ticker`, `exchange`, `cusip`, `isin`, `figi`, `cik`, `periodType`, `currency`, `includeReportingTemplates`, `includeMappingAlternatives`
- **`financials/balance-sheet-as-reported`** (Balance sheet, as reported): Call when fidelity to the filing matters more than comparability: the labels and groupings are the company's own, so two companies cannot be lined up against each other. Use the standardized view for that. Each value carries a link back to the filing page it came from. [Cost: 30 credit]  
  *Options:* `fscl`, `companyKey`, `ticker`, `exchange`, `cusip`, `isin`, `figi`, `cik`, `periodType`, `currency`
- **`financials/cash-flow-statement`** (Cash flow statement): Call when comparing companies, screening, or computing anything that has to mean the same thing across two filers. The mapping is visible: each standardized metric names the as-reported lines behind it, so a surprising figure can be traced rather than trusted. [Cost: 15 credit]  
  *Options:* `fscl`, `companyKey`, `ticker`, `exchange`, `cusip`, `isin`, `figi`, `cik`, `periodType`, `currency`, `includeReportingTemplates`, `includeMappingAlternatives`
- **`financials/cash-flow-statement-as-reported`** (Cash flow statement, as reported): Call when fidelity to the filing matters more than comparability: the labels and groupings are the company's own, so two companies cannot be lined up against each other. Use the standardized view for that. Each value carries a link back to the filing page it came from. [Cost: 30 credit]  
  *Options:* `fscl`, `companyKey`, `ticker`, `exchange`, `cusip`, `isin`, `figi`, `cik`, `periodType`, `currency`
- **`financials/income-statement`** (Income statement): Call when comparing companies, screening, or computing anything that has to mean the same thing across two filers. The mapping is visible: each standardized metric names the as-reported lines behind it, so a surprising figure can be traced rather than trusted. [Cost: 15 credit]  
  *Options:* `fscl`, `companyKey`, `ticker`, `exchange`, `cusip`, `isin`, `figi`, `cik`, `periodType`, `currency`, `includeReportingTemplates`, `includeMappingAlternatives`
- **`financials/income-statement-as-reported`** (Income statement, as reported): Call when fidelity to the filing matters more than comparability: the labels and groupings are the company's own, so two companies cannot be lined up against each other. Use the standardized view for that. Each value carries a link back to the filing page it came from. [Cost: 30 credit]  
  *Options:* `fscl`, `companyKey`, `ticker`, `exchange`, `cusip`, `isin`, `figi`, `cik`, `periodType`, `currency`
- **`fund-letters/companies`** (Companies in fund letters): Call to find which companies professional investors are actually writing about, and how heavily, before asking what they said. [Cost: 15 credit]  
  *Options:* `pageNumber`, `pageSize`
- **`fund-letters/company`** (Theses on a company): Call for the qualitative case on a company as professional investors put it, with the stance and conviction attached. The one capability here that answers what people think rather than what was reported. [Cost: 15 credit]  
  *Options:* `fscl`, `companyKey`, `ticker`, `exchange`, `cusip`, `isin`, `figi`, `cik`
- **`fund-letters/detail`** (Fund letter): Call for what one letter actually argued. The narrative sections are the investor's own words; the theses are the extraction, and each names what it was based on so a thin mention is not mistaken for a conviction. [Cost: 15 credit]  
  *Options:* `letterId` *(required)*
- **`fund-letters/investor`** (Investor profile): Call to understand how a firm invests before weighting what it says about a company. The profile is derived from its own letters rather than from marketing material. [Cost: 15 credit]  
  *Options:* `investorId` *(required)*
- **`fund-letters/investors`** (Fund letter investors): Call to find the investorId for a firm, or to pick firms by style or sector focus before reading any letters. Sorted by coverage, so the most-covered firms come first. [Cost: 15 credit]  
  *Options:* `pageNumber`, `pageSize`
- **`fund-letters/list`** (Fund letters): Call to see what was published in a quarter. Returns the letter index rather than the letters - take a letterId to fund-letters/detail for the content. [Cost: 15 credit]  
  *Options:* `year` *(required)*, `quarter`, `investorId`, `fundId`, `pageNumber`, `pageSize`
- **`metrics/ratios-list`** (Ratio definitions): Call to find a ratio id before requesting a series, and to check `hasDailyData` before asking for a daily one - not every ratio has it. [Cost: 0 credit]  
  *Options:* None
- **`metrics/standardized`** (Standardized metrics): Call to find the standardized metric id for a concept before requesting statements, rather than guessing at a name. Free, and takes no company. [Cost: 0 credit]  
  *Options:* None
- **`metrics/standardized-by-template`** (Standardized metrics by template): Call rather than the full list when the template is already known - it is the only place the prose definition and the sub-component breakdown of each metric are published, which is what settles what a line actually includes. [Cost: 0 credit]  
  *Options:* `templateType` *(required)*, `statementType` *(required)*
- **`ownership/holder-holdings`** (Holdings by institution): Call to read ownership from the investor's end rather than the company's - what a fund holds and how it is weighted. The counterpart to institutional-holders, over the same 13F data. [Cost: 15 credit]  
  *Options:* `holderId` *(required)*, `year`, `quarter`, `pageNumber`, `pageSize`
- **`ownership/holders-list`** (Institution directory): Call to resolve an institution's name to the holder id that ownership/holder-holdings needs. Free, and takes no company. [Cost: 0 credit]  
  *Options:* `pageNumber`, `pageSize`
- **`ownership/insider-holders`** (Insider holders): Call for the current standing position of officers and directors, including holdings held through trusts and other vehicles. Use insider-transactions for what they have been doing rather than what they hold. [Cost: 15 credit]  
  *Options:* `fscl`, `companyKey`, `ticker`, `exchange`, `cusip`, `isin`, `figi`, `cik`, `includeInactive`, `pageNumber`, `pageSize`
- **`ownership/insider-transactions`** (Insider transactions): Call to see insider activity over time. Read `transactionType` before drawing conclusions: an option exercise or a tax withholding is not a market sale, and they sit in the same series. [Cost: 15 credit]  
  *Options:* `fscl`, `companyKey`, `ticker`, `exchange`, `cusip`, `isin`, `figi`, `cik`, `includeInactive`, `pageNumber`, `pageSize`
- **`ownership/institutional-holders`** (Institutional holders): Call to see who institutionally owns a company and who moved last quarter. 13F data lags: the report date is the quarter end, the filing date is up to 45 days later, and both are returned so the lag is visible. [Cost: 15 credit]  
  *Options:* `fscl`, `companyKey`, `ticker`, `exchange`, `cusip`, `isin`, `figi`, `cik`, `year`, `quarter`, `pageNumber`, `pageSize`
- **`prices/daily`** (Daily prices): Call for a daily close series. Prices are split-adjusted already, so no correction against prices/splits is needed; the series is per listing, so a cross-listed company answers in whichever listing the identifier denoted. [Cost: 15 credit]  
  *Options:* `fscl`, `companyKey`, `ticker`, `exchange`, `cusip`, `isin`, `figi`, `cik`, `startDate`, `endDate`, `latest`
- **`prices/intraday`** (Intraday prices): Call when the question is about movement within a session - a reaction to an announcement, say. Rounded to two decimals, so it is not a tick feed for execution purposes. [Cost: 15 credit]  
  *Options:* `fscl`, `companyKey`, `ticker`, `exchange`, `cusip`, `isin`, `figi`, `cik`, `startDate`, `endDate`
- **`prices/splits`** (Stock splits): Call to explain a discontinuity, or to reconcile against a price series from elsewhere that is not split-adjusted. The series returned by prices/daily already is, so this is not needed to correct it. [Cost: 15 credit]  
  *Options:* `fscl`, `companyKey`, `ticker`, `exchange`, `cusip`, `isin`, `figi`, `cik`
- **`ratios/daily`** (Daily ratio series): Call when the question is how a ratio moved between reporting dates rather than what it was at them. Each day is recomputed against that day's close and the then-current fundamentals, so it is a real series, not a step function. [Cost: 15 credit]  
  *Options:* `fscl`, `companyKey`, `ticker`, `exchange`, `cusip`, `isin`, `figi`, `cik`, `ratioId` *(required)*, `currency`
- **`ratios/series`** (Ratios by period): Call for valuation, margin and leverage ratios already computed against the reported statements, rather than recomputing them from financials and risking a different denominator. [Cost: 15 credit]  
  *Options:* `fscl`, `companyKey`, `ticker`, `exchange`, `cusip`, `isin`, `figi`, `cik`, `periodType`, `currency`, `ratioId`

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

### Gartner (`gartner-com`)

Gartner's public marketing site: upcoming and on-demand webinars (listing servlet and detail pages with speakers, times and registration URL), the conference calendar, and public content lists (articles, newsroom press releases, experts). Anonymous, English (www.gartner.com/en).

- **`events/conferences_list`** (Conferences list): Find Gartner conferences by region, audience or format, or get the detail URL and event code for a conference. [Cost: 5 credit]  
  *Options:* `presence`, `region`, `role`, `type`
- **`events/content_list`** (Content list): Browse Gartner's latest articles or press releases, or list Gartner analysts for a function such as cybersecurity. [Cost: 5 credit]  
  *Options:* `content_type` *(required)*, `page`, `page_size`
- **`events/webinar_detail`** (Webinar detail): After webinars_search, to get speakers and the complete description for one webinar, or when a Gartner webinar URL is pasted. [Cost: 5 credit]  
  *Options:* `event_id`, `session_id`, `url`
- **`events/webinars_search`** (Webinars search): Find upcoming webinars on a topic or in a date range, or browse the on-demand library. Follow with webinar_detail for speakers and the full description. [Cost: 5 credit]  
  *Options:* `cursor`, `function_tag`, `session_type`, `start_after`, `start_before`

### GLEIF (`gleif-org`)

Global LEI search, identity and reported direct/ultimate accounting-consolidation parents and children. Preserves reporting exceptions.

- **`entities/direct_children`** (Direct children): Page through reported direct accounting-consolidated children for an LEI. This excludes unreported ownership relationships. [Cost: 5 credit]  
  *Options:* `lei` *(required)*, `limit`, `page`
- **`entities/direct_parent`** (Direct parent): Retrieve the reported direct accounting-consolidating parent, or its reporting-exception record and reason. This is not a complete beneficial-ownership graph. [Cost: 5 credit]  
  *Options:* `lei` *(required)*
- **`entities/entity`** (Entity): Resolve an exact 20-character LEI to source identity, registration, mapped identifiers and relationship links. Unknown LEIs fail as upstream not-found, not an empty success. [Cost: 5 credit]  
  *Options:* `lei` *(required)*
- **`entities/search`** (Search): Search global registered entities by legal name, with optional legal-address country. Page through matching LEIs; name matches are candidates, not guaranteed identity equivalence. [Cost: 5 credit]  
  *Options:* `country`, `limit`, `name` *(required)*, `page`
- **`entities/ultimate_children`** (Ultimate children): Page through reported ultimate accounting-consolidated children for an LEI. This excludes unreported ownership relationships. [Cost: 5 credit]  
  *Options:* `lei` *(required)*, `limit`, `page`
- **`entities/ultimate_parent`** (Ultimate parent): Retrieve the reported ultimate accounting-consolidating parent, or its reporting-exception record and reason. Preserve exceptions rather than claiming there is no parent. [Cost: 5 credit]  
  *Options:* `lei` *(required)*

### Houzz (`houzz-com`)

Public professional discovery, service profiles and portfolio summaries.

- **`professionals/profile`** (Profile): Read a public Houzz professional profile, source review aggregate, advertised services and service areas. No review text, contact actions or licensing verification. [Cost: 5 credit]  
  *Options:* `url` *(required)*
- **`professionals/projects`** (Projects): Read the initial portfolio project summaries embedded in a public professional profile, with photo counts and source location. This is a partial subset, not complete project detail. [Cost: 5 credit]  
  *Options:* `url` *(required)*
- **`professionals/search`** (Search): Read one page of Houzz professionals from an explicit location directory URL. Results may include sponsored or nonlocal providers. Follow next_url (15-step offsets, maximum 735). [Cost: 5 credit]  
  *Options:* `url` *(required)*

### Indeed US (`indeed-com`)

Indeed US job search, full job postings and employer profiles (rating, review category scores, size, revenue, industry, addresses, CEO, links) from Indeed's own GraphQL API, with the public company page as fallback and salary and location normalised.

- **`jobs/employer`** (Employer): Employer research after search or job returned an employer key or url. Prefer employer_key (solver-free, one GraphQL call); unknown keys and slugs return not_found. [Cost: 5 credit]  
  *Options:* `company`, `employer_key`, `url`
- **`jobs/job`** (Job): After search, or when you hold a viewjob?jk= or rc/clk?jk= URL. Removed postings return not_found. [Cost: 5 credit]  
  *Options:* `job_key`, `url`
- **`jobs/search`** (Search): Start here to find job_key values; pass the same filters plus next_cursor to page. No total count is exposed by Indeed; next_cursor=null is the end. [Cost: 5 credit]  
  *Options:* `cursor`, `limit`, `location`, `posted_within_days`, `query`, `radius_miles`, `remote`, `sort`

### Google Maps (`maps-google-com`)

Google Maps business search, public reviews and sampled rating trends, plus directions for driving, walking, bicycling and public transport. Directions return route alternatives, distance, duration and ordered steps; transit includes lines, stops, transfers and times. English results. Business search/reviews use the US locale and retain their existing pagination limits.

- **`businesses/directions`** (Directions): Routes between two addresses, place names, or coordinate pairs. Modes: driving (default), walking, bicycling, transit. Returns Google route alternatives with distances, estimated durations and ordered instructions. Transit includes walking connections, line and stop details, transfers, service alerts, scheduled times and estimates when supplied. Uses the current departure time; no date/time selection, intermediate waypoints, fares, or live navigation. Availability depends on Google coverage. An explicit no-route response returns routes: []. [Cost: 5 credit]  
  *Options:* `destination` *(required)*, `mode`, `origin` *(required)*
- **`businesses/rating_trend`** (Rating trend): Monthly rating trend for one business from its newest 60 Google reviews (one request): per calendar month the review count, average rating and owner responses, plus the same summary as reviews. Months are UTC; the sample never goes beyond 60 reviews. [Cost: 5 credit]  
  *Options:* `feature_id` *(required)*
- **`businesses/reviews`** (Reviews): Public Google reviews for one business identified by its Google Maps feature_id (0x..:0x.., from search or a Maps URL). One request returns 1 to 60 reviews in the chosen order with rating, timestamp, text, images and the owner's response, plus a summary with the owner response rate over the returned sample. [Cost: 5 credit]  
  *Options:* `count`, `feature_id` *(required)*, `sort`
- **`businesses/search`** (Search): Find businesses on Google Maps by free-text query (name and/or 'category in city'). Returns up to 20 places with Google feature_id (input for reviews/rating_trend), place_id, categories, address, coordinates, aggregate rating, review count, phone and website. [Cost: 5 credit]  
  *Options:* `latitude`, `longitude`, `query` *(required)*

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

### PeerSpot (`peerspot-com`)

Public PeerSpot software products, customer reviews, ratings and comparisons.

- **`software-reviews/compare`** (Compare): PeerSpot head-to-head comparison of two products: category ranking, average rating (out of 10), reviews sentiment and review count per product, category mindshare, and per-theme sentiment scores with editorial summaries and reviewer quotes (ROI, customer service, scalability, stability, room for improvement, setup cost, valuable features). Order of the two slugs does not matter. [Cost: 5 credit]  
  *Options:* `product_a` *(required)*, `product_b` *(required)*
- **`software-reviews/product`** (Product): One PeerSpot product page: average rating and review count, willingness to recommend, category ranking and mindshare, editorial review-theme summaries (valuable features, room for improvement, ROI, pricing, use cases, support, deployment, scalability, stability) with representative quotes, one-line summaries of individual reviews, reviewer company-size and industry breakdowns, and the comparison pages that link competitors. [Cost: 5 credit]  
  *Options:* `slug`, `url`
- **`software-reviews/reviews`** (Reviews): One page (10 reviews) of full-text PeerSpot reviews for a product: star rating, title, date, reviewer role and labels, company size, industry, pros, cons, every interview section (use case, valuable features, room for improvement, pricing/licensing, setup, support, ROI, ...) and the review permalink. Pass next_page to continue. [Cost: 5 credit]  
  *Options:* `page`, `slug`, `url`
- **`software-reviews/search`** (Search): Find PeerSpot product pages for a vendor or product name. Returns up to 10 matching products with the slug needed by product, reviews and compare. PeerSpot's search is approximate (Rimini lists Gemini products), so each product carries match: exact (same words as the query), partial (every query word is a word or word prefix of the name) or fuzzy (PeerSpot's guess), and exact_match says whether any product matches exactly. A result with exact_match false and only fuzzy products means the vendor most likely has no PeerSpot page. Empty when nothing matches. [Cost: 5 credit]  
  *Options:* `query` *(required)*

### Reclame Aqui (`reclameaqui-com-br`)

Reclame Aqui (reclameaqui.com.br), Brazil's consumer complaints platform: company reputation profiles (score, RA1000/Otimo/Bom/Regular/Ruim/Nao recomendada status, response and solution rates), company search by name or CNPJ, a company's complaints with tabs and pagination, full-text complaint search, single complaint text with the company reply and consumer evaluation, segment tree and best/worst segment rankings. Public read surfaces only; Portuguese (pt-BR) content.

- **`complaints/company`** (Company): Look up a company's reputation and identity when you know its shortname (from search_companies or a pasted profile URL). [Cost: 5 credit]  
  *Options:* `shortname`, `url`
- **`complaints/company_complaints`** (Company complaints): List or paginate a company's complaints. Pass company_id from search_companies or company (or shortname). Use page for the next page while next_page is set. [Cost: 5 credit]  
  *Options:* `category`, `company_id`, `page`, `page_size`, `problem_type`, `product_type`, `shortname`, `status`
- **`complaints/complaint`** (Complaint): Read one complaint's text, the company reply and the consumer's evaluation. Ids and URLs come from company_complaints or search_complaints. [Cost: 5 credit]  
  *Options:* `company_shortname`, `complaint_id`, `url`
- **`complaints/search_companies`** (Search companies): Start here to resolve a company's shortname and numeric id from a name or CNPJ before calling company, company_complaints or search_complaints. [Cost: 5 credit]  
  *Options:* `query` *(required)*, `size`
- **`complaints/search_complaints`** (Search complaints): Find complaints about a topic ('reembolso', a product name) across Reclame Aqui or within one company. Use company_complaints to browse a company without a search term. [Cost: 5 credit]  
  *Options:* `company_id`, `page`, `page_size`, `query` *(required)*, `status`
- **`complaints/segment_ranking`** (Segment ranking): Rank companies in a category, e.g. the best marketplaces (varejo/marketplaces) or the worst online courses. [Cost: 5 credit]  
  *Options:* `main_segment` *(required)*, `page`, `page_size`, `sub_segment` *(required)*, `type`
- **`complaints/segments`** (Segments): Discover the main_segment/sub_segment pair for segment_ranking or browse Reclame Aqui's category taxonomy. [Cost: 5 credit]  
  *Options:* `main_segment`

### Florida Sunbiz (`search-sunbiz-org`)

Florida official entity name lists and business registration records, including source-labelled officers, registered agents and filing links.

- **`entities/entity`** (Entity): Look up a Florida corporate registration by document number. Returns filing attributes, source-labelled officer and registered-agent sections, annual report history and PDF links. Unsupported registration layouts fail explicitly. [Cost: 5 credit]  
  *Options:* `document_number` *(required)*
- **`entities/search`** (Search): Browse the official alphabetical entity name list from a query. Results can include nearby names, historical registrations and trademarks, not exact matches. Follow next_cursor for the next source page. [Cost: 5 credit]  
  *Options:* `cursor`, `query` *(required)*

### Colorado Secretary of State business database (`sos-state-co-us`)

Colorado Secretary of State business database (the live registry at www.sos.state.co.us/biz): business name, ID and document-number search, entity summary with periodic report month and registered agent, and the filing history with document links and periodic-report due dates.

- **`entities/entity`** (Entity): You have an entity_id from `search` (or a Colorado SOS ID number) and need the current record. [Cost: 3 credit]  
  *Options:* `entity_id` *(required)*
- **`entities/filings`** (Filings): You need due dates, filed documents or the event timeline for an entity_id from `search` or `entity`. [Cost: 5 credit]  
  *Options:* `entity_id` *(required)*, `page`
- **`entities/search`** (Search): Start here to find the 11-digit entity_id for `entity` and `filings`. [Cost: 5 credit]  
  *Options:* `name` *(required)*, `page`

### UK IPO trade mark register (`trademarks-ipo-gov-uk`)

UK Intellectual Property Office trade mark register: search owners by name or UK postcode, list the UK national marks an owner holds, and read a trade mark's case detail (status, dates, goods and services, owners, representatives, publications) and case history (status, event and goods history).

- **`trade-marks/get_trade_mark`** (Get trade mark): When you have a trade mark number (UK000..., or UK009... for a comparable mark derived from an EU trade mark, domain 23). An unknown number is a not_found failure. [Cost: 5 credit]  
  *Options:* `domain`, `number` *(required)*
- **`trade-marks/get_trade_mark_history`** (Get trade mark history): For assignment, ownership-change and status timelines of a known trade mark number. [Cost: 5 credit]  
  *Options:* `domain`, `number` *(required)*
- **`trade-marks/list_owner_marks`** (List owner marks): After search_owners returned a client_id, or from the owner link on a case detail. Follow up with get_trade_mark for the full record. [Cost: 5 credit]  
  *Options:* `client_id` *(required)*, `page`
- **`trade-marks/search_owners`** (Search owners): Start here when you know a company or person name but not a trade mark number. An owner name that matches nothing returns zero owners, not an error. [Cost: 5 credit]  
  *Options:* `name`, `page`, `postcode`

### USAspending (`usaspending-gov`)

Federal awards, transactions, recipients and agencies from USAspending.gov.

- **`agencies/agency`** (Agency): Toptier agency overview for a fiscal year by CGAC/FREC code (097 Department of Defense, 075 Health and Human Services, 036 Veterans Affairs): name, mission, website, subtier count, DEF codes in use and the fiscal year's award obligations and transaction count. [Cost: 5 credit]  
  *Options:* `fiscal_year`, `toptier_code` *(required)*
- **`awards/award`** (Award): One USAspending prime award by generated_unique_award_id (CONT_AWD_…, CONT_IDV_…, ASST_NON_…, ASST_AGG_…) or numeric internal id: identifiers, type, agencies, recipient with location, obligations and outlays, options, period of performance, place of performance, NAICS/PSC or CFDA, parent IDV, subaward totals and last modified date. [Cost: 5 credit]  
  *Options:* `award_id` *(required)*
- **`awards/award_search`** (Award search): Search USAspending prime awards by keyword, awarding/funding agency, recipient name or UEI, action-date window, place of performance, NAICS, PSC and award amount within one award family (contracts, IDVs, grants, loans, direct payments or other). One page (default 20, max 100) of summary award records with an opaque cursor for the next page; add `award` for the full record. [Cost: 5 credit]  
  *Options:* `agencies`, `award_amounts`, `award_type_codes` *(required)*, `cursor`, `keywords`, `naics_codes`, `page_size`, `place_of_performance`, `psc_codes`, `recipient_search_text`, `sort`, `time_period`
- **`awards/idv_children`** (Idv children): Awards issued under an indefinite delivery vehicle: child awards (orders), child IDVs or grandchild awards, newest period start first, with obligated amount and period of performance. Paged with a cursor. [Cost: 5 credit]  
  *Options:* `award_id` *(required)*, `cursor`, `page_size`, `relationship`
- **`awards/subawards`** (Subawards): Subawards reported under one prime award (FSRS data), newest first: subaward number, sub-recipient name, amount, action date and description. Paged with a cursor; an award with no subawards answers an empty page with a warning. [Cost: 5 credit]  
  *Options:* `award_id` *(required)*, `cursor`, `page_size`
- **`awards/transactions`** (Transactions): Transactions (individual actions and modifications) of one award, newest action first: obligation per action (negative for de-obligations), action type, modification number and description. Paged with a cursor. [Cost: 5 credit]  
  *Options:* `award_id` *(required)*, `cursor`, `page_size`
- **`recipients/recipient`** (Recipient): Recipient profile by USAspending recipient_id (hash with -C/-P/-R level) or 12-character UEI: names, identifiers, parent, business types, location and transaction obligations for the latest 12 months or a fiscal year, plus per-fiscal-year obligations for the years requested. [Cost: 5 credit]  
  *Options:* `fiscal_year`, `fiscal_years`, `recipient_id`, `uei`

### USPTO patents, trademarks and assignments (`uspto-gov`)

United States Patent and Trademark Office public records: Patent Public Search (full-text patent and pre-grant publication search and bibliographic documents), Trademark Search (word-mark search), TSDR trademark status records by serial or registration number, and Assignment Center ownership records for patents and trademarks. Anonymous, stateless JSON APIs behind the USPTO web applications; US coverage only.

- **`intellectual-property/assignments`** (Assignments): You need who owns or has a security interest in a patent or trademark, or the reel/frame of a recorded assignment. [Cost: 5 credit]  
  *Options:* `kind` *(required)*, `page`, `property` *(required)*, `rows_per_page`, `search_by` *(required)*
- **`intellectual-property/patent_document`** (Patent document): You have a patent number, publication number or ppubs guid and need the record itself. [Cost: 5 credit]  
  *Options:* `include_full_text`, `number` *(required)*
- **`intellectual-property/patent_search`** (Patent search): Start here to find patents or publications by title, number, assignee, inventor or classification; pass `patents[].guid` to `patent_document`. [Cost: 5 credit]  
  *Options:* `databases`, `page_size`, `query` *(required)*, `start`
- **`intellectual-property/trademark_search`** (Trademark search): Find trademark serial numbers by mark text; pass `hits[].serial_number` to `trademark_status` or `assignments`. [Cost: 5 credit]  
  *Options:* `alive`, `from`, `size`, `text` *(required)*
- **`intellectual-property/trademark_status`** (Trademark status): You have a serial or registration number and need the current status and parties of the mark. [Cost: 5 credit]  
  *Options:* `registration_number`, `serial_number`

### Y Combinator (`ycombinator-com`)

Public YC startup directory: browse or search companies by batch and filters, list batches, read company profiles and advertised jobs.

- **`companies/batches`** (Batches): List every batch label published in the public YC directory with its company count, newest first. Use a returned batch label as the search batch filter. [Cost: 5 credit]  
  *Options:* None
- **`companies/company`** (Company): Read a public YC company profile: description, batch, location, team size, source-reported status and the founders listed on the profile (name, title, bio, LinkedIn and X/Twitter links). [Cost: 5 credit]  
  *Options:* `slug` *(required)*
- **`companies/jobs`** (Jobs): List public jobs advertised on a YC company profile, including source salary text, location, role and requirements. Each record adds best-effort structured locations, a remote/hybrid/onsite flag and ISO country codes parsed from the location text, plus the source role slug, skills, posting age, apply link and batch. No application or contact actions. [Cost: 5 credit]  
  *Options:* `slug` *(required)*
- **`companies/search`** (Search): Browse or search the public YC company directory. Query is optional: omit it to list every company matching the exact source labels for batch (e.g. Summer 2025), industry, region, status and tag, or the hiring, top company and nonprofit flags. Twenty entries per zero-based page, at most fifty pages. [Cost: 5 credit]  
  *Options:* `batch`, `hiring`, `industry`, `nonprofit`, `page`, `query`, `region`, `status`, `tag`, `top_company`

