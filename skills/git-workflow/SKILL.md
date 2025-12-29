---
name: git-workflow
description: Git workflow and commit guidelines. Trigger keywords: git, commit, push, .git, version control. MUST be activated before ANY git commit, push, or version control operation. Includes security scanning for secrets (API keys, tokens, .env files), commit message formatting with HEREDOC, logical commit grouping (docs, test, feat, fix, refactor, chore, build, deps), push behavior rules, safety rules for hooks and force pushes, and CRITICAL safeguards for destructive operations (filter-branch, gc --prune, reset --hard). Activate when user requests committing changes, pushing code, creating commits, rewriting history, or performing any git operations including analyzing uncommitted changes.
---

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

# Git Workflow Guidelines

**Auto-activate when:** Working with `.gitignore`, `.gitattributes`, `.git/`, or when user mentions commit, push, git, version control, pull request, branch, merge, staging changes, filter-branch, rebase, reset, or history rewrite. Should also activate when bash commands contain `git` (requires conversation parsing).

Comprehensive git workflow principles for all git operations.

## Critical Rules

### Push Behavior
**MUST NOT push without explicit "push" keyword.** Examples: "commit my changes" → NO push, "commit and push" → YES push. After committing without push, inform: "Changes committed locally. Run 'git push' to push to remote."

### When to Commit
Only commit when explicitly requested. MUST NOT commit proactively.

## Security First

**MUST scan for secrets. If found, STOP and refuse to commit.**

Critical patterns:
- AWS keys (`AKIA`, `ABIA`, `ACCA`, `ASIA` prefixes)
- GitHub tokens (`ghp_`, `gho_`, `ghu_`, `ghs_`, `ghr_`)
- Anthropic keys (`sk-ant-`)
- OpenAI keys (`sk-proj-`, `sk-`)
- Generic API keys (`API_KEY=`, `APIKEY=`, `api_key=`)
- Tokens (`TOKEN=`, `ACCESS_TOKEN=`, `Bearer `)
- Passwords (`PASSWORD=`, `pwd=`, `passwd=`, `secret=`)
- Private keys (`-----BEGIN`, `-----BEGIN RSA`, `-----BEGIN OPENSSH`)
- Connection strings (`mongodb://`, `postgres://`, `mysql://`)
- High-entropy strings (32+ char random alphanumeric)

If detected:
1. Show files/lines
2. Suggest .gitignore
3. Recommend env vars or secret manager
4. Refuse even if insisted

### Git-Crypt Exception

Files marked with `filter=git-crypt` in `.gitattributes` are exempt from security scanning.

**Why safe:**
- Automatically encrypted before commit
- Plaintext in working directory, encrypted in repository
- Explicit protection declaration

**Detection:**
Check if file matches patterns in `.gitattributes` with `filter=git-crypt` directive.

**Example .gitattributes:**
```
secrets/*.json filter=git-crypt diff=git-crypt
*.key filter=git-crypt diff=git-crypt
.env.production filter=git-crypt diff=git-crypt
```

**Validation:**
- Verify git-crypt is initialized: `git-crypt status`
- If not initialized, warn user but don't block

## Commit Organization

### Types (Conventional Commits)
| Type | Purpose | Examples |
|------|---------|----------|
| feat | New features | New functionality |
| fix | Bug fixes | Corrections |
| docs | Documentation | README, *.md |
| test | Tests | test_*.py, *.spec.* |
| refactor | Code improvements | No behavior change |
| perf | Performance | Optimization |
| style | Formatting | Whitespace, semicolons |
| chore | Maintenance | .gitignore, configs |
| build | Build system | Dockerfile, Makefile |
| ci | CI/CD | .github/workflows |
| deps | Dependencies | lock/requirements |
| revert | Reverts | Undo previous commit |

### Breaking Changes
Use `!` after type: `feat!: remove deprecated API`
Or add footer: `BREAKING CHANGE: description`

### Atomic Commits
Each commit should:
- Do ONE thing only
- Leave codebase in working state
- Be independently revertable
- Use `git add -p` to stage partial files

### Grouping Strategy
- Single commit: All changes closely related
- Multiple commits: Different types or purposes
- Follow project's existing commit style (check git log)

