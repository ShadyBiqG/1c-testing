#Requires -Version 5.1
[CmdletBinding()]
param(
    [ValidateSet('Project', 'Global')]
    [string]$Scope = 'Project',

    [string]$ProjectRoot = (Get-Location).Path,

    [string]$CodexHome
)

$ErrorActionPreference = 'Stop'
$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$SourceSkill = Join-Path $PackageRoot '1c-testing'
$SourceFragment = Join-Path $PackageRoot 'USER-RULES.fragment.md'

if (-not (Test-Path -LiteralPath $SourceSkill -PathType Container)) {
    throw "Не найден исходный skill: $SourceSkill"
}

if ($Scope -eq 'Global') {
    if ([string]::IsNullOrWhiteSpace($CodexHome)) {
        if (-not [string]::IsNullOrWhiteSpace($env:CODEX_HOME)) {
            $CodexHome = $env:CODEX_HOME
        } else {
            $CodexHome = Join-Path ([Environment]::GetFolderPath('UserProfile')) '.codex'
        }
    }

    $ResolvedCodexHome = [System.IO.Path]::GetFullPath($CodexHome)
    $TargetSkillRoot = Join-Path $ResolvedCodexHome 'skills'
    $TargetSkill = Join-Path $TargetSkillRoot '1c-testing'
} else {
    if (-not (Test-Path -LiteralPath $ProjectRoot -PathType Container)) {
        throw "Не найден каталог проекта: $ProjectRoot"
    }
    if (-not (Test-Path -LiteralPath $SourceFragment -PathType Leaf)) {
        throw "Не найден USER-RULES.fragment.md: $SourceFragment"
    }

    $ResolvedProjectRoot = [System.IO.Path]::GetFullPath($ProjectRoot)
    $TargetSkillRoot = Join-Path $ResolvedProjectRoot '.codex\skills'
    $TargetSkill = Join-Path $TargetSkillRoot '1c-testing'
}

$ResolvedSourceSkill = [System.IO.Path]::GetFullPath($SourceSkill)
$ResolvedTargetSkill = [System.IO.Path]::GetFullPath($TargetSkill)
if ($ResolvedSourceSkill -eq $ResolvedTargetSkill) {
    throw 'Исходный и целевой каталоги skill совпадают.'
}

New-Item -ItemType Directory -Force -Path $TargetSkillRoot | Out-Null

if (Test-Path -LiteralPath $ResolvedTargetSkill) {
    Remove-Item -LiteralPath $ResolvedTargetSkill -Recurse -Force
}
Copy-Item -LiteralPath $ResolvedSourceSkill -Destination $TargetSkillRoot -Recurse -Force

if ($Scope -eq 'Project') {
    $UserRules = Join-Path $ResolvedProjectRoot 'USER-RULES.md'
    $Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    $Fragment = [System.IO.File]::ReadAllText($SourceFragment)

    if (Test-Path -LiteralPath $UserRules) {
        $Current = [System.IO.File]::ReadAllText($UserRules)
    } else {
        $Current = "# User Rules`r`n"
    }

    $Pattern = '(?s)<!-- 1c-testing:start -->.*?<!-- 1c-testing:end -->'
    if ([regex]::IsMatch($Current, $Pattern)) {
        $Updated = [regex]::Replace(
            $Current,
            $Pattern,
            [System.Text.RegularExpressions.MatchEvaluator]{ param($Match) $Fragment.TrimEnd() },
            1
        )
    } else {
        $Updated = $Current.TrimEnd() + "`r`n`r`n" + $Fragment.TrimEnd() + "`r`n"
    }

    [System.IO.File]::WriteAllText($UserRules, $Updated, $Utf8NoBom)

    Write-Host '1c-testing установлен в проект:' -ForegroundColor Green
    Write-Host "  Skill:      $ResolvedTargetSkill"
    Write-Host "  User rules: $UserRules"
    Write-Host 'Не изменялись: AGENTS.md и .codex/config.toml'
} else {
    Write-Host '1c-testing установлен глобально:' -ForegroundColor Green
    Write-Host "  Skill: $ResolvedTargetSkill"
    Write-Host 'USER-RULES.md проектов не изменялись.'
}

Write-Host 'Перезапустите Codex или откройте новый чат, чтобы перечитать skill.'
