---
name: git-workflow
description: Git workflow and commit guidelines. MUST be activated before ANY git commit, push, or version control operation. Includes security scanning for secrets (API keys, tokens, .env files), commit message formatting with HEREDOC, logical commit grouping (docs, test, feat, fix, refactor, chore, build, deps), push behavior rules, and safety rules for hooks and force pushes. Activate when user requests committing changes, pushing code, creating commits, or performing any git operations including analyzing uncommitted changes.
---

# Git Workflow Guidelines

This skill provides comprehensive git workflow guidelines that apply to all git operations.

## When to Commit

- **Only commit when explicitly requested**
- Ask for clarification if commit intent is unclear
- Multiple related changes can be a single commit
- Unrelated changes should be separate commits

## Before Committing (CRITICAL - Security First)

### 1. Scan for sensitive data FIRST

**Always scan before creating ANY commits:**
- API keys, tokens, passwords (patterns: `API_KEY=`, `TOKEN=`, `sk-`, `Bearer`)
- Files: `.env`, `credentials.json`, `.pem`, `.key`, private keys
- Hardcoded secrets in code
- Any patterns typically containing secrets

### 2. If security issues found

**STOP IMMEDIATELY** - do NOT create any commits:
- Show which files/lines contain sensitive data
- Suggest `.gitignore` entries
- Suggest using environment variables instead
- Exit without committing

### 3. Analyze changes

Run in parallel to understand the context:
- `git status` - See all uncommitted changes
- `git diff` - Understand what changed
- `git log` - Learn repository's commit message style

## Commit Organization

Group changes logically by type/purpose:

- **docs**: Documentation (`*.md`, README, comments)
- **test**: Tests (`test_*.py`, `*.spec.*`, `tests/`)
- **feat**: New features (new capabilities)
- **fix**: Bug fixes (corrections to existing functionality)
- **refactor**: Code improvements without behavior changes
- **chore**: Configuration (`.gitignore`, `pyproject.toml`, config files)
- **build**: Build/CI (`Dockerfile`, `.github/`, CI configs)
- **deps**: Dependencies only (`uv.lock`, `requirements.txt`)

**Important:**
- **Single commit** if all changes are closely related
- **Multiple commits** only when changes serve different purposes

## Commit Message Format

Always use HEREDOC format for proper multi-line formatting:

```bash
git commit -m "$(cat <<'EOF'
<type>: <concise summary>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### Guidelines

- Follow project's commit message style (from git log)
- Focus on "why" rather than "what"
- Keep summary concise (1-2 sentences)
- Always include Claude Code attribution (format above)

## Verification

After creating commits:

- Run `git status` to verify NO uncommitted changes remain
- Show summary of commits created
- If files remain uncommitted (and no security issues), create additional commits

## Pushing to Remote

**Only push when explicitly requested:**

- "commit these changes" → Commit only, do NOT push
- "commit and push" → Commit + push
- "push after committing" → Commit + push

When pushing:
- Push ONLY after ALL commits are successfully created
- Single push for all commits
- Verify push succeeds

## Safety Rules

- **Never skip hooks** (no `--no-verify`) unless explicitly requested
- **Never run destructive commands** without confirmation
- **No force pushes** to main/master branches
- **Check authorship** before amending commits (only amend your own)
- **Never amend commits** by other developers
- **If pre-commit hooks modify files**: Only amend if safe (check authorship first)

## Integration with /commit Command

This skill provides the principles and guidelines. The `/commit` slash command provides the detailed procedural implementation. Both should follow the same workflow standards documented here.

---

**Remember:** Security first, always. Every commit operation should begin with scanning for sensitive data.
