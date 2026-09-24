---
category: "jobs"
type: reference-card
provider_count: 7
---

# Category: jobs

> Job postings: who is hiring for which roles, where, and since when.

**Providers in this category:** 7

| Provider ID | Provider Name | Capabilities | Tier | Cost | Bypass Route |
|---|---|---|---|---|---|
| `builtin-com` | **Built In** | 3 | Public Commercial Web / Frontend JSON Endpoints | 0 Credits (Direct Web / Scraping Bypass) | Direct unauthenticated web fetch or lightweight house scraper |
| `greenhouse-io` | **Greenhouse job boards** | 6 | Proprietary Commercial B2B Data Brokers | Credits Required or Paid Vendor Key | Use Alexandria credits or direct vendor account |
| `icims-com` | **iCIMS** | 3 | Proprietary Commercial B2B Data Brokers | Credits Required or Paid Vendor Key | Use Alexandria credits or direct vendor account |
| `indeed-com` | **Indeed US** | 3 | Proprietary Commercial B2B Data Brokers | Credits Required or Paid Vendor Key | Use Alexandria credits or direct vendor account |
| `join-com` | **JOIN job ads** | 4 | Proprietary Commercial B2B Data Brokers | Credits Required or Paid Vendor Key | Use Alexandria credits or direct vendor account |
| `ycombinator-com` | **Y Combinator** | 4 | Open Non-Profit, Legal & Community Ecosystems | 0 Credits (Public API) | Direct community/non-profit REST API |
| `ziprecruiter-com` | **ZipRecruiter US** | 6 | Public Commercial Web / Frontend JSON Endpoints | 0 Credits (Direct Web / Scraping Bypass) | Direct unauthenticated web fetch or lightweight house scraper |

## Capabilities Overview

### Built In (`builtin-com`)

Technology job search, public role details and company profiles from Built In.

- **`jobs/company`** (Company): Read one company profile by returned slug: description, website, logo, source employee count and industries. Headcount is a public source observation; founding year omitted because source metadata is unreliable. [Cost: 5 credit]  
  *Options:* `slug` *(required)*
- **`jobs/job`** (Job): Read one canonical Built In job URL: description, employer, source salary range/currency/unit, posting/expiry dates, locations, benefits and industry. Missing values remain unknown; a listing is not a current hiring guarantee. [Cost: 5 credit]  
  *Options:* `url` *(required)*
- **`jobs/search`** (Search): Search Built In public technology jobs by keyword, with pages1-100 and source ordering. Returns job URLs and company slugs for detail lookups. No location or remote filters in this initial contract. [Cost: 5 credit]  
  *Options:* `page`, `query`

### Greenhouse job boards (`greenhouse-io`)

Employer job boards hosted by Greenhouse: list every opening on a board, search it with Greenhouse's own keyword, department and office filters, read one post with its description, pay ranges and application questions, and enumerate a board's departments and offices. Keyed by the employer's board token; there is no directory of boards.

- **`jobs/board`** (Board): To confirm a board token exists on Greenhouse and read the employer's name and blurb before listing its openings with jobs or search. [Cost: 5 credit]  
  *Options:* `board_token`, `url`
- **`jobs/departments`** (Departments): To discover department ids for search or to see how openings spread across departments. [Cost: 5 credit]  
  *Options:* `board_token`, `include_jobs`, `url`
- **`jobs/job`** (Job): When you have a job post id from jobs or search, or a pasted job page URL, and need the description, departments or application questions. [Cost: 5 credit]  
  *Options:* `board_token`, `job_id`, `url`
- **`jobs/jobs`** (Jobs): Start here with a board token to enumerate every opening with id, title, location, requisition id, dates and the public job URL. Pass next_page back as page. Use search for the board's own server-side keyword, department and office filters, and job for descriptions and application questions. [Cost: 5 credit]  
  *Options:* `board_token`, `keyword`, `page`, `per_page`, `url`
- **`jobs/offices`** (Offices): To discover office ids for search or to see where an employer is hiring. [Cost: 5 credit]  
  *Options:* `board_token`, `url`
- **`jobs/search`** (Search): When you need Greenhouse's own keyword search or a department/office filter, or the department of each post. Ids for department_id and office_id come from this function's departments/offices lists or from the departments and offices functions. [Cost: 5 credit]  
  *Options:* `board_token`, `department_id`, `keyword`, `office_id`, `page`, `url`

### iCIMS (`icims-com`)

Employer career portals hosted by iCIMS at <portal>.icims.com: search and paginate openings with the portal's own filters, read one posting with its header fields, body sections and JobPosting metadata, and describe a portal's categories, locations and position types.

- **`jobs/job`** (Job): When you have a posting id from search or a pasted https://<portal>.icims.com/jobs/<id>/... URL. [Cost: 5 credit]  
  *Options:* `job_id`, `portal`, `url`