## Commit Message Format

Use HEREDOC for multi-line messages:
```bash
git commit -m "$(cat <<'EOF'
type: concise summary

Optional details focusing on why, not what
EOF
)"
```

Focus on "why" rather than "what". Keep summary to 1-2 sentences.

### Human-Like Commit Style

To avoid obvious AI patterns (while keeping good documentation):
- **No emojis**: MUST NOT use ✅❌⚠️ℹ️ or any emojis in commits
- **Natural grammar**: Use natural phrasing, don't worry about perfect grammar
- **Avoid excessive structure**: Limit section headers (one "Changes:" section is fine, but avoid multiple like "Technical improvements:", "Benefits:", "Result:", etc.)
- **Detail when needed**: Include relevant details, but focus on what and why, not exhaustive documentation of every file

### Code Comment Guidelines

When writing code in commits, avoid AI patterns:
- **No border comments**: Don't use `# ===...===` or `# ---...---` style separators
- **No "WHY" labels**: Instead of "# WHY: reason", just explain naturally: "# Reason for this..."
- **No emojis in code**: MUST NOT use ✅❌⚠️ℹ️ in comments or strings
- **Brief explanations**: Comment purpose, not every detail
- **Casual tone**: "This handles..." not "This implementation provides comprehensive handling of..."

## Workflow Process

1. **Security scan** - Check for secrets first
2. **Analyze** - Run git status, diff, log in parallel
3. **Group** - Organize by commit type
4. **Commit** - Use HEREDOC format
5. **Verify** - Ensure clean status
6. **Push** - Only if explicitly requested

## Safety Rules

- MUST NOT skip hooks (--no-verify) without explicit request
- Only amend your own unpushed commits
- MUST check authorship before amending
- If pre-commit hooks modify files, only amend if safe

### Force Push - AVOID
**Never use `git push --force` or `--force-with-lease` unless explicitly requested by user.**

Why force push is dangerous:
- Rewrites published history others may have pulled
- Can cause collaborators to lose work
- Breaks CI/CD pipelines referencing old commits
- Makes debugging harder (commit SHAs change)

Common mistakes that lead to force push:
- Amending after push → just make a new commit instead
- Rebasing a pushed branch → merge instead, or only rebase unpushed commits
- "Cleaning up" commit history → leave it alone once pushed

**If you pushed a commit, it's done.** Fix mistakes with new commits, not by rewriting history.

## Destructive Operations - BANNED

### MUST NOT Use These Commands
- `git filter-branch` - BANNED (deprecated by git project, use git-filter-repo)
- `git gc --prune=now` - BANNED (bypasses 14-day safety window)
- `git gc --aggressive` - BANNED (makes recovery harder)
- `git reset --hard` - BANNED without explicit user request
- `git clean -fd` - BANNED without explicit user request
- `git add -f` on gitignored files - BANNED (causes data loss later)

### If User Asks to Remove Files from Git History
1. STOP - Do not use filter-branch (it is deprecated)
2. Tell user: "git-filter-repo is the recommended tool. It requires a fresh clone."
3. Ask: "Do you have backups? Assume any secrets are already compromised."
4. Suggest: Rotate credentials first, then rewrite history
5. If proceeding: User must install git-filter-repo and work on fresh clone
6. MUST NOT run `gc --prune` after - default 14-day window allows recovery

### If File is in .gitignore But Needs Committing
1. STOP - Do not use `git add -f`
2. Better: Add exception to .gitignore using `!` prefix
   ```
   # In .gitignore:
   *.log
   !important.log  # Exception - this file WILL be tracked
   ```
3. Or: Remove file pattern from .gitignore entirely
4. Then: `git add <file>` normally

### Undo Accidental Force-Add
```bash
git rm --cached <file>  # Removes from git, keeps on disk
```

### Recovery Options (before gc --prune=now)
```bash
git reflog                    # Find lost commits
git fsck --unreachable        # Find orphaned objects
git fsck --lost-found         # Recover to .git/lost-found/
```

## Philosophy

This skill defines the principles. The `/commit` command implements the procedural execution. Security always comes first, commits require explicit request, and pushes require the "push" keyword.