---
description: Toggle session context commits for current project
argument-hint: enable|disable
model: haiku
---

# Snapshot Tracking Command

Manage session context commit configuration for the current project.

## Execution Workflow

### No Arguments: Show Status

**Run status check:**
```bash
grep -q enable-session-commits .claude/CLAUDE.md 2>/dev/null&&M=1||M=0;grep -q "^\.session/" .gitignore 2>/dev/null&&G=1||G=0;echo "$M:$G"
```

**Parse output** (format: `M:G` where M=marker exists, G=gitignored):

- `1:0` = **ENABLED** (marker exists, NOT gitignored)
  ```
  Session Commits: ENABLED
    ✓ enable-session-commits: true in .claude/CLAUDE.md
    ✓ .session/ not in .gitignore
  ```

- `0:1` = **DISABLED** (no marker, gitignored)
  ```
  Session Commits: DISABLED
    ✗ enable-session-commits not found in .claude/CLAUDE.md
    ✓ .session/ in .gitignore
  ```

- `1:1` or `0:0` = **INCONSISTENT**
  ```
  Session Commits: INCONSISTENT
    [show actual states based on M and G values]

  Run '/snapshot-tracking enable' or '/snapshot-tracking disable' to fix.
  ```

---

### Argument: `enable`

**Single command:**
```bash
mkdir -p .claude;grep -q enable-session-commits .claude/CLAUDE.md 2>/dev/null||printf '\n## Session Context Management\nenable-session-commits: true\n'>>.claude/CLAUDE.md;grep -v "^\.session/" .gitignore 2>/dev/null>.gitignore.tmp&&mv .gitignore.tmp .gitignore||true;echo ✓
```

**What it does:**
1. Creates `.claude/` directory if missing
2. Adds `enable-session-commits: true` to `.claude/CLAUDE.md` (idempotent - only if not already present)
3. Removes `.session/` from `.gitignore` (creates clean .gitignore without that line)
4. Prints `✓` on success

**Display after execution:**
```
✓ Session commits ENABLED
  - Added enable-session-commits: true to .claude/CLAUDE.md
  - Removed .session/ from .gitignore

.session/ files will be included in commits when using /commit
```

---

### Argument: `disable`

**Single command:**
```bash
mkdir -p .claude;grep -v -e enable-session-commits -e "^## Session Context Management$" .claude/CLAUDE.md 2>/dev/null>.claude/CLAUDE.md.tmp&&mv .claude/CLAUDE.md.tmp .claude/CLAUDE.md||true;grep -q "^\.session/" .gitignore 2>/dev/null||echo ".session/">>.gitignore;echo ✓
```

**What it does:**
1. Creates `.claude/` directory if missing
2. Removes `enable-session-commits` line and section header from `.claude/CLAUDE.md`
3. Adds `.session/` to `.gitignore` (idempotent - only if not already present)
4. Prints `✓` on success

**Display after execution:**
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

Usage: /snapshot-tracking [enable|disable]
  No argument: Show current status
  enable:      Enable session commits for this project
  disable:     Disable session commits (default behavior)
```

---

## Implementation Notes

- **Simplified design**: Uses relative paths (no git root finding)
- **Idempotent**: All operations safe to run multiple times
- **Portable**: Uses `grep -v` + temp files instead of `sed -i`
- **Atomic writes**: Uses `mv` for safe file updates
- **Status output**: Parseable `M:G` format (marker:gitignored)
- **Pre-approved commands**: `mv` and `printf` whitelisted in settings.json
