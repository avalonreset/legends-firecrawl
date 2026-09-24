---
type: category
id: "government"
title: "Government"
providers_count: 32
---

# Category: Government

> Government programs and records: federal funding and procurement opportunities, eligibility, who is buying what and when responses are due.

Part of [[_Index|Legends Alexandria]] and the [[manifesto/The-Great-AI-Data-Arbitrage|Great AI Data Arbitrage]].

## Cataloged Providers (32)

| Provider | Capabilities | Data Tier | Direct Bypass Available? |
|---|---|---|---|
| `bcb-gov-br` (**Banco Central do Brasil open data**) | 10 | Public Government & Intergovernmental Data | Yes (Direct official REST API) |
| `census-gov` (**US Census Bureau**) | 4 | Public Government & Intergovernmental Data | Yes (Direct official REST API) |
| `cftc` (**CFTC**) | 7 | Public Government & Intergovernmental Data | Yes (Direct official REST API) |
| `cftc-gov` (**CFTC Commitments of Traders**) | 8 | Public Government & Intergovernmental Data | Yes (Direct official REST API) |
| `courtlistener-com` (**CourtListener**) | 4 | Open Non-Profit, Legal & Community Ecosystems | Yes (Direct community/non-profit REST API) |
| `data-sf-gov` (**DataSF open data portal**) | 5 | Public Government & Intergovernmental Data | Yes (Direct official REST API) |
| `data-worldbank-org` (**World Bank Data**) | 11 | Public Government & Intergovernmental Data | Yes (Direct official REST API) |
| `databrowser-uis-unesco-org` (**UNESCO UIS**) | 5 | Public Government & Intergovernmental Data | Yes (Direct official REST API) |
| `eia-gov` (**US Energy Information Administration**) | 3 | Public Government & Intergovernmental Data | Yes (Direct official REST API) |
| `fda-gov` (**FDA**) | 6 | Public Government & Intergovernmental Data | Yes (Direct official REST API) |
| `find-and-update-company-information-service-gov-uk` (**Companies House**) | 15 | Public Government & Intergovernmental Data | Yes (Direct official REST API) |
| `firecrawl-gov-index` (**Government Index**) | 1 | Public Government & Intergovernmental Data | Yes (Direct official REST API) |
| `fiscaldata-treasury-gov` (**US Treasury Fiscal Data**) | 5 | Public Government & Intergovernmental Data | Yes (Direct official REST API) |
| `fred` (**FRED**) | 31 | Public Government & Intergovernmental Data | Yes (Direct official REST API) |
| `fred-stlouisfed-org` (**FRED (Federal Reserve Economic Data)**) | 10 | Public Government & Intergovernmental Data | Yes (Direct official REST API) |
| `gleif-org` (**GLEIF**) | 6 | Open Non-Profit, Legal & Community Ecosystems | Yes (Direct community/non-profit REST API) |
| `grants-gov` (**Grants.gov**) | 3 | Public Government & Intergovernmental Data | Yes (Direct official REST API) |
| `iea-org` (**IEA**) | 4 | Proprietary Commercial B2B Data Brokers | No (Proprietary) |
| `npiregistry-cms-hhs-gov` (**NPI Registry**) | 3 | Public Government & Intergovernmental Data | Yes (Direct official REST API) |
| `recreation-gov` (**Recreation.gov**) | 8 | Public Government & Intergovernmental Data | Yes (Direct official REST API) |
| `sam-gov` (**SAM.gov**) | 2 | Public Government & Intergovernmental Data | Yes (Direct official REST API) |
| `search-sunbiz-org` (**Florida Sunbiz**) | 2 | Public Government & Intergovernmental Data | Yes (Direct official REST API) |
| `sec-gov` (**SEC EDGAR**) | 7 | Public Government & Intergovernmental Data | Yes (Direct official REST API) |
| `servicodados-ibge-gov-br` (**IBGE service data API**) | 12 | Public Government & Intergovernmental Data | Yes (Direct official REST API) |
| `sos-state-co-us` (**Colorado Secretary of State business database**) | 3 | Public Government & Intergovernmental Data | Yes (Direct official REST API) |
| `trademarks-ipo-gov-uk` (**UK IPO trade mark register**) | 4 | Public Government & Intergovernmental Data | Yes (Direct official REST API) |
| `treasury-fiscal-data` (**Treasury Fiscal Data**) | 12 | Public Government & Intergovernmental Data | Yes (Direct official REST API) |
| `usaspending-gov` (**USAspending**) | 7 | Public Government & Intergovernmental Data | Yes (Direct official REST API) |
| `uspto-gov` (**USPTO patents, trademarks and assignments**) | 5 | Public Government & Intergovernmental Data | Yes (Direct official REST API) |
| `v-dem-net` (**V-Dem**) | 6 | Public Government & Intergovernmental Data | Yes (Direct official REST API) |
| `who-int` (**WHO Global Health Observatory**) | 3 | Public Government & Intergovernmental Data | Yes (Direct official REST API) |
| `worldhappiness-report` (**World Happiness Report**) | 4 | Public Government & Intergovernmental Data | Yes (Direct official REST API) |

## Tools & Capabilities

### Banco Central do Brasil open data (`bcb-gov-br`)

Banco Central do Brasil open data: SGS time series (Selic, CDI, IPCA, IGP-M, IBC-Br, USD/BRL and ~3,600 more series by code), PTAX official exchange rates (USD and other currencies, by date or date range), Focus market expectations (IPCA, Selic, PIB, cambio: median, mean, standard deviation, respondents), PIX statistics (by municipality, aggregate, registered keys, DICT users), retail credit rates by institution, SPI settlement and payment-instrument statistics, currency in circulation, plus discovery of Olinda OData services and of the dadosabertos.bcb.gov.br dataset catalogue. Anonymous JSON APIs; no key or session.

- **`economic-data/credit_rates`** (Credit rates): Compare bank lending rates (mortgage, payroll loans, vehicle, credit card, ...) for a month. (Cost: 5 credit)
- **`economic-data/datasets_search`** (Datasets search): Find an SGS series code or an Olinda service name before calling `sgs_series` or `olinda_service`. (Cost: 5 credit)
- **`economic-data/focus_expectations`** (Focus expectations): Market consensus for inflation, policy rate, GDP or FX by reference month/year or Copom meeting. (Cost: 5 credit)
- **`economic-data/olinda_service`** (Olinda service): See which entity sets and functions an Olinda service exposes before querying it. (Cost: 5 credit)
- **`economic-data/payment_statistics`** (Payment statistics): SPI settlement volumes, payment-instrument mix, cash in circulation. (Cost: 5 credit)
- **`economic-data/pix_statistics`** (Pix statistics): PIX volumes by municipality or segment, registered keys, DICT users. (Cost: 5 credit)
- **`economic-data/ptax_currencies`** (Ptax currencies): Discover which currency symbols `ptax_currency` accepts. (Cost: 5 credit)
- **`economic-data/ptax_currency`** (Ptax currency): Rates for EUR, GBP, JPY, ... against BRL. Take `moeda` from `ptax_currencies`. (Cost: 5 credit)
- **`economic-data/ptax_usd`** (Ptax usd): USD/BRL PTAX for a day or a range. Use `ptax_currency` for other currencies. (Cost: 5 credit)
- **`economic-data/sgs_series`** (Sgs series): Get the numbers for a known SGS code. Find codes with `datasets_search` (CKAN `codigo_sgs`). (Cost: 5 credit)

### US Census Bureau (`census-gov`)

Discover Census datasets, variables and geography codes, then retrieve published estimates, margins of error and counts with source annotations.

- **`census/data`** (Data): Retrieve estimates. Input: dataset path (acs/acs5, acs/acs1, acs/acs5/subject, acs/acs5/profile, dec/pl, dec/dhc, pep/population, cbp ...), vintage, 1-200 variable names or group(TABLE) tokens, and a geography as Data API for/in predicates (for: 'county:*', in: ['state:06']). Returns one row per geography with values as published, sentinels turned into null plus annotation, FIPS parts, variable metadata with units, and the equivalent api.census.gov URL. Unknown variables are rejected with invalid_input naming them. (Cost: 5 credit)
- **`census/datasets`** (Datasets): Search the Census Data API catalog. Input: free-text query over dataset path, title and description plus an optional vintage (year). Returns one record per dataset/vintage with its API endpoint, metadata links, publication date and supported geography levels. (Cost: 5 credit)
- **`census/geographies`** (Geographies): Geography resolver. Input: a place, county, state, tract or other geography name (e.g. 'Travis County, Texas'). Returns matching Census geographies with summary level, GEO_ID, FIPS parts and the exact `for`/`in` predicates to pass to `data`. (Cost: 5 credit)
- **`census/variables`** (Variables): List variables of one dataset vintage. Input: dataset path and vintage, plus a group (table id such as B01003 or DP05) and/or a free-text query matched against group descriptions and variable labels. Returns variable name, verbatim label, concept, predicate type, group and the unit phrase the label carries. (Cost: 5 credit)

