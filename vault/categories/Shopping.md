---
type: category
id: "shopping"
title: "Shopping"
providers_count: 20
---

# Category: Shopping

> Products, prices, sizes, availability and customer reviews.

Part of [[_Index|Legends Alexandria]] and the [[manifesto/The-Great-AI-Data-Arbitrage|Great AI Data Arbitrage]].

## Cataloged Providers (20)

| Provider | Capabilities | Data Tier | Direct Bypass Available? |
|---|---|---|---|
| `allbirds-com` (**Allbirds**) | 6 | Public Commercial Web / Frontend JSON Endpoints | Yes (Direct unauthenticated web fetch or lightweight house scraper) |
| `amazon-com` (**Amazon US**) | 10 | Public Commercial Web / Frontend JSON Endpoints | Yes (Direct unauthenticated web fetch or lightweight house scraper) |
| `autotrader-com` (**Autotrader**) | 5 | Public Commercial Web / Frontend JSON Endpoints | Yes (Direct unauthenticated web fetch or lightweight house scraper) |
| `bestbuy-com` (**Best Buy US**) | 8 | Public Commercial Web / Frontend JSON Endpoints | Yes (Direct unauthenticated web fetch or lightweight house scraper) |
| `discogs-com` (**Discogs**) | 8 | Open Non-Profit, Legal & Community Ecosystems | Yes (Direct community/non-profit REST API) |
| `doordash-com` (**DoorDash US**) | 8 | Public Commercial Web / Frontend JSON Endpoints | Yes (Direct unauthenticated web fetch or lightweight house scraper) |
| `ebay-com` (**eBay listings**) | 4 | Public Commercial Web / Frontend JSON Endpoints | Yes (Direct unauthenticated web fetch or lightweight house scraper) |
| `etsy-com` (**Etsy**) | 5 | Proprietary Commercial B2B Data Brokers | No (Proprietary) |
| `ikea-com` (**IKEA US**) | 6 | Proprietary Commercial B2B Data Brokers | No (Proprietary) |
| `kbb-com` (**Kelley Blue Book**) | 4 | Proprietary Commercial B2B Data Brokers | No (Proprietary) |
| `newegg-com` (**Newegg US**) | 3 | Proprietary Commercial B2B Data Brokers | No (Proprietary) |
| `nike-com` (**Nike US**) | 6 | Proprietary Commercial B2B Data Brokers | No (Proprietary) |
| `peerspot-com` (**PeerSpot**) | 4 | Proprietary Commercial B2B Data Brokers | No (Proprietary) |
| `psacard-com` (**PSA**) | 5 | Proprietary Commercial B2B Data Brokers | No (Proprietary) |
| `reclameaqui-com-br` (**Reclame Aqui**) | 7 | Proprietary Commercial B2B Data Brokers | No (Proprietary) |
| `rtings-com` (**RTINGS**) | 4 | Proprietary Commercial B2B Data Brokers | No (Proprietary) |
| `shopify` (**Shopify Catalog**) | 6 | Proprietary Commercial B2B Data Brokers | No (Proprietary) |
| `target-com` (**Target**) | 3 | Public Commercial Web / Frontend JSON Endpoints | Yes (Direct unauthenticated web fetch or lightweight house scraper) |
| `traderjoes-com` (**Trader Joe's**) | 3 | Public Commercial Web / Frontend JSON Endpoints | Yes (Direct unauthenticated web fetch or lightweight house scraper) |
| `uhaul-com` (**U-Haul**) | 5 | Public Commercial Web / Frontend JSON Endpoints | Yes (Direct unauthenticated web fetch or lightweight house scraper) |

## Tools & Capabilities

### Allbirds (`allbirds-com`)

Explore Allbirds collections, product suggestions, size-level offers and published materials/care details.

- **`products/collections`** (Collections): List curated collection links from the Allbirds US homepage. Partial discovery, not every archived collection. (Cost: 5 credit)
- **`products/details`** (Details): Read substantive product design, materials, sustainability and care sections. Unsupported layouts fail closed. (Cost: 5 credit)
- **`products/product`** (Product): Read the canonical product profile and source-labelled offer currency; stock is a source snapshot. (Cost: 5 credit)
- **`products/products`** (Products): Browse one Allbirds collection page. Follow next_page with the same collection and limit; prices are omitted until product details supply currency. (Cost: 5 credit)
- **`products/search`** (Search): Find predictive product suggestions for a query. Up to ten results; this is not exhaustive or paginated search. (Cost: 5 credit)
- **`products/variants`** (Variants): Compare published sizes, SKUs, color labels and size-level prices and stock for one product. (Cost: 5 credit)

### Amazon US (`amazon-com`)

Amazon US public product details, photos, specifications, variants, displayed review totals, search, suggestions, featured offers, sellers, stock and batch prices.

- **`products/offer`** (Offer): Get the featured buy-box offer for one Amazon.com ASIN or product URL: displayed price, list price and savings, boolean in-stock state with Amazon's availability text, seller and shipper, item condition, delivery promise, coupon and other-offers hints. Unknown values are null. (Cost: 5 credit)
- **`products/photos`** (Photos): Get the selected product image gallery. (Cost: 5 credit)
- **`products/prices`** (Prices): Check current buy-box price and stock state for up to five Amazon.com ASINs in one call. Each row carries price, list price, in-stock flag, availability text, seller and condition; an ASIN that cannot be read gets an error string instead of failing the batch. (Cost: 5 credit)
- **`products/product`** (Product): Get public Amazon product details, displayed price, images, variants and review totals. (Cost: 5 credit)
- **`products/review_summary`** (Review summary): Get the displayed rating and count; individual review text is not included. (Cost: 5 credit)
- **`products/search`** (Search): Fetch one search page. Next-page input is returned; blocked pages raise an error. (Cost: 5 credit)
- **`products/specifications`** (Specifications): Get product specification tables and feature bullets. (Cost: 5 credit)
- **`products/suggestions`** (Suggestions): Get autocomplete suggestions for a search prefix. (Cost: 5 credit)
- **`products/variants`** (Variants): List the variant dimensions (color, size, style...) and sibling ASINs of an Amazon.com product, with the swatch availability flag Amazon renders. Set include_prices to also fetch the buy-box price and stock state of the selected ASIN and up to max_priced-1 sibling ASINs. (Cost: 5 credit)
- **`products/variations`** (Variations): List product variants and their attributes. Availability and prices require a separate lookup. (Cost: 5 credit)

### Autotrader (`autotrader-com`)

Autotrader.com (Cox Automotive) US vehicle marketplace: search new, used and certified listings by location, make/model, year, price and mileage; read one listing with pricing, specifications, features and seller; resolve make/model names to codes; facet counts by model year, trim and city; model specifications by style id.

- **`vehicles/get_listing`** (Get listing): After search_listings, or when the user pastes an autotrader.com/cars-for-sale/vehicle/{id} URL or a VIN. (Cost: 5 credit)
- **`vehicles/listing_facets`** (Listing facets): To see which years, trims or cities have inventory before searching, or to pick a trim_code for search_listings. (Cost: 5 credit)
- **`vehicles/search_listings`** (Search listings): Discovering vehicles for sale in the US; chain listing_id into get_listing, style_id into vehicle_specs and seller.owner_id into dealer_id. Use suggest_make_model to turn 'Toyota Camry' into make_code/model_code first. (Cost: 5 credit)
- **`vehicles/suggest_make_model`** (Suggest make model): Before search_listings or listing_facets when you have a make/model name rather than codes. (Cost: 5 credit)
- **`vehicles/vehicle_specs`** (Vehicle specs): After get_listing or search_listings, to read the manufacturer specifications behind a listing. (Cost: 5 credit)

### Best Buy US (`bestbuy-com`)

Public Best Buy US catalog, product details, prices, review totals and location-specific availability.

- **`products/availability`** (Availability): Get shipping, delivery and pickup promises for a SKU, ZIP code and store. Quantities are upstream indicators, not verified stock counts. (Cost: 5 credit)
- **`products/pricing`** (Pricing): Get displayed US pricing, condition and mobile-contract terms. (Cost: 5 credit)
- **`products/product`** (Product): Get public Bestbuy product details, displayed price, images, variants and review totals. (Cost: 5 credit)
- **`products/review_summary`** (Review summary): Get the displayed rating and count; individual review text is not included. (Cost: 5 credit)
- **`products/search`** (Search): Fetch one search page. Next-page input is returned; blocked pages raise an error. (Cost: 5 credit)
- **`products/stores`** (Stores): Find nearby open Best Buy stores by US ZIP code; use store_id for availability. (Cost: 5 credit)
- **`products/suggestions`** (Suggestions): Get autocomplete suggestions for a search prefix. (Cost: 5 credit)
- **`products/variations`** (Variations): List product variants and their attributes. Availability and prices require a separate lookup. (Cost: 5 credit)

### Discogs (`discogs-com`)

Public Discogs music releases, masters, artists and labels with search and paginated catalogs.

- **`releases/artist`** (Artist): One Discogs artist or group by artist ID: name, real name, profile text, name variations, aliases, members (for groups) or groups (for people), external URLs and images. (Cost: 5 credit)
- **`releases/artist_releases`** (Artist releases): Releases by an artist (their discography as Discogs credits it), one page at a time: masters and standalone releases with role (Main, Remix, Appearance, ...), year, format and label, sortable by year, title or format. (Cost: 5 credit)
- **`releases/label`** (Label): One Discogs label by label ID: name, profile, contact info, parent label, sublabels, external URLs and images. (Cost: 5 credit)
- **`releases/label_releases`** (Label releases): A label's catalog, one page at a time: every release on the label with its catalog number, artist, title, format and year, in Discogs' catalog-number order. (Cost: 5 credit)
- **`releases/master`** (Master): One Discogs master release (the grouping of all pressings of the same album or single) by master ID: title, artists, original year, main and most recent release IDs, genres, styles, canonical tracklist, images, videos and marketplace summary. Use master_versions to list its pressings. (Cost: 5 credit)
- **`releases/master_versions`** (Master versions): Pressing variants of a master release: every release (country, label, catalog number, format, year) grouped under the master, one page at a time, with the filter facets Discogs offers (format, label, country, released) and optional filters and sort. (Cost: 5 credit)
- **`releases/release`** (Release): One Discogs release (a specific pressing or edition) by release ID: artists, labels with catalog numbers, companies and pressing plants, formats and their descriptions, identifiers (barcodes, matrix/runout etchings, label codes), tracklist, notes, images, videos, marketplace count and lowest price, community have/want and rating. (Cost: 5 credit)
- **`releases/search`** (Search): Search the Discogs database for releases, masters, artists or labels by free text, artist, release title, track, label, catalog number or barcode, optionally narrowed by year, format, country, genre and style. Returns one page of matches with type, title, year, country, formats, labels, catalog number, barcodes and IDs to pass to the detail functions. (Cost: 5 credit)

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

### eBay listings (`ebay-com`)

eBay.com listings through the site's item-module JSON: item detail, variations, shipping and returns terms, and search autosuggest. Keyword search, sold listings and seller pages are HTML behind Akamai/orch and are not offered. Public US marketplace (www.ebay.com, USD), anonymous session, no bidding or purchases.

- **`listings/item`** (Item): You have an item number or /itm/ URL and want its current listing data without loading the HTML page. (Cost: 5 credit)
- **`listings/item_shipping`** (Item shipping): You need the shipping service, delivery estimate, ships-to list or returns policy of a listing. (Cost: 5 credit)
- **`listings/item_variations`** (Item variations): The item has variations (item.has_variations) and you need per-SKU prices and availability. (Cost: 5 credit)
- **`listings/suggest`** (Suggest): Expand a partial product query into the keywords eBay proposes before searching. (Cost: 5 credit)

### Etsy (`etsy-com`)

Etsy marketplace listings: listing details and prices, per-variation pricing, similar listings, shop sections and search query suggestions from Etsy's public ajax JSON API. Keyword search, shop listing enumeration and reviews are DataDome-gated and not available.

- **`listings/listing`** (Listing): You have a listing id or an etsy.com/listing/{id}/ URL. Use similar_listings for discovery, listing_variations for option prices, shop_sections for the seller's sections. (Cost: 5 credit)
- **`listings/listing_variations`** (Listing variations): A listing shows has_variation_pricing or you need the option values a buyer can pick. Needs a listing id from listing or similar_listings. (Cost: 5 credit)
- **`listings/search_suggestions`** (Search suggestions): Expand or normalize a shopping query before looking for listings elsewhere. Keyword search itself is not available from this program. (Cost: 5 credit)
- **`listings/shop_sections`** (Shop sections): You have a shop_id from a listing and want the shop's catalog structure and active listing counts. (Cost: 5 credit)
- **`listings/similar_listings`** (Similar listings): Fan out from one known listing to related listings. Etsy keyword search is DataDome-gated and not available; use search_suggestions for query completions. (Cost: 5 credit)

### IKEA US (`ikea-com`)

US IKEA category discovery, product specifications and advertised prices, variants, materials, care, safety documents and review excerpts. No store stock or delivery availability.

- **`products/discover`** (Discover): Discover product cards on the first US IKEA category page. Partial collection only; no filtering or pagination. Follow a returned product URL for detail. (Cost: 5 credit)
- **`products/materials_care`** (Materials care): Read component materials and care instructions from a US IKEA product page. (Cost: 5 credit)
- **`products/product`** (Product): Read a US IKEA product article, advertised USD price, dimensions, color and aggregate rating. Store stock and delivery availability remain unknown. (Cost: 5 credit)
- **`products/reviews`** (Reviews): Read review excerpts embedded on a US IKEA product page. These may cover a product family rather than only the selected color; no pagination or exhaustive review history. (Cost: 5 credit)
- **`products/safety_documents`** (Safety documents): Read IKEA product safety warnings and links to assembly or care PDFs. Document contents are not fetched. (Cost: 5 credit)
- **`products/variants`** (Variants): Read source-linked color/style variants from a US IKEA product page. Partial alternatives only; fetch each returned URL for its own article and price. (Cost: 5 credit)

### Kelley Blue Book (`kbb-com`)

US car inventory, listing details, model-year trims and regional Kelley Blue Book valuations.

- **`vehicles/book_value`** (Book value): Kelley Blue Book value for one vehicle: make, model, year, trim (slug from `trims`, or KBB vehicle_id), mileage and condition. Returns the selected trade-in or private-party value with its KBB range, all four condition values for both price types, typical mileage and the ZIP/edition the values are valid for. (Cost: 5 credit)
- **`vehicles/listing`** (Listing): One kbb.com listing by its numeric listing id (from `listings`): full description, features, every photo URL, seller address and rating, warranties, price history and KBB Fair Purchase Price. Expired or unknown ids are an error. (Cost: 5 credit)
- **`vehicles/listings`** (Listings): Search kbb.com dealer and private-seller inventory for a make (optionally model and trim) within a radius of a US ZIP code, optionally filtered by year, price, maximum mileage, exterior colour and drivetrain. Returns one page of 25 listings with price, KBB Fair Purchase Price and deal rating, mileage, VIN, seller and distance, plus the total match count for pagination. (Cost: 5 credit)
- **`vehicles/trims`** (Trims): Every trim kbb.com prices for a model year (make, model, year): KBB vehicle id, trim slug for `book_value`, Fair Purchase Price, typical-mileage trade-in and private-party values, engine, drivetrain and EPA figures, plus the model year's depreciation history and forecast. (Cost: 5 credit)

### Newegg US (`newegg-com`)

Search Newegg US electronics and open-box listings, then retrieve live prices, condition and availability for an item.

- **`products/open_box`** (Open box): Open-box availability on Newegg US for a model number or product keywords: the retailer's Open Box facet, only listings flagged open-box, each with price, in-stock flag and seller. An empty results list means no open-box units are listed right now. (Cost: 5 credit)
- **`products/product`** (Product): Live price and stock for one Newegg US item number (N82E16814932771, 14-932-771, open-box variant 14-932-771R, or marketplace 9SIB0GJKJ60641): displayed price, list price, instant savings, shipping, 30-day low, in-stock flag and quantity indicator, purchase limit, condition, seller, warranty and rating. Item numbers come from search or open_box. (Cost: 5 credit)
- **`products/search`** (Search): Search Newegg US by model number, SKU-like keyword or product name. Returns one page of listings with displayed price, in-stock flag, condition (new/open-box/refurbished), seller and model number. Filter by condition or in-stock, and follow next_page for more. (Cost: 5 credit)

### Nike US (`nike-com`)

Nike US products, prices, sizes, availability and public customer reviews from Nike's own web APIs.

- **`products/availability`** (Availability): Stock bands per size for one style/color or a product family; no exact inventory counts. (Cost: 5 credit)
- **`products/product`** (Product): One known style/color or a nike.com/t/ product URL. Use search for discovery, availability for stock only. (Cost: 5 credit)
- **`products/review_summary`** (Review summary): Rating histogram and fit/comfort summary for a style; cheaper than paging reviews. (Cost: 5 credit)
- **`products/reviews`** (Reviews): One page of recent public reviews; use review_summary for the histogram, review_photos for images. (Cost: 5 credit)
- **`products/search`** (Search): Search Nike US products with query or browse path. For the first page, provide query or path and optionally count (24, 50 or 100; default 24). For the next page, send next_cursor as cursor without query, path or count. Use product for one known style. (Cost: 5 credit)
- **`products/suggestions`** (Suggestions): Autocomplete or popular searches; call before search when the query is uncertain. (Cost: 5 credit)

### PeerSpot (`peerspot-com`)

Public PeerSpot software products, customer reviews, ratings and comparisons.

- **`software-reviews/compare`** (Compare): PeerSpot head-to-head comparison of two products: category ranking, average rating (out of 10), reviews sentiment and review count per product, category mindshare, and per-theme sentiment scores with editorial summaries and reviewer quotes (ROI, customer service, scalability, stability, room for improvement, setup cost, valuable features). Order of the two slugs does not matter. (Cost: 5 credit)
- **`software-reviews/product`** (Product): One PeerSpot product page: average rating and review count, willingness to recommend, category ranking and mindshare, editorial review-theme summaries (valuable features, room for improvement, ROI, pricing, use cases, support, deployment, scalability, stability) with representative quotes, one-line summaries of individual reviews, reviewer company-size and industry breakdowns, and the comparison pages that link competitors. (Cost: 5 credit)
- **`software-reviews/reviews`** (Reviews): One page (10 reviews) of full-text PeerSpot reviews for a product: star rating, title, date, reviewer role and labels, company size, industry, pros, cons, every interview section (use case, valuable features, room for improvement, pricing/licensing, setup, support, ROI, ...) and the review permalink. Pass next_page to continue. (Cost: 5 credit)
- **`software-reviews/search`** (Search): Find PeerSpot product pages for a vendor or product name. Returns up to 10 matching products with the slug needed by product, reviews and compare. PeerSpot's search is approximate (Rimini lists Gemini products), so each product carries match: exact (same words as the query), partial (every query word is a word or word prefix of the name) or fuzzy (PeerSpot's guess), and exact_match says whether any product matches exactly. A result with exact_match false and only fuzzy products means the vendor most likely has no PeerSpot page. Empty when nothing matches. (Cost: 5 credit)

