---
description: Create logical git commits with optional push
argument-hint: push
model: haiku
---

Run git status to check uncommitted files. If working tree is clean or merge conflicts exist, exit with appropriate message.

Check for git-crypt encrypted files by reading .gitattributes if it exists. Parse lines with "filter=git-crypt" to identify encrypted file patterns. These files will be skipped during security scanning since they're encrypted before pushing.

Scan all non-encrypted modified and untracked files for secrets. Look for:
- Secret files: .env, credentials.json, secrets.yaml, *.pem, *.key, *.p12, *.pfx
- AWS keys: AKIA, ABIA, ACCA, ASIA prefixes
- GitHub tokens: ghp_, gho_, ghu_, ghs_, ghr_
- Anthropic keys: sk-ant-
- OpenAI keys: sk-proj-, sk-
- Generic API keys: API_KEY=, APIKEY=, api_key=
- Tokens: TOKEN=, ACCESS_TOKEN=, Bearer
- Passwords: PASSWORD=, pwd=, passwd=, secret=
- Private keys: -----BEGIN PRIVATE KEY-----, -----BEGIN RSA, -----BEGIN OPENSSH
- Connection strings: mongodb://, postgres://, mysql://

If secrets are found, STOP immediately. Show details and suggest adding files to .gitignore. Do not proceed with commits.

Categorize uncommitted files using this approach:
- Auto-ignore and add to .gitignore: *.log, *.csv, *.tsv, *.db, *.sqlite, *.sqlite3, large data files (*.json over 1MB, *.xml data dumps)
- Auto-stage for commit: Source code files (*.py, *.js, *.ts, etc.), documentation (*.md, *.rst, *.txt), configuration files (pyproject.toml, package.json, Dockerfile, docker-compose.yml), small JSON/YAML configs, test files
- Ask the user only when: Ambiguous data files that could be fixtures or user data, binary files not in .gitignore, unclear file types not covered above

When asking about unclear files, use batch prompting if there are multiple files. Show the list and ask "Track these files? (y/n/pattern)" where pattern allows specifying a .gitignore rule.

Group files by logical change using commit types: feat (new features), fix (bug fixes), docs (documentation), test (tests), refactor (code improvements), perf (performance), style (formatting), chore (maintenance), build (build system), ci (CI/CD), deps (dependencies), revert (undo previous). Related functionality changes go together. Don't mix unrelated changes. Each commit should do ONE thing (atomic commits).

For each group of related files:
1. Stage the files with git add
2. Write a commit message that is human-style with natural grammar
3. NO emojis in commit messages
4. Brief summary line with optional detailed body
5. Use HEREDOC format for multi-line messages: git commit -m "$(cat <<'EOF'\ntype: summary\n\nOptional details\nEOF\n)"
6. Create the commit

After each commit, run git status again. If legitimate files remain (not matching the auto-ignore patterns), categorize and group them, then commit. Repeat this loop until git status shows only ignored files or working tree is clean.

Exit the loop when:
- Working tree is clean
- Only files matching .gitignore patterns remain
- User says to stop when prompted about unclear files

Show a brief summary of commits created with commit hashes and messages.

If $ARGUMENTS contains "push", run git push after all commits are complete. Otherwise, stop after creating commits without pushing.
