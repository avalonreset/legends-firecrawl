# Operation map

| Job | Default scope | Gate | Output |
|---|---:|---|---|
| Credits | account read | doctor/auth | JSON |
| Scrape | 1 URL, Markdown | auth | JSON |
| Map | 100 URLs, no subdomains | auth | JSON |
| Search | 5 web results, no result scraping | auth | JSON |
| Crawl preview | 25 pages, depth 2 | none; no HTTP | JSON plan |
| Crawl | 25 pages, depth 2 | auth + `--confirm` | JSON job |
| Crawl status | 1 job id | auth | JSON |

Advanced provider commands are available through the guarded `vendor` escape
hatch. The wrapper refuses vendor integration installers (`init`, `setup`,
`launch`, `launcher`). Add a first-class house route only after a real repeated
job proves the need.
