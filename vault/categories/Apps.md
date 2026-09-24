---
type: category
id: "apps"
title: "Apps"
providers_count: 3
---

# Category: Apps

> Mobile apps on the Apple App Store and Google Play: listings, ratings, review counts, charts, reviews and version history.

Part of [[_Index|Legends Alexandria]] and the [[manifesto/The-Great-AI-Data-Arbitrage|Great AI Data Arbitrage]].

## Cataloged Providers (3)

| Provider | Capabilities | Data Tier | Direct Bypass Available? |
|---|---|---|---|
| `aptoide-com` (**Aptoide**) | 3 | Public Commercial Web / Frontend JSON Endpoints | Yes (Direct unauthenticated web fetch or lightweight house scraper) |
| `github-com` (**GitHub**) | 8 | Open Non-Profit, Legal & Community Ecosystems | Yes (Direct community/non-profit REST API) |
| `pypi-org` (**PyPI**) | 8 | Open Non-Profit, Legal & Community Ecosystems | Yes (Direct community/non-profit REST API) |

## Tools & Capabilities

### Aptoide (`aptoide-com`)

Android app metadata from Aptoide: search packages, inspect app permissions, downloads, ratings and signing certificates, and read version history.

- **`apps/app`** (App): Metadata for one Android package on Aptoide: latest APK (version name/code, size, md5, min SDK, signing certificate, malware scan), declared permissions and features, downloads (store and all-store), rating histogram, developer, age rating, description, what's new and screenshots. Errors when the package is not hosted. (Cost: 5 credit)
- **`apps/search`** (Search): Search Aptoide's Android APK catalog by keyword (app name, developer or package fragment). Returns up to `limit` listings with package name, latest version, size, store, downloads and ratings; paginate with `offset`. (Cost: 5 credit)
- **`apps/versions`** (Versions): Version history for one Android package: the APK uploads Aptoide holds across its stores, newest first, each with version name/code, size, md5, min SDK, CPU ABIs, malware verdict, store, downloads and rating. Depth depends on what uploaders kept; an empty list means Aptoide has no other builds. (Cost: 5 credit)

### GitHub (`github-com`)

Public GitHub repositories, releases, issues, labels and contributors.

- **`repositories/contributors`** (Contributors): One page of a repository's contributors ordered by commit count on the default branch, with login, account type and contribution count. Anonymous (email-only) contributors are not listed. GitHub refuses this listing for repositories with very large histories (for example torvalds/linux), which surfaces as an error naming the reason. (Cost: 5 credit)
- **`repositories/issue_counts`** (Issue counts): Exact issue counts for a repository (pull requests excluded, unlike the repository's open_issues_count): the total for the given state plus one count per requested label, from GitHub's issue search. Makes 1 + labels.length search requests; at most 5 labels per call because GitHub allows 10 keyless searches per minute per IP. (Cost: 5 credit)
- **`repositories/issues`** (Issues): One page of a repository's issues filtered by state and labels (all given labels must match), sorted by created/updated/comments. Pull requests are excluded unless include_pull_requests is true, so a page may hold fewer than per_page records; pull_requests_excluded says how many were dropped. Each record carries title, state, labels, assignees, milestone, comment and reaction counts, body and timestamps. (Cost: 5 credit)
- **`repositories/labels`** (Labels): The labels defined in a repository (name, color, description, whether GitHub-default), one page of up to 100. Use the names with issues and issue_counts. (Cost: 5 credit)
- **`repositories/latest_release`** (Latest release): The latest published, non-prerelease, non-draft release of a repository with its release notes (Markdown body), tag, publish date, author and downloadable assets. found=false with release=null when the repository exists but has no published release. (Cost: 5 credit)
- **`repositories/releases`** (Releases): One page of a repository's releases, newest first, including pre-releases and drafts visible to the public, each with tag, name, notes body, publish date and assets. Paginate with page/per_page; has_next says whether another page exists. (Cost: 5 credit)
- **`repositories/repo`** (Repo): One GitHub repository by owner/name or URL: stars, forks, watchers, open issue+PR count, creation/last-push dates, primary language, topics, license, default branch, homepage and flags (archived, fork, template). One request to GET /repos/{owner}/{name}; an unknown repository is an error. (Cost: 5 credit)
- **`repositories/search_repos`** (Search repos): Search public GitHub repositories with GitHub's search syntax (free text plus qualifiers such as language:rust, stars:>1000, topic:llm, org:firecrawl, created:>2025-01-01), sorted by best match, stars, forks, help-wanted issues or last update. Returns one page of repository records with stars, forks and dates; total_count is GitHub's overall match count, capped at 1000 reachable results (page * per_page <= 1000). Keyless search is limited to 10 requests per minute per IP. (Cost: 5 credit)

### PyPI (`pypi-org`)

Python Package Index: project and release metadata, dependencies and Python compatibility, distribution files with hashes, PEP 740 provenance, release feeds, the global change log, a user's projects and site statistics.

- **`packages/changelog`** (Changelog): Incrementally track everything that changes on PyPI: poll with the last seen serial. Upstream serves up to 50 000 events per call; `limit` windows them and `next_serial` resumes. (Cost: 5 credit)
- **`packages/files`** (Files): Enumerate all files across all versions of a package (for mirroring, hash pinning or compatibility scans), or get the complete version list cheaply. (Cost: 5 credit)
- **`packages/project`** (Project): Look up a Python package by name or pasted pypi.org URL: what it is, who publishes it, which Python versions and dependencies it needs, which versions exist, and whether the current release has advisories. (Cost: 5 credit)
- **`packages/provenance`** (Provenance): Verify where a specific wheel or sdist was built and published from (GitHub/GitLab Trusted Publishing) before trusting it. (Cost: 5 credit)
- **`packages/recent_releases`** (Recent releases): Watch for new versions of a package, or discover what was just released or created on PyPI. Fixed windows; no history beyond the feed. (Cost: 5 credit)
- **`packages/release`** (Release): Check a specific version: dependency pins, Python compatibility, wheels/sdist available with hashes, whether it was yanked, and advisories for that exact version. (Cost: 5 credit)
- **`packages/stats`** (Stats): Size PyPI as a whole or see which projects dominate its storage. (Cost: 5 credit)
- **`packages/user_projects`** (User projects): Find every package published or maintained by a given PyPI username (from a project's ownership or maintainer links). (Cost: 5 credit)


