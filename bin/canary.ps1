#Requires -Version 5.1
param([switch]$Plan, [switch]$Confirm)

$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$lfc = Join-Path $PSScriptRoot 'lfc.ps1'
$receipt = Join-Path $root 'var\canary-receipt.json'
$proposal = [ordered]@{
  schema = 'legends-firecrawl-canary/v1'
  target = 'https://example.com'
  operation = 'single-page scrape'
  formats = @('markdown')
  external_publish = $false
  destructive = $false
  expected_scope = @{ pages = 1 }
  requires_confirm = $true
}
if ($Plan -or -not $Confirm) {
  $proposal | ConvertTo-Json -Depth 10
  if (-not $Plan) { Write-Error 'Canary requires -Confirm after reviewing this plan.' }
  exit $(if ($Plan) { 0 } else { 2 })
}

& (Join-Path $PSScriptRoot 'doctor.ps1') | Out-Null
if ($LASTEXITCODE -ne 0) { throw 'Doctor did not pass; canary stopped before a charged request.' }
$beforeRaw = & $lfc credits
if ($LASTEXITCODE -ne 0) { throw 'Could not read starting credits.' }
$pageRaw = & $lfc scrape 'https://example.com'
if ($LASTEXITCODE -ne 0) { throw 'Disposable scrape failed.' }
$afterRaw = & $lfc credits
if ($LASTEXITCODE -ne 0) { throw 'Could not read ending credits.' }
$before = $beforeRaw | ConvertFrom-Json
$page = $pageRaw | ConvertFrom-Json
$after = $afterRaw | ConvertFrom-Json
$markdown = if ($page.data.markdown) { [string]$page.data.markdown } else { '' }
$result = [ordered]@{
  schema = 'legends-firecrawl-canary/v1'
  ran_at = (Get-Date).ToUniversalTime().ToString('o')
  target = 'https://example.com'
  result = if ($page.success -and $markdown.Length -gt 0) { 'WORKS' } else { 'BLOCKED' }
  evidence = @{
    success = [bool]$page.success
    markdown_length = $markdown.Length
    source_url = $page.data.metadata.sourceURL
    status_code = $page.data.metadata.statusCode
  }
  credit_usage_before = $before
  credit_usage_after = $after
  cleanup = 'not applicable; read-only public page scrape'
}
$parent = Split-Path $receipt -Parent
if (-not (Test-Path $parent)) { New-Item -ItemType Directory -Force -Path $parent | Out-Null }
$result | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $receipt -Encoding UTF8
$result | ConvertTo-Json -Depth 20
if ($result.result -ne 'WORKS') { exit 1 }
