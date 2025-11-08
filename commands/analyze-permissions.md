---
description: Analyze permission patterns and optionally add them to settings.json
model: haiku
---

# Permission Analyzer Command

Analyze debug logs for frequently-requested permissions. Filter out existing patterns. Present new suggestions grouped by safety level.

## Execution Workflow

### 1. Run Analyzer

Check script exists:
```bash
test -f ~/.claude/scripts/permission-analyzer.py || exit 1
```

Create temp directory and run:
```bash
mkdir -p ./tmp
python ~/.claude/scripts/permission-analyzer.py --json ./tmp/analyze-permissions-temp.json --min-count 3
```

### 2. Read Current Permissions

Load existing patterns from settings.json:
```bash
settings_path=~/.claude/settings.json
```

Extract current allow list (will use this to filter duplicates).

### 3. Parse Analyzer Results

Read JSON output:
```bash
temp_file=./tmp/analyze-permissions-temp.json
```

Get suggestions array from JSON.

### 4. Filter & Categorize

For each suggestion:
1. Check if pattern already in allow list → skip if yes
2. Check safety level:
   - "safe" → add to safe_patterns list
   - "risky" → add to review_patterns list
   - "dangerous" → skip (never suggest)

Result: Two lists of NEW patterns only (duplicates removed).

### 5. Present Results

Display format:
```
🔍 Analyzing permission patterns...

Found: [X] debug logs with [Y] permission requests
Existing: [Z] patterns already approved
New suggestions: [N]

✅ SAFE patterns (read-only):
  • Pattern - Used X times

⚠️ REVIEW patterns (may have side effects):
  • Pattern - Used X times

Would you like to:
1. Add all SAFE patterns only
2. Add all patterns (SAFE + REVIEW)
3. Select individually
4. Skip (no changes)

Your choice:
```

### 6. Get User Choice

Parse input:
- "1" → patterns_to_add = safe_patterns
- "2" → patterns_to_add = safe_patterns + review_patterns
- "3" → prompt for each pattern individually
- "4" → patterns_to_add = [] (exit)

### 7. Update Settings

If patterns_to_add not empty:

1. Read settings.json
2. Get current permissions.allow array
3. Merge: new_list = current + patterns_to_add
4. Remove duplicates: unique_list = list(set(new_list))
5. Sort alphabetically
6. Update permissions.allow
7. Write settings.json

### 8. Verify & Report

Show summary:
```
✅ Successfully added [N] new permission patterns

Summary:
- Analyzed: [X] debug logs
- Suggested: [Y] new patterns
- Added: [N] patterns

Settings updated at: ~/.claude/settings.json
```

### 9. Cleanup

```bash
rm -f ./tmp/analyze-permissions-temp.json
rmdir ./tmp 2>/dev/null
```

## Safety Categories

**SAFE (auto-approve safe):**
- Read operations
- Bash(ls:*), Bash(pwd:*), Bash(cat:*)
- Bash(git status:*), Bash(git log:*)

**REVIEW (examine carefully):**
- Write operations
- Bash(mkdir:*), Bash(rm:*)
- Broad path patterns (//c/Users/**)

**DANGEROUS (never suggest):**
- Bash(git commit:*), Bash(git push:*)
- Bash(rm -rf:*)
- Write(~/**), Edit(/etc/**)

## Error Handling

Script not found:
```
ERROR: Analyzer script not found
Check: ~/.claude/scripts/permission-analyzer.py
```

No debug logs:
```
No debug logs found
Use Claude Code to generate usage history first
```

No new suggestions:
```
All frequently-used patterns already approved
Your permissions are up to date!
```

JSON parse error:
```
Failed to parse analyzer output
Check ./tmp/analyze-permissions-temp.json
```

Settings update failed:
```
Failed to update settings.json
Check file permissions and JSON validity
```