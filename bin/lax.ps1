#Requires -Version 5.1

$scriptPath = Join-Path (Split-Path $PSScriptRoot -Parent) "alexandria-src\cli.js"
& node $scriptPath @args
exit $LASTEXITCODE
