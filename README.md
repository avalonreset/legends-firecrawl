# legends-firecrawl

An agent-oriented CLI wrapper for official Firecrawl web operations and Alexandria queries, with a local catalog and saved response evidence.

**Version 0.3.0 scope:** official Firecrawl execution only. All native bypass and direct-source substitutions are retired, including the experimental Treasury routes. Read the [release scope](docs/RELEASE-SCOPE.md) and [evidence workflow](docs/RESEARCH-MEMORY.md).

## Why use it

Collect once, retain the complete response, then let an agent inspect the evidence as needed. The wrapper supplies a repeatable collection workflow: full JSON on disk, vault references, request provenance and bounded execution. It leaves interpretation to the agent and keeps the underlying Firecrawl service visible.

## What it adds

- Intent-level commands for official scrape, map, search and bounded crawl jobs.
- Offline catalog search and provider inspection. The saved snapshot contains 114 provider labels and 797 capabilities; these are discovery records, not independently tested integrations.
- Explicit confirmation before Alexandria execution and crawl submission.
- Full captures, portable evidence export, integrity verification, offline finding/viewing and exact-scope freshness checks.
- Integration with the existing `cto-legends` agent workflow.

The value is workflow convenience and reviewable execution. This project does not claim cheaper equivalent data, unique intelligence, superior source coverage, or a measured savings percentage. Firecrawl's own API and CLI also work without MCP, and its discovery is free.

## Commands

```powershell
# Offline catalog discovery; cached descriptions and prices may be stale
lax search "treasury"
lax inspect treasury-fiscal-data
lax audit

# Preview an official Alexandria query; no native route is selected
lax query treasury-fiscal-data debt/to-the-penny

# Submit the reviewed request through Firecrawl; may consume credits
lax query treasury-fiscal-data debt/to-the-penny --confirm

# Captured evidence
lax captures

# Official Firecrawl web operations may consume credits
lfc credits
lfc scrape https://example.com
lfc map https://example.com --limit 100
lfc search "machine learning benchmarks" --limit 5
lfc crawl-preview https://example.com --limit 25 --max-depth 2
lfc crawl https://example.com --limit 25 --max-depth 2 --confirm
```

Alexandria queries default to preview. `--preview` requests that explicitly; `--confirm` authorizes submission; `--no-save` skips local capture. The confirmation rule does not mean every existing `lfc` operation is a no-charge preview. Provider contracts and prices govern live requests.

## Capture first, inspect afterward

Scrape, map, search, crawl submission and crawl-status save the complete returned JSON to `var/captures/firecrawl/` and a Markdown reference in `vault/captures/firecrawl/`. Alexandria also preserves its full response and vault card. CLI web results retain all original fields and add `_capture` paths. `--no-save` explicitly opts out; `LEGENDS_FIRECRAWL_CAPTURE_ROOT` selects another workspace. Python client calls alone do not automatically save.

Default storage is `~/.legends-firecrawl/research`, outside replaceable module installations. Existing installation-local captures are not moved automatically. Set `LEGENDS_WORKSPACE_ID` or core `--workspace` for client identity. Optional `--receipt` prints only saved paths; full output remains the default.

Use `lfc evidence export-capture`, `inventory`, `find`, `verify`, `view` and `reuse` for a portable offline evidence bank. The [research-memory guide](docs/RESEARCH-MEMORY.md) explains requests, freshness, partial results and Empire handoff.

The agent can read selected fields or the entire saved file without another provider call. Each capture is one response, not proof that every page or all pagination has been collected. Captures are excluded from releases.

Catalog search is a compact view over the complete local JSON catalog, whose path is included in each result. Use `lax inspect <provider> --full` for complete cached contracts. Compact discovery never truncates the underlying archive.

## Agent setup (via `cto-legends`)

Part of [cto-legends](https://github.com/avalonreset/cto-legends). The one registered router skill is vendored at `skills/cto-legends/SKILL.md`; this module is not a separate registered skill and does not require an ambient MCP daemon.

Run `cto-legends handoff legends-firecrawl` and read the returned installed recipe and task-readiness checks. If the module is missing, preview setup with `cto-legends install legends-firecrawl`, perform the authorized setup, then repeat the handoff. Use `cto-legends check-updates` to compare your installed version with the catalog and published release.

```powershell
npm install -g firecrawl-cli@1.23.3
pwsh -File bin/setup-auth.ps1
pwsh -File bin/doctor.ps1
```

## Verification and limits

```powershell
pytest tests -v
python scripts/run_behavioral_evals.py
```

Offline tests verify command contracts, not the correctness or availability of every provider. This wrapper does not improve the underlying provider's data, replace source access limits, or guarantee proxy protection. Catalog records and prices can become stale; current provider contracts govern live execution.

## License

MIT License. Copyright (c) 2026 Avalon Reset.
