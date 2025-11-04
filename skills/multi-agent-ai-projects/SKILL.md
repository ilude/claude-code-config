---
name: multi-agent-ai-projects
description: Guidelines for multi-agent AI and learning projects with lesson-based structures. Activate when working with AI learning projects, experimental directories like .spec/, lessons/ directories, STATUS.md progress tracking, or structured learning curricula with multiple modules or lessons.
---

# Multi-Agent AI Projects

Guidelines for working with multi-agent AI learning projects and experimental codebases.

## CRITICAL: First Actions When Starting or Resuming Work

**ALWAYS start by reading STATUS.md** (usually in `.spec/STATUS.md` or project root):

1. **Read STATUS.md FIRST** - Before anything else
   - Shows completed lessons/modules and current phase
   - Documents known issues and blockers
   - Provides resume instructions for new sessions
   - Explains project structure and patterns

2. **Check git status** - See what's uncommitted

3. **Verify dependencies installed** - Check if lesson deps are synced

4. **Look for lesson-specific .env files** - API keys needed

**Why this matters:** Multi-agent learning projects evolve rapidly. STATUS.md is the source of truth for current state. Reading it first prevents working on wrong lesson, missing context, or repeating completed work.

**Auto-activate this workflow when:**
- Project has `.spec/` directory with `lessons/` subdirectory
- `STATUS.md` exists in project
- Directory names suggest learning context (lesson-001, module-01, etc.)

## Project Structure Recognition

### Common Patterns
- `.spec/` directory - Learning specifications and experimental code
- `lessons/` or similar learning directories
- `STATUS.md` - Progress tracking for learning journey
- Per-lesson or per-module structure
- Self-contained lesson directories

### Typical Lesson Structure
```
lesson-XXX/
├── <name>_agent/          # Agent implementation
│   ├── __init__.py
│   ├── agent.py           # Pydantic AI agent setup
│   ├── tools.py           # Tool implementations
│   ├── prompts.py         # System prompts
│   └── cli.py             # CLI interface
├── .env                   # API keys (gitignored)
├── PLAN.md                # Lesson plan
├── README.md              # Quick reference
├── COMPLETE.md            # Learnings after completion
└── test_*.py              # Tests and demos
```

## Workflow Patterns

### Execution Patterns
- Use `uv run python` for execution (most AI projects use modern Python tooling)
- Each lesson may have its own virtual environment or shared venv
- Check lesson README for specific setup instructions
- Navigate to lesson directory before running code

### API Keys and Secrets
- API keys typically in per-lesson `.env` files
- Each lesson might require different API credentials
- Always check `.env.example` or `.env.template` in lesson directories
- **Never commit `.env` files** - always gitignored

### Dependencies
- Check for dependency groups in `pyproject.toml` (e.g., `lesson-001`, `lesson-002`)
- Run `uv sync --group lesson-XXX` to install lesson-specific deps
- Some projects use shared root venv, others have per-lesson venvs

## Progress Tracking

### STATUS.md Pattern
- **Read before starting work** (most important!)
- Update after completing lessons
- Note blockers and next steps
- Document learnings and insights
- Track which lessons are complete

### Session Management
- **Always check STATUS.md at session start** (FIRST action)
- Update STATUS.md before ending sessions
- Note any experimental findings
- Document what worked and what didn't

## Common Project Types

### Learning Spike Projects
- Focus on exploration and experimentation
- Code may not be production-quality
- Documentation of learnings is important
- Test different approaches
- Iterate quickly

### Multi-Agent Frameworks
- Agent coordination patterns
- Tool usage and integration
- Message passing between agents
- State management across agents
- Router/coordinator patterns

## Quick Reference

**ALWAYS start with:**
1. ✅ **Read STATUS.md** - FIRST action, non-negotiable
2. ✅ Check git status
3. ✅ Verify dependencies installed
4. ✅ Check lesson-specific .env files

**Then proceed with:**
- Lesson-specific README files
- .spec/ or lessons/ directory structure
- Per-lesson dependencies and setup

**Execution:**
- Use `uv run python` for modern projects
- Navigate to lesson directory first
- Check for per-lesson dependencies
- Respect lesson isolation if present

**Documentation:**
- Update STATUS.md with progress
- Document experimental findings
- Note blockers and next steps
- Keep COMPLETE.md for finished lessons

---

**Note:** These projects are learning-focused - prioritize understanding and documentation over production perfection. STATUS.md is your single source of truth for project state.
