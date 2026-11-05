# legends-firecrawl Agent Recipe

This recipe is the canonical agent handoff for `legends-firecrawl`, loaded by the `cto-legends` router (`cto-legends handoff legends-firecrawl`). Do not register `legends-firecrawl` as a separate skill.

## 1. Readiness Check (`doctor`)

Before running live Firecrawl or Alexandria operations, verify local environment readiness offline:

```sh
lfc doctor --offline
python -m legends_firecrawl doctor --offline
```

For a live credit-usage verification (when `FIRECRAWL_API_KEY` is configured):

```sh
lfc doctor
```

## 2. Core CLI Workflows (`lfc` and `lax`)

| Command | Purpose |
| --- | --- |
| `lfc version` / `python -m legends_firecrawl version` | Print module and expected vendor CLI version |
| `lfc doctor [--offline]` | Check module layout, Python version, `firecrawl-cli@1.23.3`, and `FIRECRAWL_API_KEY` |
| `lfc routes` / `lfc route <operation>` | List supported operations and default scope bounds |
| `lfc estimate <operation> [--limit <n>] [--formats <csv>]` | Offline scope and page ceiling estimate |
| `lfc credits` / `lfc cost` | Check live account credit usage or local usage ledger summary |
| `lfc scrape <url> [--formats markdown,links] [--receipt] [--no-save]` | Bounded single-page scrape with automatic local JSON capture |
| `lfc map <url> [--limit 100] [--search <terms>]` | Discover URLs on a target domain |
| `lfc search "<query>" [--limit 5] [--scrape-results]` | Bounded web search via official Firecrawl API |
| `lfc crawl-preview <url> [--limit 25] [--max-depth 2]` | Offline preview of crawl scope and bounds |
| `lfc crawl <url> [--limit 25] [--max-depth 2] --confirm` | Execute a bounded multi-page crawl after preview confirmation |
| `lfc crawl-status <job_id>` | Check asynchronous crawl status and archive returned results |
| `lax search "<term>"` / `lax inspect <provider> [--full]` / `lax audit` | Offline Alexandria catalog discovery (114 providers, 797 capabilities) |
| `lax query <provider> <capability> [--options JSON] [--confirm]` | Preview (default) or submit (`--confirm`) an official Alexandria query |
| `lax captures [--legacy]` | List local Alexandria response captures |
| `lfc evidence export\|export-capture\|inventory\|find\|verify\|view\|reuse ...` | Portable offline evidence bank operations |

## 3. Spend Gates and Credential Discipline

- Alexandria queries (`lax query`) default to offline preview and require explicit `--confirm` before submitting a billable request.
- Multi-page crawls require running `lfc crawl-preview` first, followed by `lfc crawl ... --confirm`.
- Configure `FIRECRAWL_API_KEY` in the process environment, Windows user environment, or via `FIRECRAWL_API_KEY_FILE` pointing to an explicit regular file. Never print, log, or commit API keys.

## 4. EDR and Security Guardrails

- **No hidden consoles or execution-policy bypass wrappers**: invoke `lfc`, `lax`, `legends-firecrawl`, or `python -m legends_firecrawl` directly through standard process execution without hidden console flags or shell execution-policy bypass wrappers.
- **No parent-process tree walking**: never enumerate parent processes or inspect system process trees.
- **No browser profile or OS credential harvesting**: read credentials strictly from `FIRECRAWL_API_KEY` or an explicit `FIRECRAWL_API_KEY_FILE` path, never from local browser profile databases or OS DPAPI stores.
- **Symlink refusal**: refuse symlink paths (`Path.is_symlink()`) on file inputs, key files, and evidence packages.
- **Network allowlist**: outbound HTTPS requests are restricted to `https://api.firecrawl.dev` (or explicit HTTPS `FIRECRAWL_API_URL`) and target public HTTP(S) URLs.
