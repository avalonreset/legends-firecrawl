#Requires -Version 5.1

$scriptPath = Join-Path (Split-Path $PSScriptRoot -Parent) "alexandria-src\cli.js"
$previousKey = $env:FIRECRAWL_API_KEY
try {
    if (-not $previousKey -and $env:FIRECRAWL_DISABLE_USER_ENV -ne '1') {
        $env:FIRECRAWL_API_KEY = [Environment]::GetEnvironmentVariable('FIRECRAWL_API_KEY', 'User')
    }
    & node $scriptPath @args
    $resultCode = $LASTEXITCODE
} finally {
    $env:FIRECRAWL_API_KEY = $previousKey
}
exit $resultCode
