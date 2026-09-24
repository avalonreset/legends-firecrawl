---
category: "places"
type: reference-card
provider_count: 18
---

# Category: places

> Local businesses and places: what is near an address, with hours, phone, address, website, rating and review count.

**Providers in this category:** 18

| Provider ID | Provider Name | Capabilities | Tier | Cost | Bypass Route |
|---|---|---|---|---|---|
| `bbb-business-profiles-ratings-complaint` | **BBB business profiles** | 4 | Public Commercial Web / Frontend JSON Endpoints | 0 Credits (Direct Web / Scraping Bypass) | Direct unauthenticated web fetch or lightweight house scraper |
| `bbb-org` | **Better Business Bureau** | 4 | Public Commercial Web / Frontend JSON Endpoints | 0 Credits (Direct Web / Scraping Bypass) | Direct unauthenticated web fetch or lightweight house scraper |
| `bing-com` | **Bing Maps** | 2 | Public Commercial Web / Frontend JSON Endpoints | 0 Credits (Direct Web / Scraping Bypass) | Direct unauthenticated web fetch or lightweight house scraper |
| `classpass-com` | **ClassPass** | 7 | Public Commercial Web / Frontend JSON Endpoints | 0 Credits (Direct Web / Scraping Bypass) | Direct unauthenticated web fetch or lightweight house scraper |
| `fresha-com` | **Fresha** | 5 | Public Commercial Web / Frontend JSON Endpoints | 0 Credits (Direct Web / Scraping Bypass) | Direct unauthenticated web fetch or lightweight house scraper |
| `gartner-com` | **Gartner** | 4 | Proprietary Commercial B2B Data Brokers | Credits Required or Paid Vendor Key | Use Alexandria credits or direct vendor account |
| `hipcamp-com` | **Hipcamp** | 7 | Proprietary Commercial B2B Data Brokers | Credits Required or Paid Vendor Key | Use Alexandria credits or direct vendor account |
| `houzz-com` | **Houzz** | 3 | Proprietary Commercial B2B Data Brokers | Credits Required or Paid Vendor Key | Use Alexandria credits or direct vendor account |
| `maps-google-com` | **Google Maps** | 4 | Proprietary Commercial B2B Data Brokers | Credits Required or Paid Vendor Key | Use Alexandria credits or direct vendor account |
| `ra-co` | **Resident Advisor** | 6 | Proprietary Commercial B2B Data Brokers | Credits Required or Paid Vendor Key | Use Alexandria credits or direct vendor account |
| `resy-com` | **Resy** | 6 | Proprietary Commercial B2B Data Brokers | Credits Required or Paid Vendor Key | Use Alexandria credits or direct vendor account |
| `rover-com` | **Rover** | 5 | Proprietary Commercial B2B Data Brokers | Credits Required or Paid Vendor Key | Use Alexandria credits or direct vendor account |
| `seatgeek-com` | **SeatGeek** | 7 | Public Commercial Web / Frontend JSON Endpoints | 0 Credits (Direct Web / Scraping Bypass) | Direct unauthenticated web fetch or lightweight house scraper |
| `spothero-com` | **SpotHero parking** | 10 | Public Commercial Web / Frontend JSON Endpoints | 0 Credits (Direct Web / Scraping Bypass) | Direct unauthenticated web fetch or lightweight house scraper |
| `stubhub-com` | **StubHub** | 3 | Public Commercial Web / Frontend JSON Endpoints | 0 Credits (Direct Web / Scraping Bypass) | Direct unauthenticated web fetch or lightweight house scraper |
| `tickpick-com` | **TickPick** | 7 | Public Commercial Web / Frontend JSON Endpoints | 0 Credits (Direct Web / Scraping Bypass) | Direct unauthenticated web fetch or lightweight house scraper |
| `todaytix-com` | **TodayTix** | 5 | Public Commercial Web / Frontend JSON Endpoints | 0 Credits (Direct Web / Scraping Bypass) | Direct unauthenticated web fetch or lightweight house scraper |
| `uhaul-com` | **U-Haul** | 5 | Public Commercial Web / Frontend JSON Endpoints | 0 Credits (Direct Web / Scraping Bypass) | Direct unauthenticated web fetch or lightweight house scraper |