### PSA (`psacard-com`)

Browse public collectible price-guide categories, sets, grade values and featured dealer profiles. No cert or population lookup.

- **`collectibles/categories`** (Categories): Browse public PSA price-guide categories. (Cost: 5 credit)
- **`collectibles/dealer`** (Dealer): Read one public PSA dealer profile: address, phone, specialties and services. (Cost: 5 credit)
- **`collectibles/dealers`** (Dealers): List featured dealers from the public PSA dealer directory, not the complete dealer database. (Cost: 5 credit)
- **`collectibles/sets`** (Sets): List collectible sets within a PSA price-guide category. Offset/limit slice the fetched page. (Cost: 5 credit)
- **`collectibles/values`** (Values): Read card names and published guide values by grade. Blank cells remain unknown; +/- change markers are retained. These are not offers or recent sales. (Cost: 5 credit)

### Reclame Aqui (`reclameaqui-com-br`)

Reclame Aqui (reclameaqui.com.br), Brazil's consumer complaints platform: company reputation profiles (score, RA1000/Otimo/Bom/Regular/Ruim/Nao recomendada status, response and solution rates), company search by name or CNPJ, a company's complaints with tabs and pagination, full-text complaint search, single complaint text with the company reply and consumer evaluation, segment tree and best/worst segment rankings. Public read surfaces only; Portuguese (pt-BR) content.

