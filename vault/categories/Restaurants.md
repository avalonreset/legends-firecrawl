---
type: category
id: "restaurants"
title: "Restaurants"
providers_count: 6
---

# Category: Restaurants

> Restaurant locations, opening hours, menus, prices and product options.

Part of [[_Index|Legends Alexandria]] and the [[manifesto/The-Great-AI-Data-Arbitrage|Great AI Data Arbitrage]].

## Cataloged Providers (6)

| Provider | Capabilities | Data Tier | Direct Bypass Available? |
|---|---|---|---|
| `dominos-ca` (**Domino's Canada**) | 7 | Public Commercial Web / Frontend JSON Endpoints | Yes (Direct unauthenticated web fetch or lightweight house scraper) |
| `dominos-com` (**Domino's US**) | 7 | Public Commercial Web / Frontend JSON Endpoints | Yes (Direct unauthenticated web fetch or lightweight house scraper) |
| `doordash-com` (**DoorDash US**) | 8 | Public Commercial Web / Frontend JSON Endpoints | Yes (Direct unauthenticated web fetch or lightweight house scraper) |
| `pizzahut-ca` (**Pizza Hut Canada**) | 9 | Proprietary Commercial B2B Data Brokers | No (Proprietary) |
| `pizzahut-com` (**Pizza Hut US**) | 7 | Proprietary Commercial B2B Data Brokers | No (Proprietary) |
| `resy-com` (**Resy**) | 6 | Proprietary Commercial B2B Data Brokers | No (Proprietary) |

## Tools & Capabilities

### Domino's Canada (`dominos-ca`)

Public Canadian store directory, nearby locations, profiles and complete store-specific menus. Read-only; no order placement.

- **`restaurants/categories`** (Menu categories): Read the flattened menu category tree and coupon categories for a store. (Cost: 5 credit)
- **`restaurants/category`** (Category products): Read products and priced size/crust variants in a category and its direct subcategories. (Cost: 5 credit)
- **`restaurants/directory`** (Store directory): List Canadian stores from the public national directory: store ID, city, province and page URL. (Cost: 5 credit)
- **`restaurants/menu`** (Full menu): Read the whole structured store menu: categories, products, variants, modifier tables and coupons. (Cost: 5 credit)
- **`restaurants/modifiers`** (Product options): Read full sizes, crusts, toppings, sides, cooking instructions and priced variants for a product. (Cost: 5 credit)
- **`restaurants/store`** (Store details): Read one store profile, hours, payment methods, waits and service capabilities. (Cost: 5 credit)
- **`restaurants/stores`** (Find nearby stores): Find Canadian stores near latitude and longitude; returns address, hours, availability and waits. (Cost: 5 credit)

### Domino's US (`dominos-com`)

Public US store lookup, menus, product customization and published delivery fees.

- **`restaurants/categories`** (Categories): List menu categories for one US store. (Cost: 5 credit)
- **`restaurants/category`** (Category): Read category products and direct subcategories for one store. (Cost: 5 credit)
- **`restaurants/delivery_cost`** (Delivery cost): Read the published store delivery fee and minimum in USD. Does not validate an address or create an order. (Cost: 5 credit)
- **`restaurants/menu`** (Menu): Read the complete store menu, variants, modifiers and coupons in one request. (Cost: 5 credit)
- **`restaurants/modifiers`** (Modifiers): Read product sizes, bases, toppings, sides and cooking options. (Cost: 5 credit)
- **`restaurants/store`** (Store): Read public store details, availability and hours. (Cost: 5 credit)
- **`restaurants/stores`** (Stores): Find US stores near a postal code or city and state, nearest first with the distance in miles. (Cost: 5 credit)

### DoorDash US (`doordash-com`)

DoorDash US store and product search, convenience/grocery catalogs, product details and public reviews from DoorDash's own web APIs.

- **`products/categories`** (Categories): Top-level category list of one store. Use items for the products themselves. (Cost: 5 credit)
- **`products/items`** (Items): Storefront item groups of one store, up to max_pages feed pages; category carousels, not full inventory. Use search_items to look up a specific product. (Cost: 5 credit)
- **`products/product`** (Product): One product by store_id + item_id (from items or search_items): name, brand, prices, photos, purchase rules, descriptive sections. (Cost: 5 credit)
- **`products/review_summary`** (Review summary): Rating and review totals with star percentages for one product. (Cost: 5 credit)
- **`products/reviews`** (Reviews): Public customer reviews for one product, paged with limit/offset. (Cost: 5 credit)
- **`products/search`** (Search): Find stores and restaurants near a latitude/longitude for a query. Use search_items to search products inside one store. (Cost: 5 credit)
- **`products/search_items`** (Search items): Products matching a query inside one store, paged by cursor up to max_pages. (Cost: 5 credit)
- **`products/store`** (Store): Store details for one grocery/convenience store id. Use search for discovery. (Cost: 5 credit)

### Pizza Hut Canada (`pizzahut-ca`)

Canadian Pizza Hut store, menu, builder and promotion data from the public Yum storefront.

- **`restaurants/bundles`** (Deal bundles): Read deal bundles, optionally selected by code. (Cost: 5 credit)
- **`restaurants/categories`** (Menu categories): Read the store menu category index. (Cost: 5 credit)
- **`restaurants/category`** (Category products): Read items in one category and optional subcategories. (Cost: 5 credit)
- **`restaurants/directory`** (Store directory): List Pizza Hut Canada stores, optionally by province, walking the source connection. (Cost: 5 credit)
- **`restaurants/menu`** (Full menu): Read the full menu query with deduplicated products, variants and bundles. Products and variants are paginated (default and maximum 10 each); category/bundle metadata and total counts repeat on each page. (Cost: 5 credit)
- **`restaurants/modifiers`** (Product options): Read a product builder with variants, slots, modifiers and prices. (Cost: 5 credit)
- **`restaurants/promotions`** (Promotions): Read public promotions and their requirements and effects. (Cost: 5 credit)
- **`restaurants/store`** (Store details): Read one store profile, address, occasions and service hours. (Cost: 5 credit)
- **`restaurants/stores`** (Find nearby stores): Find nearby and delivering Pizza Hut Canada stores by coordinates or postal anchor. (Cost: 5 credit)

### Pizza Hut US (`pizzahut-com`)

Discover Pizza Hut US stores and read menus, products, modifiers, bundles and the paginated store directory.

- **`restaurants/bundles`** (Bundles): Read Pizza Hut US bundles and their choices; optionally filter by bundle codes. For online deals and prices, keep only bundles whose redeemable_online and visible_online are true. (Cost: 5 credit)
- **`restaurants/categories`** (Categories): List menu categories and subcategories for a Pizza Hut US store, with the first item in each. (Cost: 5 credit)
- **`restaurants/category`** (Category): Read products, variants and bundles in a Pizza Hut US menu category. For online deals and prices, keep only bundles whose redeemable_online and visible_online are true. (Cost: 5 credit)
- **`restaurants/directory`** (Directory): Page through the Pizza Hut US store directory, optionally filtered by state. Resume with next_cursor when has_more is true. (Cost: 5 credit)
- **`restaurants/modifiers`** (Modifiers): Read a Pizza Hut US product with variants, options, modifier slots, weights and prices. (Cost: 5 credit)
- **`restaurants/store`** (Store): Read one Pizza Hut US store, including address, hours, order availability and tax configuration. (Cost: 5 credit)
- **`restaurants/stores`** (Stores): Discover nearby Pizza Hut stores and their store numbers, addresses, hours and supported occasions. (Cost: 5 credit)

### Resy (`resy-com`)

Resy restaurant discovery and reservation availability from Resy's own web API: city lookup, venue search with inline slots, venue details, per-day availability with booked-out vs closed distinction, availability calendars and slot deposit/cancellation conditions. Read-only: no bookings, holds or notifications.

- **`restaurants/availability`** (Availability): Given a venue_id (from search_venues or venue) and a date. One upstream availability call plus one calendar call. (Cost: 5 credit)
- **`restaurants/calendar`** (Calendar): To find which days a venue has any table for a party size before calling availability, or to tell a closed day from a sold-out one. (Cost: 5 credit)
- **`restaurants/locations`** (Locations): First hop when you know a city name but not its Resy slug or coordinates. Returns the coordinates to pass to search_venues. (Cost: 5 credit)
- **`restaurants/search_venues`** (Search venues): Discovery: find restaurants near a point (optionally by name or cuisine keyword) that have a table on a day. Follow with venue, availability or slot_conditions using venue_id and config_token. (Cost: 5 credit)
- **`restaurants/slot_conditions`** (Slot conditions): After availability or search_venues returned a slot `config_token`. Alternatively give venue_id + day (+ optional start time and seating type) and the first matching slot of that day is described. (Cost: 5 credit)
- **`restaurants/venue`** (Venue): Detail hop after search_venues, or when given a resy.com/cities/{city}/venues/{slug} URL. Use availability for slots. (Cost: 5 credit)


