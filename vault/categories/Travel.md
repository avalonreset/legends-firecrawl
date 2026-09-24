---
type: category
id: "travel"
title: "Travel"
providers_count: 15
---

# Category: Travel

> Travel: hotels, their guest ratings, rankings in a destination and public reviews.

Part of [[_Index|Legends Alexandria]] and the [[manifesto/The-Great-AI-Data-Arbitrage|Great AI Data Arbitrage]].

## Cataloged Providers (15)

| Provider | Capabilities | Data Tier | Direct Bypass Available? |
|---|---|---|---|
| `amtrak-com` (**Amtrak**) | 7 | Proprietary Commercial B2B Data Brokers | No (Proprietary) |
| `flights-google-com` (**Google Flights**) | 2 | Public Commercial Web / Frontend JSON Endpoints | Yes (Direct unauthenticated web fetch or lightweight house scraper) |
| `golfnow-com` (**GolfNow US**) | 8 | Proprietary Commercial B2B Data Brokers | No (Proprietary) |
| `hipcamp-com` (**Hipcamp**) | 7 | Proprietary Commercial B2B Data Brokers | No (Proprietary) |
| `ra-co` (**Resident Advisor**) | 6 | Proprietary Commercial B2B Data Brokers | No (Proprietary) |
| `recreation-gov` (**Recreation.gov**) | 8 | Public Government & Intergovernmental Data | Yes (Direct official REST API) |
| `seatgeek-com` (**SeatGeek**) | 7 | Public Commercial Web / Frontend JSON Endpoints | Yes (Direct unauthenticated web fetch or lightweight house scraper) |
| `skyscanner-net` (**Skyscanner**) | 4 | Public Commercial Web / Frontend JSON Endpoints | Yes (Direct unauthenticated web fetch or lightweight house scraper) |
| `spothero-com` (**SpotHero parking**) | 10 | Public Commercial Web / Frontend JSON Endpoints | Yes (Direct unauthenticated web fetch or lightweight house scraper) |
| `stubhub-com` (**StubHub**) | 3 | Public Commercial Web / Frontend JSON Endpoints | Yes (Direct unauthenticated web fetch or lightweight house scraper) |
| `tickpick-com` (**TickPick**) | 7 | Public Commercial Web / Frontend JSON Endpoints | Yes (Direct unauthenticated web fetch or lightweight house scraper) |
| `todaytix-com` (**TodayTix**) | 5 | Public Commercial Web / Frontend JSON Endpoints | Yes (Direct unauthenticated web fetch or lightweight house scraper) |
| `trip-com` (**Trip.com**) | 6 | Public Commercial Web / Frontend JSON Endpoints | Yes (Direct unauthenticated web fetch or lightweight house scraper) |
| `turo-com` (**Turo**) | 3 | Public Commercial Web / Frontend JSON Endpoints | Yes (Direct unauthenticated web fetch or lightweight house scraper) |
| `untourism-int` (**UN Tourism**) | 3 | Public Government & Intergovernmental Data | Yes (Direct official REST API) |

## Tools & Capabilities

### Amtrak (`amtrak-com`)

Amtrak (US national passenger rail) read-only: station directory and search with addresses, hours and amenities; named routes with ordered stops and train numbers; live train positions and stop-by-stop status decrypted from the public Track Your Train feed. Public feeds of www.amtrak.com and maps.amtrak.com, no login. Fares, schedules by date and booking are not covered (the /dotcom/ APIs sit behind Akamai Bot Manager).

- **`train-status/get_route`** (Get route): Route detail after `list_routes`; the train numbers feed `train_status`, the stop codes feed `get_station`. (Cost: 5 credit)
- **`train-status/get_station`** (Get station): Station detail once you have a code from `list_stations`, `search_stations`, a route's stops or a train's stops. (Cost: 5 credit)
- **`train-status/list_routes`** (List routes): Find a route code or name for `get_route`, or filter `live_trains` by `route_name`. (Cost: 5 credit)
- **`train-status/list_stations`** (List stations): Start here to find station codes for `get_station`, `search_stations` inputs or route stops; filter by `state` to keep the result small. (Cost: 5 credit)
- **`train-status/live_trains`** (Live trains): A snapshot of where trains are right now; use `train_status` for one train with its stop-by-stop times. (Cost: 5 credit)
- **`train-status/search_stations`** (Search stations): Find a station code when you know a place name or a partial name; `get_station` for full detail. (Cost: 5 credit)
- **`train-status/train_status`** (Train status): Train status by number, the Track Your Train equivalent. Train numbers come from `get_route` or `live_trains`. (Cost: 5 credit)

