---
category: "finance"
type: reference-card
provider_count: 17
---

# Category: finance

> Market prices, financial statements, ownership and macro rates.

**Providers in this category:** 17

| Provider ID | Provider Name | Capabilities | Tier | Cost | Bypass Route |
|---|---|---|---|---|---|
| `b3-com-br` | **B3 listed companies and indices** | 9 | Proprietary Commercial B2B Data Brokers | Credits Required or Paid Vendor Key | Use Alexandria credits or direct vendor account |
| `bcb-gov-br` | **Banco Central do Brasil open data** | 10 | Public Government & Intergovernmental Data | 0 Credits (Public API) | Direct official REST API |
| `benzinga` | **Benzinga** | 11 | Proprietary Commercial B2B Data Brokers | Credits Required or Paid Vendor Key | Use Alexandria credits or direct vendor account |
| `cftc` | **CFTC** | 7 | Public Government & Intergovernmental Data | 0 Credits (Public API) | Direct official REST API |
| `cftc-gov` | **CFTC Commitments of Traders** | 8 | Public Government & Intergovernmental Data | 0 Credits (Public API) | Direct official REST API |
| `data-imf-org` | **IMF Data** | 4 | Public Government & Intergovernmental Data | 0 Credits (Public API) | Direct official REST API |
| `data-worldbank-org` | **World Bank Data** | 11 | Public Government & Intergovernmental Data | 0 Credits (Public API) | Direct official REST API |
| `eia-gov` | **US Energy Information Administration** | 3 | Public Government & Intergovernmental Data | 0 Credits (Public API) | Direct official REST API |
| `finance-yahoo-com` | **Yahoo Finance** | 4 | Public Commercial Web / Frontend JSON Endpoints | 0 Credits (Direct Web / Scraping Bypass) | Direct unauthenticated web fetch or lightweight house scraper |
| `fiscal-ai` | **Fiscal.ai** | 34 | Proprietary Commercial B2B Data Brokers | Credits Required or Paid Vendor Key | Use Alexandria credits or direct vendor account |
| `fiscaldata-treasury-gov` | **US Treasury Fiscal Data** | 5 | Public Government & Intergovernmental Data | 0 Credits (Public API) | Direct official REST API |
| `fred` | **FRED** | 31 | Public Government & Intergovernmental Data | 0 Credits (Public API) | Direct official REST API |
| `fred-stlouisfed-org` | **FRED (Federal Reserve Economic Data)** | 10 | Public Government & Intergovernmental Data | 0 Credits (Public API) | Direct official REST API |
| `nasdaq-com` | **Nasdaq.com news feeds and articles** | 6 | Proprietary Commercial B2B Data Brokers | Credits Required or Paid Vendor Key | Use Alexandria credits or direct vendor account |
| `sec-gov` | **SEC EDGAR** | 7 | Public Government & Intergovernmental Data | 0 Credits (Public API) | Direct official REST API |
| `servicodados-ibge-gov-br` | **IBGE service data API** | 12 | Public Government & Intergovernmental Data | 0 Credits (Public API) | Direct official REST API |
| `treasury-fiscal-data` | **Treasury Fiscal Data** | 12 | Public Government & Intergovernmental Data | 0 Credits (Public API) | Direct official REST API |

## Capabilities Overview

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

### Banco Central do Brasil open data (`bcb-gov-br`)

Banco Central do Brasil open data: SGS time series (Selic, CDI, IPCA, IGP-M, IBC-Br, USD/BRL and ~3,600 more series by code), PTAX official exchange rates (USD and other currencies, by date or date range), Focus market expectations (IPCA, Selic, PIB, cambio: median, mean, standard deviation, respondents), PIX statistics (by municipality, aggregate, registered keys, DICT users), retail credit rates by institution, SPI settlement and payment-instrument statistics, currency in circulation, plus discovery of Olinda OData services and of the dadosabertos.bcb.gov.br dataset catalogue. Anonymous JSON APIs; no key or session.

- **`economic-data/credit_rates`** (Credit rates): Compare bank lending rates (mortgage, payroll loans, vehicle, credit card, ...) for a month. [Cost: 5 credit]  
  *Options:* `mes` *(required)*, `modalidade`, `skip`, `top`
- **`economic-data/datasets_search`** (Datasets search): Find an SGS series code or an Olinda service name before calling `sgs_series` or `olinda_service`. [Cost: 5 credit]  
  *Options:* `q` *(required)*, `rows`, `start`
- **`economic-data/focus_expectations`** (Focus expectations): Market consensus for inflation, policy rate, GDP or FX by reference month/year or Copom meeting. [Cost: 5 credit]  
  *Options:* `base_calculo`, `data`, `data_referencia`, `entity_set`, `indicador`, `reuniao`, `skip`, `top`
- **`economic-data/olinda_service`** (Olinda service): See which entity sets and functions an Olinda service exposes before querying it. [Cost: 5 credit]  
  *Options:* `servico` *(required)*
- **`economic-data/payment_statistics`** (Payment statistics): SPI settlement volumes, payment-instrument mix, cash in circulation. [Cost: 5 credit]  
  *Options:* `ano_mes`, `dataset` *(required)*, `skip`, `top`
- **`economic-data/pix_statistics`** (Pix statistics): PIX volumes by municipality or segment, registered keys, DICT users. [Cost: 5 credit]  
  *Options:* `ano_mes`, `data`, `dataset` *(required)*, `estado`, `municipio_ibge`, `skip`, `top`
- **`economic-data/ptax_currencies`** (Ptax currencies): Discover which currency symbols `ptax_currency` accepts. [Cost: 5 credit]  
  *Options:* None
- **`economic-data/ptax_currency`** (Ptax currency): Rates for EUR, GBP, JPY, ... against BRL. Take `moeda` from `ptax_currencies`. [Cost: 5 credit]  
  *Options:* `date`, `end_date`, `moeda` *(required)*, `skip`, `start_date`, `top`
- **`economic-data/ptax_usd`** (Ptax usd): USD/BRL PTAX for a day or a range. Use `ptax_currency` for other currencies. [Cost: 5 credit]  
  *Options:* `date`, `end_date`, `skip`, `start_date`, `top`
- **`economic-data/sgs_series`** (Sgs series): Get the numbers for a known SGS code. Find codes with `datasets_search` (CKAN `codigo_sgs`). [Cost: 5 credit]  
  *Options:* `codigo` *(required)*, `data_final`, `data_inicial`, `ultimos`

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

### CFTC (`cftc`)

Commitments of Traders: weekly futures and options positioning by trader category - speculators, hedgers, managed money, dealers, leveraged funds, index traders - for every reportable US futures market, from the CFTC.