### CFTC (`cftc`)

Commitments of Traders: weekly futures and options positioning by trader category - speculators, hedgers, managed money, dealers, leveraged funds, index traders - for every reportable US futures market, from the CFTC.

- **`disaggregated/combined`** (Disaggregated report, futures and options combined): The disaggregated split with options included. Prefer it for crude, natural gas and gold, where a large share of managed-money exposure is held through options and the futures-only figure understates it. (Cost: 1 credit)
- **`disaggregated/futures-only`** (Disaggregated report, futures only): Physical commodities - agriculture, energy, metals - when the question is which kind of participant is positioned, not just speculator versus hedger: managed money is the fund positioning most reports quote, swap dealers carry the index-fund flow, producers and merchants are the physical hedge. Financial futures are not here; use the financial report. (Cost: 1 credit)
- **`financial/combined`** (Financial futures report, futures and options combined): The financial split with options included, which matters most for equity index and Treasury futures, where options open interest is a large fraction of the total. (Cost: 1 credit)
- **`financial/futures-only`** (Financial futures report, futures only): Currencies, Treasury and SOFR futures, equity index futures, VIX: who is long the dollar, how short leveraged funds are in ten-year notes, how asset managers are positioned in S&P futures. Leveraged funds is the hedge-fund column; asset managers is pensions, insurers and mutual funds. (Cost: 1 credit)
- **`legacy/combined`** (Legacy report, futures and options combined): The legacy split with options included, which is the fuller picture of a group's exposure in markets where options are liquid - energy, metals, rates. The row id ends in C rather than F; everything else reads the same as futures-only. (Cost: 1 credit)
- **`legacy/futures-only`** (Legacy report, futures only): The report most commentary means by 'the COT': speculators versus hedgers, futures positions only, back to 1986 for every market. Filter by `cftc_contract_market_code` or `commodity_name` and order by `report_date_as_yyyy_mm_dd DESC` for the latest week. Use legacy/combined when options positions matter, and the disaggregated or financial report when the two-way speculator/hedger split is too coarse. (Cost: 1 credit)
- **`supplemental/index-traders`** (Supplemental report, commodity index traders): Thirteen agricultural markets - corn, wheat, soybeans, sugar, coffee, cocoa, cotton, cattle, hogs - when the question is how much of the length is passive index money rather than a directional view. Nowhere else in the COT is index-trader positioning stated on its own. (Cost: 1 credit)

### CFTC Commitments of Traders (`cftc-gov`)

US Commodity Futures Trading Commission Commitments of Traders (COT) reports from the public reporting SODA API (publicreporting.cftc.gov): the seven weekly datasets (Legacy, Disaggregated and Traders in Financial Futures, each futures-only and combined, plus the Supplemental commodity index report) with filters, column projection, deterministic recent-first order and offset pagination, and a contract-market discovery function.

- **`commitments-of-traders/disaggregated_combined`** (Disaggregated combined): Positions and open interest from the CFTC Disaggregated - Combined report for one or many markets and weeks. Use `markets` first to find contract_market_code values; use `fields` to keep the payload small. (Cost: 5 credit)
- **`commitments-of-traders/disaggregated_futures_only`** (Disaggregated futures only): Positions and open interest from the CFTC Disaggregated - Futures Only report for one or many markets and weeks. Use `markets` first to find contract_market_code values; use `fields` to keep the payload small. (Cost: 5 credit)
- **`commitments-of-traders/legacy_combined`** (Legacy combined): Positions and open interest from the CFTC Legacy - Combined report for one or many markets and weeks. Use `markets` first to find contract_market_code values; use `fields` to keep the payload small. (Cost: 5 credit)
- **`commitments-of-traders/legacy_futures_only`** (Legacy futures only): Positions and open interest from the CFTC Legacy - Futures Only report for one or many markets and weeks. Use `markets` first to find contract_market_code values; use `fields` to keep the payload small. (Cost: 5 credit)
- **`commitments-of-traders/markets`** (Markets): Start here to find the contract_market_code (and exchange_code / commodity names) to pass to a report function, or to see which markets a dataset covers and how far back. (Cost: 5 credit)
- **`commitments-of-traders/supplemental`** (Supplemental): Positions and open interest from the CFTC Supplemental Commodity Index report for one or many markets and weeks. Use `markets` first to find contract_market_code values; use `fields` to keep the payload small. (Cost: 5 credit)
- **`commitments-of-traders/tff_combined`** (Tff combined): Positions and open interest from the CFTC Traders in Financial Futures - Combined report for one or many markets and weeks. Use `markets` first to find contract_market_code values; use `fields` to keep the payload small. (Cost: 5 credit)
- **`commitments-of-traders/tff_futures_only`** (Tff futures only): Positions and open interest from the CFTC Traders in Financial Futures - Futures Only report for one or many markets and weeks. Use `markets` first to find contract_market_code values; use `fields` to keep the payload small. (Cost: 5 credit)

### CourtListener (`courtlistener-com`)

Public CourtListener opinions, federal dockets, entries and court metadata.

- **`courts/courts`** (Courts): List the courts CourtListener indexes, with their ids for the court filter of the search functions. Filter by jurisdiction code (S = state supreme, SA = state appellate, ST = state trial, F = federal appellate, FD = federal district, FB = federal bankruptcy) and page through 20 courts at a time. (Cost: 5 credit)
- **`dockets/docket_entries`** (Docket entries): List the docket entries and filed documents of one federal PACER docket identified by its CourtListener docket_id (from search_dockets), oldest first by default. Each entry carries the entry number, filing date, description, PACER document id, availability and a free PDF link when RECAP has the document. (Cost: 5 credit)
- **`dockets/search_dockets`** (Search dockets): Search federal PACER dockets (RECAP archive) on CourtListener by party name, attorney, case name, docket number, judge, nature of suit, cause, court and filing dates, or look one docket up by docket_id. Returns docket metadata (parties, judge, dates, PACER case id) and the docket_id needed for docket_entries. (Cost: 5 credit)
- **`opinions/search_opinions`** (Search opinions): Search published case law (opinions) from federal and state courts on CourtListener by full text, citation, case name, judge, docket number, court and filing date. Returns opinion clusters with citations, court, dates, cite counts and per-opinion snippets, PDF links and cited-opinion ids. (Cost: 5 credit)

### DataSF open data portal (`data-sf-gov`)

San Francisco's open data portal (data.sf.gov, a Socrata site): search the dataset catalog, read a dataset's metadata and columns, query and count rows of any dataset with SoQL ($select/$where/$order/$group/$q and bare field filters, including spatial functions), and list the portal's category and tag facets.

- **`open-data/dataset`** (Dataset): Before `rows`: column field names and datatypes must come from here, not be guessed. Accepts a 4x4 id or any data.sf.gov / data.sfgov.org dataset URL. (Cost: 5 credit)
- **`open-data/datasets`** (Datasets): Start here when the 4x4 dataset id is unknown: find the dataset, then call `dataset` for its columns and `rows` for its data. Only results with type `dataset` (and a non-null api_url) have rows. (Cost: 5 credit)
- **`open-data/facets`** (Facets): Discover how the portal organises its assets before searching by category or tag. (Cost: 5 credit)
- **`open-data/row_count`** (Row count): Size a `rows` query before paging, or answer a pure how-many question. (Cost: 5 credit)
- **`open-data/rows`** (Rows): Any question that needs actual records from a DataSF dataset. Get the 4x4 id from `datasets` and the column field names from `dataset` first. Use `row_count` to size a query before paging. (Cost: 5 credit)

### World Bank Data (`data-worldbank-org`)

World Bank Indicators API v2: database catalog, indicator discovery, economies and aggregates, reference lists, observations (classic and dimension paths including International Debt Statistics) and extended series/economy metadata. Keyless public API.

