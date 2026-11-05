# Legends Firecrawl agent rules

1. Read `README.md`, `docs/AGENT-RECIPE.md`, and `skills/cto-legends/SKILL.md`.
2. Run `lfc doctor --offline` (or `python -m legends_firecrawl doctor --offline`) for offline readiness, or `lfc doctor` before live work; a failing doctor check stops live work.
3. Use `lfc` (`python -m legends_firecrawl`) and `lax` (`python -m legends_firecrawl alexandria`) for intent-level jobs, routing, and JSON output.
4. Never install, configure, recommend, or fall back to Firecrawl MCP.
5. Never run vendor `firecrawl init`, `setup`, `launch`, or `launcher`.
6. Preview crawl scope with `lfc crawl-preview`, then require explicit `--confirm` for the live crawl.
7. Use official Firecrawl only. No direct-source bypass or substitutes. Alexandria queries require explicit `--confirm`; preview first. Never silently retry a possibly billed submission.
8. Keep keys out of chat, files, logs, receipts, and shell history.
9. Runtime captures and usage ledgers stay under `var/` or `~/.legends-firecrawl/research`.

## EDR and Security Guardrails

- **No hidden consoles or execution-policy bypass wrappers**: invoke `lfc`, `lax`, `legends-firecrawl`, or `python -m legends_firecrawl` directly through standard process execution without hidden console flags or shell execution-policy bypass wrappers.
- **No parent-process tree walking**: never enumerate parent processes or inspect system process trees.
- **No browser profile or OS credential harvesting**: read credentials strictly from `FIRECRAWL_API_KEY` or an explicit `FIRECRAWL_API_KEY_FILE` path, never from local browser profile databases or OS DPAPI stores.
- **Symlink refusal**: refuse symlink paths (`Path.is_symlink()`) on file inputs, key files, and evidence packages.
- **Network allowlist**: outbound HTTPS requests are restricted to `https://api.firecrawl.dev` (or explicit HTTPS `FIRECRAWL_API_URL`) and target public HTTP(S) URLs.
