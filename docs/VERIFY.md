# Verification

## Offline qualification

```powershell
$env:PYTHONPATH = 'E:\legends-firecrawl\python'
python -m pytest E:\legends-firecrawl\tests
pwsh -File E:\legends-firecrawl\bin\lfc.ps1 version
pwsh -File E:\legends-firecrawl\bin\lfc.ps1 routes
pwsh -File E:\legends-firecrawl\bin\lfc.ps1 crawl-preview https://example.com
```

## Doctor

```powershell
pwsh -File E:\legends-firecrawl\bin\doctor.ps1
```

Doctor PASS requires the exact pinned official CLI, an API key, and a live
credit-usage response. Missing auth is BLOCKED, never disguised as PASS.

## Disposable live canary

```powershell
pwsh -File E:\legends-firecrawl\bin\canary.ps1 -Plan
pwsh -File E:\legends-firecrawl\bin\canary.ps1 -Confirm
```

The canary scrapes only `https://example.com`, records structural evidence and
credit snapshots, and does not publish or mutate the site.

## Package and clean room

```powershell
python E:\legends-firecrawl\scripts\build_release.py
python E:\legends-firecrawl\scripts\verify_package.py
```

