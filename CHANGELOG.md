# Changelog

## 0.1.0 - 2026-09-25

- Router-native reset generation: de-skillified to the single registered `cto-legends` router skill (vendored pinned copy at `skills/cto-legends/SKILL.md`, router commit `6975dcb`).
- Removed per-module skill registrations (`skills/legends-firecrawl/`, `skills/legends-alexandria/`), host shims (`CLAUDE.md`, `GEMINI.md`, `LEGENDS.md`), house-only `NEXT.md`, and per-host module installers (`bin/setup-multi-agent.ps1`/`.sh`, `bin/install-spine.ps1`). Kept `lfc`/`lax` CLI launchers and `bin/setup-auth.ps1`.
- `VERSION` is the authoritative version string; `pyproject.toml` reads it dynamically. Old releases and tags wiped; history preserved.

## 0.2.1

- Unique skill id for Legends Alexandria (was colliding with legends-firecrawl).
- Alexandria skill links repaired to live category, provider, and vault targets.
- Direct-routing language across skill, README, and hot cache; anti-abuse rules unchanged.
- Public version and MIT license metadata aligned; local paths and telemetry scrubbed.

## 0.2.0

- Deprecated the '-kit' moniker across module names.
- Fully consolidated Legends Alexandria into Legends Firecrawl.
- Unified the CLI with lfc.ps1 and lfc.cmd for both Firecrawl and Alexandria commands.
- Established Legends Alexandria as the data catalog, credit circumvention, and IP safety routing engine inside Legends Firecrawl.
- Merged 114 providers, 797 capabilities offline catalog, 3 IP safety tiers, and 8 production zero-credit native REST adapters.
- Upgraded the Empire Vault Data Encapsulation Engine and Obsidian knowledge vault.

## 0.1.0+local.20260830

- Founded Legends Firecrawl as a CLI-first, no-MCP house product.
- Pinned official firecrawl-cli@1.23.3 as vendor spine.
- Added bounded scrape, map, search, crawl preview/start/status, credit usage,
  route discovery, scope estimates, and a local usage ledger.
- Added a direct API compatibility layer for Legends Packet.
- Added secure Windows user-environment auth setup and multi-agent skill install.
- Added offline qualification, package build, and clean-room verification.
