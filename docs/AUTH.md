# Authentication and first-run trust ceremony

Firecrawl requires a human-created account and API key. The module does
not create an account, scrape a dashboard session, copy cookies, or put a key in
the repository.

## One-time setup

1. Create or select the intended Firecrawl account in the vendor
   dashboard and create an API key.
2. Set `FIRECRAWL_API_KEY` in your environment (or point `FIRECRAWL_API_KEY_FILE` to a local plain-text key file outside the repository).
3. Run `lfc doctor` (or `python -m legends_firecrawl doctor`) to verify readiness.

Do not pass secret keys as inline CLI arguments because command history
and process inspection can expose arguments.

## Rotation

Create a replacement key, update `FIRECRAWL_API_KEY`, verify `lfc doctor`, then revoke the
old key in the vendor dashboard. Never record key material in version control or vault notes.
