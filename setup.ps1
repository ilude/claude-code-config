# PowerShell setup script for installing Claude Code configuration on Windows

param(
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ClaudeDir = Join-Path $env:USERPROFILE ".claude"

Write-Host "Claude Code Configuration Setup" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if .claude directory exists
if (Test-Path $ClaudeDir) {
    $BackupDir = "$ClaudeDir.backup.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    Write-Host "⚠️  Existing .claude directory found" -ForegroundColor Yellow

    if (-not $Force) {
        $response = Read-Host "Create backup at $BackupDir? (y/n)"
        if ($response -ne 'y' -and $response -ne 'Y') {
            Write-Host "Setup cancelled." -ForegroundColor Red
            exit 1
        }
    }

    Write-Host "Creating backup..."
    Move-Item -Path $ClaudeDir -Destination $BackupDir
    Write-Host "✓ Backup created at: $BackupDir" -ForegroundColor Green
}

# Create .claude directory
Write-Host "Creating $ClaudeDir..."
New-Item -ItemType Directory -Path $ClaudeDir -Force | Out-Null

# Copy configuration files
Write-Host "Copying configuration files..."
$filesToCopy = @(
    "CLAUDE.md",
    "settings.json",
    "COMMANDS-QUICKSTART.md",
    ".gitignore",
    "README.md"
)

foreach ($file in $filesToCopy) {
    $sourcePath = Join-Path $ScriptDir $file
    if (Test-Path $sourcePath) {
        Copy-Item -Path $sourcePath -Destination $ClaudeDir -Verbose
    } else {
        Write-Host "⚠️  File not found: $file" -ForegroundColor Yellow
    }
}

# Copy commands directory
$commandsSource = Join-Path $ScriptDir "commands"
if (Test-Path $commandsSource) {
    Write-Host "Copying commands directory..."
    Copy-Item -Path $commandsSource -Destination $ClaudeDir -Recurse -Verbose
}

# Initialize git repository
Write-Host ""
Write-Host "Initializing git repository..."
Push-Location $ClaudeDir

try {
    if (Test-Path ".git") {
        Write-Host "Git repository already exists"
    } else {
        git init

        # Prompt for remote URL
        Write-Host ""
        $repoUrl = Read-Host "Enter your GitHub repository URL (or press Enter to skip)"

        if ($repoUrl) {
            git remote add origin $repoUrl
            Write-Host "✓ Remote 'origin' added" -ForegroundColor Green
        }
    }
} finally {
    Pop-Location
}

Write-Host ""
Write-Host "✓ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Review your configuration: cd ~/.claude"
Write-Host "  2. If you added a remote, push your changes:"
Write-Host "     cd ~/.claude"
Write-Host "     git add -A"
Write-Host "     git commit -m 'Initial commit'"
Write-Host "     git push -u origin main"
Write-Host "  3. Restart Claude Code to apply settings"
Write-Host ""