- **`jobs/portal`** (Portal): To discover filter ids for search or to check that a portal exists and still serves listings on icims.com. [Cost: 5 credit]  
  *Options:* `portal`, `url`
- **`jobs/search`** (Search): Start here with a portal subdomain (or a pasted .icims.com/jobs/search URL). Pass next_page back as page to paginate; use job for the full posting. [Cost: 5 credit]  
  *Options:* `category_id`, `keyword_relation`, `location`, `page`, `portal`, `position_type_id`, `query`, `radius_miles`, `sort`, `sort_order`, `url`, `zip`

### Indeed US (`indeed-com`)

Indeed US job search, full job postings and employer profiles (rating, review category scores, size, revenue, industry, addresses, CEO, links) from Indeed's own GraphQL API, with the public company page as fallback and salary and location normalised.

- **`jobs/employer`** (Employer): Employer research after search or job returned an employer key or url. Prefer employer_key (solver-free, one GraphQL call); unknown keys and slugs return not_found. [Cost: 5 credit]  
  *Options:* `company`, `employer_key`, `url`
- **`jobs/job`** (Job): After search, or when you hold a viewjob?jk= or rc/clk?jk= URL. Removed postings return not_found. [Cost: 5 credit]  
  *Options:* `job_key`, `url`
- **`jobs/search`** (Search): Start here to find job_key values; pass the same filters plus next_cursor to page. No total count is exposed by Indeed; next_cursor=null is the end. [Cost: 5 credit]  
  *Options:* `cursor`, `limit`, `location`, `posted_within_days`, `query`, `radius_miles`, `remote`, `sort`

### JOIN job ads (`join-com`)

Employer career pages hosted by JOIN (join.com): read an employer's profile with offices and benefits, list its online job ads with category and city filters, read one ad with description, salary, contract and working terms, and enumerate the employer's job categories. Keyed by the employer's join.com slug; JOIN publishes no cross-employer search or directory.

- **`jobs/categories`** (Categories): To find category ids for jobs, or to name the category ids in jobs aggregations. [Cost: 5 credit]  
  *Options:* `company_id`, `company_slug`, `url`
- **`jobs/company`** (Company): To resolve an employer slug (the segment after join.com/companies/) to its numeric company id and city ids before listing jobs, or to read the employer's benefits and offices. [Cost: 5 credit]  
  *Options:* `company_slug`, `url`
- **`jobs/job`** (Job): When you have a job id or last_id from jobs, or a pasted ad URL (join.com/companies/<slug>/<id_param> or join.com/jobs/<last_id>), and need the description, salary, hours, vacation or contract terms. [Cost: 5 credit]  
  *Options:* `job_id`, `url`
- **`jobs/jobs`** (Jobs): Start here with an employer slug (or company_id from company) to enumerate its openings; pass next_page back as page. Use category_ids from categories or this function's aggregations, city_id from company offices or aggregations. There is no keyword search on JOIN. [Cost: 5 credit]  
  *Options:* `category_ids`, `city_id`, `company_id`, `company_slug`, `page`, `page_size`, `url`

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

### ZipRecruiter US (`ziprecruiter-com`)

ZipRecruiter US job marketplace: job search by title and city/state (the public /Jobs/ directory pages, 20 cards a page with pay, employment and location types, benefits and posting time), full job postings (JobPosting JSON-LD plus the page's job details), a company's open jobs near a city, salary percentiles for a title in a city, and title/location autocomplete.

- **`jobs/company_jobs`** (Company jobs): After search_jobs, with the company slug from a card's company_url (e.g. YO-AI-Labs from /co/YO-AI-Labs/Jobs) and a city. [Cost: 5 credit]  
  *Options:* `company_slug` *(required)*, `location` *(required)*, `radius_miles`
- **`jobs/job`** (Job): After search_jobs or company_jobs, with a card's url. Any pasted ziprecruiter.com /c/.../Job/... URL with a jid works. [Cost: 5 credit]  
  *Options:* `url` *(required)*
- **`jobs/salary`** (Salary): Pay benchmark for a title and city; not a posting's pay (that is on the job card). [Cost: 5 credit]  
  *Options:* `location`, `title` *(required)*
- **`jobs/search_jobs`** (Search jobs): Start here to find job detail URLs and company slugs; pass page=next_page to continue. Only title and city/state are filterable: pay, distance and date filters live behind ZipRecruiter's challenged interactive search and are not exposed. [Cost: 5 credit]  
  *Options:* `location`, `page`, `title` *(required)*
- **`jobs/suggest_locations`** (Suggest locations): Resolve a place name to the "City, ST" form that search_jobs, company_jobs and salary take. An unknown prefix returns an empty list. [Cost: 5 credit]  
  *Options:* `prefix` *(required)*
- **`jobs/suggest_titles`** (Suggest titles): Normalize free text into a title ZipRecruiter knows before search_jobs or salary. An unknown prefix returns an empty list. [Cost: 5 credit]  
  *Options:* `prefix` *(required)*