- **`complaints/company`** (Company): Look up a company's reputation and identity when you know its shortname (from search_companies or a pasted profile URL). (Cost: 5 credit)
- **`complaints/company_complaints`** (Company complaints): List or paginate a company's complaints. Pass company_id from search_companies or company (or shortname). Use page for the next page while next_page is set. (Cost: 5 credit)
- **`complaints/complaint`** (Complaint): Read one complaint's text, the company reply and the consumer's evaluation. Ids and URLs come from company_complaints or search_complaints. (Cost: 5 credit)
- **`complaints/search_companies`** (Search companies): Start here to resolve a company's shortname and numeric id from a name or CNPJ before calling company, company_complaints or search_complaints. (Cost: 5 credit)
- **`complaints/search_complaints`** (Search complaints): Find complaints about a topic ('reembolso', a product name) across Reclame Aqui or within one company. Use company_complaints to browse a company without a search term. (Cost: 5 credit)
- **`complaints/segment_ranking`** (Segment ranking): Rank companies in a category, e.g. the best marketplaces (varejo/marketplaces) or the worst online courses. (Cost: 5 credit)
- **`complaints/segments`** (Segments): Discover the main_segment/sub_segment pair for segment_ranking or browse Reclame Aqui's category taxonomy. (Cost: 5 credit)

