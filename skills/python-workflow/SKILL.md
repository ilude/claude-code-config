---
name: python-workflow
description: Python project workflow guidelines including package management (uv, pip, poetry), virtual environment handling, and Python code style preferences. Activate when working with Python files (.py), Python projects, pyproject.toml, requirements.txt, setup.py, uv commands, pip, virtual environments, pytest, or any Python-specific tooling and development tasks.
---

# Python Projects Workflow

Guidelines for working with Python projects across different package managers and environments.

## CRITICAL: Virtual Environment Best Practices

**NEVER reference .venv paths manually** (e.g., `.venv/Scripts/python.exe` or `../../../.venv/`).

**ALWAYS use `uv run python`** in uv-based projects, which:
- Automatically finds project root and correct .venv
- Works cross-platform (Windows/Linux/Mac)
- No manual activation needed
- No path management required

**Prefer shared root .venv** unless project explicitly requires isolation (saves ~7GB per environment).

**Examples:**
```bash
# ❌ Don't do this (brittle, platform-specific)
../../../.venv/Scripts/python.exe script.py
.venv/bin/python script.py

# ✅ Always do this
uv run python script.py
uv run python -m module.cli
```

**Why this matters**: Manual paths cause cross-platform issues, waste disk space with multiple venvs, and break when project structure changes.

## Python Module CLI Syntax

**When running Python modules as CLI tools**, use the `-m` flag:

```bash
# ✅ Correct (with -m flag)
uv run python -m youtube_agent.cli analyze "URL"
uv run python -m pytest
uv run python -m pip install package

# ❌ Wrong (missing -m flag - will fail)
uv run python youtube_agent.cli analyze "URL"
```

The `-m` flag tells Python to run the module as a script. Without it, Python tries to open the module path as a file, which fails.

## Package Management

### UV Package Manager
- **Prefer uv over pip** when project uses uv
- Always use `uv run python` in uv-based projects
- Run `uv sync` before executing code in new projects
- Use `uv add <package>` to add dependencies

### General Package Management
- Respect the project's chosen package manager (uv, pip, poetry, pipenv)
- Check `pyproject.toml` for project configuration
- Don't mix package managers in the same project

## Virtual Environments

### Best Practices
- Let package managers (uv, poetry, etc.) handle venv automatically
- Don't activate venvs manually - use tool-specific run commands:
  - UV: `uv run python script.py`
  - Poetry: `poetry run python script.py`
  - Standard venv: `python -m venv .venv` then activate

### Common Patterns
- Check project ruleset for venv structure (shared vs per-module)
- Let the tooling abstract the virtual environment

## Code Style

### Style Guidelines
- Follow project's existing style (check `pyproject.toml`, `.editorconfig`)
- Default to PEP 8 if no project style defined
- Use type hints when writing new Python code
- Prefer f-strings over `.format()` or `%` formatting

### Configuration Files
Check these files for style preferences:
- `pyproject.toml` - Modern Python project configuration
- `.editorconfig` - Editor-agnostic style settings
- `setup.cfg` - Legacy project configuration
- `.flake8`, `.pylintrc` - Linter-specific configs

## Common Patterns

### Project Structure Recognition
- `pyproject.toml` - Modern Python project (PEP 518)
- `requirements.txt` - Pip dependencies
- `setup.py` - Package definition (legacy or hybrid)
- `Pipfile` - Pipenv projects
- `poetry.lock` - Poetry projects
- `uv.lock` - UV projects

### Testing
- Respect existing test framework (pytest, unittest, nose)
- Look for test configuration in `pyproject.toml` or `pytest.ini`
- Use project's test runner: `uv run pytest`, `poetry run pytest`, etc.

## Quick Reference

**Package managers:**
- UV: `uv run`, `uv sync`, `uv add`
- Poetry: `poetry run`, `poetry install`, `poetry add`
- Pip: `pip install`, `python -m pip`

**Never do:**
- ❌ Manual `.venv` path references
- ❌ System Python in uv/poetry projects
- ❌ Mix package managers
- ❌ Activate venvs manually when tools provide `run` commands

**Always do:**
- ✅ Use tool-specific run commands (especially `uv run python`)
- ✅ Use `-m` flag when running Python modules as CLIs
- ✅ Check `pyproject.toml` for configuration
- ✅ Follow project's existing patterns
- ✅ Respect configured code style

---

**Note:** For project-specific Python patterns, check `.claude/CLAUDE.md` in the project directory.