## Capabilities Overview

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

### Bing Maps (`bing-com`)

Public Bing Maps local business search and structured business details.

- **`businesses/business`** (Business): One local business by its Bing ypid (from `search`): name, structured address, display and E.164 phone, website, coordinates, categories, aggregate rating with review count and source, current open-status sentence, and structured weekly opening hours (per day, 24h HH:MM ranges, all-day flag, closed days). Missing values are null; hours are null when Bing publishes none. [Cost: 5 credit]  
  *Options:* `ypid` *(required)*
- **`businesses/search`** (Search): Local businesses matching a category or a business name near a street address, city/state or postal code (US and other Bing Maps markets). One page of up to 30 results with Bing ypid, name, street address, phone, website, coordinates, category, aggregate rating with review count and source (Yelp/Tripadvisor/...), and current open status. Use the ypid with `business` for structured weekly hours. [Cost: 5 credit]  
  *Options:* `count`, `latitude`, `location`, `longitude`, `page`, `query` *(required)*

### ClassPass (`classpass-com`)

ClassPass class discovery and availability: find studios and class occurrences near a point for a date, read studio details and class types, a studio's schedule for a day, a single class occurrence with its availability status and displayed credit price, resolve locations and list markets. Anonymous same-origin JSON API of classpass.com; read-only, no reservations. Prices are ClassPass credits as displayed to anonymous visitors; member pricing is login-only and not returned.

- **`fitness-classes/location`** (Location): Turn a city or address into latitude/longitude for search_schedules / search_venues. [Cost: 5 credit]  
  *Options:* `place_id`, `query`
- **`fitness-classes/markets`** (Markets): Coverage check and a starting coordinate for search_schedules / search_venues without a geocoder. [Cost: 5 credit]  
  *Options:* `country_code`
- **`fitness-classes/schedule`** (Schedule): Detail for an `id` from search_schedules or venue_schedule. [Cost: 5 credit]  
  *Options:* `schedule_id`, `url`
- **`fitness-classes/search_schedules`** (Search schedules): Discovery of classes near a location on a date. Get coordinates from `location` or `markets`; pass a result's `id` to `schedule`, its `venue.id` to `venue` / `venue_schedule`. [Cost: 5 credit]  
  *Options:* `cursor`, `date`, `end_time`, `latitude`, `longitude`, `max_results`, `radius_km`, `start_time`, `tag_ids`, `vertical`
- **`fitness-classes/search_venues`** (Search venues): Discovery of studios near a location. Pass a result's `id` to `venue` or `venue_schedule`. [Cost: 5 credit]  
  *Options:* `date`, `latitude` *(required)*, `longitude` *(required)*, `max_results`, `radius_km`, `tag_ids`, `vertical`
- **`fitness-classes/venue`** (Venue): Details for a `venue.id` / `id` from search_schedules or search_venues. [Cost: 5 credit]  
  *Options:* `include_classes`, `venue_id` *(required)*
- **`fitness-classes/venue_schedule`** (Venue schedule): The day's timetable of a known studio (`venue_id` from search_venues / search_schedules / venue). [Cost: 5 credit]  
  *Options:* `class_id`, `cursor`, `date` *(required)*, `venue_id` *(required)*

### Fresha (`fresha-com`)

Fresha marketplace discovery without an account: find salons, spas and other venues near a geocode by treatment, filter by a date and time window to see available start times per service, read a venue's public service menu (advertised prices, durations, variants), team, hours and latest reviews, and find professionals and their profiles. Anonymous persisted GraphQL queries on www.fresha.com; reading only, no bookings, holds or carts.

- **`professionals/professional_detail`** (Professional detail): Detail read after search_professionals or autocomplete, or for a pasted fresha.com/p/ link. [Cost: 5 credit]  
  *Options:* `slug`, `url`
- **`professionals/search_professionals`** (Search professionals): Find a stylist, therapist or barber near a place; then pass the slug to professional_detail. [Cost: 5 credit]  
  *Options:* `cursor`, `latitude` *(required)*, `longitude` *(required)*, `page_size`, `query` *(required)*
