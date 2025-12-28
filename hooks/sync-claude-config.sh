#!/bin/bash
# Sync ~/.claude config from git remote on session start
# Runs silently - only outputs if updates are pulled

CLAUDE_DIR="$HOME/.claude"

# Exit silently if not a git repo
if [ ! -d "$CLAUDE_DIR/.git" ]; then
    exit 0
fi

cd "$CLAUDE_DIR" || exit 0

# Check if remote exists
if ! git remote get-url origin &>/dev/null; then
    exit 0
fi

# Fetch quietly
if ! git fetch --quiet 2>/dev/null; then
    exit 0
fi

# Check if behind remote
LOCAL=$(git rev-parse HEAD 2>/dev/null)
REMOTE=$(git rev-parse @{u} 2>/dev/null)

if [ -z "$REMOTE" ] || [ "$LOCAL" = "$REMOTE" ]; then
    # Up to date or no upstream
    exit 0
fi

# Check for uncommitted changes that would block pull
if ! git diff --quiet 2>/dev/null || ! git diff --cached --quiet 2>/dev/null; then
    echo "[claude-config] Updates available but you have uncommitted changes in ~/.claude"
    exit 0
fi

# Pull updates
if git pull --quiet 2>/dev/null; then
    BEHIND=$(git rev-list --count HEAD.."$REMOTE" 2>/dev/null || echo "some")
    echo "[claude-config] Pulled updates from remote"
fi

exit 0
