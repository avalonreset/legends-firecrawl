# Authentication and first-run trust ceremony

Firecrawl currently requires a human-created account and API key. The Kit does
not create an account, scrape a dashboard session, copy cookies, or put a key in
the repository.

## One-time setup

1. Benjamin creates or selects the intended Firecrawl account in the vendor
   dashboard and creates an API key.
2. Run `pwsh -File E:\legends-firecrawl\bin\setup-auth.ps1`.
3. Paste the key into the hidden prompt.
4. The helper stores `FIRECRAWL_API_KEY` at Windows user-environment scope and
   immediately runs doctor.

The key is not echoed. Do not pass it as a CLI argument because command history
and process inspection can expose arguments.

## Rotation

Create a replacement key, rerun `setup-auth.ps1`, verify doctor, then revoke the
old key in the vendor dashboard. Never record key material in Empire.

