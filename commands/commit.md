---
description: Create logical git commits with optional push
argument-hint: [push]
---

Create git commits following best practices with security-first approach and logical grouping.

## CRITICAL: Security Scan FIRST

BEFORE creating any commits, scan ALL uncommitted changes for security issues:

1. **Scan for sensitive data:**
   - API keys, tokens, passwords (patterns like `API_KEY=`, `TOKEN=`, `sk-`, `Bearer`)
   - `.env` files, `credentials.json`, `.pem`, `.key`, private keys
   - Hardcoded secrets in code files
   - Any file patterns typically containing secrets

2. **If security issues found:**
   - STOP IMMEDIATELY - do NOT create any commits
   - Show user which files/lines contain sensitive data
   - Suggest `.gitignore` entries for sensitive files (e.g., `.env`, `credentials.json`)
   - Suggest code changes to use environment variables instead of hardcoded secrets
   - Exit without committing anything

3. **Only proceed if no security issues detected**

## Workflow Steps

### 1. Analyze Changes

Run git status, git diff, and git log in parallel to understand:
- All uncommitted changes (staged and unstaged)
- File types and purposes
- Recent commit message style in the repository

### 2. Group Changes Logically

Group uncommitted changes into logical commits by type/purpose:

- **docs**: Documentation (`*.md`, `docs/`, README, comments)
- **test**: Tests (`test_*.py`, `*_test.py`, `tests/`, `__tests__/`, `*.spec.*`)
- **build**: Build/CI (`Dockerfile`, `.github/`, `Makefile`, CI configs)
- **chore**: Configuration (`pyproject.toml`, `package.json`, `.gitignore`, config files)
- **feat**: New features (new files, new functions/classes, new capabilities)
- **fix**: Bug fixes (fixes to existing functionality)
- **refactor**: Code improvements without behavior changes
- **deps**: Dependencies only (`uv.lock`, `package-lock.json`, `requirements.txt`)

**Important**: If all changes are closely related, a single commit is appropriate. Only split into multiple commits when changes serve different purposes.

### 3. Create Commits

For each logical group:

1. Stage the relevant files for that group
2. Create a commit with this format (using HEREDOC):
   ```
   <prefix>: <concise summary>

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>
   ```

3. Follow repository's commit message style (from git log analysis)
4. Focus on "why" rather than "what"
5. Keep summary concise (1-2 sentences)

**Safety:**
- Follow git hooks (NEVER use --no-verify)
- If pre-commit hooks modify files, amend commit only if safe (check authorship first)
- Never amend commits by other developers

### 4. Verify Complete

After all commits are created:
- Run `git status` to verify NO uncommitted changes remain
- Show summary of commits created
- If any files remain uncommitted (and no security issues), create additional commits until everything is committed

### 5. Push (ONLY if explicitly requested)

**CRITICAL**: ONLY push if the argument "$1" exactly equals "push"

- `/commit` - Creates commits, does NOT push
- `/commit push` - Creates commits AND pushes to remote

If pushing:
- Push ONLY after ALL commits are successfully created
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
