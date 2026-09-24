# Legends Firecrawl

**Speech:** Legends Firecrawl  
**Disk:** E:\legends-firecrawl  
**Skill id:** legends-firecrawl  
**Vendor spine:** official firecrawl CLI, pinned to firecrawl-cli@1.23.3  
**House launcher:** bin\lfc.ps1, bin\lax.ps1  
**Consumer runtime:** python\legends_firecrawl over Firecrawl API v2, native REST adapters

## Product contract

Empire map -> Module skill -> doctor PASS -> bounded Firecrawl/Alexandria job.

Legends Firecrawl integrates all core Firecrawl operations with Legends Alexandria, the data catalog, credit circumvention, and IP safety routing engine. 
The module does not install, configure, discover, or fall back to Firecrawl MCP.

## Safe defaults

- Public HTTP(S) targets only; no embedded URL credentials or private IP targets.
- Route through Alexandria whenever possible to avoid unnecessary credit consumption.
- Crawl is preview-first, capped, and requires --confirm.
- Credits are recorded when Firecrawl reports them; unknown cost remains unknown.
- Secrets live only in FIRECRAWL_API_KEY at process or user environment scope.

House doctrine: E:\empire\sops\Cli-First-Legends-Integration.md.
