# Operation map

| Job | Default scope | Gate | Output |
|---|---:|---|---|
| Doctor | offline or live readiness | `--offline` or auth | JSON |
| Routes / Route / Estimate / Cost | local metadata or ledger | none; no HTTP | JSON |
| Credits | account read | doctor/auth | JSON |
| Scrape | 1 URL, Markdown | auth | JSON |
| Map | 100 URLs, no subdomains | auth | JSON |
| Search | 5 web results, no result scraping | auth | JSON |
| Resolve | up to 25 map URLs (+ fallback search, optional `--scrape`) | auth | JSON |
| Crawl preview | 25 pages, depth 2 | none; no HTTP | JSON plan |
| Crawl | 25 pages, depth 2 | auth + `--confirm` | JSON job |
| Crawl status | 1 job id | auth | JSON |
| Alexandria (`lax` / `lfc alexandria`) | 114 providers, 797 capabilities | `--preview` default; `--confirm` for query | JSON |
| Evidence (`lfc evidence`) | export, export-capture, verify, inventory, find, view, reuse | none; offline | JSON |

Advanced provider commands are available through the guarded `vendor` escape
hatch. The wrapper refuses vendor integration installers and credential/config
mutators (`init`, `setup`, `launch`, `launcher`, `login`, `logout`, `auth`,
`config`, `mcp`). Add a first-class house route only after a real repeated
job proves the need.
