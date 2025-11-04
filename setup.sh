#!/bin/bash
# Setup script for installing Claude Code configuration

set -e  # Exit on error

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CLAUDE_DIR="$HOME/.claude"

echo "Claude Code Configuration Setup"
echo "================================"
echo ""

# Check if .claude directory exists
if [ -d "$CLAUDE_DIR" ]; then
    BACKUP_DIR="${CLAUDE_DIR}.backup.$(date +%Y%m%d-%H%M%S)"
    echo "⚠️  Existing .claude directory found"
    read -p "Create backup at $BACKUP_DIR? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Creating backup..."
        mv "$CLAUDE_DIR" "$BACKUP_DIR"
        echo "✓ Backup created at: $BACKUP_DIR"
    else
        echo "Setup cancelled."
        exit 1
    fi
fi

# Create .claude directory
echo "Creating $CLAUDE_DIR..."
mkdir -p "$CLAUDE_DIR"

# Copy configuration files
echo "Copying configuration files..."
cp -v "$SCRIPT_DIR/CLAUDE.md" "$CLAUDE_DIR/"
cp -v "$SCRIPT_DIR/settings.json" "$CLAUDE_DIR/"
cp -v "$SCRIPT_DIR/COMMANDS-QUICKSTART.md" "$CLAUDE_DIR/"
cp -v "$SCRIPT_DIR/.gitignore" "$CLAUDE_DIR/"
cp -v "$SCRIPT_DIR/README.md" "$CLAUDE_DIR/"

# Copy commands directory
if [ -d "$SCRIPT_DIR/commands" ]; then
    echo "Copying commands directory..."
    cp -rv "$SCRIPT_DIR/commands" "$CLAUDE_DIR/"
fi

# Initialize git repository
echo ""
echo "Initializing git repository..."
cd "$CLAUDE_DIR"

if [ -d ".git" ]; then
    echo "Git repository already exists"
else
    git init

    # Prompt for remote URL
    echo ""
    read -p "Enter your GitHub repository URL (or press Enter to skip): " REPO_URL

    if [ -n "$REPO_URL" ]; then
        git remote add origin "$REPO_URL"
        echo "✓ Remote 'origin' added"
    fi
fi

echo ""
echo "✓ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Review your configuration: cd ~/.claude"
echo "  2. If you added a remote, push your changes: cd ~/.claude && git add -A && git commit -m 'Initial commit' && git push -u origin main"
echo "  3. Restart Claude Code to apply settings"
echo ""
