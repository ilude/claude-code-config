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

### 5. Verify and Iterate

Run `git status` after all commits created. **LOOP:** Check for uncommitted files, skip exclusion patterns (see 5.5), categorize and commit remaining legitimate files. **Repeat this loop** until git status shows only excluded files or clean state.

### 5.5. Handle Remaining Files

After initial commits, check for remaining untracked/unstaged files:
```bash
git status --porcelain | grep -E '^\?\?|^ M'
```

**Exclusion patterns to skip (DO NOT COMMIT):**

| Category | Patterns |
|----------|----------|
| **Backup files** | `*.backup`, `*.bak`, `*~`, `*.orig` |
| **Python** | `__pycache__/`, `*.pyc`, `*.pyo`, `*.pyd`, `.pytest_cache/`, `*.egg-info/`, `.tox/`, `.venv/`, `venv/` |
| **JavaScript/TypeScript** | `node_modules/`, `.next/`, `.nuxt/`, `dist/`, `build/`, `coverage/`, `.turbo/`, `*.map`, `.cache/`, `.parcel-cache/`, `out/` |
| **Sass/CSS** | `*.css.map`, `.sass-cache/` |
| **C#** | `bin/`, `obj/`, `*.suo`, `*.user`, `*.userosscache`, `*.sln.docstates`, `*.csproj.user`, `packages/`, `.vs/` |
| **System** | `.DS_Store`, `Thumbs.db`, `.update.lock`, `desktop.ini` |
| **Build artifacts** | `*.o`, `*.so`, `*.log`, `npm-debug.log*`, `yarn-debug.log*`, `yarn-error.log*` |
| **Editor** | `.vscode/`, `.idea/`, `*.swp`, `*.swo`, `*.swn` |

**Iterative process for remaining files:**
1. Check `git status --porcelain`
2. Identify files NOT matching exclusion patterns
3. If legitimate files found:
   - Determine commit type (feat/docs/test/chore/build/deps)
   - Group similar files together
   - Stage: `git add [files]`
   - Commit with appropriate message
   - **RETURN TO STEP 1** - check for more files
4. If NO legitimate files remain (only excluded patterns or clean):
   - Proceed to step 6 (push if requested)

**Example iteration:**
```
First check: Found tools/ directory → commit as feat
Second check: Found .backup files → skip (excluded)
Third check: Clean or only excluded files → done
```

**Safety check before push:**
- Verify no legitimate files remain uncommitted
- If found, warn and list them
- Do NOT push until resolved

### 6. Push (If Requested)

**VERIFY:** Run `git status` to confirm clean state. List created commits.

**PUSH:** Only if `/commit push` argument provided. Run `git push` after all commits complete.
