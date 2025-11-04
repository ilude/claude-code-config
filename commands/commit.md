---
description: Create logical git commits with optional push
argument-hint: [push]
---

Automated commit workflow that implements the `git-workflow` skill principles.

## Prerequisites

**This command implements the workflow defined in the `git-workflow` skill.**

All workflow principles are defined in the skill:
- Security scanning patterns and requirements
- Commit organization types (docs, test, feat, fix, etc.)
- Commit message format with HEREDOC
- Verification requirements
- Push behavior rules
- Safety rules for hooks and amending

The skill serves as the source of truth. This command provides procedural automation.

## Execution Flow

### 1. Security Scan (CRITICAL FIRST STEP)

**Follow git-workflow skill security requirements:**
- Scan ALL uncommitted changes for sensitive data
- Use security patterns defined in git-workflow skill
- If issues found: STOP, show details, suggest fixes, exit
- Only proceed if no security issues detected

### 2. Analyze Changes

**Run in parallel (per git-workflow skill):**
- `git status` - All uncommitted changes
- `git diff` - What changed
- `git log` - Repository commit message style

### 3. Group Changes Logically

**Group by commit types defined in git-workflow skill:**
- Single commit if all changes closely related
- Multiple commits when changes serve different purposes
- Use commit types from git-workflow skill (docs, test, feat, fix, refactor, chore, build, deps)

### 4. Create Commits

**For each logical group:**
1. Stage relevant files
2. Create commit using git-workflow skill message format (HEREDOC)
3. Follow git-workflow skill commit message guidelines
4. Apply git-workflow skill safety rules (hooks, amending)

### 5. Verify Complete

**Follow git-workflow skill verification requirements:**
- Run `git status` to verify NO uncommitted changes remain
- Show summary of commits created
- Create additional commits for any remaining files (if no security issues)

### 6. Push (Argument-Dependent)

**CRITICAL**: Only push if argument "$1" exactly equals "push"

- `/commit` → Creates commits, does NOT push
- `/commit push` → Creates commits AND pushes to remote

**If pushing:**
- Follow git-workflow skill push behavior rules
- Push ONLY after ALL commits successfully created
- Single push for all commits
- Verify push succeeds

## Example Scenarios

**Scenario 1: Documentation and code changes**
```
/commit
# Creates 2 commits:
# - docs: update README with new setup instructions
# - feat: add user authentication system
```

**Scenario 2: All related changes**
```
/commit
# Creates 1 commit:
# - feat: add user authentication with tests and docs
```

**Scenario 3: Security issue detected**
```
/commit
# Output:
# ⚠️  SECURITY ISSUE DETECTED - Aborting commits
#
# File: .env
# Issue: Contains API keys
#
# Suggested fix:
# 1. Add to .gitignore: .env
# 2. Unstage the file: git reset .env
#
# No commits were created.
```

**Scenario 4: Commit and push**
```
/commit push
# Creates commits, then pushes all to remote
```

Remember: Use HEREDOC format for all commit messages to ensure proper formatting.
