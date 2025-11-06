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

### File Operations Best Practices (Claude-Specific)

**Reading/Writing Home Directory Files:**
- Use `os.path.expanduser('~/.claude/file.md')` in Python (NOT `/c/Users/...`)
- MSYS paths like `/c/Users/...` work in bash but NOT in Python's open()
- Bash `~/.claude/` works reliably for simple operations
- For complex content modifications, prefer Task tool over heredocs

**Python String Escaping:**
- Use raw strings for Windows paths: `r'C:\path\to\file'`
- Use `chr(92)` for literal backslash or raw strings (NOT `'\'`)
- Use triple-quoted strings for markdown/code content with quotes
- Avoid multiple levels of string escaping - use Task tool instead

**When to Use Task Tool vs Direct Operations:**
- Complex multi-file updates → Task tool (better error handling)
- Home directory files on Windows → Task tool (path resolution)
- Content with complex escaping (markdown, code blocks) → Task tool
- Simple reads/backups → Direct bash/Read tool
- Single-file edits in project → Edit tool

---

## Python Projects

**Python workflow guidelines have been moved to a skill for context efficiency.**

The `python-workflow` skill contains guidelines for:
- Package management (uv, pip, poetry)
- Virtual environment handling
- Python code style preferences

**The skill auto-activates** when working with Python files or Python projects.

**Quick reference:**
- Use `uv run python` in uv-based projects (never manual .venv paths)
- Let package managers handle virtual environments
- Follow project's code style (check pyproject.toml)
- Use type hints and f-strings in new code

See `~/.claude/skills/python-workflow/SKILL.md` for complete guidelines.

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

**Project-specific patterns have been moved to individual skills for context efficiency.**

Three specialized skills auto-activate based on project type:

### Multi-Agent AI Projects Skill
Auto-activates for: AI learning projects, .spec/ directories, STATUS.md, lessons/
- See `~/.claude/skills/multi-agent-ai-projects/SKILL.md`

### Web Projects Skill
Auto-activates for: package.json, npm/yarn/pnpm, React, Next.js, Vue, Angular
- See `~/.claude/skills/web-projects/SKILL.md`

### Container Projects Skill
Auto-activates for: Dockerfile, docker-compose.yml, Kubernetes, containers
- See `~/.claude/skills/container-projects/SKILL.md`

### Prompt Engineering Skill
**Manual invoke only** (via `/optimize-prompt` and `/prompt-help` commands)
- Advanced prompting techniques for transforming basic prompts into high-quality structured prompts
- 7 techniques: meta-prompting, recursive-review, deep-analyze, multi-perspective, deliberate-detail, reasoning-scaffold, temperature-simulation
- Based on "The Mental Models of Master Prompters"
- See `~/.claude/skills/prompt-engineering/SKILL.md`

**Available commands:**
- `/optimize-prompt [techniques] <prompt>` - Transform prompt using advanced techniques
- `/prompt-help [technique]` - Documentation and examples

**Each skill loads only when relevant**, saving context in unrelated projects.

---

## Learning & Improvement

### Patterns to Remember
- `uv run python` for uv-based projects
- Ask for clarification over assumptions

### Common Mistakes to Avoid
- Assuming project structure without checking
- Creating files without reading project patterns
- Committing without explicit request
- Overcomplicating simple tasks
- Using `/c/Users/...` paths in Python (use `os.path.expanduser('~/')`)
- Complex bash heredocs for markdown/code content (use Task tool instead)
- Assuming Read/Edit tools work same as bash for home directory on Windows
- Unescaped backslashes in Python strings (use raw strings or chr(92))
- Using Edit/Write for complex multi-file operations (use Task tool)
- Bash heredocs for content with nested quotes/backticks (fragile escaping)

---

## Notes

Key learnings:

- **Always check for local project ruleset** - It contains project-specific critical info
- **uv vs pip** - Many modern projects use uv; respect that choice
- **Virtual environments** - Let tools manage them, don't reference manually
- **Terminology matters** - Be precise about "local" vs "personal" rulesets

---

**See `~/.claude/CHANGELOG.md` for detailed change history.**
