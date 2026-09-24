---
type: category
id: "real-estate"
title: "Real Estate"
providers_count: 3
---

# Category: Real Estate

> Property records and home valuation comparables.

Part of [[_Index|Legends Alexandria]] and the [[manifesto/The-Great-AI-Data-Arbitrage|Great AI Data Arbitrage]].

## Cataloged Providers (3)

| Provider | Capabilities | Data Tier | Direct Bypass Available? |
|---|---|---|---|
| `craigslist-org` (**Craigslist**) | 3 | Public Commercial Web / Frontend JSON Endpoints | Yes (Direct unauthenticated web fetch or lightweight house scraper) |
| `redfin-com` (**Redfin**) | 6 | Proprietary Commercial B2B Data Brokers | No (Proprietary) |
| `zillow-com` (**Zillow**) | 15 | Public Commercial Web / Frontend JSON Endpoints | Yes (Direct unauthenticated web fetch or lightweight house scraper) |

## Tools & Capabilities

### Craigslist (`craigslist-org`)

Craigslist housing rentals: every region worldwide, filtered search of apartments, rooms, sublets and swaps by rent, beds, baths, pets, type and keyword, and full postings with attributes, photos, map location and timestamps.

- **`housing/posting`** (Posting): Pass a card's `url` (or its posting_token as posting_id). A numeric post id also needs `region` (and optionally `category`). A deleted or unknown posting is not_found; flagged or expired ones return with flagged/expired true. (Cost: 5 credit)
- **`housing/regions`** (Regions): Find the `region` slug for search (sfbay, newyork, austin, london) or list all regions in a country. (Cost: 5 credit)
- **`housing/search`** (Search): Search rentals in a region; then call `posting` with a card's url or posting_id for the full text and attributes. Page with `cursor` (pages of 36, up to 91 pages). (Cost: 5 credit)

### Redfin (`redfin-com`)

Read publicly advertised US rental listings, floor plans, amenities and policies. Preview pending runner validation.

- **`properties/amenities`** (Amenities): Read published in-unit and community amenity names for a rental listing. (Cost: 5 credit)
- **`properties/floor_plans`** (Floor plans): Read published rental floor plans with names, rent, size/bath text and unit availability text. Unit counts are separate from building counts. (Cost: 5 credit)
- **`properties/policies`** (Policies): Read published rental policy text, including pet restrictions and any displayed fees. Does not infer missing policies. (Cost: 5 credit)
- **`properties/related_areas`** (Related areas): Discover linked nearby city rental search pages from an existing city rental page. This is not free-text location geocoding. (Cost: 5 credit)
- **`properties/rental`** (Rental): Read primary rental identity, rent, beds, baths, area, description and source attribution. Requires a current For rent listing; excludes nearby for-sale recommendations. (Cost: 5 credit)
- **`properties/search`** (Search): Read one rental search page with published rent, bedroom/bathroom text, listing URLs and availability facts. Accept city rental URLs and observed price/bedroom filter URLs; excludes cards explicitly reporting zero matching units. Does not guarantee every unit matches. (Cost: 5 credit)

### Zillow (`zillow-com`)

US home search, property details, photos, schools, scores and valuation history, plus rental listings (apartments, houses, townhomes, condos, rooms) and apartment buildings with per-unit availability, and the Zillow Observed Rent Index (ZORI) market rent series by metro, city, county or ZIP from Zillow Research.

- **`properties/building`** (Building): Details and unit availability for one building URL from rental_search (is_building = true). Single homes and units use rental. (Cost: 5 credit)
- **`properties/comparables`** (Comparables): Zillow home valuation comparables, distinct from nearby homes. (Cost: 5 credit)
- **`properties/locations`** (Locations): Resolve text into region or other typed suggestions. Results vary by type and do not include a bounding box; pass region_id (or region_ids[0]) with region_types[0] / region_subtype straight to search, which accepts a region alone and returns the region's bounds. Do not treat every suggestion id as a property zpid. (Cost: 5 credit)
- **`properties/map`** (Map): Property/building clusters in a small map viewport (at most 0.1 degrees per axis). Each card carries only what Zillow's safelisted map document returns: zpid, url, status, price, currency, tax_assessed_value, coordinates, provider_listing_id and community/subdivision. Call property with the zpid for beds, baths, areas, home type, photos and the street address. (Cost: 5 credit)
- **`properties/nearby`** (Nearby): Nearby property cards, including off-market homes. (Cost: 5 credit)
- **`properties/price_history`** (Price history): Public listing and sale price events, timestamps and changes. (Cost: 5 credit)
- **`properties/property`** (Property): Property facts, original photos, price/tax history, schools and nearby homes; optionally fetch scores and valuation data in the same session. (Cost: 5 credit)
- **`properties/rental`** (Rental): Details for one rental identified by zpid or /homedetails/ URL from rental_search (is_building = false). For apartment communities use building. (Cost: 5 credit)
- **`properties/rental_search`** (Rental search): Discovery of rentals by area and filters; pass next_cursor back as cursor for later pages. Use rental for one listing and building for one apartment community. (Cost: 5 credit)
- **`properties/schools`** (Schools): Nearby and assigned schools remain distinct, with ratings, grade levels and distance in miles. (Cost: 5 credit)
- **`properties/scores`** (Scores): Walk, transit and bike scores; unavailable scores are null. (Cost: 5 credit)
- **`properties/search`** (Search): Find for-sale listings in a region or a map box. Chain from locations: pass its region_id (or region_ids[0]) as region_id and its region_types[0] / region_subtype as region_type; bounds are then optional and the response's pages[].region.bounds carries the region's box for map or a narrower search. Alternatively supply bounds as {west, east, south, north} in longitude/latitude degrees. Rental listings are not supported by this search. (Cost: 5 credit)
- **`properties/tax_history`** (Tax history): Tax payment and assessed-value history with provider timestamps. (Cost: 5 credit)
- **`properties/value_history`** (Value history): Named valuation chart series. Point timestamps are Unix milliseconds; null values remain null. (Cost: 5 credit)
- **`properties/zori`** (Zori): Market-level rent index questions (median asking rent over time, YoY rent change for a metro/city/county/ZIP). Not for individual listings: use rental_search, rental or building for those. Resolve ambiguous names with the state (`Springfield, IL`) or pass the Zillow RegionID. (Cost: 5 credit)