### RTINGS (`rtings-com`)

RTINGS public-tier lab reviews, buying guides, rankings and tested-product metadata; member-only measurements remain unavailable.

- **`tests/guides`** (Guides): List the published buying guides ("Best X" recommendation pages), popular reviews and tools for one RTINGS product category, e.g. tv, headphones, monitor, soundbar, laptop, vacuum, keyboard, mouse, printer, projector, speaker, camera, tablet, air-purifier, blender, toaster. (Cost: 5 credit)
- **`tests/products`** (Products): Every product RTINGS has lab-tested in a category, across all methodology (test bench) versions: name, brand, review URL, variant SKUs, release and last-update dates, and the category's scored usages. This is the directory to pick a review from; the per-usage scores themselves are member-only. (Cost: 5 credit)
- **`tests/ranking`** (Ranking): One RTINGS buying guide: the ranked, lab-tested picks for a category (or a sub-guide such as by-size/65-inch), each with the product's public overall score, award title, per-usage ratings (score null when the tester paywalls it), featured test results and links to the full review; plus alternatives mentioned and the guide's update log. (Cost: 5 credit)
- **`tests/review`** (Review): One RTINGS lab review: the product's public overall score, test bench version, featured test results with measured values and scores, per-usage ratings (null when paywalled) with pros/cons summaries and better/worse alternatives, authors and publication dates. Identify the review by its rtings.com URL or by category, brand and model slugs. (Cost: 5 credit)

