---
type: category
id: "software"
title: "Software"
providers_count: 1
---

# Category: Software

> Open-source packages: registry metadata, versions, licences, download counts and dependents on npm, PyPI, crates.io and Maven Central.

Part of [[_Index|Legends Alexandria]] and the [[manifesto/The-Great-AI-Data-Arbitrage|Great AI Data Arbitrage]].

## Cataloged Providers (1)

| Provider | Capabilities | Data Tier | Direct Bypass Available? |
|---|---|---|---|
| `package-registry-metadata-download-stats` (**Package registries**) | 4 | Proprietary Commercial B2B Data Brokers | No (Proprietary) |

## Tools & Capabilities

### Package registries (`package-registry-metadata-download-stats`)

npm, PyPI, crates.io and Maven Central package metadata: latest version, license, links, version history, weekly and monthly downloads and dependent counts.

- **`packages/dependents`** (Dependents): How many packages depend on one version of a package (deps.dev total/direct/indirect; the default version unless one is named). For crates also crates.io's package-wide reverse-dependency count and a named sample. (Cost: 1 credit)
- **`packages/downloads`** (Daily downloads): Daily download counts for one npm, PyPI or crates.io package as a series with 1/7/30-day sums; last-week, last-month or last-year (capped by what the source keeps). Maven Central has no download statistics. (Cost: 1 credit)
- **`packages/package`** (Package record): One package's current record: latest version and publish time, description, license, homepage/repository/issues links, keywords, version count, a download summary (npm and PyPI last week/month; crates.io last week/month/90 days/total; Maven Central publishes none) and a dependent count. (Cost: 1 credit)
- **`packages/versions`** (Version history): A package's version history from deps.dev, newest first, with publish time, default flag and deprecation; paged with offset and limit. All four registries. (Cost: 1 credit)


