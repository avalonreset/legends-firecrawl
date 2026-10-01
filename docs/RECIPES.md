# Intent-first recipes

Set `$lfc = 'E:\legends-firecrawl\bin\lfc.ps1'` in examples below.

## Collect once, review offline

Set `LEGENDS_FIRECRAWL_CAPTURE_ROOT` to the intended client workspace and `LEGENDS_WORKSPACE_ID` to its stable identity. Before buying fresh data, use `lfc evidence find` and `reuse` against that workspace's evidence bank. Eligibility still requires semantic review; never quietly substitute stale or partial observations.

Collect the full response once. Use `--receipt` only when short chat output is helpful; it does not shorten the saved evidence. Export the capture with `lfc evidence export-capture PATH BANK --workspace CLIENT`, verify it, then use `view --select` or `view --full` to inspect relevant data without another API call. Stage reviewed evidence through Empire's existing transaction workflow. Read [research-memory](RESEARCH-MEMORY.md) for scope, freshness and incomplete-state checks.

## Prospect homepage evidence

```powershell
pwsh -File $lfc scrape https://example.com --formats markdown,links
```

Use when a normal HTTP fetch cannot reliably render the public page or when
clean Markdown provides better evidence. Preserve the source URL and metadata.

## Find the pages that matter before scraping

```powershell
pwsh -File $lfc map https://example.com --limit 100 --search 'services pricing about contact'
```

Map first, then choose a small set of pages. Do not crawl the full site merely
because a map exists.

## Search for corroborating public evidence

```powershell
pwsh -File $lfc search 'Example Company reviews complaints' --limit 5
```

Search returns links/snippets by default. Add `--scrape-results` only when the
job truly needs full contents from every result.

## Bounded multi-page site collection

```powershell
pwsh -File $lfc crawl-preview https://example.com --limit 25 --max-depth 2 --include-paths /services,/about
pwsh -File $lfc crawl https://example.com --limit 25 --max-depth 2 --include-paths /services,/about --confirm
```

The first command makes no HTTP request. Review domain, limits, depth, and path
filters before starting the second.

## Legends Packet formula

1. Map the prospect site with a 100-URL ceiling.
2. Select homepage plus the few pages that support the packet theses.
3. Scrape only the selected pages; preserve URLs and retrieval metadata.
4. Use search sparingly for third-party corroboration.
5. Use crawl only when a bounded map-and-select workflow cannot find the needed
   evidence.

Firecrawl complements DataForSEO. DataForSEO supplies SERP/keyword/local-search
measurements; Firecrawl supplies retrievable public-web content. Neither should
be used as a pretend source for the other's evidence.