### Shopify Catalog (`shopify`)

Search products across Shopify merchants or within one store, resolve product identifiers and inspect variants through Shopify's UCP catalogs.

- **`catalog/get_product`** (Product details): Get details, variants and availability for a product_id returned by search or lookup. Optional selected options refine the variant. Does not create a cart or place an order. (Cost: 5 credit)
- **`catalog/lookup_catalog`** (Look up products): Look up 1-50 products using product_ids returned by search, or product URLs. Inspect messages for unmatched identifiers. (Cost: 5 credit)
- **`catalog/search_catalog`** (Search products): Search products across Shopify merchants by query, such as trail running shoes under $150. Narrow results by country and use limit and cursor to page through them. Results are estimates, not an exhaustive merchant inventory. (Cost: 5 credit)
- **`storefront/get_product`** (Storefront: Product details): Get details and availability for a product_id from the selected store's search or lookup. Keep the same store_domain. Optional selected options refine the variant without executing checkout. (Cost: 5 credit)
- **`storefront/lookup_catalog`** (Storefront: Look up products): Look up 1-10 product_ids within store_domain. Use IDs returned by that store's search, not Global Catalog IDs. Inspect messages for unmatched identifiers. (Cost: 5 credit)
- **`storefront/search_catalog`** (Storefront: Search products): Search products in a Shopify store by store_domain and query, or leave query empty to browse. Use limit and cursor for pagination. The store must expose Shopify's Storefront Catalog endpoint. (Cost: 5 credit)

