#Requires -Version 5.1
param([string]$Version = '1.23.3')

$ErrorActionPreference = 'Stop'
if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
  throw 'npm is required to install the official Firecrawl CLI spine.'
}
Write-Host "Installing official firecrawl-cli@$Version only." -ForegroundColor Cyan
Write-Host 'The vendor init/setup/MCP installers are deliberately not run.' -ForegroundColor DarkGray
& npm install -g "firecrawl-cli@$Version"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$observed = (& firecrawl --version).Trim()
if ($observed -ne $Version) { throw "Firecrawl CLI version mismatch: expected $Version, observed $observed" }
Write-Host "PASS firecrawl $observed" -ForegroundColor Green