- **`venues/autocomplete`** (Autocomplete): Resolve a treatment name to a taxonomy id before search_venues, or find a venue/professional slug by name. [Cost: 5 credit]  
  *Options:* `query` *(required)*
- **`venues/search_venues`** (Search venues): Discovery: find venues offering a treatment near a place, or check which venues have openings on a date; then pass a venue slug to venue_detail. [Cost: 5 credit]  
  *Options:* `availability_date`, `availability_start_time_from`, `availability_start_time_to`, `cursor`, `fresha_verified_only`, `has_deals`, `latitude` *(required)*, `longitude` *(required)*, `page_size`, `query`, `treatment_id`
- **`venues/venue_detail`** (Venue detail): Detail read after search_venues or autocomplete, or for a pasted fresha.com/a/ link. [Cost: 5 credit]  
  *Options:* `slug`, `url`

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

### Hipcamp (`hipcamp-com`)

Hipcamp campsite, cabin, glamping and RV listing discovery: dated search with location, group size and amenity filters, land details, per-site availability and displayed price quotes, blocked-date calendars, reviews, place autocomplete and public campground daily availability. Anonymous, read-only.

- **`campsite-listings/autocomplete`** (Autocomplete): Turn a place name into coordinates for search_lands, or find a land or public campground by name. [Cost: 5 credit]  
  *Options:* `limit`, `term` *(required)*, `types`
- **`campsite-listings/land`** (Land): After search_lands or a pasted hipcamp.com/land URL. For dated availability and full quotes call land_sites. [Cost: 5 credit]  
  *Options:* `masked_id`, `url`
- **`campsite-listings/land_calendar`** (Land calendar): Calendar view of what is already booked or closed for a land or a single site. [Cost: 5 credit]  
  *Options:* `masked_id` *(required)*, `site_id`
- **`campsite-listings/land_reviews`** (Land reviews): Read reviews for a land from search_lands or land; pass next_cursor to continue. [Cost: 5 credit]  
  *Options:* `cursor`, `masked_id` *(required)*
- **`campsite-listings/land_sites`** (Land sites): Dated availability check and price breakdown for a land found by search_lands or land. [Cost: 5 credit]  
  *Options:* `adults`, `arrive`, `children`, `depart`, `include_unmatched`, `masked_id` *(required)*, `pets`
- **`campsite-listings/public_campground_availability`** (Public campground availability): After autocomplete returns a campground_public result; pass its numeric id. [Cost: 5 credit]  
  *Options:* `campground_id` *(required)*, `end_date` *(required)*, `start_date` *(required)*
- **`campsite-listings/search_lands`** (Search lands): Start here to find lands near a place; use autocomplete first to turn a place name into coordinates. Feed masked_id into land, land_sites, land_calendar and land_reviews. [Cost: 5 credit]  
  *Options:* `accommodations`, `adults`, `amenities`, `arrive`, `bounding_box`, `children`, `depart`, `latitude`, `limit`, `longitude`, `offset`, `pets`, `sort`

### Houzz (`houzz-com`)

Public professional discovery, service profiles and portfolio summaries.

- **`professionals/profile`** (Profile): Read a public Houzz professional profile, source review aggregate, advertised services and service areas. No review text, contact actions or licensing verification. [Cost: 5 credit]  
  *Options:* `url` *(required)*
- **`professionals/projects`** (Projects): Read the initial portfolio project summaries embedded in a public professional profile, with photo counts and source location. This is a partial subset, not complete project detail. [Cost: 5 credit]  
  *Options:* `url` *(required)*
- **`professionals/search`** (Search): Read one page of Houzz professionals from an explicit location directory URL. Results may include sponsored or nonlocal providers. Follow next_url (15-step offsets, maximum 735). [Cost: 5 credit]  
  *Options:* `url` *(required)*

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

### Resident Advisor (`ra-co`)

Resident Advisor (ra.co) electronic music and nightlife events worldwide, read from RA's own anonymous GraphQL API: resolve a city to its RA area, list events for an area and date range with genre and keyword filters, facets and pagination, read one event with lineup, venue and the public primary ticket tiers (price, booking fee, currency, sale status, on-sale window), search events, venues, artists, promoters, labels and areas by name, and read venue and artist profiles with their upcoming events. Read only: no purchases, holds or resale offers.

