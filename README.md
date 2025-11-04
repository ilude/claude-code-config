# Claude Code Configuration

Personal Claude Code configuration files for synchronizing settings, custom commands, and rulesets across multiple machines.

## Contents

- **CLAUDE.md** - Personal ruleset with preferences and patterns that apply to all projects
- **commands/** - Custom slash commands for Claude Code
  - `commit.md` - Enhanced git commit workflow
  - `optimize-ruleset.md` - Ruleset optimization and analysis
- **COMMANDS-QUICKSTART.md** - Documentation for using custom commands
- **settings.json** - Claude Code global settings

## Installation

### Initial Setup (New Machine)

1. **Clone this repository:**
   ```bash
   git clone https://github.com/YOUR-USERNAME/claude-code-config.git ~/claude-code-config-temp
   ```

2. **Run the setup script:**
   ```bash
   cd ~/claude-code-config-temp
   ./setup.sh
   ```

   Or manually:
   ```bash
   # Backup existing .claude directory if it exists
   mv ~/.claude ~/.claude.backup.$(date +%Y%m%d-%H%M%S)

   # Copy configuration files
   mkdir -p ~/.claude
   cp -r ~/claude-code-config-temp/* ~/.claude/

   # Clean up
   rm -rf ~/claude-code-config-temp
   ```

3. **Verify installation:**
   ```bash
   ls -la ~/.claude
   ```

### Updating Configuration

To pull the latest changes on any machine:

```bash
cd ~/.claude
git pull origin main
```

### Pushing Changes

After making changes to your configuration:

```bash
cd ~/.claude
git add CLAUDE.md commands/ settings.json COMMANDS-QUICKSTART.md
git commit -m "Update configuration"
git push origin main
```

## File Structure

```
.claude/
├── .gitignore              # Protects sensitive files
├── README.md               # This file
├── CLAUDE.md               # Personal ruleset (global)
├── COMMANDS-QUICKSTART.md  # Command documentation
├── settings.json           # Claude Code settings
└── commands/               # Custom slash commands
    ├── commit.md
    ├── optimize-ruleset.md
    └── README.md
```

### Excluded from Version Control

The following files/directories are automatically excluded via `.gitignore`:

- `.credentials.json` - API credentials (sensitive)
- `history.jsonl` - Session history
- `file-history/` - File version history
- `projects/` - Project-specific session data
- `todos/` - Session todos
- `debug/` - Debug logs
- `shell-snapshots/` - Temporary shell snapshots
- `statsig/` - Analytics data
- `ide/` - IDE state files

## Usage

### Personal Ruleset

The `CLAUDE.md` file contains your personal preferences that apply to ALL Claude Code sessions. It includes:

- Communication style preferences
- Code quality standards
- Tool usage patterns
- Python project conventions
- Git workflow preferences
- Todo list management guidelines

**Important:** This personal ruleset is overridden by project-specific rulesets (`.claude/CLAUDE.md` in project directories).

### Custom Commands

Available custom slash commands:

- `/commit [push]` - Create logical git commits with optional push
- `/optimize-ruleset` - Analyze and optimize CLAUDE.md ruleset files

See `COMMANDS-QUICKSTART.md` for detailed usage instructions.

## Best Practices

### Before Committing Changes

1. **Review your changes:**
   ```bash
   cd ~/.claude
   git status
   git diff
   ```

2. **Ensure no sensitive data:**
   - Check that `.credentials.json` is not staged
   - Verify no API keys or secrets are in committed files

3. **Test on current machine:**
   - Restart Claude Code session
   - Verify ruleset is applied correctly
   - Test custom commands

### Syncing Across Machines

1. **Machine A (make changes):**
   ```bash
   cd ~/.claude
   git add -A
   git commit -m "Update ruleset: description of changes"
   git push
   ```

2. **Machine B (pull changes):**
   ```bash
   cd ~/.claude
   git pull
   ```

3. **Verify sync:**
   - Check that files match
   - Restart Claude Code if needed

## Troubleshooting

### Git says directory is not a repository

```bash
cd ~/.claude
git init
git remote add origin https://github.com/YOUR-USERNAME/claude-code-config.git
git fetch
git checkout main
```

### Changes not being applied

- Restart Claude Code session
- Check file permissions: `ls -la ~/.claude`
- Verify file contents match repository

### Accidentally committed sensitive data

1. **Remove from history:**
   ```bash
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch .credentials.json" \
     --prune-empty --tag-name-filter cat -- --all
   ```

2. **Force push (CAUTION):**
   ```bash
   git push origin --force --all
   ```

3. **Rotate compromised credentials immediately**

## Contributing

This is a personal configuration repository. If you're setting up your own:

1. Fork or create your own repository
2. Update `YOUR-USERNAME` in this README
3. Customize `CLAUDE.md` with your preferences
4. Add your own custom commands

## Security Notes

- **NEVER commit** `.credentials.json` or any files with API keys
- The `.gitignore` is configured to prevent common sensitive files
- Review all changes before pushing
- Use private repository if it contains any identifying information

## License

Personal configuration - use as you see fit for your own Claude Code setup.

## Related Resources

- [Claude Code Documentation](https://docs.claude.com/claude-code)
- [Writing Custom Commands](https://docs.claude.com/claude-code/custom-commands)
- [CLAUDE.md Ruleset Guide](https://docs.claude.com/claude-code/rulesets)
