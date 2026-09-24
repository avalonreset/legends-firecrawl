#Requires -Version 5.1
$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path $PSScriptRoot -Parent
$skillsRoot = Join-Path $repoRoot 'skills'
$packName = 'legends-firecrawl'
$target = Join-Path $skillsRoot $packName
if (-not (Test-Path (Join-Path $target 'SKILL.md'))) { throw 'House skill is missing.' }

function Set-HouseJunction {
  param([string]$LinkPath, [string]$TargetPath, [string]$Harness)
  $parent = Split-Path $LinkPath -Parent
  if (-not (Test-Path $parent)) { New-Item -ItemType Directory -Force -Path $parent | Out-Null }
  if (Test-Path $LinkPath) {
    $item = Get-Item -LiteralPath $LinkPath -Force
    if (-not ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
      throw "[$Harness] existing path is not a junction: $LinkPath"
    }
    $current = if ($item.Target -is [array]) { $item.Target -join ';' } else { [string]$item.Target }
    $wanted = (Resolve-Path -LiteralPath $TargetPath).Path
    if (($current -replace '/', '\').TrimEnd('\') -eq ($wanted -replace '/', '\').TrimEnd('\')) {
      Write-Host "[$Harness] current" -ForegroundColor DarkGray
      return
    }
    cmd /c "rmdir `"$LinkPath`"" | Out-Null
  }
  cmd /c "mklink /J `"$LinkPath`" `"$TargetPath`"" | Out-Null
  if (-not (Test-Path (Join-Path $LinkPath 'SKILL.md'))) { throw "[$Harness] link verification failed" }
  Write-Host "[$Harness] linked $LinkPath" -ForegroundColor Green
}

Write-Host 'Legends Firecrawl multi-agent install' -ForegroundColor Cyan
Write-Host 'Installing the house skill only; no vendor integration or MCP setup.' -ForegroundColor DarkGray
foreach ($entry in @(
  @{ Name='Grok'; Root=(Join-Path $env:USERPROFILE '.grok\skills') },
  @{ Name='Codex'; Root=(Join-Path $env:USERPROFILE '.codex\skills') },
  @{ Name='Claude'; Root=(Join-Path $env:USERPROFILE '.claude\skills') },
  @{ Name='Gemini'; Root=(Join-Path $env:USERPROFILE '.gemini\skills') },
  @{ Name='Antigravity'; Root=(Join-Path $env:USERPROFILE '.gemini\antigravity\skills') }
)) {
  Set-HouseJunction -LinkPath (Join-Path $entry.Root $packName) -TargetPath $target -Harness $entry.Name
}
$version = (Get-Content -LiteralPath (Join-Path $repoRoot 'VERSION') -Raw).Trim()
$sourceHash = (Get-FileHash -LiteralPath (Join-Path $target 'SKILL.md') -Algorithm SHA256).Hash.ToLowerInvariant()
$fingerprint = 'sha256:' + $sourceHash.Substring(0, 16)
$agentPaths = [ordered]@{
  grok=(Join-Path $env:USERPROFILE '.grok\skills\legends-firecrawl')
  codex=(Join-Path $env:USERPROFILE '.codex\skills\legends-firecrawl')
  claude=(Join-Path $env:USERPROFILE '.claude\skills\legends-firecrawl')
  gemini=(Join-Path $env:USERPROFILE '.gemini\skills\legends-firecrawl')
  antigravity=(Join-Path $env:USERPROFILE '.gemini\antigravity\skills\legends-firecrawl')
}
$agentRows = @()
foreach ($entry in $agentPaths.GetEnumerator()) {
  $skillMd = Join-Path $entry.Value 'SKILL.md'
  $readable = Test-Path -LiteralPath $skillMd
  $matches = $readable -and ((Get-FileHash -LiteralPath $skillMd -Algorithm SHA256).Hash.ToLowerInvariant() -eq $sourceHash)
  $item = if ($readable) { Get-Item -LiteralPath $entry.Value -Force } else { $null }
  $kind = if ($item -and ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) { 'junction' } elseif ($item) { 'directory' } else { 'missing' }
  $resolved = if ($kind -eq 'junction') { [string]($item.Target -join ';') } elseif ($matches) { (Resolve-Path -LiteralPath $target).Path } else { $null }
  $reasons = @()
  if (-not $matches) { $reasons = @('skill_missing_or_content_mismatch') }
  $agentRows += [ordered]@{
    agent_id=$entry.Key
    skill_link_path=$entry.Value
    resolved_target=$resolved
    link_kind=$kind
    target_matches_source=[bool]$matches
    skill_md_readable=[bool]$readable
    installed_commit=$null
    content_fingerprint=$(if ($matches) { $fingerprint } else { $null })
    result=$(if ($matches) { 'pass' } else { 'fail' })
    reasons=[object[]]@($reasons)
  }
}
$installResult = if (@($agentRows | Where-Object result -ne 'pass').Count -eq 0) { 'pass' } else { 'partial' }
$receiptDir = Join-Path $repoRoot '.kit-visibility'
if (-not (Test-Path $receiptDir)) { New-Item -ItemType Directory -Force -Path $receiptDir | Out-Null }
$receipt = [ordered]@{
  schema_version='kit-install-receipt.v1'
  receipt_kind='installer'
  emitted_at=(Get-Date).ToString('o')
  host=[ordered]@{ id='NERV'; os='Windows' }
  kit=[ordered]@{
    id=$packName
    brand='Legends Firecrawl'
    canonical_repo_path=$repoRoot
    release_version=$version
    repo_head=$null
    repo_dirty=$null
    skill_source_path=(Resolve-Path -LiteralPath $target).Path
  }
  install=[ordered]@{
    mode='link'
    result=$installResult
    installer_script='bin/setup-multi-agent.ps1'
    notes=@('House skill only. Vendor init/setup/MCP integrations were not run.')
  }
  spine=[ordered]@{
    name='firecrawl'
    version=((& firecrawl --version).Trim())
    path_present=[bool](Get-Command firecrawl -ErrorAction SilentlyContinue)
  }
  agents=$agentRows
  doctor=[ordered]@{ ran=$false; result=$null; evidence_at=$null; summary=$null }
  smoke=[ordered]@{ ran=$false; result=$null; evidence_at=$null; summary=$null }
}
$receipt | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $receiptDir 'install-last.json') -Encoding UTF8
Write-Host "PASS house skill linked for Grok, Codex, Claude, and Gemini ($version; $installResult)." -ForegroundColor Green

