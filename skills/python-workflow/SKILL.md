---
name: python-workflow
description: Python project workflow guidelines including package management (uv, pip, poetry), virtual environment handling, and Python code style preferences. Activate when working with Python files (.py), Python projects, pyproject.toml, requirements.txt, setup.py, uv commands, pip, virtual environments, pytest, or any Python-specific tooling and development tasks.
---

# Python Projects Workflow

Guidelines for working with Python projects across different package managers and environments.

## CRITICAL: Virtual Environment Best Practices

**NEVER reference .venv paths manually** (e.g., `.venv/Scripts/python.exe` or `../../../.venv/`) - causes cross-platform issues and breaks on structure changes.

**ALWAYS use `uv run python`** in uv-based projects (auto-finds venv, works cross-platform, no activation needed):

```bash
# ❌ Don't: ../../../.venv/Scripts/python.exe script.py
# ✅ Do: uv run python script.py

uv run python -m module.cli
```

**Prefer shared root .venv** unless isolation required (saves ~7GB per environment).

## Python Module CLI Syntax

**Use `-m` flag** when running modules as CLIs (tells Python to run module as script, not file):

```bash
# ✅ Do: uv run python -m module.cli
# ❌ Don't: uv run python module.cli  # fails - treats as file path
```

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

- Use tool-specific run commands (UV: `uv run python`, Poetry: `poetry run python`)
- Check project ruleset for venv structure (shared vs per-module)

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

**Key rules:**
- ✅ Use `uv run python` (never manual .venv paths)
- ✅ Use `-m` flag for module CLIs
- ✅ Check `pyproject.toml` for config
- ❌ Don't mix package managers

---

**Note:** For project-specific Python patterns, check `.claude/CLAUDE.md` in the project directory.
