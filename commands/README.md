# Personal Claude Code Commands

This directory contains custom slash commands available across all your projects.

## Available Commands

### `/analyze-permissions`

**Purpose**: Analyze permission patterns from debug logs and optionally add them to settings.json.

**Location**: `~/.claude/commands/analyze-permissions.md`

**What it does**:
1. **Pattern Analysis**: Scans debug logs to find frequently-requested permissions
2. **Safety Classification**: Groups patterns as SAFE or REVIEW NEEDED
3. **Interactive Approval**: Lets you choose which patterns to add
4. **Settings Update**: Automatically updates settings.json with approved patterns

**Usage**:
```bash
/analyze-permissions
```

**Example Output**:
```
🔍 Analyzing permission patterns...

Found 48 debug logs with 127 permission requests.

📋 NEW PERMISSION SUGGESTIONS:

✅ SAFE patterns (read-only):
  • Bash(cat:*) - Used 6 times
  • Bash(git status:*) - Used 5 times

⚠️  REVIEW patterns:
  • Bash(mkdir:*) - Used 3 times

Add all SAFE patterns? (y/n)
```

**When to Use**:
- After using Claude Code for a while with new tools/commands
- When tired of approving the same commands repeatedly
- Periodically (weekly/monthly) to optimize your workflow

---

### `/optimize-ruleset [personal]`

**Purpose**: Analyze and optimize CLAUDE.md ruleset files with meta-learning from chat history.

**Location**: `~/.claude/commands/optimize-ruleset.md`

**What it does**:
1. **Meta-Learning**: Analyzes your chat history to detect patterns and issues
2. **Ruleset Analysis**: Examines the target CLAUDE.md for problems
3. **Smart Recommendations**: Combines history insights with ruleset issues
4. **Incremental Learning**: Uses CHECKPOINT system to only analyze new history

**Usage**:

```bash
# Optimize the project ruleset (current project's .claude/CLAUDE.md)
/optimize-ruleset

# Optimize your personal ruleset (~/.claude/CLAUDE.md)
/optimize-ruleset personal

# Skip history analysis (just analyze ruleset)
/optimize-ruleset --no-history

# Only analyze history and suggest rules (don't modify ruleset)
/optimize-ruleset --history-only
```

**First Run**:
- Analyzes entire chat history (~/.claude/history.jsonl)
- Creates CHECKPOINT file with current timestamp
- Provides comprehensive optimization report
- Suggests rules learned from your past sessions

**Subsequent Runs**:
- Only analyzes NEW history since last checkpoint
- Updates CHECKPOINT with new timestamp
- Incrementally improves based on recent patterns
- Builds on previous learnings

**Example Output**:

```markdown
# Ruleset Optimization Analysis

**Target**: .claude/CLAUDE.md
**History Analyzed**: 156 new entries since 2025-11-03
**Checkpoint Updated**: 2025-11-04T14:47:09Z

## Part 1: Meta-Learning from History

### Pattern: Manual .venv Path Usage (HIGH Priority)
- **Frequency**: 3 occurrences across 2 sessions
- **Issue**: Used explicit paths instead of `uv run python`
- **Suggested Rule**: "Always use `uv run python` in uv projects"

## Part 2: Current Ruleset Analysis

### HIGH Priority Issues
1. **Outdated Project Description**
   - **Problem**: Says "CLI application" but it's a "learning spike"
   - **Fix**: Rewrite overview to accurately describe project

## Part 3: Unified Recommendations

1. Rewrite project overview (from ruleset analysis)
2. Add rule about `uv run python` (from history)
3. Fix .venv documentation (from both!)
4. Add Quick Start section
...
```

**Key Features**:

1. **Self-Improving**: Learns from your actual experience
2. **Incremental**: Uses CHECKPOINT to avoid re-analyzing same history
3. **Educational**: Explains WHY each recommendation helps
4. **Prioritized**: HIGH/MEDIUM/LOW priorities with rationale
5. **Context-Aware**: Understands project type and structure
6. **Flexible**: Multiple modes (analyze-only, apply fixes, show draft)

**Files Involved**:

```
~/.claude/
├── CLAUDE.md                      # Your personal ruleset
├── CHECKPOINT                     # Last history analysis timestamp
├── history.jsonl                  # Your chat history
└── commands/
    ├── optimize-ruleset.md        # This command
    └── README.md                  # This file

<project>/.claude/
└── CLAUDE.md                      # Project-specific ruleset
```

**CHECKPOINT Format**:

```
2025-11-04T14:47:09Z
```

ISO 8601 UTC timestamp. Updated after each history analysis.

**When to Use**:

- ✅ **After completing a project** - Capture learnings
- ✅ **When starting a new project** - Optimize project ruleset
- ✅ **Periodically** (weekly/monthly) - Keep personal ruleset updated
- ✅ **After frustrating sessions** - Turn pain points into rules
- ✅ **When onboarding to existing project** - Ensure ruleset is accurate

**Benefits**:

1. **Fewer repeated mistakes** - Patterns become rules
2. **Better onboarding** - New Claude sessions have better context
3. **Accurate documentation** - Ruleset matches reality
4. **Continuous improvement** - Each session makes the next one better
5. **Knowledge retention** - Lessons persist across sessions

---

## How to Create New Commands

1. Create a markdown file in `~/.claude/commands/`
2. Add frontmatter with description:
   ```markdown
   ---
   description: Brief description of what this command does
   ---
   ```
3. Write instructions for Claude
4. Commands become available as `/command-name`

Example:
```markdown
---
description: Commit changes with conventional commit format
---

# Commit Command

When this command is run:
1. Check git status
2. Generate commit message following conventional commits
3. Ask user for confirmation
4. Commit with attribution
```

---

## Best Practices

- **Keep commands focused** - One clear purpose per command
- **Be explicit** - Guide Claude step-by-step
- **Include examples** - Show what good looks like
- **Handle edge cases** - What if files don't exist?
- **Be educational** - Explain WHY, not just WHAT

---

## Future Command Ideas

- `/commit [push]` - Smart commit with conventional commits (✅ Implemented)
- `/review` - Code review checklist
- `/test` - Run tests with smart reporting
- `/doc` - Generate/update documentation
- `/refactor` - Suggest refactorings
- `/migrate` - Help with migrations/upgrades

---

**Created**: 2025-11-04
**Updated**: 2025-11-06 (Added /analyze-permissions command)