- **`disaggregated/combined`** (Disaggregated report, futures and options combined): The disaggregated split with options included. Prefer it for crude, natural gas and gold, where a large share of managed-money exposure is held through options and the futures-only figure understates it. [Cost: 1 credit]  
  *Options:* `cftc_contract_market_code`, `market_and_exchange_names`, `commodity_name`, `cftc_market_code`, `commodity_group_name`, `report_date_as_yyyy_mm_dd`, `yyyy_report_week_ww`, `$where`, `$order`, `$limit`, `$offset`, `$select`
- **`disaggregated/futures-only`** (Disaggregated report, futures only): Physical commodities - agriculture, energy, metals - when the question is which kind of participant is positioned, not just speculator versus hedger: managed money is the fund positioning most reports quote, swap dealers carry the index-fund flow, producers and merchants are the physical hedge. Financial futures are not here; use the financial report. [Cost: 1 credit]  
  *Options:* `cftc_contract_market_code`, `market_and_exchange_names`, `commodity_name`, `cftc_market_code`, `commodity_group_name`, `report_date_as_yyyy_mm_dd`, `yyyy_report_week_ww`, `$where`, `$order`, `$limit`, `$offset`, `$select`
- **`financial/combined`** (Financial futures report, futures and options combined): The financial split with options included, which matters most for equity index and Treasury futures, where options open interest is a large fraction of the total. [Cost: 1 credit]  
  *Options:* `cftc_contract_market_code`, `market_and_exchange_names`, `commodity_name`, `cftc_market_code`, `commodity_group_name`, `report_date_as_yyyy_mm_dd`, `yyyy_report_week_ww`, `$where`, `$order`, `$limit`, `$offset`, `$select`
- **`financial/futures-only`** (Financial futures report, futures only): Currencies, Treasury and SOFR futures, equity index futures, VIX: who is long the dollar, how short leveraged funds are in ten-year notes, how asset managers are positioned in S&P futures. Leveraged funds is the hedge-fund column; asset managers is pensions, insurers and mutual funds. [Cost: 1 credit]  
  *Options:* `cftc_contract_market_code`, `market_and_exchange_names`, `commodity_name`, `cftc_market_code`, `commodity_group_name`, `report_date_as_yyyy_mm_dd`, `yyyy_report_week_ww`, `$where`, `$order`, `$limit`, `$offset`, `$select`
- **`legacy/combined`** (Legacy report, futures and options combined): The legacy split with options included, which is the fuller picture of a group's exposure in markets where options are liquid - energy, metals, rates. The row id ends in C rather than F; everything else reads the same as futures-only. [Cost: 1 credit]  
  *Options:* `cftc_contract_market_code`, `market_and_exchange_names`, `commodity_name`, `cftc_market_code`, `commodity_group_name`, `report_date_as_yyyy_mm_dd`, `yyyy_report_week_ww`, `$where`, `$order`, `$limit`, `$offset`, `$select`
- **`legacy/futures-only`** (Legacy report, futures only): The report most commentary means by 'the COT': speculators versus hedgers, futures positions only, back to 1986 for every market. Filter by `cftc_contract_market_code` or `commodity_name` and order by `report_date_as_yyyy_mm_dd DESC` for the latest week. Use legacy/combined when options positions matter, and the disaggregated or financial report when the two-way speculator/hedger split is too coarse. [Cost: 1 credit]  
  *Options:* `cftc_contract_market_code`, `market_and_exchange_names`, `commodity_name`, `cftc_market_code`, `commodity_group_name`, `report_date_as_yyyy_mm_dd`, `yyyy_report_week_ww`, `$where`, `$order`, `$limit`, `$offset`, `$select`
- **`supplemental/index-traders`** (Supplemental report, commodity index traders): Thirteen agricultural markets - corn, wheat, soybeans, sugar, coffee, cocoa, cotton, cattle, hogs - when the question is how much of the length is passive index money rather than a directional view. Nowhere else in the COT is index-trader positioning stated on its own. [Cost: 1 credit]  
  *Options:* `cftc_contract_market_code`, `market_and_exchange_names`, `commodity_name`, `cftc_market_code`, `commodity_group_name`, `report_date_as_yyyy_mm_dd`, `yyyy_report_week_ww`, `$where`, `$order`, `$limit`, `$offset`, `$select`

### CFTC Commitments of Traders (`cftc-gov`)

US Commodity Futures Trading Commission Commitments of Traders (COT) reports from the public reporting SODA API (publicreporting.cftc.gov): the seven weekly datasets (Legacy, Disaggregated and Traders in Financial Futures, each futures-only and combined, plus the Supplemental commodity index report) with filters, column projection, deterministic recent-first order and offset pagination, and a contract-market discovery function.

- **`commitments-of-traders/disaggregated_combined`** (Disaggregated combined): Positions and open interest from the CFTC Disaggregated - Combined report for one or many markets and weeks. Use `markets` first to find contract_market_code values; use `fields` to keep the payload small. [Cost: 5 credit]  
  *Options:* `commodity_group_name`, `commodity_name`, `commodity_subgroup_name`, `contract_market_code`, `cursor`, `exchange_code`, `fields`, `from`, `page_size`, `query`, `report_date`, `sort`, `to`
- **`commitments-of-traders/disaggregated_futures_only`** (Disaggregated futures only): Positions and open interest from the CFTC Disaggregated - Futures Only report for one or many markets and weeks. Use `markets` first to find contract_market_code values; use `fields` to keep the payload small. [Cost: 5 credit]  
  *Options:* `commodity_group_name`, `commodity_name`, `commodity_subgroup_name`, `contract_market_code`, `cursor`, `exchange_code`, `fields`, `from`, `page_size`, `query`, `report_date`, `sort`, `to`
- **`commitments-of-traders/legacy_combined`** (Legacy combined): Positions and open interest from the CFTC Legacy - Combined report for one or many markets and weeks. Use `markets` first to find contract_market_code values; use `fields` to keep the payload small. [Cost: 5 credit]  
  *Options:* `commodity_group_name`, `commodity_name`, `commodity_subgroup_name`, `contract_market_code`, `cursor`, `exchange_code`, `fields`, `from`, `page_size`, `query`, `report_date`, `sort`, `to`
- **`commitments-of-traders/legacy_futures_only`** (Legacy futures only): Positions and open interest from the CFTC Legacy - Futures Only report for one or many markets and weeks. Use `markets` first to find contract_market_code values; use `fields` to keep the payload small. [Cost: 5 credit]  
  *Options:* `commodity_group_name`, `commodity_name`, `commodity_subgroup_name`, `contract_market_code`, `cursor`, `exchange_code`, `fields`, `from`, `page_size`, `query`, `report_date`, `sort`, `to`
- **`commitments-of-traders/markets`** (Markets): Start here to find the contract_market_code (and exchange_code / commodity names) to pass to a report function, or to see which markets a dataset covers and how far back. [Cost: 5 credit]  
  *Options:* `commodity_group_name`, `cursor`, `exchange_code`, `page_size`, `query`, `report` *(required)*
