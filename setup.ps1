# Claude Code Dotfiles Setup
# Run this on a new Windows machine (PowerShell as admin not required)
# Usage: irm https://raw.githubusercontent.com/digitalthreadai/claude-sync/main/setup.ps1 | iex

$repoUrl = "https://github.com/digitalthreadai/claude-sync.git"
$claudeDir = "$env:USERPROFILE\.claude"

Write-Host ""
Write-Host "=== Claude Code Dotfiles Setup ===" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check prerequisites
Write-Host "[1/5] Checking prerequisites..." -ForegroundColor Yellow

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: git not found. Install from https://git-scm.com/download/win" -ForegroundColor Red
    exit 1
}

$hasPython = Get-Command python -ErrorAction SilentlyContinue
if (-not $hasPython) {
    Write-Host "WARNING: python not found — last30days skill won't work. Install Python 3 from python.org" -ForegroundColor Yellow
}

Write-Host "  git: OK" -ForegroundColor Green
if ($hasPython) { Write-Host "  python: OK" -ForegroundColor Green }

# Step 2: Close Claude Code warning
Write-Host ""
Write-Host "[2/5] Important: Close Claude Code before continuing." -ForegroundColor Yellow
Write-Host "      Press Enter when Claude Code is closed, or Ctrl+C to cancel."
Read-Host

# Step 3: Back up existing .claude if it exists
Write-Host "[3/5] Backing up existing .claude (if any)..." -ForegroundColor Yellow
if (Test-Path $claudeDir) {
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $backupDir = "$env:USERPROFILE\.claude.bak.$timestamp"
    Rename-Item $claudeDir $backupDir
    Write-Host "  Backed up to: $backupDir" -ForegroundColor Green
} else {
    Write-Host "  No existing .claude found — skipping backup." -ForegroundColor Green
}

# Step 4: Clone the repo
Write-Host "[4/5] Cloning dotfiles..." -ForegroundColor Yellow
git clone $repoUrl $claudeDir
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: git clone failed." -ForegroundColor Red
    exit 1
}
Write-Host "  Cloned to: $claudeDir" -ForegroundColor Green

# Step 5: Install Python dependencies
Write-Host "[5/5] Installing skill dependencies..." -ForegroundColor Yellow
if ($hasPython) {
    $req = "$claudeDir\skills\last30days\requirements.txt"
    if (Test-Path $req) {
        python -m pip install -r $req --quiet
        Write-Host "  last30days: dependencies installed" -ForegroundColor Green
    }
} else {
    Write-Host "  Skipped (python not found)" -ForegroundColor Yellow
}

# Done
Write-Host ""
Write-Host "=== Setup Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Set GITHUB_PERSONAL_ACCESS_TOKEN as a system environment variable"
Write-Host "     (for GitHub MCP): System Properties > Environment Variables"
Write-Host "  2. Open Claude Code"
Write-Host "  3. Run: /plugin install codex@openai-codex"
Write-Host "  4. Run: /reload-plugins"
Write-Host ""
Write-Host "Your skills, agents, commands, and settings are ready." -ForegroundColor Green
