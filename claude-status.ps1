# Read JSON input from stdin
$stdinInput = @($input) -join "`n"

# Extract values from JSON
$jsonData = $null

if ($stdinInput) {
    try {
        $jsonData = $stdinInput | ConvertFrom-Json
        $model = $jsonData.model.display_name
        $cwd = $jsonData.workspace.current_dir
    } catch {
        # If JSON parsing fails, use defaults
        $model = "input-error"
    }
}
else {
    $model = "no-input"
}

# Find git repository root by searching up the directory tree
$currentPath = Get-Location
$searchPath = $currentPath.Path
$gitRepoPath = $null

while ($searchPath) {
    $gitPath = Join-Path $searchPath ".git"
    if (Test-Path $gitPath) {
        $gitRepoPath = $searchPath
        break
    }
    $parent = Split-Path $searchPath -Parent
    if ($parent -eq $searchPath) {
        break
    }
    $searchPath = $parent
}

# Get directory name to display
$homePath = $env:USERPROFILE

if ($gitRepoPath) {
    # Display basename of directory containing .git
    $basename = Split-Path $gitRepoPath -Leaf
    
    # Check if git repo is in home directory and preface with ~/
    if ($gitRepoPath.StartsWith($homePath, [StringComparison]::OrdinalIgnoreCase)) {
        $dir = "~/$basename"
    } else {
        $dir = $basename
    }
} else {
    # No git repo found, use current directory with ~/ prefix if in home directory
    if ($currentPath.Path.StartsWith($homePath, [StringComparison]::OrdinalIgnoreCase)) {
        $relativePath = $currentPath.Path.Substring($homePath.Length)
        if ($relativePath) {
            $dir = "~" + $relativePath.Replace('\', '/')
        } else {
            $dir = "~"
        }
    } else {
        $dir = $currentPath.Path.Replace('\', '/')
    }
}

$branch = ""

try {
    $branchName = git branch --show-current 2>$null
    if ($branchName) {
        # ANSI color codes: Yellow for brackets, Blue for branch name
        $branch = "`e[33m[`e[34m${branchName}`e[33m]`e[0m"
    }
} catch {
    $branch = ""
}

# ANSI color codes: Green for directory, Orange for model, Reset at end
# Format: green_dir yellow[blue_branch yellow] | orange_model
if ($branch) {
    Write-Output "`e[32m${dir}`e[0m${branch} | `e[38;5;208m${model}`e[0m"
} else {
    Write-Output "`e[32m${dir}`e[0m `e[38;5;208m${model}`e[0m"
}