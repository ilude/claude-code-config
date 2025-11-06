# Permission Analyzer for Claude Code

A Python utility that analyzes Claude Code debug logs to identify permission request patterns and suggest wildcard rules for `settings.json`.

## Purpose

When using Claude Code, you may be frequently prompted to approve bash commands and file access. This analyzer:

1. **Identifies patterns** - Finds which commands are triggered most often
2. **Suggests wildcards** - Recommends patterns like `Bash(git:*)` instead of approving each git command
3. **Classifies safety** - Distinguishes between safe read-only commands and risky operations
4. **Avoids duplicates** - Only suggests patterns not already in your settings.json

## Usage

```bash
# Basic analysis - shows statistics and suggestions
python ~/.claude/scripts/permission-analyzer.py

# Export results to JSON for automation
python ~/.claude/scripts/permission-analyzer.py --json results.json

# Lower the threshold for suggestions (default: 3)
python ~/.claude/scripts/permission-analyzer.py --min-count 2

# Analyze a different Claude directory
python ~/.claude/scripts/permission-analyzer.py --claude-dir /path/to/.claude
```

## Output

The analyzer provides three types of output:

### 1. Statistics
Shows usage counts by tool and command:
```
Bash:
  Total requests: 109
  Unique commands: 79
  Top commands:
    cat                                        6x
    git add                                    4x
    mkdir                                      2x
```

### 2. Wildcard Suggestions
Recommends patterns based on frequency:
```
[SAFE] patterns (read-only, no side effects):
      "Bash(cat:*)",  // Used 6 times

[REVIEW NEEDED] patterns (may have side effects):
      "Bash(timeout 180 uv run:*)",  // Used 4 times - REVIEW
```

### 3. JSON Export
Machine-readable format for automation and tracking.

## Safety Classification

The analyzer classifies commands into three categories:

### Safe (Green Zone)
Read-only operations with no side effects:
- `ls`, `pwd`, `echo`, `whoami`, `date`, `which`
- `cat`, `head`, `tail`, `grep`, `find`
- `git status`, `git diff`, `git log`, `git branch`
- `docker ps`, `docker images`, `docker inspect`

### Risky (Yellow Zone)
Commands that modify state but are usually safe:
- `mkdir`, `chmod`
- `git checkout` (can modify files)
- `docker pull` (network operation)
- `npm install`, `pip install` (with patterns)

### Dangerous (Red Zone)
Never auto-approved by the analyzer:
- `git commit`, `git push` (require manual approval per CLAUDE.md)
- `rm`, `rmdir` (file deletion)
- `sudo` (system changes)
- `git reset --hard`, `git push --force` (destructive)

## Integration with settings.json

After reviewing the suggestions, add desired patterns to `~/.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(cat:*)",
      "Bash(docker:*)",
      "Bash(git log:*)",
      "WebFetch(domain:code.claude.com)"
    ]
  }
}
```

## Command-Line Options

- `--claude-dir PATH` - Specify Claude directory (default: `~/.claude`)
- `--json FILE` - Export results to JSON file
- `--min-count N` - Minimum usage count for suggestions (default: 3)
- `--help` - Show help message

## How It Works

1. **Scans debug logs** - Reads all `*.txt` files in `~/.claude/debug/`
2. **Extracts patterns** - Finds `[DEBUG] Permission suggestions for <Tool>:` entries
3. **Counts usage** - Groups by tool and command pattern
4. **Filters existing** - Removes patterns already in settings.json
5. **Classifies safety** - Marks patterns as safe, risky, or dangerous
6. **Suggests wildcards** - Recommends patterns exceeding threshold

## Files

- `permission-analyzer.py` - Main script
- `permission-analyzer-README.md` - This documentation
- `~/.claude/debug/*.txt` - Debug logs analyzed
- `~/.claude/settings.json` - Current permissions checked

## Requirements

- Python 3.6+ (uses pathlib and f-strings)
- No external dependencies (uses Python standard library only)

## Examples

### Analyze recent activity
```bash
python ~/.claude/scripts/permission-analyzer.py
```

### Generate report for team sharing
```bash
python ~/.claude/scripts/permission-analyzer.py --json ./tmp/team-permissions.json
```

### Check what needs frequent approval
```bash
python ~/.claude/scripts/permission-analyzer.py --min-count 5
```

## Notes

- **Encoding**: Windows users may see encoding warnings - the script handles this gracefully
- **Privacy**: Directory paths in Read patterns may contain usernames - review before sharing
- **Updates**: Run periodically as your usage patterns evolve
- **Cross-machine**: Can analyze debug logs from other machines if copied to local debug directory

## Author

Created for Claude Code users to reduce repetitive permission prompts while maintaining security.

## Version

1.0.0 - Initial release (November 2024)