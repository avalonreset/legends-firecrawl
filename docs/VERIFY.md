# Verification

## Offline qualification

```sh
python -m pytest tests
python -m legends_firecrawl version
python -m legends_firecrawl routes
python -m legends_firecrawl crawl-preview https://example.com
python scripts/check_release.py
```

## Doctor

```sh
python -m legends_firecrawl doctor --offline
python -m legends_firecrawl doctor
```

Live `doctor` PASS requires the exact pinned official CLI, an API key, and a live
credit-usage response. Missing auth is reported as failed, never disguised as PASS.

## Package and clean room

```sh
python scripts/build_release.py
python scripts/verify_package.py
```
