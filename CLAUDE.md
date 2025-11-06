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

**Use these terms precisely** to avoid confusion. When referencing rulesets, always clarify which one.

---

## Context Efficiency Philosophy

**PRIMARY GOAL**: Minimize baseline context, maximize signal-to-noise ratio.

Context efficiency is THE most important optimization principle. Every token counts.

### Strategy

1. **Use skills for domain-specific rules** (git, python, web, containers)
   - Only loaded when relevant (file patterns, project structure)
   - 30-70% context reduction when inactive
   - Progressive disclosure of detailed procedures

2. **Keep CLAUDE.md minimal**
   - Project overview and purpose (essential context)
   - Quick start checklist
   - Project-specific patterns not covered by skills
   - References to skills for details

3. **Progressive disclosure wins**
   - Baseline = always-needed info only (~20% of content)
   - Details = loaded on-demand via skills (~80% of content)
   - Result: Faster responses, better reasoning

### When Optimizing Rulesets

- Calculate token savings from skill extraction
- Prioritize moves that save >100 tokens
- Report context efficiency gains
- Deduplicate personal/project rulesets
- Move procedural "how-to" content to skills
- Keep policy "what/why" content in rulesets

### Example Impact

Without skills: 6,000 tokens baseline
With skills: 4,000 tokens baseline, 5,500 with skills (when needed)
Savings: 2,000 tokens baseline (33% reduction)

**This compounds across projects**: As you optimize one project, skills help ALL projects.

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
- Using `/c/Users/...` paths in Python (use `os.path.expanduser('~/')`)
- Complex bash heredocs for markdown/code content (use Task tool instead)
- Assuming Read/Edit tools work same as bash for home directory on Windows
- Unescaped backslashes in Python strings (use raw strings or chr(92))
- Using Edit/Write for complex multi-file operations (use Task tool)
- Bash heredocs for content with nested quotes/backticks (fragile escaping)

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

**See `~/.claude/CHANGELOG.md` for detailed change history.**

**Latest:** 2025-11-05 - Added Prompt Engineering Skill and Commands

---

**For project-specific guidance, always check `.claude/CLAUDE.md` in the project directory first!**
