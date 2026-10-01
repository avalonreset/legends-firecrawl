# 0.2.1: capture first and usable agent commands

Live testing of the published 0.2.0 package found a PowerShell argument-forwarding defect: one-word Alexandria commands failed through `lfc`. This patch fixes it and adds regressions. Catalog search no longer prints entire example response schemas by default; it points to the complete saved catalog, and `--full` exposes full cached contracts.

Web commands now automatically preserve their entire returned JSON, with a SHA-256 and a vault reference card. The original output fields remain available, with `_capture` paths added. Agents may inspect any subset or the complete saved file without another provider request. `--no-save` explicitly disables capture, and `LEGENDS_FIRECRAWL_CAPTURE_ROOT` selects the workspace. Python client use alone does not automatically save.

Alexandria capture listing now returns usable JSON and raw file paths; nested records are counted correctly. An archive write failure retains the received provider response and reports that the request completed, rather than repeating a possibly paid request.

## Evidence

The published 0.2.0 ZIP, extracted outside the checkout, successfully scraped DataForSEO (6,691 Markdown characters), mapped five links, searched two results, submitted one official Alexandria query and completed a bounded one-page crawl. Scrape took 23.66 seconds, map 10.22 seconds, search 1.53 seconds and Alexandria 1.50 seconds in this run. These are individual observations, not latency guarantees. The failed one-word capture-list command was preserved as evidence and fixed in this patch.

A fresh patched live scrape was compared with its archived JSON: every returned field matched, the hash verified, and the vault card existed. Independent tests also preserve a 120,000-character Unicode response with arbitrary nested fields, test unique filenames, opt-out and write-failure behavior.

48 Python and 11 Node tests passed. Extracted-package verification repeats both suites and checks basic commands. Raw live responses remain local under `var/battle-020`, excluded from release assets. Only some provider responses reported credits, so no complete batch-cost claim is made.

Official Firecrawl remains the sole data service. There are no direct-source substitutes, savings claims or demonstrated intelligence advantage over the underlying service. Full capture means the complete response to one request; it does not mean an entire site or every page of a dataset has been collected.
