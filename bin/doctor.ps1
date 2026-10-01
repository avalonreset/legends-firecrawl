#Requires -Version 5.1
param([switch]$Offline)
$ErrorActionPreference = 'Stop'
$argsList = @('doctor')
if ($Offline) { $argsList += '--offline' }
& (Join-Path $PSScriptRoot 'lfc.ps1') @argsList
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$baseDir = Split-Path $PSScriptRoot -Parent
& node (Join-Path $baseDir 'alexandria-src/cli.js') audit
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'Readiness passed. Catalog and routing checks do not establish source availability, savings, or scale.'
exit 0
