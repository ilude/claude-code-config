---
description: Create logical git commits with optional push
argument-hint: push
model: haiku
---

# Commit Command

Automated git commit workflow with security scanning and logical grouping.

## Execution Workflow

### 1. Security Scan

Check files:
- .env, .env.local, .env.production
- credentials.json, secrets.yaml, config.json
- .pem, .key, .p12, .pfx
- Files with "secret", "credential", "password" in name

Scan patterns:
- API_KEY=, ANTHROPIC_API_KEY=, OPENAI_API_KEY=
- sk-ant-, sk-proj-, key-
- TOKEN=, ACCESS_TOKEN=, Bearer, token:
- PASSWORD=, pwd=, passwd=
- -----BEGIN PRIVATE KEY-----, -----BEGIN RSA PRIVATE KEY-----
- password = "...", api_key = "sk-..."

If found: STOP, show details, suggest .gitignore, exit.

### 2. Analyze Changes

Run in parallel:
- `git status` - uncommitted changes
- `git diff` - what changed
- `git log --oneline -5` - commit style

### 3. Group Changes

Commit types:
| Type | For |
|------|-----|
| docs | Documentation (*.md, README, comments) |
| test | Tests (test_*.py, *.spec.*, tests/) |
| feat | New features |
| fix | Bug fixes |
| refactor | Code improvements without behavior change |
| chore | Config (.gitignore, pyproject.toml) |
| build | Build/CI (Dockerfile, .github/) |
| deps | Dependencies (uv.lock, requirements.txt) |

Single commit: related changes
Multiple commits: different types

### 4. Create Commits

For each group:
1. Stage files: `git add [files]`
2. Commit with HEREDOC:

```bash
git commit -m "$(cat <<'EOF'
type: brief summary

[Optional details]

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### 5. Verify

- `git status` - should be clean
- List commits created
- If uncommitted files remain (and secure), create additional commits

### 6. Push (If Requested)

Check argument:
- `/commit` → NO push
- `/commit push` → `git push`

If pushing:
- Push after all commits created
- Verify push succeeds
- Report status