# Research evidence and Empire integration

Collect once, preserve the complete response, and inspect it offline. Provider data remains provider data; this module adds provenance, integrity checks, scoped reuse review and portable handoff.

## Storage and scope

Core web commands and submitted Alexandria queries save full responses, including returned empty/error/pending states. The default root is `~/.legends-firecrawl/research` on every platform (`C:\Users\<user>\.legends-firecrawl\research` on Windows). Set `LEGENDS_FIRECRAWL_CAPTURE_ROOT` to the intended client workspace before collecting. Existing captures under an old installation remain there; upgrades do not silently move them. Set `LEGENDS_WORKSPACE_ID` or core `--workspace` to record the client identity. These are labels, not access controls.

Raw captures live under `var/captures/`; Markdown references under `vault/captures/`. Links are relative. Sidecar manifests permit metadata-only `lax captures` listing. Legacy captures are listed as unindexed; `lax captures --legacy` explicitly reads those older raw files. Sidecar listings do not verify response hashes. `--no-save` retains full stdout without files. Optional `--receipt` prints only saved paths while preserving full files. These flags cannot be combined.

## Portable evidence bank

All commands below are offline and require no API credentials:

```powershell
lfc evidence export response.json evidence --workspace client-a --endpoint scrape --request-file request.json --observed-at 2026-10-01T12:00:00Z
lfc evidence export-capture capture.raw.json evidence --workspace client-a
lfc evidence inventory evidence --workspace client-a --limit 50
lfc evidence find evidence --query example.com
lfc evidence verify evidence/PACKAGE_ID
lfc evidence view evidence/PACKAGE_ID --select data.markdown
lfc evidence view evidence/PACKAGE_ID --full
lfc evidence reuse evidence/PACKAGE_ID --workspace client-a --endpoint scrape --request-file request.json --max-age-hours 24
```

Export creates `response.json`, `manifest.json`, and `README.md`. Original standalone response bytes are preserved. The capture bridge extracts and serializes the complete inner response, retaining every field but not the source capture's whitespace. Legacy captures missing original request settings require `--request-file`; never invent missing settings or timestamps. `observed_at` is actual collection time, not export time.

The provider-specific `legends-firecrawl-evidence/v1` manifest binds the response and README hashes, complete request, workspace, operation, observation time and response state. Identical exports verify and reuse the same package. Interrupted packages remain visible and fail verification; they are not silently overwritten. Copying a complete package preserves working relative links. Hashes detect accidental changes; they are not signatures or proof that the provider is correct.

Inventory reads only bounded-size manifests, never full responses. It reports `response_integrity: not_checked`. Verification checks all three files and response-state consistency. Views verify first; selected/bounded views report omissions and never modify raw data. `--full` explicitly returns full JSON. JSON parsing still uses memory proportional to response size; this is not a streaming multi-gigabyte engine.

Reuse requires exact workspace, operation and request identity, a finite freshness window and a completed response. Partial pagination, unknown, pending, empty and failed responses require separate review. Even eligible reuse requires semantic review. `reuse` exits 0 for eligible and 2 for ineligible or verification failure. No command automatically buys replacement data or retries a possibly billed request.

## Empire handoff

Keep evidence in the chosen client/project workspace. Empire holds its map and reviewed meaning, not a mirror of every raw result. Stage a verified evidence package through the installed `legends-empire` research-evidence workflow, then use its existing capture/transaction process for accepted knowledge. Raw evidence, proposed interpretations, accepted findings and decisions remain separate. Export does not itself ingest or approve knowledge. No Obsidian UI or MCP is required.

This release does not claim provider scale, savings or source parity. Local bank benchmarks measure offline operations only. Treat request/response files as private: they may contain queries or client data and are not automatically redacted.
