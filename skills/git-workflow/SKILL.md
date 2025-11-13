---
name: git-workflow
description: Git workflow and commit guidelines. MUST be activated before ANY git commit, push, or version control operation. Includes security scanning for secrets (API keys, tokens, .env files), commit message formatting with HEREDOC, logical commit grouping (docs, test, feat, fix, refactor, chore, build, deps), push behavior rules, and safety rules for hooks and force pushes. Activate when user requests committing changes, pushing code, creating commits, or performing any git operations including analyzing uncommitted changes.
---

# Git Workflow Guidelines

Comprehensive git workflow principles for all git operations.

## Critical Rules

### Push Behavior
**NEVER push without explicit "push" keyword.** Examples: "commit my changes" → NO push, "commit and push" → YES push. After committing without push, inform: "Changes committed locally. Run 'git push' to push to remote."

### When to Commit
Only commit when explicitly requested. Never commit proactively.

## Security First

**Always scan for secrets. If found, STOP and refuse to commit.**

Critical patterns:
- API keys (API_KEY=, sk-ant-, sk-proj-)
- Tokens (TOKEN=, Bearer)
- Passwords (PASSWORD=, pwd=)
- Private keys (-----BEGIN)
- Hardcoded credentials

If detected:
1. Show files/lines
2. Suggest .gitignore
3. Recommend env vars
4. Refuse even if insisted

## Commit Organization

### Types
| Type | Purpose | Examples |
|------|---------|----------|
| docs | Documentation | README, *.md |
| test | Tests | test_*.py, *.spec.* |
| feat | New features | New functionality |
| fix | Bug fixes | Corrections |
| refactor | Code improvements | No behavior change |
| chore | Configuration | .gitignore, configs |
| build | Build/CI | Dockerfile, .github/ |
| deps | Dependencies | lock/requirements |

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

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

Focus on "why" rather than "what". Keep summary to 1-2 sentences.

## Workflow Process

1. **Security scan** - Check for secrets first
2. **Analyze** - Run git status, diff, log in parallel
3. **Group** - Organize by commit type
4. **Commit** - Use HEREDOC format
5. **Verify** - Ensure clean status
6. **Push** - Only if explicitly requested

## Safety Rules

- Never skip hooks (--no-verify) without request
- No force push to main/master
- Only amend your own commits
- Check authorship before amending
- If pre-commit hooks modify files, only amend if safe

## Philosophy

This skill defines the principles. The `/commit` command implements the procedural execution. Security always comes first, commits require explicit request, and pushes require the "push" keyword.