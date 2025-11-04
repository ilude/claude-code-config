# Improved CHECKPOINT System Design

## Overview

This document describes the improved checkpoint system for `/optimize-ruleset` that is **project-aware** and **extensible**.

## Problem Statement

The current CHECKPOINT system (`~/.claude/CHECKPOINT`) is global, which causes:
- Re-analyzing ProjectA history when optimizing ProjectB
- No isolation between projects
- Inefficient incremental learning
- Single timestamp format (not extensible)

## Solution

### Project-Specific Checkpoints

**Project Mode** (`/optimize-ruleset`):
- Checkpoint location: `.claude/CHECKPOINT` (in project directory)
- History filter: Only entries where `project` field matches current directory
- Scope: Tracks analysis for THIS project only

**Personal Mode** (`/optimize-ruleset personal`):
- Checkpoint location: `~/.claude/CHECKPOINT` (in home directory)
- History filter: All entries (any project)
- Scope: Tracks analysis across all projects

### Multi-Line Checkpoint Format

Extensible format supports multiple checkpoint types:

```
optimize-ruleset: 2025-11-04T14:47:09Z
commit-command: 2025-11-03T10:00:00Z
pr-workflow: 2025-11-02T15:30:00Z
```

Each command tracks its own checkpoint independently.

## File Structure

### Before (Current)
```
~/.claude/
└── CHECKPOINT                    # Global, not project-aware
    Content: 2025-11-04T14:47:09Z

<project>/.claude/
└── CLAUDE.md                     # No checkpoint
```

### After (Improved)
```
~/.claude/
├── CHECKPOINT                    # For personal ruleset only
│   Content:
│   optimize-ruleset: 2025-11-04T14:47:09Z
│   commit-command: 2025-11-03T10:00:00Z
└── CLAUDE.md

<project>/.claude/
├── CHECKPOINT                    # For THIS project (NEW!)
│   Content:
│   optimize-ruleset: 2025-11-04T14:47:09Z
└── CLAUDE.md
```

## Benefits

1. **Project Isolation**: Each project tracks its own history analysis
2. **No Redundancy**: Don't re-analyze ProjectA history when working on ProjectB
3. **Accurate Patterns**: Patterns detected are specific to current project context
4. **Extensible**: Format supports multiple checkpoint types for future commands
5. **Clear Scope**: Project checkpoints for project work, personal checkpoint for personal ruleset

## Key Implementation Files

1. **optimize-ruleset.md** - Updated command with project-aware logic
2. **path-normalization.md** - Cross-platform path handling
3. **checkpoint-operations.md** - Read/write checkpoint logic
4. **history-filtering.md** - Project-aware history filtering
5. **examples.md** - Usage scenarios

## Next Steps

See individual documentation files for implementation details:
- [Path Normalization](./path-normalization.md)
- [Checkpoint Operations](./checkpoint-operations.md)
- [History Filtering](./history-filtering.md)
- [Usage Examples](./examples.md)