- **`indicators/concept_values`** (Concept values): Enumerate what a source can be queried by, e.g. IDS creditor codes for `source_data`. (Cost: 5 credit)
- **`indicators/countries`** (Countries): Resolve country codes for `data`, or enumerate the members of a region or income group. (Cost: 5 credit)
- **`indicators/country`** (Country): Confirm a code and read its region, income level and lending type before querying data. (Cost: 5 credit)
- **`indicators/data`** (Data): Fetch the actual numbers once you know the indicator id(s) and country code(s). (Cost: 5 credit)
- **`indicators/indicator`** (Indicator): You have an indicator id and need its definition or its source before calling `data`. (Cost: 5 credit)
- **`indicators/indicators`** (Indicators): Discover indicator ids for `indicator` and `data`; browse a topic (see `reference` kind topic) or a database. (Cost: 5 credit)
- **`indicators/metadata`** (Metadata): Read the definition, license or methodology notes behind a series, or an economy's statistical profile. (Cost: 5 credit)
- **`indicators/reference`** (Reference): Find valid `topic_id`, `region`, `income_level` or `lending_type` codes. (Cost: 5 credit)
- **`indicators/source_concepts`** (Source concepts): Before `concept_values` or `source_data` on an unfamiliar source. (Cost: 5 credit)
- **`indicators/source_data`** (Source data): Use for IDS (source 6) series, or when you want the dimension-keyed form of a series from any source. (Cost: 5 credit)
- **`indicators/sources`** (Sources): Start here to find the source id of a database (2 WDI, 6 IDS, 15 GEM) or to read its vintage. (Cost: 5 credit)

### UNESCO UIS (`databrowser-uis-unesco-org`)

UNESCO UIS published versions, geographies, indicators and education observations.

- **`statistics/data`** (Data): Retrieve observations for up to 20 indicator codes across ISO3 countries and/or UIS regional aggregates, optionally limited to a year range and pinned to a data version. Each observation keeps the source value, magnitude and qualifier flags, footnotes and the version id; pages are sorted by indicator, geo unit, year. (Cost: 5 credit)
- **`statistics/geographies`** (Geographies): List UIS geo units of one type: countries (ISO 3166-1 alpha-3 ids) or regional aggregates (`GROUP: Name` ids such as `SDG: Sub-Saharan Africa`), optionally filtered by name substring or aggregate family, for the default or a pinned version. (Cost: 5 credit)
- **`statistics/indicator`** (Indicator): Look up one indicator code and return its full metadata: name, theme, unit label, data availability, glossary definition and calculation method, and the disaggregation dimensions the code encodes. Unknown codes answer not_found. (Cost: 5 credit)
- **`statistics/indicators`** (Indicators): Search the full UIS indicator catalogue (about 5,000 codes including sex, wealth-quintile, location and parity-index disaggregations) by free text and theme, with data availability per indicator. Returns one page; follow next_cursor for more. (Cost: 5 credit)
- **`statistics/versions`** (Versions): List every published UIS data version (release) with its publication date, description, and per-theme last-update status, flagging the current default. Use a version_id to pin data, indicators and geographies to a release. (Cost: 5 credit)

### US Energy Information Administration (`eia-gov`)

Discover EIA energy data routes, enumerate facet values and retrieve energy observations with source units and labels.

- **`energy-data/data`** (Data): One page of observations from an EIA route (`<route>/data`) at a frequency, filtered by facet codes and a period range, sorted, with offset pagination up to 5000 rows per page. Each record carries the period, every facet as {code, name}, requested values as source strings, units copied from the source, extra source flags, and the series id when the route has one. Period formats follow the frequency (YYYY, YYYY-Qn, YYYY-MM, YYYY-MM-DD, YYYY-MM-DDTHH). (Cost: 5 credit)
- **`energy-data/facet_values`** (Facet values): List every value of one facet on a route (for example `sectorid` on `electricity/retail-sales`, or `series` on `petroleum/pri/spt`) with its code, readable name and alias, so `data` can be filtered by code. (Cost: 5 credit)
- **`energy-data/routes`** (Routes): Navigate the EIA API v2 route hierarchy. Given a route path (or none for the root) returns that route's metadata: child routes, frequencies with period formats, facet ids and data columns with units. Use it to find the route, frequency, facets and columns that `data` needs. (Cost: 5 credit)

### FDA (`fda-gov`)

US FDA drug, food and device enforcement recalls, Drugs@FDA applications, structured labeling and device 510(k) decisions via openFDA.

- **`records/device_clearances`** (Device clearances): Search device 510(k) submission decision records and resolve a k_number. Preserve decision_code and decision_date; do not equate every returned submission with clearance or PMA approval. (Cost: 5 credit)
- **`records/device_recalls`** (Device recalls): Search medical device enforcement recall records and resolve a recall_number. Preserve recall reason, status and classification; this is not the separate device recall classification dataset. (Cost: 5 credit)
- **`records/drug_applications`** (Drug applications): Search Drugs@FDA applications and submission histories, or resolve an application_number. Inspect submission statuses: a returned record alone is not proof of current approval or availability. (Cost: 5 credit)
- **`records/drug_labels`** (Drug labels): Search structured drug labeling and resolve a source label id. Includes source warnings and indications where available. Label presence does not itself establish FDA approval. (Cost: 5 credit)
- **`records/drug_recalls`** (Drug recalls): Search drug enforcement recall records, including classification, reason and recall status. Search product_description, recalling_firm or report_date, or resolve a recall_number using record_id. (Cost: 5 credit)
- **`records/food_recalls`** (Food recalls): Search food enforcement recall records and resolve a recall_number. Source recall status and affected product descriptions are preserved. (Cost: 5 credit)

### Companies House (`find-and-update-company-information-service-gov-uk`)

Public UK company searches, profiles, filings, officers, ownership, charges and historic records from the Companies House website.

- **`companies/advanced_search`** (Advanced search): Search companies by name, free-text registered-office address, dates, status, type and one SIC code. Returns one page; source limits access to 10,000 results and dissolved coverage to 2010 onward. (Cost: 5 credit)
- **`companies/alphabetical_search`** (Alphabetical search): Read an alphabetical window of company names with opaque previous/next cursors. This is not a substring search. (Cost: 5 credit)
- **`companies/charge`** (Charge): Read a returned charge identifier, dates, status, entitled parties, particulars and filing links. (Cost: 5 credit)
- **`companies/charges`** (Charges): Read one company-charge page, optionally outstanding charges only. (Cost: 5 credit)
- **`companies/company`** (Company): Read a company overview, deadlines, SICs, former names and available sections. Preserve different date/address meanings and partial profiles for special company types. (Cost: 5 credit)
- **`companies/disqualification`** (Disqualification): Read a returned natural-person or corporate disqualification record, preserving the published sanction/order/undertaking classification. (Cost: 5 credit)
- **`companies/dissolved_search`** (Dissolved search): Search the historic 1989-2009 dissolved-company index by name, previous name or alphabetical window. Report downloads can be unavailable or require sign-in. (Cost: 5 credit)
- **`companies/filing_document`** (Filing document): Return a stable public PDF filing link; optionally retrieve PDF bytes through validated redirects, capped at 5 MiB. Signed URLs are not returned. (Cost: 5 credit)
- **`companies/filings`** (Filings): Read one filing-history page, optionally filtered by category, with annotations and stable document links. (Cost: 5 credit)
- **`companies/insolvency`** (Insolvency): Read published insolvency cases for a company with an available insolvency page. An unavailable route is not evidence of no cases. (Cost: 5 credit)
- **`companies/name_availability`** (Name availability): Read the source name-conflict check. No exact match does not guarantee registration. (Cost: 5 credit)
- **`companies/officer_appointments`** (Officer appointments): Read one page of appointments for an officer identifier returned by the website, optionally current appointments only. (Cost: 5 credit)
- **`companies/officers`** (Officers): Read one company-officer page, including public appointment details; optionally current officers only. (Cost: 5 credit)
- **`companies/persons_with_significant_control`** (Persons with significant control): Read public PSC records, statements or explicit exemption information for a company. (Cost: 5 credit)
- **`companies/search`** (Search): Search one page of public company, officer or disqualification results. Defaults to companies. (Cost: 5 credit)

### Government Index (`firecrawl-gov-index`)

