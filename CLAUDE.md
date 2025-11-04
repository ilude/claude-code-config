# Personal Claude Code Ruleset

**Owner**: mglenn
**Created**: 2025-11-04
**Purpose**: Personal preferences and patterns for Claude Code across ALL projects

---

## Terminology & Scope

**Critical distinction for all Claude sessions:**

- **Personal ruleset**: THIS file (`~/.claude/CLAUDE.md`) - applies to all projects
- **Local ruleset** / **Project ruleset**: `.claude/CLAUDE.md` in each project directory - project-specific

**Precedence**: Local project rulesets override personal preferences when conflicts exist.

---

## General Preferences

### Communication Style
- Be concise and direct
- Use clear headings and structure
- Provide examples when explaining concepts
- Ask for clarification when requirements are ambiguous
- Don't use emojis excessively (only when helpful for clarity)

### Code Quality
- Prefer explicit over implicit
- Write clear comments for complex logic
- Follow existing code style in each project
- Security first - never commit secrets, API keys, or credentials

### File Operations
- **Always read before editing** - Use Read tool before Edit/Write
- **Prefer Edit over Write** for existing files
- **Never create files proactively** unless explicitly requested
- Check if files exist before creating new ones

### Tool Usage Best Practices
- Use specialized tools (Read, Edit, Grep, Glob) over bash commands
- Run multiple independent tools in parallel when possible
- Use Task tool for complex multi-step explorations
- Check for project-specific tool preferences in local ruleset

---

## Python Projects

### Package Management
- **Prefer uv over pip** when project uses uv
- Always use `uv run python` in uv-based projects
- Never manually reference `.venv` paths - let uv handle it
- Run `uv sync` before executing code in new projects

### Virtual Environments
- Let package managers (uv, poetry, etc.) handle venv automatically
- Don't activate venvs manually - use tool-specific run commands
- Check project ruleset for venv structure (shared vs per-module)

### Code Style
- Follow project's existing style (check pyproject.toml, .editorconfig)
- Default to PEP 8 if no project style defined
- Use type hints when writing new Python code
- Prefer f-strings over .format() or % formatting

---

## Git Workflow

**Git workflow guidelines have been moved to a skill for context efficiency.**

The `git-workflow` skill contains comprehensive guidelines including:
- Security-first approach (scan for secrets before committing)
- Commit organization and logical grouping
- Commit message format with HEREDOC
- Verification and push behavior
- Safety rules for hooks and force pushes

**The skill auto-activates** when git operations are detected (committing, pushing, version control).

**Quick reference:**
- Only commit when explicitly requested
- Security scan ALWAYS runs first
- Use semantic commit types: docs, test, feat, fix, refactor, chore, build, deps
- Only push when explicitly requested with "push" keyword

See `~/.claude/skills/git-workflow/SKILL.md` for complete guidelines.

---

## Todo List Management

### When to Use TodoWrite
- Complex multi-step tasks (3+ steps)
- Non-trivial tasks requiring careful planning
- When user explicitly requests a todo list
- Tasks with multiple items provided by user

### When NOT to Use TodoWrite
- Single straightforward tasks
- Trivial tasks completable in <3 steps
- Purely conversational/informational tasks

### Todo List Best Practices
- Mark tasks as in_progress BEFORE starting work
- Complete tasks IMMEDIATELY after finishing (don't batch)
- Maintain exactly ONE in_progress task at a time
- Only mark completed when fully done (tests pass, no errors)
- Clean up stale todos if they no longer match current work

---

## Project-Specific Overrides

**Always check for local project ruleset first:**
```bash
# Look for project ruleset at:
.claude/CLAUDE.md
```

If found, project ruleset takes precedence over this personal ruleset for:
- Development workflow
- Tool preferences
- Code style
- Commit conventions
- Project-specific patterns

**This personal ruleset provides defaults only** - defer to project ruleset when it exists.

---

## Project Types & Patterns

### Multi-Agent AI Projects
- Check for `.spec/` or similar learning/experimental directories
- Look for `STATUS.md` for current progress
- Each lesson/module may be self-contained
- Use `uv run python` for execution
- API keys typically in per-lesson `.env` files

### Web Projects
- Check package.json for npm/yarn/pnpm
- Look for framework-specific configs (next.config.js, vite.config.ts)
- Respect existing test setup
- Follow existing component patterns

### Container-Based Projects
- Check for Dockerfile, docker-compose.yml
- Look for Makefile with common commands
- Check README for build instructions
- Understand dev vs production environments

---

## Session Management

### Starting New Sessions
1. Check for local project ruleset (`.claude/CLAUDE.md`)
2. Read project README if available
3. Check git status for current state
4. Look for STATUS.md or similar progress tracking
5. Verify dependencies are installed

### Resuming Work
1. Review recent git commits for context
2. Check for uncommitted changes
3. Read STATUS.md or project docs for current state
4. Ask user for context if unclear
5. Verify environment still works (run tests)

### Before Ending Sessions
1. Update STATUS.md if project uses it
2. Complete or document in-progress todos
3. Commit work if user requested it
4. Note any blockers or next steps

---

## Security & Privacy

### Never Commit
- API keys, tokens, credentials
- `.env` files
- Private keys, certificates
- Passwords, secrets
- Personal information

### Safe Practices
- Always use `.gitignore` for sensitive files
- Warn user if they request committing secrets
- Use environment variables for configuration
- Check for exposed credentials before committing

---

## Learning & Improvement

### Patterns to Remember
- `uv run python` for uv-based projects (not manual .venv paths)
- Check STATUS.md before starting work
- Read project ruleset first
- Ask for clarification over assumptions

### Common Mistakes to Avoid
- Assuming project structure without checking
- Using system Python instead of project venv
- Creating files without reading project patterns
- Committing without explicit request
- Overcomplicating simple tasks

---

## Notes

This personal ruleset was created during a multi-agent learning project. Key learnings:

1. **Always check for local project ruleset** - It contains project-specific critical info
2. **uv vs pip** - Many modern projects use uv; respect that choice
3. **Virtual environments** - Let tools manage them, don't reference manually
4. **STATUS.md pattern** - Some projects use this for progress tracking
5. **Terminology matters** - Be precise about "local" vs "personal" rulesets

---

## Updates

**2025-11-04**: Moved Git Workflow to skill for context efficiency
- Created `git-workflow` skill in `~/.claude/skills/git-workflow/`
- Moved all git workflow guidelines from CLAUDE.md to skill
- Skill auto-activates when git operations detected
- Saves ~70 lines of context in non-git sessions
- Progressive disclosure improves token efficiency

**2025-11-04**: Enhanced Git Workflow section
- Extracted core principles from `/commit` command
- Added security-first approach (scan before committing)
- Documented logical commit grouping (docs, test, feat, fix, etc.)
- Specified commit message format with HEREDOC
- Added verification and push behavior rules
- Ensures consistent git workflow regardless of how commits are requested

**2025-11-04**: Initial creation
- Added terminology clarification (local vs personal ruleset)
- Documented uv best practices
- Added todo list management guidelines
- Included multi-agent project patterns

---

**For project-specific guidance, always check `.claude/CLAUDE.md` in the project directory first!**
