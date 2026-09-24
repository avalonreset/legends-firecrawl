#Requires -Version 5.1
param([switch]$Offline)

Write-Host "=== Legends Firecrawl Unified Doctor ===" -ForegroundColor Cyan

$argsList = @('doctor')
if ($Offline) { $argsList += '--offline' }

# 1. Core Firecrawl Subsystem Doctor
Write-Host "--- Core Firecrawl ---" -ForegroundColor Cyan
& (Join-Path $PSScriptRoot 'lfc.ps1') @argsList
if ($LASTEXITCODE -ne 0) {
    Write-Host "[FAIL] Core Firecrawl doctor failed." -ForegroundColor Red
} else {
    Write-Host "[PASS] Core Firecrawl doctor passed." -ForegroundColor Green
}

# 2. Alexandria Subsystem Doctor
Write-Host "--- Alexandria Engine ---" -ForegroundColor Cyan
$baseDir = "E:\legends-firecrawl"
$catalogPath = "$baseDir\data\alexandria_catalog.json"
$safetyAuditPath = "$baseDir\data\safety_audit.json"
$secretsPath = "$env:USERPROFILE\.empire\secrets\empire.env"
$shelfPath = "E:\empire\wiki\library\legends-firecrawl\_Index.md"

if (Test-Path $catalogPath) {
    $catalog = Get-Content $catalogPath -Raw | ConvertFrom-Json
    if ($catalog.totalProviders -ge 114 -and $catalog.totalCapabilities -ge 797) {
        Write-Host "[PASS] Alexandria Catalog: >= 114 providers and 797 capabilities cached." -ForegroundColor Green
    } else {
        Write-Host "[WARN] Alexandria Catalog counts: $($catalog.totalProviders) providers, $($catalog.totalCapabilities) capabilities." -ForegroundColor Yellow
    }
} else {
    Write-Host "[FAIL] Alexandria Catalog missing at $catalogPath" -ForegroundColor Red
}

if (Test-Path $safetyAuditPath) {
    $sAudit = Get-Content $safetyAuditPath -Raw | ConvertFrom-Json
    $green = ($sAudit.providers | Where-Object { $_.ipSafety -eq 'GREEN_SAFE' }).Count
    $yellow = ($sAudit.providers | Where-Object { $_.ipSafety -eq 'YELLOW_SHIELDED' }).Count
    $blue = ($sAudit.providers | Where-Object { $_.ipSafety -eq 'BLUE_LICENSED' }).Count
    Write-Host "[PASS] IP Safety Audit: $green GREEN_SAFE, $yellow YELLOW_SHIELDED, $blue BLUE_LICENSED." -ForegroundColor Green
} else {
    Write-Host "[FAIL] Safety Audit missing at $safetyAuditPath" -ForegroundColor Red
}

try {
    $routerTest = node "$baseDir\alexandria-src\cli.js" query treasury-fiscal-data debt/to-the-penny
    $testOutput = ($routerTest -join "
") -replace '\x1b\[[0-9;]*m', ''
    if ($testOutput -match "ROUTER DECISION:\s+NATIVE_DIRECT" -and $testOutput -match "Credits Burned:\s+0") {
        Write-Host "[PASS] Router Decision Engine: GREEN_SAFE auto-routed direct with 0 credits burned." -ForegroundColor Green
    } else {
        Write-Host "[WARN] Router test output unexpected: $testOutput" -ForegroundColor Yellow
    }
} catch {
    Write-Host "[FAIL] Router execution test failed: $_" -ForegroundColor Red
}

$dashFound = $false
Get-ChildItem -Path "$baseDir\vault", "$baseDir\skills", "$baseDir\alexandria-src" -Recurse -Include *.md,*.js | ForEach-Object {
    $txt = [System.IO.File]::ReadAllText($_.FullName)
    if ($txt.Contains([char]0x2014) -or $txt.Contains([char]0x2013)) {
        Write-Host "[FAIL] House style violation (em/en dash) in $($_.FullName)" -ForegroundColor Red
        $dashFound = $true
    }
}
if (-not $dashFound) {
    Write-Host "[PASS] House Style Law: Zero em dashes and zero en dashes." -ForegroundColor Green
}

Write-Host "Doctor checks complete." -ForegroundColor Cyan
