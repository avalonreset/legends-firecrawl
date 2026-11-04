#Requires -Version 5.1
param(
  [string]$ApiKey
)

$ErrorActionPreference = 'Stop'
Write-Host 'Legends Firecrawl auth setup' -ForegroundColor Cyan
Write-Host 'Paste a Firecrawl API key. It will be stored at Windows user-environment scope and will not be printed.'
$plain = if ($ApiKey) {
  $ApiKey.Trim()
} else {
  (& python -c "import getpass; print(getpass.getpass('FIRECRAWL_API_KEY: '), end='')").Trim()
}
try {
  if ([string]::IsNullOrWhiteSpace($plain) -or -not $plain.StartsWith('fc-')) {
    throw 'The value did not look like a Firecrawl API key. Nothing was stored.'
  }
  [Environment]::SetEnvironmentVariable('FIRECRAWL_API_KEY', $plain, 'User')
  $env:FIRECRAWL_API_KEY = $plain
}
finally {
  $plain = $null
}
Write-Host 'Stored FIRECRAWL_API_KEY at Windows user scope. Running doctor.' -ForegroundColor Green
& (Join-Path $PSScriptRoot 'doctor.ps1')
exit $LASTEXITCODE