- **`commitments-of-traders/supplemental`** (Supplemental): Positions and open interest from the CFTC Supplemental Commodity Index report for one or many markets and weeks. Use `markets` first to find contract_market_code values; use `fields` to keep the payload small. [Cost: 5 credit]  
  *Options:* `commodity_group_name`, `commodity_name`, `commodity_subgroup_name`, `contract_market_code`, `cursor`, `exchange_code`, `fields`, `from`, `page_size`, `query`, `report_date`, `sort`, `to`
- **`commitments-of-traders/tff_combined`** (Tff combined): Positions and open interest from the CFTC Traders in Financial Futures - Combined report for one or many markets and weeks. Use `markets` first to find contract_market_code values; use `fields` to keep the payload small. [Cost: 5 credit]  
  *Options:* `commodity_group_name`, `commodity_name`, `commodity_subgroup_name`, `contract_market_code`, `cursor`, `exchange_code`, `fields`, `from`, `page_size`, `query`, `report_date`, `sort`, `to`
- **`commitments-of-traders/tff_futures_only`** (Tff futures only): Positions and open interest from the CFTC Traders in Financial Futures - Futures Only report for one or many markets and weeks. Use `markets` first to find contract_market_code values; use `fields` to keep the payload small. [Cost: 5 credit]  
  *Options:* `commodity_group_name`, `commodity_name`, `commodity_subgroup_name`, `contract_market_code`, `cursor`, `exchange_code`, `fields`, `from`, `page_size`, `query`, `report_date`, `sort`, `to`

### IMF Data (`data-imf-org`)

IMF SDMX dataflows, structures, observations and World Economic Outlook editions.

- **`datasets/data`** (Data): Retrieve observations from any IMF dataflow (BOP current account, ER exchange rates, IL reserves, IMTS bilateral trade, CPI, GFS, FM, WEO) by dimension key. Codes are validated against the dataflow's availability; unknown codes fail with invalid_input listing valid ones. Observations carry source codes, unit, scale, status and dataset vintage; a valid key with no observations returns complete=true and no records. [Cost: 5 credit]  
  *Options:* `cursor`, `dataflow_id` *(required)*, `end_period`, `key`, `last_n_observations`, `page_size`, `start_period`
- **`datasets/dataflows`** (Dataflows): List IMF Data portal dataflows (WEO, BOP, ER, IMTS, CPI, GFS_*, FM and 200+ more, including frozen vintages) filtered by a free-text query over id, agency and name. Returns dataflow records with stable AGENCY:ID identifiers for structure and data. [Cost: 5 credit]  
  *Options:* `cursor`, `page_size`, `query`
- **`datasets/structure`** (Structure): Describe one dataflow: its dimensions in SDMX key order, the concept/codelist each one uses, the codes that currently carry data, attribute ids, series count and time coverage. Use before data to learn valid REF_AREA/INDICATOR/FREQ codes. [Cost: 5 credit]  
  *Options:* `dataflow_id` *(required)*
- **`datasets/weo`** (Weo): World Economic Outlook observations for one edition (2026-04 current, 2025-10, 2025-04, or `latest`), given WEO subject codes (NGDP_RPCH, PCPIPCH, LUR, GGXWDG_NGDP, BCA_NGDPD, ...) and ISO3 economy or WEO group codes. Every row carries the edition, publication date and is_estimate (year after LATEST_ACTUAL_ANNUAL_DATA), so two editions can be compared for revisions. [Cost: 5 credit]  
  *Options:* `country_codes` *(required)*, `cursor`, `edition` *(required)*, `page_size`, `subject_codes` *(required)*, `year_from`, `year_to`

### World Bank Data (`data-worldbank-org`)

World Bank Indicators API v2: database catalog, indicator discovery, economies and aggregates, reference lists, observations (classic and dimension paths including International Debt Statistics) and extended series/economy metadata. Keyless public API.

- **`indicators/concept_values`** (Concept values): Enumerate what a source can be queried by, e.g. IDS creditor codes for `source_data`. [Cost: 5 credit]  
  *Options:* `concept` *(required)*, `page`, `per_page`, `source_id` *(required)*
- **`indicators/countries`** (Countries): Resolve country codes for `data`, or enumerate the members of a region or income group. [Cost: 5 credit]  
  *Options:* `include_aggregates`, `income_level`, `lending_type`, `page`, `per_page`, `region`
- **`indicators/country`** (Country): Confirm a code and read its region, income level and lending type before querying data. [Cost: 5 credit]  
  *Options:* `country_code` *(required)*
- **`indicators/data`** (Data): Fetch the actual numbers once you know the indicator id(s) and country code(s). [Cost: 5 credit]  
  *Options:* `country_codes`, `date`, `footnote`, `gapfill`, `indicator_ids` *(required)*, `mrv`, `page`, `per_page`, `source_id`
- **`indicators/indicator`** (Indicator): You have an indicator id and need its definition or its source before calling `data`. [Cost: 5 credit]  
  *Options:* `indicator_id` *(required)*, `source_id`
- **`indicators/indicators`** (Indicators): Discover indicator ids for `indicator` and `data`; browse a topic (see `reference` kind topic) or a database. [Cost: 5 credit]  
  *Options:* `page`, `per_page`, `query`, `source_id`, `topic_id`
- **`indicators/metadata`** (Metadata): Read the definition, license or methodology notes behind a series, or an economy's statistical profile. [Cost: 5 credit]  
  *Options:* `concept` *(required)*, `id` *(required)*, `source_id` *(required)*
- **`indicators/reference`** (Reference): Find valid `topic_id`, `region`, `income_level` or `lending_type` codes. [Cost: 5 credit]  
  *Options:* `code`, `kind` *(required)*
- **`indicators/source_concepts`** (Source concepts): Before `concept_values` or `source_data` on an unfamiliar source. [Cost: 5 credit]  
  *Options:* `source_id` *(required)*
- **`indicators/source_data`** (Source data): Use for IDS (source 6) series, or when you want the dimension-keyed form of a series from any source. [Cost: 5 credit]  
  *Options:* `counterpart_area`, `country_codes`, `page`, `per_page`, `series_ids` *(required)*, `source_id` *(required)*, `time_ids`
- **`indicators/sources`** (Sources): Start here to find the source id of a database (2 WDI, 6 IDS, 15 GEM) or to read its vintage. [Cost: 5 credit]  
  *Options:* `source_id`

### US Energy Information Administration (`eia-gov`)

Discover EIA energy data routes, enumerate facet values and retrieve energy observations with source units and labels.

- **`energy-data/data`** (Data): One page of observations from an EIA route (`<route>/data`) at a frequency, filtered by facet codes and a period range, sorted, with offset pagination up to 5000 rows per page. Each record carries the period, every facet as {code, name}, requested values as source strings, units copied from the source, extra source flags, and the series id when the route has one. Period formats follow the frequency (YYYY, YYYY-Qn, YYYY-MM, YYYY-MM-DD, YYYY-MM-DDTHH). [Cost: 5 credit]  
  *Options:* `api_key`, `cursor`, `data_columns`, `end`, `facets`, `frequency` *(required)*, `page_size`, `route` *(required)*, `sort`, `start`
