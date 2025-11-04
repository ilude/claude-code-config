---
name: python-workflow
description: Python project workflow guidelines including package management (uv, pip, poetry), virtual environment handling, and Python code style preferences. Activate when working with Python files (.py), Python projects, pyproject.toml, requirements.txt, setup.py, uv commands, pip, virtual environments, pytest, or any Python-specific tooling and development tasks.
---

# Python Projects Workflow

Guidelines for working with Python projects across different package managers and environments.

## Package Management

### UV Package Manager
- **Prefer uv over pip** when project uses uv
- Always use `uv run python` in uv-based projects
- Never manually reference `.venv` paths - let uv handle it
- Run `uv sync` before executing code in new projects

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
- Never use absolute paths to `.venv/bin/python` or `.venv/Scripts/python.exe`
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
- ✅ Use tool-specific run commands
- ✅ Check `pyproject.toml` for configuration
- ✅ Follow project's existing patterns
- ✅ Respect configured code style

---

**Note:** For project-specific Python patterns, check `.claude/CLAUDE.md` in the project directory.