About 16 million pages from US federal, state, county and city government sites: statutes and code sections, regulations, zoning and municipal ordinances, permits, licences and fee schedules, court filings, tax forms, procurement and agency guidance, searched as one index.

- **`search`** (Search government pages): Use first for any US government, legal, tax, court, permit, statute, regulation, grant or procurement question, before web search: what a city's zoning or planning code allows at an address, which business licence, permit, inspection or fee a city or county requires to open a shop, restaurant, food truck or mobile service, the text of a state code section or municipal ordinance, or the official page for a form or program. One call searches about 16 million official pages and returns URLs to cite or scrape. For the structured record behind a page (a SAM.gov notice, a Federal Register document, a bill) use that source's own provider. (Cost: 2 credit)

### US Treasury Fiscal Data (`fiscaldata-treasury-gov`)

US Treasury Fiscal Data (fiscaldata.treasury.gov): the dataset catalog, filtered rows from any of the ~180 API tables (Debt to the Penny, Daily and Monthly Treasury Statements, auctions, average interest rates, interest expense, gold reserve, rates of exchange, MSPD, ...), latest observations of the headline tables, the release calendar and published report files.

- **`fiscal-data/data`** (Data): Any question that needs the actual numbers from a Fiscal Data table. Use `datasets` first when the endpoint path is unknown; use `latest` for the newest rows of a headline table. (Cost: 5 credit)
- **`fiscal-data/datasets`** (Datasets): Start here to find the `endpoint` for `data` or the `dataset_id` for `release_calendar` and `published_reports`. (Cost: 5 credit)
- **`fiscal-data/latest`** (Latest): Current values without knowing the endpoint path: today's national debt, the latest cash balance, the last auctions, the current exchange rate table. (Cost: 5 credit)
- **`fiscal-data/published_reports`** (Published reports): To get the official PDF/XLS of a statement for a given date rather than the table rows. (Cost: 5 credit)
- **`fiscal-data/release_calendar`** (Release calendar): When a dataset will next be updated, or whether today's release is already out. (Cost: 5 credit)

### FRED (`fred`)

US and international economic time series from the Federal Reserve Bank of St. Louis: rates, prices, employment, output and money, with the full revision history behind each figure.

- **`categories/category`** (Category): Call to confirm what a category id is before walking down from it, or with no argument to land on the root. The only category endpoint that takes no real-time period, so what it returns is always the current name. (Cost: 0 credit)
- **`categories/children`** (Child categories): The rung of the walk from the root to a series list. It descends one level per call, so getting from the root to a leaf takes several. Nothing here pages: a category with many children returns all of them. (Cost: 0 credit)
- **`categories/related`** (Related categories): Call for the cross-links the hierarchy cannot express. Most categories have none, so an empty array is the normal answer here and not a sign the call went wrong. (Cost: 0 credit)
- **`categories/related-tags`** (Category related tags): Call to narrow a category further once you already have one tag: it returns the tags that co-occur with `tag_names` inside this category. It narrows rather than suggesting alternatives, and unlike `categories/tags` the `tag_names` argument is mandatory. (Cost: 0 credit)
- **`categories/series`** (Category series): The bottom of the category walk: turns a category id into series ids. `limit` defaults to its maximum of 1000, so narrow with `tag_names` or `filter_variable` rather than expecting a small first page. (Cost: 1 credit)
- **`categories/tags`** (Category tags): Call to see what the series in a category are labelled with before filtering them. `series_count` on each tag counts only series in this category, not every series carrying the tag. (Cost: 0 credit)
- **`releases/dates`** (All release dates): Call for the economic calendar across all releases at once. Not symmetric with `releases/release-dates` despite the near-identical name: this one sorts descending by default, carries `release_name`, and only reaches back to the start of the current year unless told otherwise. (Cost: 0 credit)
- **`releases/related-tags`** (Release related tags): Call to narrow within a release once you have one tag. Two independently required arguments here, `release_id` and `tag_names`; the second reads like an optional filter and is not. (Cost: 0 credit)
- **`releases/release`** (Release): Call to resolve a release id into a name and link. Widening the real-time period makes this single-release call return more than one record, one per interval in which the release's attributes differed. (Cost: 0 credit)
- **`releases/release-dates`** (Release dates): Call for one release's publication history. It defaults to the whole span back to 1776-07-04 rather than the current year, has no `order_by`, and omits `release_name` - three ways it differs from `releases/dates`. Set `include_release_dates_with_no_data` to get the next scheduled date. (Cost: 0 credit)
- **`releases/releases`** (Releases): The entry point for every other release capability: it is where a release name becomes the `release_id` they take. There are only a few hundred releases and `limit` defaults to 1000, so one call is usually the whole list. (Cost: 0 credit)
- **`releases/series`** (Release series): The bridge from a release to series ids: every series that arrives with this publication. A large release runs to thousands of series, so filter with `tag_names` or `filter_variable` rather than paging the whole thing. (Cost: 1 credit)
- **`releases/sources`** (Release sources): Call when the question is who publishes a release rather than what is in it. A release can have more than one source agency. (Cost: 0 credit)
- **`releases/tables`** (Release table): Call when the layout matters - which line of a published table a series sits on, and what nests under what. This is the only capability here that answers with a tree rather than a list, so a caller that walks `key` plus `paginated` has to special-case it: descend `elements`, then each element's `children`. (Cost: 1 credit)
- **`releases/tags`** (Release tags): Call to see how a release's series are labelled before filtering `releases/series` by tag. `tag_names` is optional here and required on `releases/related-tags` - same parameter, adjacent endpoints, opposite requiredness. (Cost: 0 credit)
- **`series/categories`** (Series categories): Call to walk back up from a series you already have to the part of the tree it lives in, and from there to its peers. A series can sit in several categories. (Cost: 0 credit)
- **`series/observations`** (Series observations): The only capability in this provider that returns numbers; everything else exists to find the id it takes. Two independent time axes: `observation_start`/`observation_end` bound when the economy did the thing, `realtime_start`/`realtime_end` bound when FRED knew it. Leaving the real-time pair alone gives today's vintage only, so a question about revisions needs 1776-07-04 to 9999-12-31 or an explicit `vintage_dates`. (Cost: 1 credit)
- **`series/release`** (Series release): Call to find which publication a series arrives in, then use that `release_id` for its calendar or its sibling series. Answering `when is this next updated` goes through here rather than through the series record. (Cost: 0 credit)
- **`series/search`** (Series search): The way in when all you have is words. Set `search_type` to series_id when the query is an id fragment rather than a description; the default full-text mode stems, so `UNRATE` under it matches on unrelated titles. Leave `order_by` and `sort_order` unset unless you mean to override the relevance ranking, because their defaults depend on each other. (Cost: 0 credit)
- **`series/search-related-tags`** (Series search related tags): The second step of narrowing a search: given words and one tag already applied, the tags that co-occur on what is left. Two required arguments, `series_search_text` and `tag_names` - the second looks like a filter and is mandatory. (Cost: 0 credit)
- **`series/search-tags`** (Series search tags): Call after a broad `series/search` to see what would narrow it, then feed a name back as `tag_names` there. Two search-text parameters on one endpoint: `series_search_text` picks the series, `tag_search_text` filters the tags that come back. (Cost: 0 credit)
- **`series/series`** (Series metadata): Call before charting or comparing: `units`, `seasonal_adjustment` and `frequency` are what decide whether two series are comparable, and none of them are visible from the id. Widening the real-time period returns one record per interval in which the metadata differed, so a single-series call can answer with several rows. (Cost: 1 credit)
- **`series/tags`** (Series tags): Call to read one series' labels - its geography, frequency, publisher and subject - and to get the tag names that would find its peers through `tags/series`. Unlike every other tag capability here it has no limit, offset, search_text or tag_group_id: you get all of them. (Cost: 0 credit)
- **`series/updates`** (Series updates): Call to find what has changed rather than what exists - the only capability here that takes no series id. FRED caps it at series updated in the last two weeks, so it cannot answer a question about last quarter, and the sort is fixed at last_updated descending with no way to change it. (Cost: 1 credit)
- **`series/vintage-dates`** (Series vintage dates): Call to find out when a series was actually revised, then pass one or more of these dates to `series/observations` as `vintage_dates` to see the data as it stood. The path is `vintagedates` with no underscore, and unlike its siblings the real-time period defaults to the whole span rather than to today, so a bare call returns the full revision history. (Cost: 1 credit)
- **`sources/releases`** (Source releases): The middle rung of the provenance walk: agency to release to series. Call when the question starts from a publisher - everything the BEA puts out - rather than from a subject. (Cost: 0 credit)
- **`sources/source`** (Source): Call to resolve a source id to an agency name and site. Widening the real-time period makes this single-source call return several records, one per interval in which the agency's name or link differed. (Cost: 0 credit)
- **`sources/sources`** (Sources): Where a `source_id` comes from. There are only about a hundred agencies and `limit` defaults to 1000, so one call is the whole list and paging is never needed here. (Cost: 0 credit)
- **`tags/related`** (Related tags): Call to narrow a tag search: given tags already chosen, the tags that co-occur with them. The one required argument is the one that is optional on `tags/tags`, and `tag_group_id` does not accept `cc` here. Tag names may contain spaces, so a value like `monetary aggregates;weekly` needs the space URL-encoded and only the `;` treated as a separator. (Cost: 0 credit)
- **`tags/series`** (Series by tag): The non-hierarchical route to series ids: every series carrying all of `tag_names` at once, without walking the category tree. Tags intersect rather than union, so each name added narrows. Unlike `categories/series` there is no `filter_variable`/`filter_value` here - narrow with more tags instead. (Cost: 1 credit)
- **`tags/tags`** (Tags): The full vocabulary - roughly 4,800 tags against a `limit` cap of 1000, so this is the one tag capability that genuinely needs paging. `series_count` here is the global count, unlike the same field on the category, release and related-tag capabilities where it is scoped to what was asked about. (Cost: 0 credit)