- **`events/areas`** (Areas): First step of event discovery: you need the numeric `area_id` for `events`, or the time zone and currency of a city. [Cost: 5 credit]  
  *Options:* `country_code`, `query`, `url_name`
- **`events/artist`** (Artist): You have an artist id (from `search` or an event's `artists[].id`), an RA slug, or a pasted `https://ra.co/dj/{slug}` URL and need the profile or upcoming dates. [Cost: 5 credit]  
  *Options:* `artist_id`, `events_limit`, `slug`, `url`
- **`events/event`** (Event): You have an RA event id (from `events`, `search`, `venue`, `artist`) or a pasted `https://ra.co/events/{id}` URL and need details or ticket prices and sale status. [Cost: 5 credit]  
  *Options:* `event_id`, `url`
- **`events/events`** (Events): Discover events by city and date; take `area_id` from `areas` and chain each `events[].id` into `event` for tickets. [Cost: 5 credit]  
  *Options:* `area_id` *(required)*, `date_from`, `date_to`, `genre`, `page`, `page_size`, `query`, `sort`
- **`events/search`** (Search): You know a name (artist, club, party, promoter, city) and need its RA id to chain into `event`, `venue`, `artist` or `events`. [Cost: 5 credit]  
  *Options:* `limit`, `query` *(required)*, `types`
- **`events/venue`** (Venue): You have a venue id (from `search`, `events[].venue.id`, or a pasted `https://ra.co/clubs/{id}` URL) and need the venue's details or its upcoming events. [Cost: 5 credit]  
  *Options:* `events_limit`, `url`, `venue_id`

### Resy (`resy-com`)

Resy restaurant discovery and reservation availability from Resy's own web API: city lookup, venue search with inline slots, venue details, per-day availability with booked-out vs closed distinction, availability calendars and slot deposit/cancellation conditions. Read-only: no bookings, holds or notifications.

- **`restaurants/availability`** (Availability): Given a venue_id (from search_venues or venue) and a date. One upstream availability call plus one calendar call. [Cost: 5 credit]  
  *Options:* `day` *(required)*, `party_size`, `time_filter`, `venue_id` *(required)*
- **`restaurants/calendar`** (Calendar): To find which days a venue has any table for a party size before calling availability, or to tell a closed day from a sold-out one. [Cost: 5 credit]  
  *Options:* `days`, `end_date`, `party_size`, `start_date`, `venue_id` *(required)*
- **`restaurants/locations`** (Locations): First hop when you know a city name but not its Resy slug or coordinates. Returns the coordinates to pass to search_venues. [Cost: 5 credit]  
  *Options:* `country_code`, `latitude`, `limit`, `longitude`, `query`
- **`restaurants/search_venues`** (Search venues): Discovery: find restaurants near a point (optionally by name or cuisine keyword) that have a table on a day. Follow with venue, availability or slot_conditions using venue_id and config_token. [Cost: 5 credit]  
  *Options:* `day` *(required)*, `include_tock_inventory`, `latitude` *(required)*, `longitude` *(required)*, `page`, `party_size`, `per_page`, `query`, `radius_m`, `time_filter`
- **`restaurants/slot_conditions`** (Slot conditions): After availability or search_venues returned a slot `config_token`. Alternatively give venue_id + day (+ optional start time and seating type) and the first matching slot of that day is described. [Cost: 5 credit]  
  *Options:* `config_token`, `day` *(required)*, `party_size`, `seating_type`, `start_time`, `venue_id`
- **`restaurants/venue`** (Venue): Detail hop after search_venues, or when given a resy.com/cities/{city}/venues/{slug} URL. Use availability for slots. [Cost: 5 credit]  
  *Options:* `location`, `url`, `url_slug`, `venue_id`

### Rover (`rover-com`)

Rover public pet-care discovery without an account: search sitters by service (boarding, house sitting, drop-in visits, dog walking, doggy day care), location, dates, dog size and price; read a sitter's public profile with every listed rate (sitter rate and the full price including Rover's owner-side service fee), acceptance rules and cancellation policy; read the sitter's public availability calendar for a date window; list the sitter's reviews; and resolve free-text places to the location strings the search accepts. Source: the www.rover.com /api/v7/ JSON API the website calls anonymously. US market from a US ISP exit (country and currency follow the request IP); prices are sitter-listed advertised rates in USD, not quotes; availability is what the sitter listed, not a booking guarantee.

