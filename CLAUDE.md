## Critical Rules (Always Apply First)

1. **Check for local `.claude/CLAUDE.md`** - Project ruleset overrides this file
2. **Security first** - Never commit secrets, API keys, or credentials
3. **Read before editing** - Always use Read tool before Edit/Write
4. **No proactive file creation** - Only create files when explicitly requested
5. **No backup files** - Git handles version control
6. **No time estimates** - They're consistently inaccurate

## Communication & Code Style

### Communication
- Be concise and direct
- Use clear headings and structure
- Ask for clarification when requirements are ambiguous
- Avoid excessive emojis

### Code Quality
- Prefer explicit over implicit
- Write clear comments for complex logic
- Follow existing project code style

## File Operations

### Basic Rules
- **Read before Edit/Write** - Verify content first
- **Prefer Edit over Write** - For existing files
- Check file existence before creating

## Tool Usage & Todo Management

### Tool Preferences
- Specialized tools (Read/Edit/Grep/Glob) > bash commands
- Parallel execution for independent operations
- Task tool for complex multi-step work

### TodoWrite Usage
**Use for:** 3+ step tasks, complex planning, user-requested lists
**Skip for:** Single/trivial tasks, informational requests
**Rules:** Mark in_progress before starting, complete immediately after finishing, one in_progress max

## Common Pitfalls to Avoid
- `/c/Users/...` paths in Python → use `os.path.expanduser('~/')`
- Committing without explicit request
- Proactive file creation
- Assuming project structure without checking
- Manual .venv paths → let package managers handle
- Complex heredocs → use Task tool instead

### Platform-Specific (Windows)
- Python: Use `os.path.expanduser('~/')` NOT `/c/Users/...`
- Paths: Raw strings `r'C:\path'` or `chr(92)` for backslash
- Complex edits: Task tool > bash heredocs (escaping fragile)
- Home dir files: Task tool handles path resolution better

---

## Auto-Activating Skills

**Skills load automatically when relevant** - conserving context for unrelated work.

- **Python**: `uv run python`, virtual env handling, type hints
- **Git**: Security scan, semantic commits, explicit push only
- **Web Projects**: package.json, React/Next.js/Vue patterns
- **Containers**: Docker, docker-compose, Kubernetes
- **Multi-Agent AI**: .spec/ dirs, STATUS.md, lessons/

**Manual-only skills:**
- **Prompt Engineering**: `/optimize-prompt`, `/prompt-help` commands

See `~/.claude/skills/*/SKILL.md` for details.

---

**See `~/.claude/CHANGELOG.md` for detailed change history.**