### Google Flights (`flights-google-com`)

Google Flights airport/city lookup and one-way or two-step round-trip fare search.

- **`flights/search_flights`** (Search flights): Search Google Flights one-way fares or round-trip outbound options. For matching returns, call again with a chosen selection in selected_outbound. Round-trip outbound prices are starting prices; return prices cover the selected pair. Bounded first-page coverage, without retries or pagination. (Cost: 5 credit)
- **`flights/suggest_places`** (Suggest places): Find Google Flights airport and city identifiers by name or IATA code. Includes nearby airports, deduplicated; omits rail stations and regions. (Cost: 0 credit)

### GolfNow US (`golfnow-com`)

GolfNow US public course discovery: location and course search, courses with tee times near a point, per-facility tee times with displayed rates, per-day availability summaries, course profiles and GolfNow reviews. Anonymous, read-only.

- **`tee-times/course_detail`** (Course detail): Details for one `facility_id`. Two page fetches; no availability (use `facility_tee_times`). (Cost: 5 credit)
- **`tee-times/course_reviews`** (Course reviews): Read what golfers wrote about a course. Only reviews left on GolfNow itself; the larger GolfPass review count on course records is a different corpus. (Cost: 5 credit)
- **`tee-times/courses_near`** (Courses near): Discover courses near a place (coordinates from `suggest_locations`); then call `facility_tee_times` with a `facility_id`. (Cost: 5 credit)
- **`tee-times/facility_day_summaries`** (Facility day summaries): Pick a day before calling `facility_tee_times`; up to 31 days per call. (Cost: 5 credit)
- **`tee-times/facility_tee_times`** (Facility tee times): Availability and displayed prices for a known `facility_id` on one day. Discovery only: nothing is held or booked. (Cost: 5 credit)
- **`tee-times/search_courses`** (Search courses): Find a `facility_id` from a course name; every id-keyed function needs one. (Cost: 5 credit)
- **`tee-times/suggest_locations`** (Suggest locations): Turn a place name into latitude/longitude for `courses_near`. (Cost: 5 credit)
- **`tee-times/tee_time_rates`** (Tee time rates): Expand `has_more_rates` on a `facility_tee_times` row. Without `tee_time_id`, the first tee time of `date` for `players` is used. (Cost: 5 credit)

### Hipcamp (`hipcamp-com`)

Hipcamp campsite, cabin, glamping and RV listing discovery: dated search with location, group size and amenity filters, land details, per-site availability and displayed price quotes, blocked-date calendars, reviews, place autocomplete and public campground daily availability. Anonymous, read-only.

- **`campsite-listings/autocomplete`** (Autocomplete): Turn a place name into coordinates for search_lands, or find a land or public campground by name. (Cost: 5 credit)
- **`campsite-listings/land`** (Land): After search_lands or a pasted hipcamp.com/land URL. For dated availability and full quotes call land_sites. (Cost: 5 credit)
- **`campsite-listings/land_calendar`** (Land calendar): Calendar view of what is already booked or closed for a land or a single site. (Cost: 5 credit)
- **`campsite-listings/land_reviews`** (Land reviews): Read reviews for a land from search_lands or land; pass next_cursor to continue. (Cost: 5 credit)
- **`campsite-listings/land_sites`** (Land sites): Dated availability check and price breakdown for a land found by search_lands or land. (Cost: 5 credit)
- **`campsite-listings/public_campground_availability`** (Public campground availability): After autocomplete returns a campground_public result; pass its numeric id. (Cost: 5 credit)
- **`campsite-listings/search_lands`** (Search lands): Start here to find lands near a place; use autocomplete first to turn a place name into coordinates. Feed masked_id into land, land_sites, land_calendar and land_reviews. (Cost: 5 credit)

### Resident Advisor (`ra-co`)

Resident Advisor (ra.co) electronic music and nightlife events worldwide, read from RA's own anonymous GraphQL API: resolve a city to its RA area, list events for an area and date range with genre and keyword filters, facets and pagination, read one event with lineup, venue and the public primary ticket tiers (price, booking fee, currency, sale status, on-sale window), search events, venues, artists, promoters, labels and areas by name, and read venue and artist profiles with their upcoming events. Read only: no purchases, holds or resale offers.