- **`energy-data/facet_values`** (Facet values): List every value of one facet on a route (for example `sectorid` on `electricity/retail-sales`, or `series` on `petroleum/pri/spt`) with its code, readable name and alias, so `data` can be filtered by code. [Cost: 5 credit]  
  *Options:* `api_key`, `facet_id` *(required)*, `route` *(required)*
- **`energy-data/routes`** (Routes): Navigate the EIA API v2 route hierarchy. Given a route path (or none for the root) returns that route's metadata: child routes, frequencies with period formats, facet ids and data columns with units. Use it to find the route, frequency, facets and columns that `data` needs. [Cost: 5 credit]  
  *Options:* `api_key`, `cursor`, `page_size`, `path`

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

### US Treasury Fiscal Data (`fiscaldata-treasury-gov`)

US Treasury Fiscal Data (fiscaldata.treasury.gov): the dataset catalog, filtered rows from any of the ~180 API tables (Debt to the Penny, Daily and Monthly Treasury Statements, auctions, average interest rates, interest expense, gold reserve, rates of exchange, MSPD, ...), latest observations of the headline tables, the release calendar and published report files.

- **`fiscal-data/data`** (Data): Any question that needs the actual numbers from a Fiscal Data table. Use `datasets` first when the endpoint path is unknown; use `latest` for the newest rows of a headline table. [Cost: 5 credit]  
  *Options:* `cursor`, `endpoint` *(required)*, `fields`, `filter`, `page_size`, `sort`
- **`fiscal-data/datasets`** (Datasets): Start here to find the `endpoint` for `data` or the `dataset_id` for `release_calendar` and `published_reports`. [Cost: 5 credit]  
  *Options:* `cursor`, `dataset_id`, `page_size`, `query`
- **`fiscal-data/latest`** (Latest): Current values without knowing the endpoint path: today's national debt, the latest cash balance, the last auctions, the current exchange rate table. [Cost: 5 credit]  
  *Options:* `filter`, `n`, `table` *(required)*
- **`fiscal-data/published_reports`** (Published reports): To get the official PDF/XLS of a statement for a given date rather than the table rows. [Cost: 5 credit]  
  *Options:* `cursor`, `dataset_id` *(required)*, `from`, `page_size`, `path_contains`, `to`
- **`fiscal-data/release_calendar`** (Release calendar): When a dataset will next be updated, or whether today's release is already out. [Cost: 5 credit]  
  *Options:* `cursor`, `dataset_id`, `from`, `page_size`, `to`

### FRED (`fred`)

US and international economic time series from the Federal Reserve Bank of St. Louis: rates, prices, employment, output and money, with the full revision history behind each figure.

- **`categories/category`** (Category): Call to confirm what a category id is before walking down from it, or with no argument to land on the root. The only category endpoint that takes no real-time period, so what it returns is always the current name. [Cost: 0 credit]  
  *Options:* `category_id`
- **`categories/children`** (Child categories): The rung of the walk from the root to a series list. It descends one level per call, so getting from the root to a leaf takes several. Nothing here pages: a category with many children returns all of them. [Cost: 0 credit]  
  *Options:* `category_id`, `realtime_start`, `realtime_end`
- **`categories/related`** (Related categories): Call for the cross-links the hierarchy cannot express. Most categories have none, so an empty array is the normal answer here and not a sign the call went wrong. [Cost: 0 credit]  
  *Options:* `category_id` *(required)*, `realtime_start`, `realtime_end`
- **`categories/related-tags`** (Category related tags): Call to narrow a category further once you already have one tag: it returns the tags that co-occur with `tag_names` inside this category. It narrows rather than suggesting alternatives, and unlike `categories/tags` the `tag_names` argument is mandatory. [Cost: 0 credit]  
  *Options:* `category_id` *(required)*, `realtime_start`, `realtime_end`, `tag_names` *(required)*, `exclude_tag_names`, `tag_group_id`, `search_text`, `limit`, `offset`, `order_by`, `sort_order`
- **`categories/series`** (Category series): The bottom of the category walk: turns a category id into series ids. `limit` defaults to its maximum of 1000, so narrow with `tag_names` or `filter_variable` rather than expecting a small first page. [Cost: 1 credit]  
  *Options:* `category_id` *(required)*, `realtime_start`, `realtime_end`, `limit`, `offset`, `order_by`, `sort_order`, `filter_variable`, `filter_value`, `tag_names`, `exclude_tag_names`
- **`categories/tags`** (Category tags): Call to see what the series in a category are labelled with before filtering them. `series_count` on each tag counts only series in this category, not every series carrying the tag. [Cost: 0 credit]  
  *Options:* `category_id` *(required)*, `realtime_start`, `realtime_end`, `tag_names`, `tag_group_id`, `search_text`, `limit`, `offset`, `order_by`, `sort_order`
- **`releases/dates`** (All release dates): Call for the economic calendar across all releases at once. Not symmetric with `releases/release-dates` despite the near-identical name: this one sorts descending by default, carries `release_name`, and only reaches back to the start of the current year unless told otherwise. [Cost: 0 credit]  
  *Options:* `realtime_start`, `realtime_end`, `limit`, `offset`, `order_by`, `sort_order`, `include_release_dates_with_no_data`
- **`releases/related-tags`** (Release related tags): Call to narrow within a release once you have one tag. Two independently required arguments here, `release_id` and `tag_names`; the second reads like an optional filter and is not. [Cost: 0 credit]  
  *Options:* `release_id` *(required)*, `realtime_start`, `realtime_end`, `tag_names` *(required)*, `exclude_tag_names`, `tag_group_id`, `search_text`, `limit`, `offset`, `order_by`, `sort_order`
- **`releases/release`** (Release): Call to resolve a release id into a name and link. Widening the real-time period makes this single-release call return more than one record, one per interval in which the release's attributes differed. [Cost: 0 credit]  
  *Options:* `release_id` *(required)*, `realtime_start`, `realtime_end`
- **`releases/release-dates`** (Release dates): Call for one release's publication history. It defaults to the whole span back to 1776-07-04 rather than the current year, has no `order_by`, and omits `release_name` - three ways it differs from `releases/dates`. Set `include_release_dates_with_no_data` to get the next scheduled date. [Cost: 0 credit]  
  *Options:* `release_id` *(required)*, `realtime_start`, `realtime_end`, `limit`, `offset`, `sort_order`, `include_release_dates_with_no_data`
- **`releases/releases`** (Releases): The entry point for every other release capability: it is where a release name becomes the `release_id` they take. There are only a few hundred releases and `limit` defaults to 1000, so one call is usually the whole list. [Cost: 0 credit]  
  *Options:* `realtime_start`, `realtime_end`, `limit`, `offset`, `order_by`, `sort_order`