### Target (`target-com`)

Discover featured Target US products and inspect product specifications and child variant options. No search, price or inventory coverage.

- **`products/featured`** (Featured): Discover the limited set of product links featured on the Target US homepage; not a searchable or exhaustive catalog. (Cost: 5 credit)
- **`products/product`** (Product): Read a known Target product URL: brand, descriptive specifications, highlights, image and published return-policy text. Price and availability are unknown. (Cost: 5 credit)
- **`products/variants`** (Variants): List child product identifiers, option combinations and images from a Target parent product page. Follow child URLs for specifications. Catalog variants do not imply purchasable inventory. (Cost: 5 credit)

### Trader Joe's (`traderjoes-com`)

Trader Joe’s public store finder, store-specific product search and product nutrition, ingredients and allergens.

- **`products/product`** (Product): One Trader Joe's product by SKU as published for a store: price, size, availability, description, category path, images, full nutrition facts panels (serving size, calories, per-nutrient amount and % daily value), ingredients, allergens and related products. An unknown SKU is an error. (Cost: 5 credit)
- **`products/search`** (Search): Search Trader Joe's products available at one store by keyword: SKU, title, shelf price (USD), pack size, availability flag, category path and image. Paginated; total_count and next_page are returned. store_code defaults to 701 (Los Angeles - Hyperion). (Cost: 5 credit)
- **`products/stores`** (Stores): Trader Joe's stores near a US ZIP code: store code (used by search and product), address, coordinates, distance, phone, weekly hours and alcohol availability. Zero results for a ZIP with no store in range is a success with count 0. (Cost: 5 credit)

