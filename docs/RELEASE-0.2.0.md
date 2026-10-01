# 0.2.0: official Firecrawl workflows

This release retires the direct-source substitution experiment completely, including Treasury. All supported data requests use official Firecrawl services. No savings percentage, superior data quality, proprietary intelligence or proxy shielding is claimed.

Retained value: agent-friendly CLI commands, offline Alexandria catalog lookup, bounded crawl previews, explicit Alexandria paid confirmation, and saved raw responses with provenance. No MCP runtime is required. Firecrawl's own API and CLI also work without MCP.

Breaking behavior: Alexandria queries require `--confirm` before submission. `--preview` never submits, even together with `--confirm`. The retired unsafe direct override is rejected. A transport failure is not automatically retried because billing may already have occurred. Other web commands retain their documented execution semantics and can charge immediately.

Verification: 36 Python tests and 11 independently authored Node tests passed. Tests cover routing all 797 cached capabilities to the official gateway, not live execution of 797 tools. A live request through the PowerShell entry point returned HTTP 200 and reported one Firecrawl credit. Raw evidence is retained locally, outside the package. Extracted-package verification covers version, route inventory, crawl preview, catalog output and both test suites.

The release archive excludes all native adapters, local captures and retired safety classifications. Historical research documents are explicitly superseded. The catalog is a snapshot; current availability and pricing remain Firecrawl's responsibility.