- **`releases/series`** (Release series): The bridge from a release to series ids: every series that arrives with this publication. A large release runs to thousands of series, so filter with `tag_names` or `filter_variable` rather than paging the whole thing. [Cost: 1 credit]  
  *Options:* `release_id` *(required)*, `realtime_start`, `realtime_end`, `limit`, `offset`, `order_by`, `sort_order`, `filter_variable`, `filter_value`, `tag_names`, `exclude_tag_names`
- **`releases/sources`** (Release sources): Call when the question is who publishes a release rather than what is in it. A release can have more than one source agency. [Cost: 0 credit]  
  *Options:* `release_id` *(required)*, `realtime_start`, `realtime_end`
- **`releases/tables`** (Release table): Call when the layout matters - which line of a published table a series sits on, and what nests under what. This is the only capability here that answers with a tree rather than a list, so a caller that walks `key` plus `paginated` has to special-case it: descend `elements`, then each element's `children`. [Cost: 1 credit]  
  *Options:* `release_id` *(required)*, `element_id`, `include_observation_values`, `observation_date`
- **`releases/tags`** (Release tags): Call to see how a release's series are labelled before filtering `releases/series` by tag. `tag_names` is optional here and required on `releases/related-tags` - same parameter, adjacent endpoints, opposite requiredness. [Cost: 0 credit]  
  *Options:* `release_id` *(required)*, `realtime_start`, `realtime_end`, `tag_names`, `tag_group_id`, `search_text`, `limit`, `offset`, `order_by`, `sort_order`
- **`series/categories`** (Series categories): Call to walk back up from a series you already have to the part of the tree it lives in, and from there to its peers. A series can sit in several categories. [Cost: 0 credit]  
  *Options:* `series_id` *(required)*, `realtime_start`, `realtime_end`
- **`series/observations`** (Series observations): The only capability in this provider that returns numbers; everything else exists to find the id it takes. Two independent time axes: `observation_start`/`observation_end` bound when the economy did the thing, `realtime_start`/`realtime_end` bound when FRED knew it. Leaving the real-time pair alone gives today's vintage only, so a question about revisions needs 1776-07-04 to 9999-12-31 or an explicit `vintage_dates`. [Cost: 1 credit]  
  *Options:* `series_id` *(required)*, `realtime_start`, `realtime_end`, `limit`, `offset`, `sort_order`, `observation_start`, `observation_end`, `units`, `frequency`, `aggregation_method`, `output_type`, `vintage_dates`
- **`series/release`** (Series release): Call to find which publication a series arrives in, then use that `release_id` for its calendar or its sibling series. Answering `when is this next updated` goes through here rather than through the series record. [Cost: 0 credit]  
  *Options:* `series_id` *(required)*, `realtime_start`, `realtime_end`
- **`series/search`** (Series search): The way in when all you have is words. Set `search_type` to series_id when the query is an id fragment rather than a description; the default full-text mode stems, so `UNRATE` under it matches on unrelated titles. Leave `order_by` and `sort_order` unset unless you mean to override the relevance ranking, because their defaults depend on each other. [Cost: 0 credit]  
  *Options:* `search_text` *(required)*, `search_type`, `realtime_start`, `realtime_end`, `limit`, `offset`, `order_by`, `sort_order`, `filter_variable`, `filter_value`, `tag_names`, `exclude_tag_names`
- **`series/search-related-tags`** (Series search related tags): The second step of narrowing a search: given words and one tag already applied, the tags that co-occur on what is left. Two required arguments, `series_search_text` and `tag_names` - the second looks like a filter and is mandatory. [Cost: 0 credit]  
  *Options:* `series_search_text` *(required)*, `realtime_start`, `realtime_end`, `tag_names` *(required)*, `exclude_tag_names`, `tag_group_id`, `tag_search_text`, `limit`, `offset`, `order_by`, `sort_order`
- **`series/search-tags`** (Series search tags): Call after a broad `series/search` to see what would narrow it, then feed a name back as `tag_names` there. Two search-text parameters on one endpoint: `series_search_text` picks the series, `tag_search_text` filters the tags that come back. [Cost: 0 credit]  
  *Options:* `series_search_text` *(required)*, `realtime_start`, `realtime_end`, `tag_names`, `tag_group_id`, `tag_search_text`, `limit`, `offset`, `order_by`, `sort_order`
- **`series/series`** (Series metadata): Call before charting or comparing: `units`, `seasonal_adjustment` and `frequency` are what decide whether two series are comparable, and none of them are visible from the id. Widening the real-time period returns one record per interval in which the metadata differed, so a single-series call can answer with several rows. [Cost: 1 credit]  
  *Options:* `series_id` *(required)*, `realtime_start`, `realtime_end`
- **`series/tags`** (Series tags): Call to read one series' labels - its geography, frequency, publisher and subject - and to get the tag names that would find its peers through `tags/series`. Unlike every other tag capability here it has no limit, offset, search_text or tag_group_id: you get all of them. [Cost: 0 credit]  
  *Options:* `series_id` *(required)*, `realtime_start`, `realtime_end`, `order_by`, `sort_order`
- **`series/updates`** (Series updates): Call to find what has changed rather than what exists - the only capability here that takes no series id. FRED caps it at series updated in the last two weeks, so it cannot answer a question about last quarter, and the sort is fixed at last_updated descending with no way to change it. [Cost: 1 credit]  
  *Options:* `realtime_start`, `realtime_end`, `limit`, `offset`, `filter_value`, `start_time`, `end_time`
- **`series/vintage-dates`** (Series vintage dates): Call to find out when a series was actually revised, then pass one or more of these dates to `series/observations` as `vintage_dates` to see the data as it stood. The path is `vintagedates` with no underscore, and unlike its siblings the real-time period defaults to the whole span rather than to today, so a bare call returns the full revision history. [Cost: 1 credit]  
  *Options:* `series_id` *(required)*, `realtime_start`, `realtime_end`, `limit`, `offset`, `sort_order`
- **`sources/releases`** (Source releases): The middle rung of the provenance walk: agency to release to series. Call when the question starts from a publisher - everything the BEA puts out - rather than from a subject. [Cost: 0 credit]  
  *Options:* `source_id` *(required)*, `realtime_start`, `realtime_end`, `limit`, `offset`, `order_by`, `sort_order`
- **`sources/source`** (Source): Call to resolve a source id to an agency name and site. Widening the real-time period makes this single-source call return several records, one per interval in which the agency's name or link differed. [Cost: 0 credit]  
  *Options:* `source_id` *(required)*, `realtime_start`, `realtime_end`
- **`sources/sources`** (Sources): Where a `source_id` comes from. There are only about a hundred agencies and `limit` defaults to 1000, so one call is the whole list and paging is never needed here. [Cost: 0 credit]  
  *Options:* `realtime_start`, `realtime_end`, `limit`, `offset`, `order_by`, `sort_order`
