---
description: Analyze permission patterns and optionally add them to settings.json
model: haiku
---

# Permission Analyzer Command

Analyze debug logs for frequently-requested permissions. Filter out existing patterns. Present new suggestions grouped by safety level.

## Execution Workflow

### 1. Run Analyzer
Verify script exists and execute with temp directory: `python ~/.claude/scripts/permission-analyzer.py --json ./tmp/analyze-permissions-temp.json --min-count 3`

### 2. Read & Filter
Load current allow list from `~/.claude/settings.json` to identify existing patterns.

### 3. Parse & Categorize
Extract suggestions from JSON output. For each: skip if already allowed; categorize by safety level (safe/review/dangerous).

### 4. Present Results
Display new patterns grouped by safety with usage counts. Show 4 options: add safe only, add all, select individually, or skip.

### 5. Handle User Choice
Map input 1-4 to corresponding action (1=safe, 2=all, 3=individual, 4=skip).

### 6. Update Settings
Read settings.json → merge patterns → deduplicate → sort → write back to permissions.allow.

### 7. Report & Cleanup
Display summary of added patterns. Remove temp file.

## Safety Categories

| Category | Examples |
|----------|----------|
| **SAFE** | Read ops: Bash(ls:*), Bash(pwd:*), Bash(cat:*), Bash(git status:*) |
| **REVIEW** | Write ops: Bash(mkdir:*), Bash(rm:*), broad patterns (//c/Users/**) |
| **DANGEROUS** | Bash(git commit:*), Bash(push:*), Bash(rm -rf:*), Write(~/**) |

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Script not found | Analyzer missing | Verify ~/.claude/scripts/permission-analyzer.py exists |
| No debug logs | No usage history | Run Claude Code to generate debug logs |
| No new suggestions | All patterns approved | Permissions already up to date |
| JSON parse error | Corrupted output | Check ./tmp/analyze-permissions-temp.json |
| Settings update failed | File/JSON issue | Verify permissions and JSON validity in settings.json |