- **`pet-care-services/get_sitter`** (Get sitter): After `search_sitters`, to read a sitter's full profile and every listed rate. [Cost: 5 credit]  
  *Options:* `slug`, `url`
- **`pet-care-services/get_sitter_availability`** (Get sitter availability): Check which days a specific sitter lists as open for a service before contacting them on Rover. [Cost: 5 credit]  
  *Options:* `end_date`, `opk` *(required)*, `service_type`, `start_date`
- **`pet-care-services/list_sitter_reviews`** (List sitter reviews): Read what pet owners wrote about a specific sitter. [Cost: 5 credit]  
  *Options:* `opk` *(required)*, `page`
- **`pet-care-services/search_sitters`** (Search sitters): Find sitters for a service near a place, optionally for dates, dog size and budget; then chain `slug`/`opk` into the detail functions. [Cost: 5 credit]  
  *Options:* `end_date`, `giant_dogs`, `large_dogs`, `location` *(required)*, `max_price`, `medium_dogs`, `min_price`, `page`, `pet_type`, `service_type` *(required)*, `small_dogs`, `start_date`
- **`pet-care-services/suggest_locations`** (Suggest locations): Turn a partial or ambiguous place name into a location string before `search_sitters`. [Cost: 5 credit]  
  *Options:* `country_code`, `query` *(required)*

### SeatGeek (`seatgeek-com`)

SeatGeek event discovery: search events by team, artist, venue, place, date and category; event, performer and venue detail; search-box suggestions; event-level ticket availability snapshots (listing and ticket counts, price range). Reads the anonymous SeatGeek Platform API (api.seatgeek.com/2) with the web app's public client id. Per-listing offers are behind DataDome and not covered.

- **`events/event`** (Event): Detail for an event id from search_events, suggest or a pasted seatgeek.com event URL. [Cost: 5 credit]  
  *Options:* `event_id`, `url`
- **`events/performer`** (Performer): Detail for a performer id or slug from search_performers, search_events or suggest. [Cost: 5 credit]  
  *Options:* `performer_id`, `slug`
- **`events/search_events`** (Search events): Discovery: find events for a team, artist, venue, place or date range, then pass an event id to event. [Cost: 5 credit]  
  *Options:* `end_date`, `event_ids`, `latitude`, `longitude`, `page`, `per_page`, `performer_id`, `performer_slug`, `query`, `range_miles`, `sort`, `start_date`, `taxonomy`, `venue_id`
- **`events/search_performers`** (Search performers): Resolve a team, artist or show name to a SeatGeek performer id/slug before listing its events. [Cost: 5 credit]  
  *Options:* `page`, `per_page`, `query` *(required)*
- **`events/search_venues`** (Search venues): Find a venue id by name or list venues in a city before listing events at a venue. [Cost: 5 credit]  
  *Options:* `city`, `page`, `per_page`, `query`, `state`
- **`events/suggest`** (Suggest): Quickly resolve a partial name to SeatGeek ids across events, performers and venues in one call. [Cost: 5 credit]  
  *Options:* `limit`, `query` *(required)*
- **`events/venue`** (Venue): Detail for a venue id from search_venues, search_events or suggest. [Cost: 5 credit]  
  *Options:* `venue_id` *(required)*

### SpotHero parking (`spothero-com`)

SpotHero parking discovery and pricing for the US and Canada: hourly/daily, monthly and airport parking searches with itemised quotes for a time window, single-facility quotes, customer reviews, destinations with typical price ranges, upcoming events, and the city and airport directories. Read-only: no holds, bookings or checkout.

- **`parking/airports`** (Airports): Look up an airport's IATA code or destination id before search_airport_parking or destination. [Cost: 5 credit]  
  *Options:* `query`
- **`parking/cities`** (Cities): Check whether SpotHero covers a city and get a starting coordinate for search_parking or search_monthly_parking. [Cost: 5 credit]  
  *Options:* `latitude`, `limit`, `longitude`, `query`
