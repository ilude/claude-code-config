# Sync ~/.claude config from git remote on session start
# Runs silently - only outputs if updates are pulled

$ClaudeDir = Join-Path $env:USERPROFILE ".claude"

# Exit silently if not a git repo
if (-not (Test-Path (Join-Path $ClaudeDir ".git"))) {
    exit 0
}

Push-Location $ClaudeDir

try {
    # Check if remote exists
    $remote = git remote get-url origin 2>$null
    if (-not $remote) {
        exit 0
    }

    # Fetch quietly
    git fetch --quiet 2>$null
    if ($LASTEXITCODE -ne 0) {
        exit 0
    }

    # Check if behind remote
    $local = git rev-parse HEAD 2>$null
    $remoteRef = git rev-parse "@{u}" 2>$null

    if (-not $remoteRef -or $local -eq $remoteRef) {
        # Up to date or no upstream
        exit 0
    }

    # Check for uncommitted changes
    $diffStatus = git diff --quiet 2>$null
    $cachedStatus = git diff --cached --quiet 2>$null

    if ($LASTEXITCODE -ne 0) {
        Write-Host "[claude-config] Updates available but you have uncommitted changes in ~/.claude"
        exit 0
    }

    # Pull updates
    git pull --quiet 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[claude-config] Pulled updates from remote"
    }
}
finally {
    Pop-Location
}

exit 0
