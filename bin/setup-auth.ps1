#Requires -Version 5.1
param()

$ErrorActionPreference = 'Stop'
Write-Host 'Legends Firecrawl auth setup' -ForegroundColor Cyan
Write-Host 'Paste a Firecrawl API key. It will be stored at Windows user-environment scope and will not be printed.'
$secure = Read-Host 'FIRECRAWL_API_KEY' -AsSecureString
$pointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
try {
  $plain = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($pointer)
  if ([string]::IsNullOrWhiteSpace($plain) -or -not $plain.StartsWith('fc-')) {
    throw 'The value did not look like a Firecrawl API key. Nothing was stored.'
  }
  [Environment]::SetEnvironmentVariable('FIRECRAWL_API_KEY', $plain, 'User')
  $env:FIRECRAWL_API_KEY = $plain
}
finally {
  if ($pointer -ne [IntPtr]::Zero) { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($pointer) }
  $plain = $null
}
Write-Host 'Stored FIRECRAWL_API_KEY at Windows user scope. Running doctor.' -ForegroundColor Green
& (Join-Path $PSScriptRoot 'doctor.ps1')
exit $LASTEXITCODE