- **`tags/related`** (Related tags): Call to narrow a tag search: given tags already chosen, the tags that co-occur with them. The one required argument is the one that is optional on `tags/tags`, and `tag_group_id` does not accept `cc` here. Tag names may contain spaces, so a value like `monetary aggregates;weekly` needs the space URL-encoded and only the `;` treated as a separator. [Cost: 0 credit]  
  *Options:* `realtime_start`, `realtime_end`, `tag_names` *(required)*, `exclude_tag_names`, `tag_group_id`, `search_text`, `limit`, `offset`, `order_by`, `sort_order`
- **`tags/series`** (Series by tag): The non-hierarchical route to series ids: every series carrying all of `tag_names` at once, without walking the category tree. Tags intersect rather than union, so each name added narrows. Unlike `categories/series` there is no `filter_variable`/`filter_value` here - narrow with more tags instead. [Cost: 1 credit]  
  *Options:* `tag_names` *(required)*, `exclude_tag_names`, `realtime_start`, `realtime_end`, `limit`, `offset`, `order_by`, `sort_order`
- **`tags/tags`** (Tags): The full vocabulary - roughly 4,800 tags against a `limit` cap of 1000, so this is the one tag capability that genuinely needs paging. `series_count` here is the global count, unlike the same field on the category, release and related-tag capabilities where it is scoped to what was asked about. [Cost: 0 credit]  
  *Options:* `realtime_start`, `realtime_end`, `tag_names`, `tag_group_id`, `search_text`, `limit`, `offset`, `order_by`, `sort_order`

### FRED (Federal Reserve Economic Data) (`fred-stlouisfed-org`)

FRED (Federal Reserve Economic Data), the St. Louis Fed's database of US and international economic time series: headline US indicators such as the monthly unemployment rate (UNRATE), CPI inflation (CPIAUCSL), GDP (GDP, GDPC1), nonfarm payrolls (PAYEMS), the federal funds rate (FEDFUNDS) and Treasury yields (DGS10), plus 800,000+ other series. Search series by text, browse categories, releases, sources and tags, read one series' metadata (units, frequency, seasonal adjustment, source, notes, date range, last update) and fetch its observations (daily, weekly, monthly, quarterly or annual values) with date window, frequency aggregation and transformation, paginated, from the site's keyless JSON, CSV and HTML endpoints.

- **`economic-data/category`** (Category): Discover series by topic instead of by text: start at the root, follow `children[].category_id`, then read `series[].series_id` for `series` / `series_observations`. [Cost: 5 credit]  
  *Options:* `category_id`, `page`
- **`economic-data/release`** (Release): Browse the series a release publishes (e.g. release 53 = Gross Domestic Product) and hand `series[].series_id` to `series` / `series_observations`. [Cost: 5 credit]  
  *Options:* `page`, `release_id` *(required)*
- **`economic-data/releases`** (Releases): Find a `release_id` for `release`; releases group the series a statistical agency publishes together. [Cost: 5 credit]  
  *Options:* `page`
- **`economic-data/series`** (Series): Confirm what a `series_id` (or a pasted fred.stlouisfed.org/series/{id} page URL) measures and which `units`/`frequency` values `series_observations` accepts for it; the data points themselves come from `series_observations`. [Cost: 5 credit]  
  *Options:* `series_id` *(required)*
- **`economic-data/series_observations`** (Series observations): Get the historical values of a known `series_id` or a pasted fred.stlouisfed.org/series/{id} page URL (monthly US unemployment rate = UNRATE, CPI = CPIAUCSL, real GDP = GDPC1); pick `units` and `frequency` from `series.available_units` / `series.available_frequencies`. Use `series_search` first when only the concept is known. [Cost: 5 credit]  
  *Options:* `aggregation_method`, `frequency`, `limit`, `observation_end`, `observation_start`, `offset`, `series_id` *(required)*, `sort_order`, `units`
- **`economic-data/series_search`** (Series search): Start here to find a `series_id` (e.g. UNRATE, CPIAUCSL) for `series` and `series_observations`. [Cost: 5 credit]  
  *Options:* `limit`, `search_text` *(required)*
- **`economic-data/source`** (Source): See what an agency publishes (e.g. source 18 = U.S. Bureau of Economic Analysis) and hand `releases[].release_id` to `release`. [Cost: 5 credit]  
  *Options:* `source_id` *(required)*
- **`economic-data/sources`** (Sources): Find a `source_id` for `source`. [Cost: 5 credit]  
  *Options:* `page`
- **`economic-data/tag_series`** (Tag series): Find series by tag combination, e.g. gdp;quarterly or usa;monthly;nsa, then read them with `series` / `series_observations`. [Cost: 5 credit]  
  *Options:* `page`, `tag_names` *(required)*
- **`economic-data/tags`** (Tags): Discover tag names to combine in `tag_series`. [Cost: 5 credit]  
  *Options:* `page`

### Nasdaq.com news feeds and articles (`nasdaq-com`)

Nasdaq.com's public news surfaces: ticker news, press releases, market-wide and topic feeds (JSON), the RSS feeds that carry publish times, and the full text and exact publish instant of a Nasdaq article or press release page.

- **`news/article`** (Article): Full text and the exact publish time of a story listed by any feed function. Costs one ~180 KB page fetch. [Cost: 1 credit]  
  *Options:* `url` *(required)*
- **`news/feed`** (Feed): Publish times for the newest stories on a ticker or topic in one request. For older stories or more than 15 rows use `ticker_news` / `topic_news` and `article`. [Cost: 1 credit]  
  *Options:* `category`, `symbol`
- **`news/latest_headlines`** (Latest headlines): What is being published right now across the market, with no ticker or topic filter. [Cost: 1 credit]  
  *Options:* `limit`, `offset`, `with_publish_times`
- **`news/press_releases`** (Press releases): Company announcements for one ticker (earnings dates, product launches, filings) rather than third-party coverage. [Cost: 1 credit]  
  *Options:* `asset_class`, `limit`, `offset`, `ticker` *(required)*
- **`news/ticker_news`** (Ticker news): Latest third-party coverage of one stock or ETF. Official company announcements (deals, partnerships, earnings, launches) are press releases, which this feed omits: pass `include_press_releases: true` or call `press_releases`. For the exact publish time of any row pass its `url` to `article`; for only the 15 newest with times in one request use `feed`. [Cost: 1 credit]  
  *Options:* `asset_class`, `include_press_releases`, `limit`, `offset`, `ticker` *(required)*, `with_publish_times`
- **`news/topic_news`** (Topic news): Coverage of a theme (Markets, Stocks, Technology, Investing) rather than a ticker. [Cost: 1 credit]  
  *Options:* `limit`, `offset`, `topic_id` *(required)*, `with_publish_times`

### SEC EDGAR (`sec-gov`)

Official SEC company profiles, filings, filing sections, 13F holdings and XBRL concept facts.