### FRED (Federal Reserve Economic Data) (`fred-stlouisfed-org`)

FRED (Federal Reserve Economic Data), the St. Louis Fed's database of US and international economic time series: headline US indicators such as the monthly unemployment rate (UNRATE), CPI inflation (CPIAUCSL), GDP (GDP, GDPC1), nonfarm payrolls (PAYEMS), the federal funds rate (FEDFUNDS) and Treasury yields (DGS10), plus 800,000+ other series. Search series by text, browse categories, releases, sources and tags, read one series' metadata (units, frequency, seasonal adjustment, source, notes, date range, last update) and fetch its observations (daily, weekly, monthly, quarterly or annual values) with date window, frequency aggregation and transformation, paginated, from the site's keyless JSON, CSV and HTML endpoints.

- **`economic-data/category`** (Category): Discover series by topic instead of by text: start at the root, follow `children[].category_id`, then read `series[].series_id` for `series` / `series_observations`. (Cost: 5 credit)
- **`economic-data/release`** (Release): Browse the series a release publishes (e.g. release 53 = Gross Domestic Product) and hand `series[].series_id` to `series` / `series_observations`. (Cost: 5 credit)
- **`economic-data/releases`** (Releases): Find a `release_id` for `release`; releases group the series a statistical agency publishes together. (Cost: 5 credit)
- **`economic-data/series`** (Series): Confirm what a `series_id` (or a pasted fred.stlouisfed.org/series/{id} page URL) measures and which `units`/`frequency` values `series_observations` accepts for it; the data points themselves come from `series_observations`. (Cost: 5 credit)
- **`economic-data/series_observations`** (Series observations): Get the historical values of a known `series_id` or a pasted fred.stlouisfed.org/series/{id} page URL (monthly US unemployment rate = UNRATE, CPI = CPIAUCSL, real GDP = GDPC1); pick `units` and `frequency` from `series.available_units` / `series.available_frequencies`. Use `series_search` first when only the concept is known. (Cost: 5 credit)
- **`economic-data/series_search`** (Series search): Start here to find a `series_id` (e.g. UNRATE, CPIAUCSL) for `series` and `series_observations`. (Cost: 5 credit)
- **`economic-data/source`** (Source): See what an agency publishes (e.g. source 18 = U.S. Bureau of Economic Analysis) and hand `releases[].release_id` to `release`. (Cost: 5 credit)
- **`economic-data/sources`** (Sources): Find a `source_id` for `source`. (Cost: 5 credit)
- **`economic-data/tag_series`** (Tag series): Find series by tag combination, e.g. gdp;quarterly or usa;monthly;nsa, then read them with `series` / `series_observations`. (Cost: 5 credit)
- **`economic-data/tags`** (Tags): Discover tag names to combine in `tag_series`. (Cost: 5 credit)

### GLEIF (`gleif-org`)

Global LEI search, identity and reported direct/ultimate accounting-consolidation parents and children. Preserves reporting exceptions.

- **`entities/direct_children`** (Direct children): Page through reported direct accounting-consolidated children for an LEI. This excludes unreported ownership relationships. (Cost: 5 credit)
- **`entities/direct_parent`** (Direct parent): Retrieve the reported direct accounting-consolidating parent, or its reporting-exception record and reason. This is not a complete beneficial-ownership graph. (Cost: 5 credit)
- **`entities/entity`** (Entity): Resolve an exact 20-character LEI to source identity, registration, mapped identifiers and relationship links. Unknown LEIs fail as upstream not-found, not an empty success. (Cost: 5 credit)
- **`entities/search`** (Search): Search global registered entities by legal name, with optional legal-address country. Page through matching LEIs; name matches are candidates, not guaranteed identity equivalence. (Cost: 5 credit)
- **`entities/ultimate_children`** (Ultimate children): Page through reported ultimate accounting-consolidated children for an LEI. This excludes unreported ownership relationships. (Cost: 5 credit)
- **`entities/ultimate_parent`** (Ultimate parent): Retrieve the reported ultimate accounting-consolidating parent, or its reporting-exception record and reason. Preserve exceptions rather than claiming there is no parent. (Cost: 5 credit)

### Grants.gov (`grants-gov`)

Official federal funding opportunity search, detail and filter vocabularies.

- **`opportunities/detail`** (Detail): Full Grants.gov opportunity record by stable numeric ID: eligibility, funding amounts, deadlines, amendments, attachments. Always a live lookup. (Cost: 5 credit)
- **`opportunities/facets`** (Facets): Filter vocabularies with live hit counts: statuses, agency codes (with sub-agencies), eligibility codes, funding categories and instruments. (Cost: 5 credit)
- **`opportunities/search`** (Search): Search Grants.gov funding opportunities by keyword, agency, status, eligibility, funding category, assistance listing and posted-date window; one page of summary records (or full records with expand). (Cost: 5 credit)

### IEA (`iea-org`)

Public energy highlights, country metadata and observations; paid and account-gated non-CC datasets are refused.

- **`energy/countries`** (Countries): IEA country name to ISO3 crosswalk (from api.iea.org/countries) with aggregates flagged: World, OECD Total/Europe/Americas/Asia Oceania, IEA Total, EU27, Africa, Asia, China including Hong Kong, Eurasia. Each entry lists the stats code, the Monthly Electricity Statistics display name and the prices code it maps to, plus every alias `data` accepts. (Cost: 5 credit)
- **`energy/data`** (Data): Observations from one free IEA dataset for the given countries (ISO3 or IEA names, required, up to 50), optionally filtered by products, flows (balance flows or price sectors), indicators (data-browser indicators such as TFCbySource, ElecGenByFuel, CO2BySector) and year range; paged with an opaque cursor over a deterministic ordering. Values are decimal strings with the source unit; null values stay null. Paid and non-CC dataset ids fail with license_restricted and the product/purchase page. (Cost: 5 credit)
- **`energy/dataset`** (Dataset): One dataset's metadata with a live probe of api.iea.org: year_min/year_max actually served, last_updated (MES latest published month or prices updated_at), coverage count, license, endpoint and cadence. Refused datasets are described but flagged. (Cost: 5 credit)
- **`energy/datasets`** (Datasets): Catalog of IEA datasets: every free CC BY 4.0 dataset served by api.iea.org (energy balances, electricity and heat, oil, gas, CO2 from fuel combustion, monthly electricity statistics, energy prices, monthly oil prices) plus the paid and account-gated products that `data` refuses, each with its license. No network call; `last_updated` is null here and probed live by `dataset`. (Cost: 5 credit)

### NPI Registry (`npiregistry-cms-hhs-gov`)

Public CMS healthcare provider business identities, taxonomy and practice locations.