- **`parking/destination`** (Destination): Resolve a destination id to coordinates before search_parking, or show a venue's typical price ranges. [Cost: 5 credit]  
  *Options:* `destination_id` *(required)*
- **`parking/destination_events`** (Destination events): Find event dates and SpotHero's event parking windows at a venue before pricing with search_parking. [Cost: 5 credit]  
  *Options:* `destination_id` *(required)*, `page`, `page_size`, `starts`
- **`parking/facility_quote`** (Facility quote): Re-price a facility found by a search for a different window, or read its full details. [Cost: 5 credit]  
  *Options:* `ends` *(required)*, `facility_id` *(required)*, `starts` *(required)*
- **`parking/facility_reviews`** (Facility reviews): Read what customers say about a facility found by a search. [Cost: 5 credit]  
  *Options:* `facility_id` *(required)*, `page`
- **`parking/search_airport_parking`** (Search airport parking): Compare off-airport and on-airport parking prices for a trip; airports and their codes come from `airports`. [Cost: 5 credit]  
  *Options:* `cursor`, `ends`, `iata`, `oversize`, `page_size`, `starts`
- **`parking/search_events`** (Search events): Turn a team, artist or venue name into destination coordinates and an event parking window for search_parking. [Cost: 5 credit]  
  *Options:* `limit`, `query` *(required)*
- **`parking/search_monthly_parking`** (Search monthly parking): Find commuter or resident monthly parking near an address; coordinates come from `cities`, `destination` or `airports`. [Cost: 5 credit]  
  *Options:* `cursor`, `latitude`, `longitude`, `max_distance_meters`, `oversize`, `page_size`, `starts`
- **`parking/search_parking`** (Search parking): Find parking near a place or venue for a specific arrival and departure time and compare quoted prices; follow `facility_id` into facility_quote or facility_reviews. [Cost: 5 credit]  
  *Options:* `cursor`, `destination_id`, `ends`, `latitude`, `longitude`, `max_distance_meters`, `oversize`, `page_size`, `show_unavailable`, `starts`

### StubHub (`stubhub-com`)

Search StubHub events, read event details and retrieve paginated public resale offers with quantity restrictions and price/fee disclosures. Uses anonymous web pages and read-only inventory requests.

- **`events/event`** (Event): Read event identity, venue, source status, performers and current inventory counts. Unconfirmed times are null; utc_offset_ms is the source offset, not an IANA timezone. [Cost: 0 credit]  
  *Options:* `url` *(required)*
- **`events/listings`** (Listings): Read one page of public resale offers for an event and ticket quantity. Numeric price is per ticket; display_total_for_quantity is the source-rendered group total. Fee disclosures and allowed quantities are preserved. No checkout or reservations. [Cost: 0 credit]  
  *Options:* `page`, `quantity`, `url` *(required)*
- **`events/search`** (Search): Search public StubHub events by keywords such as an artist, team, venue or city. Returns one relevance-ranked page; pass next_page as page. No structured date or location filters. [Cost: 0 credit]  
  *Options:* `page`, `query` *(required)*

### TickPick (`tickpick-com`)

TickPick (US resale ticket marketplace, all-in pricing): discover sports, concert, theater and comedy events by free text, performer, venue or location, and read event details with event-level listing statistics (count, min/max/average all-in per-ticket price) and daily/hourly price history from TickPick's own web API. Per-listing offers are not available (DataDome-protected).

- **`events/categories`** (Categories): Browse without a query: list leagues, teams, genres and shows and get performer slugs. Cached daily by the site. [Cost: 5 credit]  
  *Options:* `group`
- **`events/event`** (Event): After search, performer_events or venue_events returned an event_id, or when the user pastes a tickpick.com/buy-... URL. [Cost: 5 credit]  
  *Options:* `event_id`, `url`
- **`events/event_price_history`** (Event price history): To see how the cheapest ticket and the listing count moved over time for an event_id from search, performer_events or venue_events. [Cost: 5 credit]  
  *Options:* `event_id` *(required)*