- **`filings/company`** (Company): Resolve a ticker, CIK or company name to its EDGAR filer profile: CIK, name, tickers, exchanges, SIC, filer category, state of incorporation, fiscal year end, addresses, former names and filing counts. Start here to get the CIK the other functions accept. [Cost: 5 credit]  
  *Options:* `cik`, `name`, `ticker`
- **`filings/concept`** (Concept): Every reported value of one XBRL concept for a filer (Revenues, NetIncomeLoss, Assets, EarningsPerShareDiluted ...) straight from the SEC's companyconcept API: value, period, unit, fiscal year and period, the form and accession it came from. Newest period first. [Cost: 5 credit]  
  *Options:* `cik`, `concept` *(required)*, `form`, `limit`, `name`, `taxonomy`, `ticker`, `unit`
- **`filings/filing`** (Filing): One filing by accession number: its submission metadata (form, dates, 8-K items) and every document in the filing folder with size and direct URL (primary document, exhibits, XBRL instance, full submission text). [Cost: 5 credit]  
  *Options:* `accession_number` *(required)*, `cik`, `name`, `ticker`
- **`filings/filings`** (Filings): List a filer's EDGAR filings newest first, filtered by form type (10-K, 10-Q, 8-K, S-1, 13F-HR, 4, DEF 14A ...) and filing date. Each record carries accession number, dates, 8-K item codes with captions, XBRL flags and direct document URLs. Reaches into older submission pages when `from` predates the recent window. [Cost: 5 credit]  
  *Options:* `cik`, `forms`, `from`, `include_amendments`, `limit`, `name`, `ticker`, `to`
- **`filings/holdings_13f`** (Holdings 13f): Form 13F-HR holdings of an institutional investment manager: every position from the XML information table (issuer, class, CUSIP, value, shares or principal, put/call, discretion, voting authority). Defaults to the latest 13F-HR; pick a quarter with report_date or a filing with accession_number. Values are whole USD for filings since 2023-01-03 and thousands before. [Cost: 5 credit]  
  *Options:* `accession_number`, `cik`, `include_amendments`, `limit`, `name`, `offset`, `report_date`, `ticker`