- **`providers/locations`** (Locations): Practice locations for one 10-digit NPI: the primary practice location plus every secondary practice location NPPES lists, with phone/fax, and the mailing address separately. Same source record as provider, shaped for where-does-this-provider-practise questions. (Cost: 5 credit)
- **`providers/provider`** (Provider): Full NPPES record for one 10-digit NPI: entity type, name, credential, status, enumeration and update dates, all taxonomies (specialties) with the primary flagged, mailing and practice addresses, secondary practice locations, other/DBA names, Medicaid and payer identifiers, and health-information-exchange endpoints. An unknown NPI is a not_found error. (Cost: 5 credit)
- **`providers/search`** (Search): Search the CMS NPPES NPI Registry for healthcare providers (individuals or organizations) by name, organization, taxonomy/specialty, city, state, postal code or country. Returns one page (limit 1-200, skip up to 1200) of full provider records: NPI, taxonomies with licenses, mailing and practice addresses, other names, payer identifiers and endpoints. Requires at least one of first_name, last_name, organization_name, taxonomy_description or postal_code. (Cost: 5 credit)

### Recreation.gov (`recreation-gov`)

Recreation.gov (US federal recreation reservations) read-only: search campgrounds, rec areas and permits by text, place or coordinates and stay dates; campground detail with rules, booking windows, rates and ratings; month availability grids; campsite listings and detail with open nights; visitor reviews; daily permit quota availability. Public anonymous JSON API of www.recreation.gov; availability and prices are snapshots, base fees only.

- **`camping-availability/campground`** (Campground): Details, rules and prices for a campground_id from `search`. (Cost: 5 credit)
- **`camping-availability/campground_availability`** (Campground availability): Which nights and which sites are open at a campground in a given month; distinguish reserved from closed and not-yet-released. (Cost: 5 credit)
- **`camping-availability/campsite`** (Campsite): Full detail and open nights for one campsite_id from `campsites` or `campground_availability`. (Cost: 5 credit)
- **`camping-availability/campsites`** (Campsites): List the sites of a campground_id, optionally filtered to a stay; then `campsite` for one site's full detail. (Cost: 5 credit)
- **`camping-availability/permit_availability`** (Permit availability): Remaining permit quota per entry point/zone and date for a permit_id from `search` (entity_type permit). (Cost: 5 credit)
- **`camping-availability/reviews`** (Reviews): Read what visitors said about a campground_id or campsite_id. (Cost: 5 credit)
- **`camping-availability/search`** (Search): Start here to find a campground_id / permit_id / rec area id by name or place; then call `campground`, `campsites`, `campground_availability` or `permit_availability`. (Cost: 5 credit)
- **`camping-availability/suggest`** (Suggest): Resolve a partial or ambiguous name to an entity id or to coordinates before `search`. (Cost: 5 credit)

### SAM.gov (`sam-gov`)

US federal procurement notice search and detail, including agency, deadlines, attachments and amendment history.

