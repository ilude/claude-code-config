---
description: Analyze permission patterns and optionally add them to settings.json
---

# Permission Analyzer Command

When this command is run, analyze Claude Code debug logs to find frequently-requested permissions and offer to add them to settings.json.

## Step 1: Run the analyzer

First, run the permission analyzer to extract patterns from debug logs:

```bash
python ~/.claude/scripts/permission-analyzer.py --json ./tmp/analyze-permissions-temp.json --min-count 3
```

## Step 2: Parse and present recommendations

Read the JSON output and identify new permission patterns to suggest. Group them by safety level:
- **SAFE**: Read-only operations with no side effects
- **REVIEW**: Operations that may have side effects

## Step 3: Interactive approval

Present the recommendations to the user with clear categories:

1. Show SAFE patterns (if any) and ask if they should be added
2. Show REVIEW patterns (if any) separately with warnings
3. Allow user to approve all, select individually, or skip

## Step 4: Update settings.json

If the user approves additions:

1. Read current settings.json
2. Add approved patterns to permissions.allow array
3. Remove duplicates
4. Write updated settings.json with proper formatting
5. Confirm changes were saved

## Implementation Instructions

1. Check if the analyzer script exists at `~/.claude/scripts/permission-analyzer.py`
2. Create temp directory `./tmp` if it doesn't exist
3. Run the analyzer with JSON output
4. Parse the JSON to extract suggestions
5. Filter out patterns that are marked as "dangerous" safety level
6. Present recommendations grouped by safety
7. If user approves, update settings.json atomically
8. Clean up temp files
9. Report results to user

## Error Handling

- If analyzer script not found: Inform user to run the setup first
- If no debug logs: Inform user that Claude Code needs to be used to generate logs
- If no new suggestions: Inform user all frequent patterns are already approved
- If settings.json update fails: Show error and rollback

## Example Output

```
🔍 Analyzing permission patterns...

Found 48 debug logs with 127 permission requests.
You have 34 patterns already approved.

📋 NEW PERMISSION SUGGESTIONS:

✅ SAFE patterns (read-only, no side effects):
  • Bash(cat:*) - Used 6 times
  • Bash(git status:*) - Used 5 times

⚠️  REVIEW patterns (may have side effects):
  • Bash(mkdir:*) - Used 3 times
  • Read(//c/Users/mglenn/**) - Used 3 times

Would you like to:
1. Add all SAFE patterns only
2. Add all patterns (SAFE + REVIEW)
3. Select individually
4. Skip (no changes)

Your choice: [Ask user]
```

## Notes

- Never suggest git commit or git push (these require manual approval per CLAUDE.md)
- Path patterns should be reviewed for privacy before adding
- The analyzer respects existing settings and won't suggest duplicates
- Results are based on actual usage patterns from debug logs