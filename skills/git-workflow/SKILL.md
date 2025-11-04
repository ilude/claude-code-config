---
name: git-workflow
description: Git workflow and commit guidelines. MUST be activated before ANY git commit, push, or version control operation. Includes security scanning for secrets (API keys, tokens, .env files), commit message formatting with HEREDOC, logical commit grouping (docs, test, feat, fix, refactor, chore, build, deps), push behavior rules, and safety rules for hooks and force pushes. Activate when user requests committing changes, pushing code, creating commits, or performing any git operations including analyzing uncommitted changes.
---

# Git Workflow Guidelines

This skill provides comprehensive git workflow guidelines that apply to all git operations.

## CRITICAL: Push Behavior (READ FIRST)

**NEVER push to remote unless user explicitly includes "push" keyword in their request.**

**Examples:**
- "commit my changes" → Commit only, NO push ❌
- "/commit" → Commit only, NO push ❌
- "commit these changes" → Commit only, NO push ❌
- "/commit push" → Commit AND push ✅
- "commit and push" → Commit AND push ✅
- "push after committing" → Commit AND push ✅

**Why this matters:** Pushing is irreversible and may affect team members. Always require explicit permission.

**After committing:** Inform user that changes are committed locally. If they want to push, they can say "push" or "git push".

## When to Commit

- **Only commit when explicitly requested**
- Ask for clarification if commit intent is unclear
- Multiple related changes can be a single commit
- Unrelated changes should be separate commits

## Before Committing (Security First)

### 1. Scan for Secrets and Sensitive Data

**ALWAYS scan before creating ANY commits:**

**Files to check:**
- .env, .env.local, .env.production
- credentials.json, secrets.yaml, config.json
- .pem, .key, .p12, .pfx (private keys, certificates)
- Any file with "secret", "credential", "password" in name

**Patterns to scan for:**
- API keys: API_KEY=, ANTHROPIC_API_KEY=, OPENAI_API_KEY=, sk-ant-, sk-proj-, key-
- Tokens: TOKEN=, ACCESS_TOKEN=, Bearer, token:
- Passwords: PASSWORD=, pwd=, passwd=
- Private keys: -----BEGIN PRIVATE KEY-----, -----BEGIN RSA PRIVATE KEY-----
- Hardcoded credentials: password = "...", api_key = "sk-..."

### 2. If Security Issues Found

**STOP IMMEDIATELY** - do NOT create any commits:

1. Show which files/lines contain sensitive data
2. Provide specific line numbers and content preview
3. Suggest .gitignore entries to exclude files
4. Suggest using environment variables instead
5. Warn user even if they insist on committing
6. **Never commit secrets** - refuse if user insists

### 3. Analyze Changes

Run in parallel to understand the context:
- git status - See all uncommitted changes
- git diff - Understand what changed
- git log - Learn repository's commit message style

## Commit Organization

Group changes logically by type/purpose:

- **docs**: Documentation (*.md, README, comments)
- **test**: Tests (test_*.py, *.spec.*, tests/)
- **feat**: New features (new capabilities)
- **fix**: Bug fixes (corrections to existing functionality)
- **refactor**: Code improvements without behavior changes
- **chore**: Configuration (.gitignore, pyproject.toml, config files)
- **build**: Build/CI (Dockerfile, .github/, CI configs)
- **deps**: Dependencies only (uv.lock, requirements.txt)

**Important:**
- **Single commit** if all changes are closely related
- **Multiple commits** only when changes serve different purposes

## Commit Message Format

Always use HEREDOC format for proper multi-line formatting.

### Guidelines

- Follow project's commit message style (from git log)
- Focus on "why" rather than "what"
- Keep summary concise (1-2 sentences)
- Always include Claude Code attribution

## Verification

After creating commits:

- Run git status to verify NO uncommitted changes remain
- Show summary of commits created
- If files remain uncommitted (and no security issues), create additional commits

## Pushing to Remote (Explicit Permission Required)

**Only push when explicitly requested with "push" keyword:**

When pushing:
- Push ONLY after ALL commits are successfully created
- Single push for all commits: git push
- Verify push succeeds
- Report push status to user

**After commit (without push):**
- Inform user: "Changes committed locally. Run 'git push' to push to remote."
- Do NOT suggest pushing - let user decide

## Safety Rules

- **Never skip hooks** (no --no-verify) unless explicitly requested
- **Never run destructive commands** without confirmation
- **No force pushes** to main/master branches
- **Check authorship** before amending commits (only amend your own)
- **Never amend commits** by other developers
- **If pre-commit hooks modify files**: Only amend if safe (check authorship first)

## Integration with /commit Command

This skill provides the principles and guidelines. The /commit slash command provides the detailed procedural implementation. Both should follow the same workflow standards documented here.

---

**Remember:** 
1. Security first - scan for secrets before every commit
2. Never push without explicit "push" keyword
3. Commit only when explicitly requested