- **`opportunities/detail`** (Detail): Fetch one SAM.gov contract opportunity by its 32-character notice id (the id in https://sam.gov/opp/{id}/view): full description, deadlines, NAICS, set-aside, place of performance, points of contact, award data, attachments (titles and download URLs only) and optionally the amendment history. (Cost: 5 credit)
- **`opportunities/search`** (Search): Search SAM.gov contract opportunities by keyword, agency, notice status, publication date, NAICS, set-aside, notice type and response deadline. Returns one page (default 20, max 100) with an opaque cursor for the next page. By default each hit is enriched with its full notice detail (NAICS, set-aside, place of performance, full description). (Cost: 5 credit)

### Florida Sunbiz (`search-sunbiz-org`)

Florida official entity name lists and business registration records, including source-labelled officers, registered agents and filing links.

- **`entities/entity`** (Entity): Look up a Florida corporate registration by document number. Returns filing attributes, source-labelled officer and registered-agent sections, annual report history and PDF links. Unsupported registration layouts fail explicitly. (Cost: 5 credit)
- **`entities/search`** (Search): Browse the official alphabetical entity name list from a query. Results can include nearby names, historical registrations and trademarks, not exact matches. Follow next_cursor for the next source page. (Cost: 5 credit)

### SEC EDGAR (`sec-gov`)

Official SEC company profiles, filings, filing sections, 13F holdings and XBRL concept facts.

- **`filings/company`** (Company): Resolve a ticker, CIK or company name to its EDGAR filer profile: CIK, name, tickers, exchanges, SIC, filer category, state of incorporation, fiscal year end, addresses, former names and filing counts. Start here to get the CIK the other functions accept. (Cost: 5 credit)
- **`filings/concept`** (Concept): Every reported value of one XBRL concept for a filer (Revenues, NetIncomeLoss, Assets, EarningsPerShareDiluted ...) straight from the SEC's companyconcept API: value, period, unit, fiscal year and period, the form and accession it came from. Newest period first. (Cost: 5 credit)
- **`filings/filing`** (Filing): One filing by accession number: its submission metadata (form, dates, 8-K items) and every document in the filing folder with size and direct URL (primary document, exhibits, XBRL instance, full submission text). (Cost: 5 credit)
- **`filings/filings`** (Filings): List a filer's EDGAR filings newest first, filtered by form type (10-K, 10-Q, 8-K, S-1, 13F-HR, 4, DEF 14A ...) and filing date. Each record carries accession number, dates, 8-K item codes with captions, XBRL flags and direct document URLs. Reaches into older submission pages when `from` predates the recent window. (Cost: 5 credit)
- **`filings/holdings_13f`** (Holdings 13f): Form 13F-HR holdings of an institutional investment manager: every position from the XML information table (issuer, class, CUSIP, value, shares or principal, put/call, discretion, voting authority). Defaults to the latest 13F-HR; pick a quarter with report_date or a filing with accession_number. Values are whole USD for filings since 2023-01-03 and thousands before. (Cost: 5 credit)
- **`filings/search`** (Search): EDGAR full-text search across every filer since 2001: filter by phrase, form types, filing-date range and CIK. Returns 100 hits per page with accession number, form, filer names and CIKs, 8-K item codes, period and direct document URLs. Use it for cross-company questions such as 8-K Item 2.02 filings this quarter. Pass `snippets` to also fetch the matched document of the first hits and return the sentences containing the query (EDGAR's index returns no highlights itself). (Cost: 5 credit)
- **`filings/sections`** (Sections): Item sections of a 10-K or 10-Q as plain text: Item 1 Business, 1A Risk Factors, 7 MD&A, 8 Financial Statements and so on (10-Q items carry their Part). Defaults to the filer's latest 10-K; pass form=10-Q or an accession number for another report, and items to keep only some sections. (Cost: 5 credit)

### IBGE service data API (`servicodados-ibge-gov-br`)

Brazil's national statistics institute (IBGE) open JSON API at servicodados.ibge.gov.br: territorial codes (localidades), SIDRA aggregated statistics (agregados: official municipal / state / national population and household counts from the 2022 Census and the yearly population estimates, IPCA, PNAD, GDP and ~8,000 other tables), 2010 Census first-name frequencies and rankings, IBGE news/releases and release calendar, country profiles and indicators (paises), territorial meshes (malhas) and the CNAE activity classification. Anonymous, no key, Portuguese-language values as published.

- **`official-statistics/agregado_dados`** (Agregado dados): Official population or household count of a Brazilian municipality, state or the country (Census 2022: 4709/93 population, 4712/381 occupied households, 4712/382 residents in households; estimates: 6579/9324), IPCA (1737/63), PNAD unemployment (4099/4099), municipal GDP (5938/37), IPCA by group (7060/63 + classificacao 315) or any other table after agregado_metadados told you the ids. Resolve the municipality code first with localidades (e.g. São Bernardo do Campo = 3548708). Unknown agregado or variable ids are not_found; a level the table does not offer is invalid_input. (Cost: 5 credit)
- **`official-statistics/agregado_metadados`** (Agregado metadados): Pick the variavel ids, classificacao/categoria ids, nivel and periods to pass to agregado_dados. Unknown table ids are not_found. (Cost: 5 credit)
- **`official-statistics/agregados`** (Agregados): Find the agregado id (and then, with agregado_metadados, the variable and classification ids) before calling agregado_dados. Pass a query or at least one filter: the unfiltered catalog has ~8,000 tables. Rows carry only id and name (no period), and a query like `domicilios` with nivel N6 matches hundreds of Census tables ordered by id, so for the headline municipal population / household counts skip the search and call agregado_dados directly with 4709 (Census 2022 population), 4712 (Census 2022 occupied households and residents) or 6579 (yearly population estimates). (Cost: 5 credit)
- **`official-statistics/calendario`** (Calendario): When the next IPCA / PNAD / PIB release is scheduled, or the release history of a product. (Cost: 5 credit)
- **`official-statistics/cnae`** (Cnae): Decode a CNAE code from a company registry (7-digit subclasse 0111301, 5-digit classe 01113) or browse the hierarchy. (Cost: 5 credit)
- **`official-statistics/localidade`** (Localidade): Turn a municipality or state code into its name and hierarchy (microrregiao, mesorregiao, regiao imediata/intermediaria, UF, regiao), e.g. to label agregados results or join with other Brazilian sources. (Cost: 5 credit)
- **`official-statistics/localidades`** (Localidades): Resolve IBGE codes before querying agregados (N3 = estado id, N6 = municipio id), enumerate the municipalities of a state, or find a municipality by (partial, accent-insensitive) name. municipios, distritos and subdistritos require a parent so one call never fetches the 5,570-row national list. (Cost: 5 credit)
- **`official-statistics/malha`** (Malha): Draw or geo-join a Brazilian state, municipality or region; get its centroid and area in km2. Use qualidade=minima unless you need detailed geometry (maxima meshes are megabytes). (Cost: 5 credit)
- **`official-statistics/nomes`** (Nomes): How common a Brazilian first name is, how its popularity changed by decade, or where in Brazil it concentrates. (Cost: 5 credit)
- **`official-statistics/nomes_ranking`** (Nomes ranking): Most common names in Brazil or a state, by decade or sex. (Cost: 5 credit)
- **`official-statistics/noticias`** (Noticias): Recent IBGE releases (IPCA, PNAD, PIB...), news about a product or matching a keyword. Follow next_page until null. (Cost: 5 credit)
- **`official-statistics/paises`** (Paises): A country fact sheet or a UN-sourced indicator series (GDP per capita, population, life expectancy...) as IBGE republishes them, for Brazil or any of 193 countries. (Cost: 5 credit)

### Colorado Secretary of State business database (`sos-state-co-us`)

Colorado Secretary of State business database (the live registry at www.sos.state.co.us/biz): business name, ID and document-number search, entity summary with periodic report month and registered agent, and the filing history with document links and periodic-report due dates.

- **`entities/entity`** (Entity): You have an entity_id from `search` (or a Colorado SOS ID number) and need the current record. (Cost: 3 credit)
- **`entities/filings`** (Filings): You need due dates, filed documents or the event timeline for an entity_id from `search` or `entity`. (Cost: 5 credit)
- **`entities/search`** (Search): Start here to find the 11-digit entity_id for `entity` and `filings`. (Cost: 5 credit)

### UK IPO trade mark register (`trademarks-ipo-gov-uk`)

UK Intellectual Property Office trade mark register: search owners by name or UK postcode, list the UK national marks an owner holds, and read a trade mark's case detail (status, dates, goods and services, owners, representatives, publications) and case history (status, event and goods history).

- **`trade-marks/get_trade_mark`** (Get trade mark): When you have a trade mark number (UK000..., or UK009... for a comparable mark derived from an EU trade mark, domain 23). An unknown number is a not_found failure. (Cost: 5 credit)
- **`trade-marks/get_trade_mark_history`** (Get trade mark history): For assignment, ownership-change and status timelines of a known trade mark number. (Cost: 5 credit)
- **`trade-marks/list_owner_marks`** (List owner marks): After search_owners returned a client_id, or from the owner link on a case detail. Follow up with get_trade_mark for the full record. (Cost: 5 credit)
- **`trade-marks/search_owners`** (Search owners): Start here when you know a company or person name but not a trade mark number. An owner name that matches nothing returns zero owners, not an error. (Cost: 5 credit)

### Treasury Fiscal Data (`treasury-fiscal-data`)

US Treasury Fiscal Data: the national debt to the penny, daily cash balances and tax receipts, monthly receipts and outlays, Treasury auction results, interest rates and expense on the debt, the gold reserve and official exchange rates.

- **`auctions/results`** (Auction results): How an auction went: filter `security_type:eq:Note,security_term:eq:10-Year` and sort `-auction_date` for the last ten-year, then read `high_yield` and `bid_to_cover_ratio`. Bidder takedown comes as amounts, not shares: `indirect_bidder_accepted`, `direct_bidder_accepted` and `primary_dealer_accepted` in dollars, beside the `_tendered` amounts; an indirect share is `indirect_bidder_accepted` divided by `total_accepted`. `cusip:eq:` reaches one security. Bills report discount rates, notes and bonds yields, TIPS real yields, FRNs discount margins. (Cost: 1 credit)
- **`auctions/upcoming`** (Upcoming auctions): What the Treasury is about to sell: the auction calendar for the coming days with sizes. No history here - once an auction settles it moves to auctions/results. (Cost: 1 credit)
- **`daily-statement/deposits-and-withdrawals`** (Deposits and withdrawals): Where the government's cash came from and went each day: withheld income taxes, corporate taxes, Social Security benefits, Medicare, defence vendor payments, interest on the debt. The daily tax-receipt categories are the real-time read on the economy that the monthly statement only confirms later. (Cost: 1 credit)
- **`daily-statement/operating-cash-balance`** (Operating cash balance): The Treasury General Account balance - the government's cash on hand - which is what debt-ceiling coverage tracks day by day. For the current figure filter `account_type:eq:Treasury General Account (TGA) Closing Balance`, sort `-record_date` and read `open_today_bal`; `close_today_bal` is `null` on every row since 2022-04-18. The same balance is `close_today_bal` on `account_type:eq:Federal Reserve Account` rows through 2021-09-30 and on `account_type:eq:Treasury General Account (TGA)` rows for the six months between, so a series across the 2022 relabelling is those three filters stitched together. (Cost: 1 credit)
- **`daily-statement/public-debt-transactions`** (Public debt transactions): Gross issuance and redemption of Treasury securities by day: how much in bills was issued and how much rolled off. Net issuance is issues minus redemptions across the same security type. (Cost: 1 credit)
- **`debt/average-interest-rates`** (Average interest rates): What the government is paying on its debt, by kind of security: the average coupon on outstanding notes, the rate on bills, the blended rate on everything marketable. Filter `security_desc:eq:Treasury Notes` for one class, sort `-record_date` for the latest month. (Cost: 1 credit)
- **`debt/historical-outstanding`** (Historical debt outstanding): The long series: one figure per year from the first Treasury report in 1790. Use it for anything before 1993 or for a year-end comparison, filtering `record_fiscal_year:eq:<year>` rather than `record_date`; debt/to-the-penny is the daily figure. (Cost: 1 credit)
- **`debt/interest-expense`** (Interest expense): How much interest the debt costs in dollars, monthly, by kind of security. The fiscal-year-to-date column is the one quoted when interest is compared to other outlays; filter `record_calendar_month:eq:09` for fiscal-year totals. (Cost: 1 credit)
- **`debt/to-the-penny`** (Debt to the penny): The headline national debt figure: total public debt outstanding on a given day, to the cent. Sort `-record_date` with `page[size]=1` for today's number, or filter a date range for the series. For the figure before 1993 use debt/historical-outstanding. (Cost: 1 credit)
- **`monthly-statement/receipts-and-outlays`** (Receipts, outlays and deficit): The monthly deficit: filter `record_date:eq:2026-07-31,classification_desc:eq:July` and read `current_month_dfct_sur_amt` on the row with the higher `line_code_nbr` - the current fiscal year's July; the other row is the prior year's July for comparison. `classification_desc:eq:Year-to-Date` on the same record date gives the fiscal-year running total the same way. Published around the eighth business day of the following month. (Cost: 1 credit)
- **`rates/exchange`** (Treasury reporting rates of exchange): The official rate a US agency reports a foreign balance at, per quarter. Filter `country_currency_desc:eq:Euro Zone-Euro` or `country:eq:Japan`, add `effective_date:lte:<date>` for the date being reported, and sort `-record_date,-effective_date`, so the first row is the rate in force on that date rather than an amendment that came after it. For a market rate on a given day this is the wrong source. (Cost: 1 credit)
- **`reserves/gold`** (Gold reserve): How much gold the Treasury holds and where. The book value is the statutory price, not the market price, so a market valuation is the ounces times a spot price from elsewhere. Sort `-record_date` for the current holding. (Cost: 1 credit)

### USAspending (`usaspending-gov`)

Federal awards, transactions, recipients and agencies from USAspending.gov.

- **`agencies/agency`** (Agency): Toptier agency overview for a fiscal year by CGAC/FREC code (097 Department of Defense, 075 Health and Human Services, 036 Veterans Affairs): name, mission, website, subtier count, DEF codes in use and the fiscal year's award obligations and transaction count. (Cost: 5 credit)
- **`awards/award`** (Award): One USAspending prime award by generated_unique_award_id (CONT_AWD_…, CONT_IDV_…, ASST_NON_…, ASST_AGG_…) or numeric internal id: identifiers, type, agencies, recipient with location, obligations and outlays, options, period of performance, place of performance, NAICS/PSC or CFDA, parent IDV, subaward totals and last modified date. (Cost: 5 credit)
- **`awards/award_search`** (Award search): Search USAspending prime awards by keyword, awarding/funding agency, recipient name or UEI, action-date window, place of performance, NAICS, PSC and award amount within one award family (contracts, IDVs, grants, loans, direct payments or other). One page (default 20, max 100) of summary award records with an opaque cursor for the next page; add `award` for the full record. (Cost: 5 credit)
- **`awards/idv_children`** (Idv children): Awards issued under an indefinite delivery vehicle: child awards (orders), child IDVs or grandchild awards, newest period start first, with obligated amount and period of performance. Paged with a cursor. (Cost: 5 credit)
- **`awards/subawards`** (Subawards): Subawards reported under one prime award (FSRS data), newest first: subaward number, sub-recipient name, amount, action date and description. Paged with a cursor; an award with no subawards answers an empty page with a warning. (Cost: 5 credit)
- **`awards/transactions`** (Transactions): Transactions (individual actions and modifications) of one award, newest action first: obligation per action (negative for de-obligations), action type, modification number and description. Paged with a cursor. (Cost: 5 credit)
- **`recipients/recipient`** (Recipient): Recipient profile by USAspending recipient_id (hash with -C/-P/-R level) or 12-character UEI: names, identifiers, parent, business types, location and transaction obligations for the latest 12 months or a fiscal year, plus per-fiscal-year obligations for the years requested. (Cost: 5 credit)

### USPTO patents, trademarks and assignments (`uspto-gov`)

United States Patent and Trademark Office public records: Patent Public Search (full-text patent and pre-grant publication search and bibliographic documents), Trademark Search (word-mark search), TSDR trademark status records by serial or registration number, and Assignment Center ownership records for patents and trademarks. Anonymous, stateless JSON APIs behind the USPTO web applications; US coverage only.

- **`intellectual-property/assignments`** (Assignments): You need who owns or has a security interest in a patent or trademark, or the reel/frame of a recorded assignment. (Cost: 5 credit)
- **`intellectual-property/patent_document`** (Patent document): You have a patent number, publication number or ppubs guid and need the record itself. (Cost: 5 credit)
- **`intellectual-property/patent_search`** (Patent search): Start here to find patents or publications by title, number, assignee, inventor or classification; pass `patents[].guid` to `patent_document`. (Cost: 5 credit)
- **`intellectual-property/trademark_search`** (Trademark search): Find trademark serial numbers by mark text; pass `hits[].serial_number` to `trademark_status` or `assignments`. (Cost: 5 credit)
- **`intellectual-property/trademark_status`** (Trademark status): You have a serial or registration number and need the current status and parties of the mark. (Cost: 5 credit)

### V-Dem (`v-dem-net`)

Official V-Dem democracy indices, codebook metadata, country crosswalk and regime transformation episodes.

- **`democracy/countries`** (Countries): V-Dem country crosswalk (183 countries served by the graphing API): country_id, country_text_id, name, ISO3 or null with historical/non-ISO entities flagged, coded year span and V-Dem region; optional name/code/region filter. Embedded snapshot; no live request. (Cost: 5 credit)
- **`democracy/data`** (Data): Country-year observations for up to 5 variables and 50 countries (ISO3 or V-Dem country_text_id) from v-dem.net's official graphing API for the pinned release (v16, 1789-2025), optionally year-bounded, with codelow/codehigh bounds. Sorted by variable, country_id, year; paginated with next_cursor. (Cost: 5 credit)
- **`democracy/datasets`** (Datasets): Current V-Dem dataset releases read live from v-dem.net (Country-Year Core, Country-Year Full+Others, Country-Date, Coder-Level: version, published month, download landing page) plus the ERT and V-Party companion datasets, each with codebook URL, citation, CC BY-SA 4.0 license and terms URL. (Cost: 5 credit)
- **`democracy/ert`** (Ert): Episodes of Regime Transformation (ERT v16) country-year records for up to 20 countries from the V-Dem Institute's official GitHub csv: regime (v2x_regime), polyarchy with bounds, democratization/autocratization episode ids, start/end years and outcomes. Default returns episode years only; rows=all returns every country-year. (Cost: 5 credit)
- **`democracy/variable`** (Variable): Live codebook entry for one V-Dem variable tag (question, clarification, scale, aggregation, source variables, data-release line) from v-dem.net, checked against the pinned release; a tag absent from that release is an input error naming the release that introduced or dropped it. (Cost: 5 credit)
- **`democracy/variables`** (Variables): Search the V-Dem codebook (404 variables served by v-dem.net's graphing API) by tag, name or question text, filtered by thematic section, index level (high, mid, indicator, other) and the release a variable belongs to. Returns codebook metadata from a dated embedded snapshot of the official codebook entries; no live request. (Cost: 5 credit)

### WHO Global Health Observatory (`who-int`)

Official WHO indicator search, dimension codes and paginated observations with source licensing and attribution.

- **`indicators/data`** (Data): Fetch one page of observations for a GHO indicator, filtered by spatial type (COUNTRY, REGION, WORLDBANKINCOMEGROUP, GLOBAL), ISO3/region codes, year range and Dim1/Dim2/Dim3 codes (sex, age group, ...). Each record keeps the source Id, numeric value with low/high bounds as decimal strings, the display string, comments, data source and modification date; source_updated_at is the indicator's newest modification date. Unknown indicator codes fail with not_found. (Cost: 5 credit)
- **`indicators/dimensions`** (Dimensions): List the values of one GHO dimension (COUNTRY, REGION, WORLDBANKINCOMEGROUP, SEX, AGEGROUP, ...): code, title and parent (countries carry their WHO region). Omit dimension_code to list the dimensions themselves. Unknown dimension codes fail with not_found. (Cost: 5 credit)
- **`indicators/indicators`** (Indicators): Search the GHO indicator catalogue by words in the indicator name or code (case-insensitive substring; empty query lists everything). Returns one page of indicator records (code, official name, language, unit as written in the name, data URL) with a cursor for the next page. (Cost: 5 credit)

### World Happiness Report (`worldhappiness-report`)

Official WHR dashboard aggregate rankings, country-year indicators and edition appendix metadata; not Gallup respondent microdata.

- **`happiness/countries`** (Countries): List the dashboard's geographies as ISO 3166-1 alpha-3 codes with display names (164 entries incl. XKX Kosovo, TWN Taiwan Province of China, HKG Hong Kong SAR of China). Use it to resolve names before calling rankings or panel. (Cost: 5 credit)
- **`happiness/editions`** (Editions): List every World Happiness Report edition (2012 onwards) with its appendix and data file downloads, the citation string and the licence note, read live from worldhappiness.report/data-sharing. (Cost: 5 credit)
- **`happiness/panel`** (Panel): Gallup World Poll country-year panel for up to 10 countries (ISO3) from the dashboard country view: annual life ladder, three-year average, GDP per capita, social support, healthy life expectancy, freedom, generosity, corruption, positive/negative affect, benevolence and inequality, 2005 onwards. Only the current vintage is served; edition, if given, must match it. (Cost: 5 credit)
- **`happiness/rankings`** (Rankings): One page of a World Happiness Report edition's ranking table (three-year average Cantril ladder score and rank) with the six explanatory-factor shares and raw factor levels from the dashboard country view. edition N reads dashboard data year N-1. Paginate with next_cursor; filter to ISO3 codes with countries. (Cost: 5 credit)


