# 0.3.4

- **Ecosystem Gold Standard & Release Gate**: Added `docs/AGENT-RECIPE.md`, `scripts/check_release.py`, `THIRD_PARTY_NOTICES.md`, `MANIFEST.in`, `assets/manifest.json`, and `python/legends_firecrawl/__main__.py` (`python -m legends_firecrawl`) aligned with the CTO Legends public release standard.
- **Native Cross-Platform Entrypoints & EDR Hygiene**: Removed legacy `bin/*.ps1` and `bin/*.cmd` shell wrapper scripts in favor of native Python console entrypoints (`lfc`, `lax`, `legends-firecrawl`) and added explicit `FIRECRAWL_API_KEY_FILE` support with symlink refusal (`Path.is_symlink()`).
- **Documentation & Asset Hygiene**: Sanitized `assets/banner.json`, updated documentation to `0.3.4`, and repaired release scope links.

# 0.3.3

- Add Python `[project.scripts]` entrypoints (`lfc`, `lax`, `legends-firecrawl`) and native `lfc alexandria` / `lax_main` routing in `python/legends_firecrawl/cli.py`.
- Replace execution-policy bypass flags in CLI launchers with direct `python -m legends_firecrawl.cli` invocation.
- Replace `.NET` `Marshal.SecureStringToBSTR` / `PtrToStringBSTR` memory marshaling in auth setup with Python standard library `getpass.getpass()`.
- Remove third-party `firecrawl-cli` `credentials.json` reading from `alexandria-src/router.js` so `getCredentials()` relies exclusively on `FIRECRAWL_API_KEY`.

# 0.3.2

- Raise minimum supported Python runtime to Python 3.11 (`requires-python = ">=3.11"`) across package metadata and multi-OS CI.
- Upgrade Node CI runtime from EOL Node 20 to Node 22 LTS, pin GitHub Actions to 40-character commit SHAs with explicit `contents: read` permissions, and upgrade `pip>=26.2.2` before package installation.

# 0.3.1

- Reject prohibited vendor integration commands before probing vendor availability, including on clean hosts.
- Supersedes the unpromoted 0.3.0 tag; its tag remains immutable.

# 0.3.0

- Portable offline evidence export, verification, manifest inventory, find, bounded/full view and scoped reuse review.
- External capture root, relative references and explicit workspace identity.
- Optional receipt output; complete response storage remains mandatory unless explicitly skipped.
- Provider failure envelopes retained; submitted Alexandria empty/error responses archived without retries.
- Metadata-only capture listing with explicit legacy inspection.

# 0.2.1

- Fix one-word Alexandria commands through CLI forwarding.
- Automatically save complete web-operation JSON and a vault reference; preserve full CLI response with capture paths. `--no-save` opts out.
- Catalog search returns compact discovery with the full catalog path; `--full` exposes full contracts.
- Capture listing returns timestamped JSON entries and raw paths; nested provider rows counted correctly.

# 0.2.0

- Retire all direct-source substitution, including Treasury; every Alexandria query uses official Firecrawl.
- Keep offline discovery, explicit paid confirmation, bounded crawl and source-labelled response captures.
- Remove savings, proxy shielding and superior-intelligence claims. No MCP runtime required.
- Preserve raw error responses, zero versus unknown costs and unique capture filenames.

# 0.2.0rc1

- Restrict default direct execution to two verified Treasury operations.
- Remove provider-level savings and scale guarantees; preserve paid envelopes and unknown costs.
- Require explicit paid confirmation; no automatic paid fallback.
- Validate pagination and fields; bound response size, timeout and process-local pacing.
- Exclude local captures and unvalidated adapters from release archives.

# Changelog

## 0.1.0 - 2026-09-25

- Router-native reset generation: de-skillified to the single registered `cto-legends` router skill (vendored pinned copy at `skills/cto-legends/SKILL.md`, router commit `6975dcb`).
- Removed per-module skill registrations (`skills/legends-firecrawl/`, `skills/legends-alexandria/`), host shims (`CLAUDE.md`, `GEMINI.md`, `LEGENDS.md`), house-only `NEXT.md`, and per-host module installers.
- `VERSION` is the authoritative version string; `pyproject.toml` reads it dynamically. Old releases and tags wiped; history preserved.
