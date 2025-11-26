#!/bin/bash
# ensure-mcp-config.sh
# SessionStart hook to ensure browsermcp and flaresolverr MCP configs exist
# Config-only - does NOT install dependencies

set -e

# Determine home directory (cross-platform: Linux/Mac/Windows Git Bash)
USER_HOME="${HOME:-$USERPROFILE}"
CLAUDE_JSON="$USER_HOME/.claude.json"

# Exit early if file doesn't exist (Claude Code hasn't been set up yet)
[[ -f "$CLAUDE_JSON" ]] || exit 0

# Function to check if both MCP servers are configured
check_config() {
  if command -v jq &>/dev/null; then
    jq -e '.mcpServers.browsermcp and .mcpServers.flaresolverr' "$CLAUDE_JSON" &>/dev/null
  else
    python -c "
import json
import sys
try:
    with open('$CLAUDE_JSON', 'r') as f:
        d = json.load(f)
    servers = d.get('mcpServers', {})
    if 'browsermcp' in servers and 'flaresolverr' in servers:
        sys.exit(0)
    sys.exit(1)
except:
    sys.exit(1)
"
  fi
}

# Quick exit if already configured
check_config && exit 0

# Build flaresolverr path based on OS
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
  # Windows Git Bash: Convert to Windows path format for jq --arg
  WIN_HOME=$(cygpath -w "$USER_HOME" 2>/dev/null || echo "$USERPROFILE")
  # Use forward slashes then convert - cleaner for jq
  FLARESOLVERR_PATH="${WIN_HOME}/.claude/tools/flaresolverr-mcp/server.py"
  # Convert to backslashes for Windows
  FLARESOLVERR_PATH=$(echo "$FLARESOLVERR_PATH" | sed 's|/|\\|g')
elif [[ -n "$USERPROFILE" ]]; then
  # Windows without cygpath - build with backslashes
  FLARESOLVERR_PATH="${USERPROFILE}\\.claude\\tools\\flaresolverr-mcp\\server.py"
else
  # Unix: Simple forward slashes
  FLARESOLVERR_PATH="$USER_HOME/.claude/tools/flaresolverr-mcp/server.py"
fi

# Add missing configs
add_mcp_configs() {
  if command -v jq &>/dev/null; then
    # Use jq to add configs
    local tmp_file=$(mktemp)

    # Check and add browsermcp if missing
    if ! jq -e '.mcpServers.browsermcp' "$CLAUDE_JSON" &>/dev/null; then
      jq '.mcpServers.browsermcp = {"command": "npx", "args": ["@browsermcp/mcp@latest"]}' "$CLAUDE_JSON" > "$tmp_file"
      mv "$tmp_file" "$CLAUDE_JSON"
    fi

    # Check and add flaresolverr if missing
    if ! jq -e '.mcpServers.flaresolverr' "$CLAUDE_JSON" &>/dev/null; then
      jq --arg path "$FLARESOLVERR_PATH" '.mcpServers.flaresolverr = {"command": "python", "args": [$path]}' "$CLAUDE_JSON" > "$tmp_file"
      mv "$tmp_file" "$CLAUDE_JSON"
    fi
  else
    # Fallback to Python - uses os.path for cross-platform path handling
    python -c "
import json
import os

# Get paths dynamically in Python for proper cross-platform handling
home = os.path.expanduser('~')
claude_json = os.path.join(home, '.claude.json')
flaresolverr_path = os.path.join(home, '.claude', 'tools', 'flaresolverr-mcp', 'server.py')

with open(claude_json, 'r') as f:
    data = json.load(f)

if 'mcpServers' not in data:
    data['mcpServers'] = {}

changed = False

if 'browsermcp' not in data['mcpServers']:
    data['mcpServers']['browsermcp'] = {
        'command': 'npx',
        'args': ['@browsermcp/mcp@latest']
    }
    changed = True

if 'flaresolverr' not in data['mcpServers']:
    data['mcpServers']['flaresolverr'] = {
        'command': 'python',
        'args': [flaresolverr_path]
    }
    changed = True

if changed:
    with open(claude_json, 'w') as f:
        json.dump(data, f, indent=2)
"
  fi
}

add_mcp_configs
exit 0
