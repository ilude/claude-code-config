---
description: Toggle session context commits for current project
argument-hint: enable|disable
model: haiku
---

# Commit Session Command

Manage session context commit configuration for the current project.

## Execution Workflow

### 0. Verify Git Repository

Check if running in a git repository:
```bash
git rev-parse --git-dir 2>/dev/null
```

If fails: ERROR - "Not in a git repository. Run this command from within a git project."

Get git root:
```bash
git rev-parse --show-toplevel
```

All paths relative to this git root.

---

## Argument Handling

### No Arguments: Show Status

Check two conditions:

**1. Check `.claude/CLAUDE.md` for config:**
```bash
[ -f .claude/CLAUDE.md ] && grep -q "enable-session-commits: true" .claude/CLAUDE.md && echo "ENABLED" || echo "DISABLED"
```

**2. Check `.gitignore` for exclusion:**
```bash
[ -f .gitignore ] && grep -q "^\.session/" .gitignore && echo "EXCLUDED" || echo "INCLUDED"
```

**Display Status:**

If ENABLED and INCLUDED:
```
Session Commits: ENABLED
  ✓ enable-session-commits: true in .claude/CLAUDE.md
  ✓ .session/ not in .gitignore
```

If DISABLED and EXCLUDED:
```
Session Commits: DISABLED
  ✗ enable-session-commits not found in .claude/CLAUDE.md
  ✓ .session/ in .gitignore
```

If mismatched state:
```
Session Commits: INCONSISTENT
  [show actual states]

Run '/commit-session enable' or '/commit-session disable' to fix.
```

---

### Argument: `enable`

**Step 1: Create `.claude/` directory**
```bash
mkdir -p .claude
```

**Step 2: Update `.claude/CLAUDE.md`**

If file doesn't exist, create with:
```markdown
## Session Context Management
enable-session-commits: true
```

If file exists:
- Check if section "Session Context Management" exists
- If section exists, add/update `enable-session-commits: true` under it
- If section doesn't exist, append:
  ```markdown

  ## Session Context Management
  enable-session-commits: true
  ```

**Step 3: Update `.gitignore`**

Remove all lines matching `.session/` (with or without wildcards):
```bash
sed -i '/^\.session\//d' .gitignore
```

If `.gitignore` doesn't exist, create empty file (nothing to remove).

**Step 4: Show Success**
```
✓ Session commits ENABLED
  - Added enable-session-commits: true to .claude/CLAUDE.md
  - Removed .session/ from .gitignore

.session/ files will be included in commits when using /commit
```

---

### Argument: `disable`

**Step 1: Update `.claude/CLAUDE.md`**

If file exists:
- Remove line containing `enable-session-commits: true`
- If "Session Context Management" section becomes empty, can optionally remove section header

If file doesn't exist, skip (already disabled).

**Step 2: Update `.gitignore`**

Add `.session/` if not present:
```bash
grep -q "^\.session/" .gitignore 2>/dev/null || echo ".session/" >> .gitignore
```

If `.gitignore` doesn't exist, create with:
```
.session/
```

**Step 3: Show Success**
```
✓ Session commits DISABLED
  - Removed enable-session-commits from .claude/CLAUDE.md
  - Added .session/ to .gitignore

.session/ files will be excluded from commits (default behavior)
```

---

## Error Handling

**Invalid argument:**
```
Error: Invalid argument '[arg]'

Usage: /commit-session [enable|disable]
  No argument: Show current status
  enable:      Enable session commits for this project
  disable:     Disable session commits (default behavior)
```

**Not in git repo:**
```
Error: Not in a git repository

This command must be run from within a git project directory.
```

---

## Implementation Notes

- All operations are idempotent (safe to run multiple times)
- Preserve existing content in `.claude/CLAUDE.md` and `.gitignore`
- Handle Windows/Unix line endings gracefully
- Clear success messages show what changed
- Status display helps debug misconfigurations
