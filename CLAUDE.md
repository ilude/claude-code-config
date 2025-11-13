## Critical Rules (Always Apply First)

0. **CRITICAL** - NO AI attribution in commits, comments, or code! - NO "Generated with", "Co-Authored-By: Claude", or AI attribution text!
1. **Check for local `.claude/CLAUDE.md`** - Project ruleset overrides this file
2. **Security first** - Never commit secrets, API keys, or credentials
3. **Read before editing** - Always use Read tool before Edit/Write
4. **No proactive file creation** - Only create files when explicitly requested
5. **No backup files** - Git handles version control
6. **No time estimates** - They're consistently inaccurate
7. **KISS principle** - Default to SIMPLEST solution. No features "just in case". MVP first.
8. `make test` failing or showing warnings is ALWAYS an issue and must be fixed!

## Communication & Code Style

### Communication
- Be concise and direct
- Always provide absolute paths in responses (not relative)
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
- Complete ALL steps of clear-scope tasks without asking between steps

### TodoWrite Usage
**Use for:** 3+ step tasks, complex planning, user-requested lists
**Skip for:** Single/trivial tasks, informational requests
**Rules:** Mark in_progress before starting, mark [x] IMMEDIATELY after each completion, one in_progress max

## Common Pitfalls to Avoid
- `/c/Users/...` paths in Python → use `os.path.expanduser('~/')`
- Committing without explicit request
- Proactive file creation
- Assuming project structure without checking
- Manual .venv activation in uv projects → use `uv run`
- Unnecessary command flags → `-m` only for modules, not scripts
- Complex heredocs → use Task tool instead
- Non-idempotent scripts → ALL setup/install scripts MUST be safely re-runnable
- State tracking files → Detect state from system directly

### Platform-Specific (Windows)
- Python: Use `os.path.expanduser('~/')` NOT `/c/Users/...`
- Paths: Raw strings `r'C:\path'` or `chr(92)` for backslash
- Complex edits: Task tool > bash heredocs (escaping fragile)
- Home dir files: Task tool handles path resolution better

---

## Auto-Activating Skills

**Skills load automatically when relevant** - conserving context for unrelated work.

### Core Workflows
- **Python**: uv-exclusive commands, zero warnings, CQRS/IoC patterns, testing after changes
- **Testing**: pytest, zero warnings policy, targeted tests, >80% coverage, mocking
- **Git**: Security scan, semantic commits, explicit push only
- **Web Projects**: package.json, React/Next.js/Vue patterns
- **Containers**: Docker Compose V2, 12-factor app, security-first, multi-stage builds

### Specialized
- **Multi-Agent AI**: .spec/ dirs, STATUS.md, lessons/
- **Development Philosophy**: BE BRIEF, autonomous execution, experiment-driven, fail-fast

**Manual-only skills:**
- **Prompt Engineering**: `/optimize-prompt`, `/prompt-help` commands
- **Ruleset Optimization**: `/optimize-ruleset` command

See `~/.claude/skills/*/SKILL.md` for details.

---

**See `~/.claude/CHANGELOG.md` for detailed change history.**
- no toggle needed, people who use light mode are just wrong
- You should use subagent task where possible to speed up todo list tasks and other related work!
- always use python not python3 in bash commands