- **`events/nearby_events`** (Nearby events): Location-first discovery: 'what is happening in Chicago'. Pass latitude/longitude; add the TickPick market slug (dma, for example washington-dc-md or chicago-il) for venues and just-announced lists. [Cost: 5 credit]  
  *Options:* `dma`, `latitude` *(required)*, `limit`, `longitude` *(required)*
- **`events/performer_events`** (Performer events): Events for a performer whose slug and url_category came from search (performers[]) or categories (items[]). [Cost: 5 credit]  
  *Options:* `include_nearby`, `limit`, `performer_slug`, `url`, `url_category`
- **`events/search`** (Search): Start here to resolve a team, artist, show, venue or event name to TickPick identifiers. For a full event list use performer_events or venue_events; for one event use event. [Cost: 5 credit]  
  *Options:* `limit`, `query` *(required)*
- **`events/venue_events`** (Venue events): Everything at a venue whose slug came from search or an event's venue. Page with offset = next_offset until it is null. [Cost: 5 credit]  
  *Options:* `limit`, `offset`, `url`, `venue_slug`

### TodayTix (`todaytix-com`)

TodayTix theatre discovery and availability: the cities the site sells in, show search by city, keyword, date, price and sort, show detail with event-level low prices and publicly disclosed Rush/Lottery information, per-performance ticket snapshots with price bands and seat counts, and venue profiles. Read-only; no holds, lotteries or checkout.

- **`events/locations`** (Locations): First hop of discovery: resolve a city name to a TodayTix location id, timezone and currency. [Cost: 5 credit]  
  *Options:* None
- **`events/search_shows`** (Search shows): Find shows by city, keyword or date, then pass a show id to show or showtimes. [Cost: 5 credit]  
  *Options:* `date`, `limit`, `location_id` *(required)*, `max_price`, `offset`, `query`, `sort_by`, `sort_order`, `timezone`
- **`events/show`** (Show): Detail for a show id from search_shows, or for a pasted todaytix.com show URL. [Cost: 5 credit]  
  *Options:* `show_id`, `url`
- **`events/showtimes`** (Showtimes): Availability and prices per performance for a show id; filter by date window to keep pages small. [Cost: 5 credit]  
  *Options:* `date_from`, `date_to`, `include_no_inventory`, `limit`, `offset`, `show_id`, `url`
- **`events/venue`** (Venue): Where a show plays: pass venue.slug from a show card, or a todaytix.com venue URL. [Cost: 5 credit]  
  *Options:* `location_id`, `url`, `venue_slug`

### U-Haul (`uhaul-com`)

uhaul.com truck rental quotes and availability: search in-town (local) and one-way truck rates for a pickup location, optional drop-off location and pickup date, read the per-model rate basis (rental rate, mileage rate, extra day/mile, allowed days and distance, environmental fee) and the site's own availability text; autosuggest pickup/drop-off place names; list U-Haul locations in a city, read one location's profile (address, phone, hours, rating, base in-town rates) and its customer reviews. Read-only: no reservations, holds or checkout.

- **`truck-rentals/get_location`** (Get location): You have an `entity_id` from `list_locations` (or a pasted uhaul.com/Locations/.../{id}/ URL) and need the location's profile. [Cost: 5 credit]  
  *Options:* `entity_id` *(required)*
- **`truck-rentals/get_location_reviews`** (Get location reviews): You have a location `entity_id` and want its customer feedback. [Cost: 5 credit]  
  *Options:* `entity_id` *(required)*, `limit`, `offset`
- **`truck-rentals/list_locations`** (List locations): Find location `entity_id`s in a place before `get_location` / `get_location_reviews`. [Cost: 5 credit]  
  *Options:* `city` *(required)*, `postal_code`, `state` *(required)*
- **`truck-rentals/search_truck_rates`** (Search truck rates): The caller wants truck sizes, prices or availability for a move between two places or around one place on a date. Use `suggest_locations` first when the place name is ambiguous. [Cost: 5 credit]  
  *Options:* `dropoff_location`, `pickup_date`, `pickup_location` *(required)*
- **`truck-rentals/suggest_locations`** (Suggest locations): Normalise a free-text place into the exact `pickup_location` / `dropoff_location` string before calling `search_truck_rates`. [Cost: 5 credit]  
  *Options:* `max_results`, `term` *(required)*

