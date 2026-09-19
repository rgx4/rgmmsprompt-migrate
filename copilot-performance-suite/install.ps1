[CmdletBinding()]
param(
    [ValidateSet('User', 'Project')]
    [string]$Scope = 'User',
    [string]$ProjectPath = (Get-Location).Path,
    [switch]$Force
)

$ErrorActionPreference = 'Stop'
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Payload = Join-Path $ScriptRoot '.copilot'

if ($Scope -eq 'User') {
    if ($env:COPILOT_HOME) {
        $Target = $env:COPILOT_HOME
    } else {
        $Target = Join-Path $HOME '.copilot'
    }
} else {
    $ResolvedProject = (Resolve-Path $ProjectPath).Path
    $Target = Join-Path $ResolvedProject '.github'
}

$Conflicts = @()
Get-ChildItem (Join-Path $Payload 'agents') -Filter '*.agent.md' | ForEach-Object {
    $Destination = Join-Path (Join-Path $Target 'agents') $_.Name
    if (Test-Path $Destination) { $Conflicts += $Destination }
}
Get-ChildItem (Join-Path $Payload 'skills') -Directory | ForEach-Object {
    $Destination = Join-Path (Join-Path $Target 'skills') $_.Name
    if (Test-Path $Destination) { $Conflicts += $Destination }
}

if ($Conflicts.Count -gt 0 -and -not $Force) {
    Write-Error ("Installation stopped because targets already exist:`n  " + ($Conflicts -join "`n  ") + "`nRe-run with -Force to merge/overwrite matching files.")
}

$AgentsTarget = Join-Path $Target 'agents'
$SkillsTarget = Join-Path $Target 'skills'
New-Item -ItemType Directory -Force -Path $AgentsTarget, $SkillsTarget | Out-Null
Copy-Item (Join-Path $Payload 'agents/*') -Destination $AgentsTarget -Recurse -Force
Copy-Item (Join-Path $Payload 'skills/*') -Destination $SkillsTarget -Recurse -Force

$Python = Get-Command python -ErrorAction SilentlyContinue
if (-not $Python) { $Python = Get-Command py -ErrorAction SilentlyContinue }
if (-not $Python) { throw 'Python 3 is required to run package validation.' }

if ($Python.Name -eq 'py.exe' -or $Python.Name -eq 'py') {
    & $Python.Source -3 (Join-Path $ScriptRoot 'tools/verify_package.py') $Target
} else {
    & $Python.Source (Join-Path $ScriptRoot 'tools/verify_package.py') $Target
}
if ($LASTEXITCODE -ne 0) { throw 'Package validation failed.' }

Write-Host "Installed performance suite in $Target"
Write-Host 'Restart GitHub Copilot CLI before selecting performance-orchestrator.'

