#Requires -Version 5.1

if ($args.Count -gt 0 -and $args[0] -eq 'alexandria') {
    $kitRoot = Split-Path $PSScriptRoot -Parent
    $scriptPath = Join-Path $kitRoot "alexandria-src\cli.js"
    $laxArgs = if ($args.Count -gt 1) { $args[1..($args.Count - 1)] } else { @() }
    & node $scriptPath $laxArgs
    exit $LASTEXITCODE
}

$kitRoot = Split-Path $PSScriptRoot -Parent
$pythonRoot = Join-Path $kitRoot 'python'
$previous = $env:PYTHONPATH
$env:PYTHONPATH = if ($previous) { "$pythonRoot;$previous" } else { $pythonRoot }
try {
    & python -m legends_firecrawl.cli @args
    exit $LASTEXITCODE
}
finally {
    $env:PYTHONPATH = $previous
}