### U-Haul (`uhaul-com`)

uhaul.com truck rental quotes and availability: search in-town (local) and one-way truck rates for a pickup location, optional drop-off location and pickup date, read the per-model rate basis (rental rate, mileage rate, extra day/mile, allowed days and distance, environmental fee) and the site's own availability text; autosuggest pickup/drop-off place names; list U-Haul locations in a city, read one location's profile (address, phone, hours, rating, base in-town rates) and its customer reviews. Read-only: no reservations, holds or checkout.

- **`truck-rentals/get_location`** (Get location): You have an `entity_id` from `list_locations` (or a pasted uhaul.com/Locations/.../{id}/ URL) and need the location's profile. (Cost: 5 credit)
- **`truck-rentals/get_location_reviews`** (Get location reviews): You have a location `entity_id` and want its customer feedback. (Cost: 5 credit)
- **`truck-rentals/list_locations`** (List locations): Find location `entity_id`s in a place before `get_location` / `get_location_reviews`. (Cost: 5 credit)
- **`truck-rentals/search_truck_rates`** (Search truck rates): The caller wants truck sizes, prices or availability for a move between two places or around one place on a date. Use `suggest_locations` first when the place name is ambiguous. (Cost: 5 credit)
- **`truck-rentals/suggest_locations`** (Suggest locations): Normalise a free-text place into the exact `pickup_location` / `dropoff_location` string before calling `search_truck_rates`. (Cost: 5 credit)


