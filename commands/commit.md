---
description: Create logical git commits with optional push
argument-hint: push
model: haiku
---

# Commit Command

Automated git commit workflow with security scanning and logical grouping. Use `/commit` to create commits locally or `/commit push` to push after committing.

## Execution Workflow

### 1. Security Scan

| Type | Examples |
|------|----------|
| Files | .env, .env.local, .env.production, credentials.json, secrets.yaml, config.json, *.pem, *.key, *.p12, *.pfx |
| Filenames | *secret*, *credential*, *password* |
| Environment | API_KEY=, ANTHROPIC_API_KEY=, OPENAI_API_KEY=, TOKEN=, ACCESS_TOKEN= |
| Tokens | sk-ant-, sk-proj-, key-, Bearer, token: |
| Passwords | PASSWORD=, pwd=, passwd= |
| Keys | -----BEGIN PRIVATE KEY-----, -----BEGIN RSA PRIVATE KEY-----, password = "...", api_key = "sk-..." |

If found: STOP, show details, suggest .gitignore, exit.

### 1.5. Git-Crypt Encrypted Files

**For each modified file, check if git-crypt encrypted:**
```bash
git check-attr filter <file>
```

**If output contains "git-crypt":**
- File is encrypted - SKIP security scan
- Safe to commit (encrypted before pushing to remote)

**If output contains "unspecified" or no "git-crypt":**
- File is NOT encrypted - RUN security scan
- Check for secrets as described in section 1

**Example:**
```bash
# .env is encrypted:
git check-attr filter .env
# Output: .env: filter: git-crypt
# → Skip security scan

# config.json is not encrypted:
git check-attr filter config.json
# Output: config.json: filter: unspecified
# → Run security scan
```

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
| session-context | Session context updates (.session/ files) |

Group related changes in single commit. Use separate commits for different types.

### 3.5. Session Context Files

Check if project enables session commits:
```bash
[ -f .claude/CLAUDE.md ] && grep -q "enable-session-commits: true" .claude/CLAUDE.md
```

**If enabled AND `.session/` modified:**
- Group: ALL `.session/` files into single commit
- Type: `session-context`
- Stage: `git add .session/`
- Message: `session-context: update session context for [feature-names]`
  - Extract feature names from `.session/feature/` directories
  - Format: comma-separated list

**Command**:
```bash
git commit -m "session-context: update session context for $(ls .session/feature 2>/dev/null | paste -sd, - | sed 's/,/, /g' || echo 'unknown')"
```

**If disabled:**
- Skip (remains gitignored)

### 4. Create Commits

For each group:
1. Stage: `git add [files]`
2. Commit with message: `type: brief summary` + optional details
3. NO AI attribution in commits, comments, or code! - NO "Generated with", "Co-Authored-By: Claude", or AI attribution text!
4. Write commit messages in human style (see git-workflow skill): no emojis, natural grammar, avoid excessive section headers, include details when needed
5. For code changes, use natural comments: no border separators (===), no "WHY:" labels, no emojis, brief casual explanations

### 5. Verify

Run `git status` after all commits created. If uncommitted files remain (and secure), create additional commits.

### 6. Push (If Requested)

**VERIFY:** Run `git status` to confirm clean state. List created commits.

**PUSH:** Only if `/commit push` argument provided. Run `git push` after all commits complete.