- **`events/areas`** (Areas): First step of event discovery: you need the numeric `area_id` for `events`, or the time zone and currency of a city. (Cost: 5 credit)
- **`events/artist`** (Artist): You have an artist id (from `search` or an event's `artists[].id`), an RA slug, or a pasted `https://ra.co/dj/{slug}` URL and need the profile or upcoming dates. (Cost: 5 credit)
- **`events/event`** (Event): You have an RA event id (from `events`, `search`, `venue`, `artist`) or a pasted `https://ra.co/events/{id}` URL and need details or ticket prices and sale status. (Cost: 5 credit)
- **`events/events`** (Events): Discover events by city and date; take `area_id` from `areas` and chain each `events[].id` into `event` for tickets. (Cost: 5 credit)
- **`events/search`** (Search): You know a name (artist, club, party, promoter, city) and need its RA id to chain into `event`, `venue`, `artist` or `events`. (Cost: 5 credit)
- **`events/venue`** (Venue): You have a venue id (from `search`, `events[].venue.id`, or a pasted `https://ra.co/clubs/{id}` URL) and need the venue's details or its upcoming events. (Cost: 5 credit)

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

### SeatGeek (`seatgeek-com`)

SeatGeek event discovery: search events by team, artist, venue, place, date and category; event, performer and venue detail; search-box suggestions; event-level ticket availability snapshots (listing and ticket counts, price range). Reads the anonymous SeatGeek Platform API (api.seatgeek.com/2) with the web app's public client id. Per-listing offers are behind DataDome and not covered.

- **`events/event`** (Event): Detail for an event id from search_events, suggest or a pasted seatgeek.com event URL. (Cost: 5 credit)
- **`events/performer`** (Performer): Detail for a performer id or slug from search_performers, search_events or suggest. (Cost: 5 credit)
- **`events/search_events`** (Search events): Discovery: find events for a team, artist, venue, place or date range, then pass an event id to event. (Cost: 5 credit)
- **`events/search_performers`** (Search performers): Resolve a team, artist or show name to a SeatGeek performer id/slug before listing its events. (Cost: 5 credit)
- **`events/search_venues`** (Search venues): Find a venue id by name or list venues in a city before listing events at a venue. (Cost: 5 credit)
- **`events/suggest`** (Suggest): Quickly resolve a partial name to SeatGeek ids across events, performers and venues in one call. (Cost: 5 credit)
- **`events/venue`** (Venue): Detail for a venue id from search_venues, search_events or suggest. (Cost: 5 credit)

### Skyscanner (`skyscanner-net`)

Skyscanner flight search and fare comparison: place autosuggest (sky place ids and entity ids), live itinerary search by origin, destination, dates, passengers and cabin with airlines, durations, stops, fare policy flags and booking-source deep links, plus cached indicative fares per day and per month. Anonymous same-origin JSON APIs on www.skyscanner.com; live quotes and cached indicative prices are labelled as such; live quotes include the site's estimate of taxes and fees.

- **`flights/monthly_prices`** (Monthly prices): Find the cheapest month for a route; then price_calendar for days and search_flights for a live quote. (Cost: 5 credit)
- **`flights/price_calendar`** (Price calendar): Find cheap dates for a route before running a live search_flights for a specific day. (Cost: 5 credit)
- **`flights/search_flights`** (Search flights): Compare fares and itineraries for concrete dates. Resolve places with suggest_places first; use price_calendar or monthly_prices for cheap-date discovery instead of many live searches. (Cost: 5 credit)
- **`flights/suggest_places`** (Suggest places): Start here to resolve a city or airport name into the identifiers the other functions take. (Cost: 5 credit)

### SpotHero parking (`spothero-com`)

SpotHero parking discovery and pricing for the US and Canada: hourly/daily, monthly and airport parking searches with itemised quotes for a time window, single-facility quotes, customer reviews, destinations with typical price ranges, upcoming events, and the city and airport directories. Read-only: no holds, bookings or checkout.

- **`parking/airports`** (Airports): Look up an airport's IATA code or destination id before search_airport_parking or destination. (Cost: 5 credit)
- **`parking/cities`** (Cities): Check whether SpotHero covers a city and get a starting coordinate for search_parking or search_monthly_parking. (Cost: 5 credit)
- **`parking/destination`** (Destination): Resolve a destination id to coordinates before search_parking, or show a venue's typical price ranges. (Cost: 5 credit)
- **`parking/destination_events`** (Destination events): Find event dates and SpotHero's event parking windows at a venue before pricing with search_parking. (Cost: 5 credit)
- **`parking/facility_quote`** (Facility quote): Re-price a facility found by a search for a different window, or read its full details. (Cost: 5 credit)
- **`parking/facility_reviews`** (Facility reviews): Read what customers say about a facility found by a search. (Cost: 5 credit)
- **`parking/search_airport_parking`** (Search airport parking): Compare off-airport and on-airport parking prices for a trip; airports and their codes come from `airports`. (Cost: 5 credit)
- **`parking/search_events`** (Search events): Turn a team, artist or venue name into destination coordinates and an event parking window for search_parking. (Cost: 5 credit)
- **`parking/search_monthly_parking`** (Search monthly parking): Find commuter or resident monthly parking near an address; coordinates come from `cities`, `destination` or `airports`. (Cost: 5 credit)
- **`parking/search_parking`** (Search parking): Find parking near a place or venue for a specific arrival and departure time and compare quoted prices; follow `facility_id` into facility_quote or facility_reviews. (Cost: 5 credit)

### StubHub (`stubhub-com`)

Search StubHub events, read event details and retrieve paginated public resale offers with quantity restrictions and price/fee disclosures. Uses anonymous web pages and read-only inventory requests.

- **`events/event`** (Event): Read event identity, venue, source status, performers and current inventory counts. Unconfirmed times are null; utc_offset_ms is the source offset, not an IANA timezone. (Cost: 0 credit)
- **`events/listings`** (Listings): Read one page of public resale offers for an event and ticket quantity. Numeric price is per ticket; display_total_for_quantity is the source-rendered group total. Fee disclosures and allowed quantities are preserved. No checkout or reservations. (Cost: 0 credit)
- **`events/search`** (Search): Search public StubHub events by keywords such as an artist, team, venue or city. Returns one relevance-ranked page; pass next_page as page. No structured date or location filters. (Cost: 0 credit)

### TickPick (`tickpick-com`)

TickPick (US resale ticket marketplace, all-in pricing): discover sports, concert, theater and comedy events by free text, performer, venue or location, and read event details with event-level listing statistics (count, min/max/average all-in per-ticket price) and daily/hourly price history from TickPick's own web API. Per-listing offers are not available (DataDome-protected).

- **`events/categories`** (Categories): Browse without a query: list leagues, teams, genres and shows and get performer slugs. Cached daily by the site. (Cost: 5 credit)
- **`events/event`** (Event): After search, performer_events or venue_events returned an event_id, or when the user pastes a tickpick.com/buy-... URL. (Cost: 5 credit)
- **`events/event_price_history`** (Event price history): To see how the cheapest ticket and the listing count moved over time for an event_id from search, performer_events or venue_events. (Cost: 5 credit)
- **`events/nearby_events`** (Nearby events): Location-first discovery: 'what is happening in Chicago'. Pass latitude/longitude; add the TickPick market slug (dma, for example washington-dc-md or chicago-il) for venues and just-announced lists. (Cost: 5 credit)
- **`events/performer_events`** (Performer events): Events for a performer whose slug and url_category came from search (performers[]) or categories (items[]). (Cost: 5 credit)
- **`events/search`** (Search): Start here to resolve a team, artist, show, venue or event name to TickPick identifiers. For a full event list use performer_events or venue_events; for one event use event. (Cost: 5 credit)
- **`events/venue_events`** (Venue events): Everything at a venue whose slug came from search or an event's venue. Page with offset = next_offset until it is null. (Cost: 5 credit)

### TodayTix (`todaytix-com`)

TodayTix theatre discovery and availability: the cities the site sells in, show search by city, keyword, date, price and sort, show detail with event-level low prices and publicly disclosed Rush/Lottery information, per-performance ticket snapshots with price bands and seat counts, and venue profiles. Read-only; no holds, lotteries or checkout.

- **`events/locations`** (Locations): First hop of discovery: resolve a city name to a TodayTix location id, timezone and currency. (Cost: 5 credit)
- **`events/search_shows`** (Search shows): Find shows by city, keyword or date, then pass a show id to show or showtimes. (Cost: 5 credit)
- **`events/show`** (Show): Detail for a show id from search_shows, or for a pasted todaytix.com show URL. (Cost: 5 credit)
- **`events/showtimes`** (Showtimes): Availability and prices per performance for a show id; filter by date window to keep pages small. (Cost: 5 credit)
- **`events/venue`** (Venue): Where a show plays: pass venue.slug from a show card, or a todaytix.com venue URL. (Cost: 5 credit)

### Trip.com (`trip-com`)

Public hotel destination directories and hotel profiles, room types, amenities and policies. No date-specific availability or offers.

- **`hotels/amenities`** (Amenities): Read published popular hotel amenities with source charge labels. Partial amenity coverage; no unlisted amenity is inferred absent. (Cost: 5 credit)
- **`hotels/destinations`** (Destinations): List linked hotel city directories from the public hotels landing page. Not a complete destination catalog. (Cost: 5 credit)
- **`hotels/hotel`** (Hotel): Read hotel identity, street address, description and published property facts. Does not quote a stay. (Cost: 5 credit)
- **`hotels/hotels`** (Hotels): List featured hotel profiles from a known city directory. Curated directory content, not dated availability search; marketing prices are omitted. (Cost: 5 credit)
- **`hotels/policies`** (Policies): Read published property policy sections including check-in/out, children, pets and fees when present. Policies may vary by room and do not represent a booking contract. (Cost: 5 credit)
- **`hotels/rooms`** (Rooms): Read published room types, bed descriptions and room features. Room types do not establish availability; price and availability are unknown. (Cost: 5 credit)

### Turo (`turo-com`)

Search public US Turo rental vehicles, read vehicle details and request anonymous dated price estimates. Search is a bounded source window, not exhaustive inventory. No account, booking or checkout actions.

- **`car-rentals/filters`** (Filters): Read Turo's public US vehicle-type, sort and fuel labels. vehicle_types and sort_options supply values accepted by search. Fuel labels are descriptive; this version does not expose a fuel filter. (Cost: 0 credit)
- **`car-rentals/search`** (Search): Search US Turo rentals around coordinates with optional make, vehicle type and sort. Dates use pickup-local time; omitted dates default to a three-day trip starting 21 days ahead at 10:00. Returns up to 50 vehicles from Turo's bounded source window (observed cap: 200), explicit truncation and no invented pagination cursor. Dated anonymous estimates come from the separate public pricing endpoint, with currency, source tax notice and included/excluded line items. quote=null means Turo supplied no estimate for that vehicle. Indicative daily prices are separate and must not be multiplied into trip totals. Estimates are not final booking prices. (Cost: 1 credit)
- **`car-rentals/vehicle`** (Vehicle): Read one public US Turo vehicle URL: identity, listing status, location, specifications, rating and indicative daily price. Optional paired start/end times request a separate dated home-pickup estimate for driver_age (default 30); without dates, include_quote=true uses a three-day trip starting 21 days ahead at 10:00 pickup-local time; otherwise quote and pricing_query are null. A null quote with dates means the source supplied no estimate. Taxes, protection and other costs may be excluded; inspect the source tax notice and line items. No final checkout price or availability guarantee. (Cost: 1 credit)

### UN Tourism (`untourism-int`)

Discover UN Tourism free statistical files and indicators, and read live country-year tourism observations with source units, flags and editions.

- **`statistics/data`** (Data): Country-year observations for up to 10 indicator codes (from `indicators`), parsed live from the official Excel files: value as source text (null for blank/suppressed cells with the reason in series_note), unit copied from the file, SDMX flag and label, provisional marker, country as ISO3 + M49 + label, file edition and publication date. Filter by ISO3 `countries`, `year_from`/`year_to` and, for arrivals-by-region, `partner` (total | all | UN Tourism region code). Cursor-paginated, deterministic order. (Cost: 5 credit)
- **`statistics/files`** (Files): The official UN Tourism Key Tourism Statistics Excel files (13 files: inbound arrivals/expenditure/by region/by purpose/by transport/accommodation, outbound departures/expenditure, domestic trips/accommodation, hotel capacity and occupancy, employment SDG 8.9.2, tourism GDP SDG 8.9.1). One live HEAD per file returns Last-Modified as source_updated_at, ETag and S3 version id, and changed_since_catalog flags a re-publication since the embedded catalogue. (Cost: 5 credit)
- **`statistics/indicators`** (Indicators): Search the 148 free indicators (code, name, series group, unit, source file). `query` matches words in the code, name, previous Compendium code, unit, file id or common synonyms (receipts -> inbound expenditure, occupancy -> hotel room/bed rates); `series_group` narrows to inbound, outbound, domestic, industries, employment or macro. Cursor-paginated; each page carries the live publication date of its source files. (Cost: 5 credit)