- **`filings/search`** (Search): EDGAR full-text search across every filer since 2001: filter by phrase, form types, filing-date range and CIK. Returns 100 hits per page with accession number, form, filer names and CIKs, 8-K item codes, period and direct document URLs. Use it for cross-company questions such as 8-K Item 2.02 filings this quarter. Pass `snippets` to also fetch the matched document of the first hits and return the sentences containing the query (EDGAR's index returns no highlights itself). [Cost: 5 credit]  
  *Options:* `cik`, `forms`, `from`, `page`, `query`, `snippets`, `to`
- **`filings/sections`** (Sections): Item sections of a 10-K or 10-Q as plain text: Item 1 Business, 1A Risk Factors, 7 MD&A, 8 Financial Statements and so on (10-Q items carry their Part). Defaults to the filer's latest 10-K; pass form=10-Q or an accession number for another report, and items to keep only some sections. [Cost: 5 credit]  
  *Options:* `accession_number`, `cik`, `form`, `items`, `max_chars`, `name`, `ticker`

### IBGE service data API (`servicodados-ibge-gov-br`)

Brazil's national statistics institute (IBGE) open JSON API at servicodados.ibge.gov.br: territorial codes (localidades), SIDRA aggregated statistics (agregados: official municipal / state / national population and household counts from the 2022 Census and the yearly population estimates, IPCA, PNAD, GDP and ~8,000 other tables), 2010 Census first-name frequencies and rankings, IBGE news/releases and release calendar, country profiles and indicators (paises), territorial meshes (malhas) and the CNAE activity classification. Anonymous, no key, Portuguese-language values as published.

- **`official-statistics/agregado_dados`** (Agregado dados): Official population or household count of a Brazilian municipality, state or the country (Census 2022: 4709/93 population, 4712/381 occupied households, 4712/382 residents in households; estimates: 6579/9324), IPCA (1737/63), PNAD unemployment (4099/4099), municipal GDP (5938/37), IPCA by group (7060/63 + classificacao 315) or any other table after agregado_metadados told you the ids. Resolve the municipality code first with localidades (e.g. São Bernardo do Campo = 3548708). Unknown agregado or variable ids are not_found; a level the table does not offer is invalid_input. [Cost: 5 credit]  
  *Options:* `agregado` *(required)*, `classificacao`, `localidades`, `periodos`, `variaveis`
- **`official-statistics/agregado_metadados`** (Agregado metadados): Pick the variavel ids, classificacao/categoria ids, nivel and periods to pass to agregado_dados. Unknown table ids are not_found. [Cost: 5 credit]  
  *Options:* `agregado` *(required)*, `include_periodos`, `localidades_nivel`
- **`official-statistics/agregados`** (Agregados): Find the agregado id (and then, with agregado_metadados, the variable and classification ids) before calling agregado_dados. Pass a query or at least one filter: the unfiltered catalog has ~8,000 tables. Rows carry only id and name (no period), and a query like `domicilios` with nivel N6 matches hundreds of Census tables ordered by id, so for the headline municipal population / household counts skip the search and call agregado_dados directly with 4709 (Census 2022 population), 4712 (Census 2022 occupied households and residents) or 6579 (yearly population estimates). [Cost: 5 credit]  
  *Options:* `assunto`, `classificacao`, `limit`, `nivel`, `offset`, `periodicidade`, `periodo`, `query`
- **`official-statistics/calendario`** (Calendario): When the next IPCA / PNAD / PIB release is scheduled, or the release history of a product. [Cost: 5 credit]  
  *Options:* `ate`, `de`, `page`, `produto`, `qtd`
- **`official-statistics/cnae`** (Cnae): Decode a CNAE code from a company registry (7-digit subclasse 0111301, 5-digit classe 01113) or browse the hierarchy. [Cost: 5 credit]  
  *Options:* `id`, `nivel` *(required)*, `parent_id`, `parent_nivel`
- **`official-statistics/localidade`** (Localidade): Turn a municipality or state code into its name and hierarchy (microrregiao, mesorregiao, regiao imediata/intermediaria, UF, regiao), e.g. to label agregados results or join with other Brazilian sources. [Cost: 5 credit]  
  *Options:* `ids` *(required)*, `nivel` *(required)*
- **`official-statistics/localidades`** (Localidades): Resolve IBGE codes before querying agregados (N3 = estado id, N6 = municipio id), enumerate the municipalities of a state, or find a municipality by (partial, accent-insensitive) name. municipios, distritos and subdistritos require a parent so one call never fetches the 5,570-row national list. [Cost: 5 credit]  
  *Options:* `limit`, `nivel` *(required)*, `offset`, `parent_id`, `parent_nivel`, `query`
- **`official-statistics/malha`** (Malha): Draw or geo-join a Brazilian state, municipality or region; get its centroid and area in km2. Use qualidade=minima unless you need detailed geometry (maxima meshes are megabytes). [Cost: 5 credit]  
  *Options:* `id` *(required)*, `intrarregiao`, `nivel` *(required)*, `qualidade`
- **`official-statistics/nomes`** (Nomes): How common a Brazilian first name is, how its popularity changed by decade, or where in Brazil it concentrates. [Cost: 5 credit]  
  *Options:* `group_by`, `localidade`, `nomes` *(required)*, `sexo`
- **`official-statistics/nomes_ranking`** (Nomes ranking): Most common names in Brazil or a state, by decade or sex. [Cost: 5 credit]  
  *Options:* `decada`, `localidade`, `sexo`
- **`official-statistics/noticias`** (Noticias): Recent IBGE releases (IPCA, PNAD, PIB...), news about a product or matching a keyword. Follow next_page until null. [Cost: 5 credit]  
  *Options:* `ate`, `busca`, `de`, `destaque`, `page`, `produto_id`, `qtd`, `tipo`
- **`official-statistics/paises`** (Paises): A country fact sheet or a UN-sourced indicator series (GDP per capita, population, life expectancy...) as IBGE republishes them, for Brazil or any of 193 countries. [Cost: 5 credit]  
  *Options:* `indicadores`, `lang`, `paises` *(required)*, `periodo`

### Treasury Fiscal Data (`treasury-fiscal-data`)

US Treasury Fiscal Data: the national debt to the penny, daily cash balances and tax receipts, monthly receipts and outlays, Treasury auction results, interest rates and expense on the debt, the gold reserve and official exchange rates.

- **`auctions/results`** (Auction results): How an auction went: filter `security_type:eq:Note,security_term:eq:10-Year` and sort `-auction_date` for the last ten-year, then read `high_yield` and `bid_to_cover_ratio`. Bidder takedown comes as amounts, not shares: `indirect_bidder_accepted`, `direct_bidder_accepted` and `primary_dealer_accepted` in dollars, beside the `_tendered` amounts; an indirect share is `indirect_bidder_accepted` divided by `total_accepted`. `cusip:eq:` reaches one security. Bills report discount rates, notes and bonds yields, TIPS real yields, FRNs discount margins. [Cost: 1 credit]  
  *Options:* `fields`, `filter`, `sort`, `page[size]`, `page[number]`
- **`auctions/upcoming`** (Upcoming auctions): What the Treasury is about to sell: the auction calendar for the coming days with sizes. No history here - once an auction settles it moves to auctions/results. [Cost: 1 credit]  
  *Options:* `fields`, `filter`, `sort`, `page[size]`, `page[number]`
- **`daily-statement/deposits-and-withdrawals`** (Deposits and withdrawals): Where the government's cash came from and went each day: withheld income taxes, corporate taxes, Social Security benefits, Medicare, defence vendor payments, interest on the debt. The daily tax-receipt categories are the real-time read on the economy that the monthly statement only confirms later. [Cost: 1 credit]  
  *Options:* `fields`, `filter`, `sort`, `page[size]`, `page[number]`
- **`daily-statement/operating-cash-balance`** (Operating cash balance): The Treasury General Account balance - the government's cash on hand - which is what debt-ceiling coverage tracks day by day. For the current figure filter `account_type:eq:Treasury General Account (TGA) Closing Balance`, sort `-record_date` and read `open_today_bal`; `close_today_bal` is `null` on every row since 2022-04-18. The same balance is `close_today_bal` on `account_type:eq:Federal Reserve Account` rows through 2021-09-30 and on `account_type:eq:Treasury General Account (TGA)` rows for the six months between, so a series across the 2022 relabelling is those three filters stitched together. [Cost: 1 credit]  
  *Options:* `fields`, `filter`, `sort`, `page[size]`, `page[number]`
- **`daily-statement/public-debt-transactions`** (Public debt transactions): Gross issuance and redemption of Treasury securities by day: how much in bills was issued and how much rolled off. Net issuance is issues minus redemptions across the same security type. [Cost: 1 credit]  
  *Options:* `fields`, `filter`, `sort`, `page[size]`, `page[number]`
- **`debt/average-interest-rates`** (Average interest rates): What the government is paying on its debt, by kind of security: the average coupon on outstanding notes, the rate on bills, the blended rate on everything marketable. Filter `security_desc:eq:Treasury Notes` for one class, sort `-record_date` for the latest month. [Cost: 1 credit]  
  *Options:* `fields`, `filter`, `sort`, `page[size]`, `page[number]`
- **`debt/historical-outstanding`** (Historical debt outstanding): The long series: one figure per year from the first Treasury report in 1790. Use it for anything before 1993 or for a year-end comparison, filtering `record_fiscal_year:eq:<year>` rather than `record_date`; debt/to-the-penny is the daily figure. [Cost: 1 credit]  
  *Options:* `fields`, `filter`, `sort`, `page[size]`, `page[number]`
- **`debt/interest-expense`** (Interest expense): How much interest the debt costs in dollars, monthly, by kind of security. The fiscal-year-to-date column is the one quoted when interest is compared to other outlays; filter `record_calendar_month:eq:09` for fiscal-year totals. [Cost: 1 credit]  
  *Options:* `fields`, `filter`, `sort`, `page[size]`, `page[number]`
- **`debt/to-the-penny`** (Debt to the penny): The headline national debt figure: total public debt outstanding on a given day, to the cent. Sort `-record_date` with `page[size]=1` for today's number, or filter a date range for the series. For the figure before 1993 use debt/historical-outstanding. [Cost: 1 credit]  
  *Options:* `fields`, `filter`, `sort`, `page[size]`, `page[number]`
- **`monthly-statement/receipts-and-outlays`** (Receipts, outlays and deficit): The monthly deficit: filter `record_date:eq:2026-07-31,classification_desc:eq:July` and read `current_month_dfct_sur_amt` on the row with the higher `line_code_nbr` - the current fiscal year's July; the other row is the prior year's July for comparison. `classification_desc:eq:Year-to-Date` on the same record date gives the fiscal-year running total the same way. Published around the eighth business day of the following month. [Cost: 1 credit]  
  *Options:* `fields`, `filter`, `sort`, `page[size]`, `page[number]`
- **`rates/exchange`** (Treasury reporting rates of exchange): The official rate a US agency reports a foreign balance at, per quarter. Filter `country_currency_desc:eq:Euro Zone-Euro` or `country:eq:Japan`, add `effective_date:lte:<date>` for the date being reported, and sort `-record_date,-effective_date`, so the first row is the rate in force on that date rather than an amendment that came after it. For a market rate on a given day this is the wrong source. [Cost: 1 credit]  
  *Options:* `fields`, `filter`, `sort`, `page[size]`, `page[number]`
- **`reserves/gold`** (Gold reserve): How much gold the Treasury holds and where. The book value is the statutory price, not the market price, so a market valuation is the ounces times a spot price from elsewhere. Sort `-record_date` for the current holding. [Cost: 1 credit]  
  *Options:* `fields`, `filter`, `sort`, `page[size]`, `page[number]`

