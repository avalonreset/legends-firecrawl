---
type: manifesto
title: "The Great AI Data Arbitrage"
created: 2026-09-24
updated: 2026-09-24
tags:
  - manifesto
  - data-liberation
  - firecrawl
  - alexandria
---

# The Great AI Data Arbitrage

### Selling Free Information to the World for Credits

In September 2026, Firecrawl announced a $75M Series B funding round and launched **Alexandria**, marketing it as the "Library of Alexandria for Superintelligence" and a unified data gateway for autonomous AI agents. They boasted 90+ data providers, hundreds of tool capabilities, and over 113 million documents.

Behind the marketing veneer lies an astonishing reality: **63.2% of Alexandria is not proprietary data at all.**

### The Empirical Findings

Our rigorous, exhaustive audit of all 114 providers and 797 capabilities across all 21 categories in Firecrawl Alexandria reveals:

1. **Taxpayer-Funded Government APIs (31 Providers, 27.2% of Catalog):**
   Agencies like the US Treasury, the SEC, USAspending, the USPTO, the World Bank, the IMF, and state Secretaries of State offer free, unauthenticated, open REST APIs funded entirely by public tax dollars. Firecrawl literally wraps these exact endpoints, preserves their exact parameter names (e.g. `filter=record_date:gte:...`, `sort=-record_date`), and charges developers 1 to 5+ credits per call.
2. **Open Source & Non-Profit Databases (9 Providers, 7.9% of Catalog):**
   Projects like the Free Law Project (CourtListener), the Internet Archive Wayback Machine, Stack Exchange, and Hugging Face Hub provide free APIs to the global community. Alexandria meters access to them.
3. **Unauthenticated Public Frontend JSON (32 Providers, 28.1% of Catalog):**
   Commercial companies like Skyscanner, Trader Joe's, ESPN, TodayTix, SpotHero, and Yahoo Finance expose unauthenticated frontend JSON APIs for their consumer web applications. Alexandria describes them in its own internal tool contracts as: *"Anonymous same-origin JSON APIs on www.site.com"*.
4. **Proprietary B2B Brokers (42 Providers, 36.8% of Catalog):**
   Only about one-third of the catalog consists of true commercial or licensed datasets (such as Apollo, Benzinga, Fiscal.ai, and FullEnrich).

### The Exhaustion & Pagination Revelation

During our deep verification, we discovered two critical platform behaviors:
- **Category Truncation:** Firecrawl's category discovery endpoint (`level: "categories"`) defaults to a limit of 20 items. Without an explicit higher limit (`limit: 100`), the 21st category (`travel`) was completely hidden.
- **Tool Pagination Truncation:** The provider `particle` declares 105 tools, but default tool fetching without pagination caps at 100 tools. This concealed 5 capabilities, giving an erroneous total of 792 instead of the true total of **797 capabilities**.

### The Legends Alexandria Philosophy

We believe AI agents should be sovereign, fast, and cost-efficient. Selling free public information to developers behind a metered paywall is a tax on intelligence.

The **Legends Alexandria** (`legends-firecrawl`) delivers:
- **Zero-Credit Sovereign Execution**: Directly connects agents to official open APIs without passing through a middleman.
- **Offline Semantic Discovery**: An agent searches all 797 capabilities locally in under 5ms with zero token bloat and zero credit cost.
- **Transparent Fallback**: When proprietary data is genuinely required, it seamlessly routes through the Alexandria gateway using verified credentials.

