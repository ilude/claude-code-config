---
name: testing-workflow
description: Python testing workflow patterns with pytest. Activate when working with pytest, test files (test_*.py), test directories, code quality tools, coverage reports, or testing tasks. Includes zero-warnings policy, targeted testing during development, mocking patterns, and fixture usage.
location: user
---

# Testing Workflow

Python testing workflow patterns and quality standards for pytest.

## CRITICAL: Zero Warnings Tolerance

**Treat all warnings as errors. No exceptions.**

| Status | Output | Action |
|--------|--------|--------|
| ✅ PASS | All tests passed, no warnings | Proceed |
| ❌ FAIL | Tests passed with DeprecationWarning | Fix immediately |
| ❌ FAIL | Any warning present | Block commit |

**Rules:**
- Fix all warnings before work is complete
- No deprecation messages allowed
- Use current syntax, avoid deprecated features
- `make test` must run completely clean

```bash
# ✅ Required outcome
uv run pytest
# All tests passed, no warnings

# ❌ Unacceptable - Fix before proceeding
uv run pytest
# Tests passed but with warnings
```

## Testing Strategy

### During Development - Targeted Tests

**Run specific tests for fast iteration:**

```bash
# Target specific directory
pytest tests/unit/test_providers/ -v

# Target specific file
pytest tests/unit/test_file.py -v

# Target specific function
pytest -k "test_function_name" -v

# Target exact test
pytest tests/unit/test_file.py::test_specific -v

# Cleaner error output
pytest tests/ -v --tb=short
```

### Before Commit - Full Suite

**Run complete verification:**

```bash
# Run everything
make check

# Or explicitly
uv run pytest
uv run black --check app/ tests/
uv run isort --check app/ tests/
uv run flake8 app/ tests/
```

**When to use:**
- **During iteration**: Targeted tests
- **Before commit**: Full suite (`make check`)
- **Note**: `make check` may run 1500+ tests - use sparingly

## Test Organization

**Standard directory structure:**

```
project/
├── tests/
│   ├── __init__.py
│   ├── unit/              # Fast, isolated unit tests
│   │   ├── test_models/
│   │   ├── test_services/
│   │   └── test_utils/
│   ├── integration/       # External dependencies
│   │   ├── test_api/
│   │   └── test_database/
│   └── fixtures/
│       └── conftest.py    # Shared fixtures
```

**Naming conventions:**
- Files: `test_*.py` or `*_test.py`
- Functions: `test_*`
- Classes: `Test*`

## Coverage Requirements

**Standards:**
- Maintain >80% coverage
- Focus on behavior, not implementation
- Test edge cases and errors
- Skip trivial code

**Test these:**
| Priority | What |
|----------|------|
| ✅ HIGH | Business logic, algorithms |
| ✅ HIGH | Edge cases, boundary conditions |
| ✅ HIGH | Error handling, exceptions |
| ✅ HIGH | Integration points, APIs |
| ✅ HIGH | Security-critical paths |

**Skip these:**
| Priority | What |
|----------|------|
| ❌ SKIP | Trivial getters/setters |
| ❌ SKIP | Private implementation details |
| ❌ SKIP | Third-party library internals |
| ❌ SKIP | Configuration files |
| ❌ SKIP | Simple data classes without logic |

## Test Structure - AAA Pattern

**Arrange, Act, Assert:**

```python
# ✅ GOOD - Clear AAA pattern
def test_user_registration():
    # Arrange
    user_data = {"email": "test@example.com", "password": "secure"}

    # Act
    result = register_user(user_data)

    # Assert
    assert result.success
    assert result.user.email == "test@example.com"

# ❌ BAD - Testing implementation
def test_internal_method():
    obj = MyClass()
    assert obj._internal_state == expected  # Don't test private state
```

## Fixtures

**Shared fixtures in conftest.py:**

```python
# conftest.py
@pytest.fixture
def db_connection():
    """Provide database connection for tests."""
    conn = create_test_database()
    yield conn
    conn.close()

@pytest.fixture
def sample_user():
    """Provide sample user data."""
    return User(email="test@example.com", name="Test User")

# test_file.py
def test_save_user(db_connection, sample_user):
    save_user(db_connection, sample_user)
    assert user_exists(db_connection, sample_user.email)
```

**Fixture scopes:**
- `function`: Default, per test
- `class`: Per test class
- `module`: Per test module
- `session`: Per test session

## Parametrized Tests

**Test multiple inputs efficiently:**

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("", ""),
    (None, None),
])
def test_uppercase_conversion(input, expected):
    assert to_uppercase(input) == expected
```

## Mocking External Dependencies

**Use mocks for isolation:**

```python
from unittest.mock import Mock, patch

# Mock external API
@patch('module.requests.get')
def test_api_call(mock_get):
    mock_get.return_value.json.return_value = {"status": "ok"}
    result = fetch_data()
    assert result["status"] == "ok"
    mock_get.assert_called_once()

# Mock database
@patch('module.database.query')
def test_database_query(mock_query):
    mock_query.return_value = [{"id": 1, "name": "Test"}]
    results = get_users()
    assert len(results) == 1
```

**Dependency injection for testability:**

```python
# ✅ GOOD - Testable with dependency injection
class UserService:
    def __init__(self, db_connection):
        self.db = db_connection

    def get_user(self, user_id):
        return self.db.query("SELECT * FROM users WHERE id = ?", user_id)

# Test with mock
def test_get_user():
    mock_db = Mock()
    mock_db.query.return_value = {"id": 1, "name": "Test"}
    service = UserService(mock_db)
    result = service.get_user(1)
    assert result["name"] == "Test"
```

## Debugging Failed Tests

**Essential pytest flags:**

| Flag | Purpose |
|------|---------|
| `-v` | Verbose output |
| `-l` | Show local variables on failure |
| `-s` | Show print statements |
| `--pdb` | Drop into debugger on failure |
| `--lf` | Run last failed tests only |
| `-x` | Stop on first failure |
| `--tb=short` | Short traceback format |

```bash
# Verbose with locals
pytest -v -l

# Debug on failure
pytest --pdb

# Rerun failures
pytest --lf

# Stop at first failure
pytest -x

# Specific test with short traceback
pytest tests/test_file.py::test_function -v --tb=short
```

## Integration Testing

**Test with real dependencies:**

```python
@pytest.fixture(scope="module")
def test_database():
    db = create_test_database()
    run_migrations(db)
    yield db
    drop_test_database(db)

def test_user_crud_operations(test_database):
    # Create
    user = create_user(test_database, email="test@example.com")
    assert user.id is not None

    # Read
    fetched = get_user(test_database, user.id)
    assert fetched.email == "test@example.com"

    # Update
    update_user(test_database, user.id, name="Updated")
    assert get_user(test_database, user.id).name == "Updated"

    # Delete
    delete_user(test_database, user.id)
    assert get_user(test_database, user.id) is None
```

## Test Configuration

**In pyproject.toml:**

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "-v",
    "--strict-markers",
    "--tb=short",
    "--cov=app",
    "--cov-report=term-missing",
]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
]
```

## Performance Testing

**Mark slow tests:**

```python
@pytest.mark.slow
def test_expensive_operation():
    result = process_large_dataset()
    assert result.success

# Run fast tests only
pytest -m "not slow"

# Run slow tests only
pytest -m "slow"
```

## Code Quality Integration

**Standard quality checks:**

```bash
# Format code
uv run black app/ tests/ run.py

# Sort imports
uv run isort app/ tests/ run.py

# Lint
uv run flake8 app/ tests/ run.py

# Type check
uv run mypy app/ tests/

# All checks
make check
```

## CRITICAL: Pre-Commit Requirements

**Before every commit:**

| Check | Command | Required |
|-------|---------|----------|
| Tests | `make check` | ✅ ALL PASS |
| Warnings | Visual inspection | ✅ ZERO |
| Linting | `flake8` | ✅ NO ERRORS |
| Format | `black --check` | ✅ NO CHANGES |
| Types | `mypy` | ✅ NO ERRORS |

**Never commit with:**
- ❌ Failing tests
- ❌ Any warnings present
- ❌ Linting errors
- ❌ Type errors
- ❌ Unformatted code

## Test-Driven Development (TDD)

**When appropriate:**

```python
# 1. Write failing test
def test_calculate_discount():
    result = calculate_discount(price=100, discount_percent=10)
    assert result == 90

# 2. Write minimal code to pass
def calculate_discount(price, discount_percent):
    return price - (price * discount_percent / 100)

# 3. Refactor with tests as safety net
def calculate_discount(price, discount_percent):
    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount must be between 0 and 100")
    discount_amount = price * (discount_percent / 100)
    return price - discount_amount
```

**TDD benefits:**
- Documents intent
- Prevents regressions
- Supports refactoring
- Clarifies requirements

## Development Workflow

**Continuous testing cycle:**

1. Write/modify code
2. Run targeted tests (`pytest tests/unit/test_file.py -v`)
3. Fix issues immediately
4. Iterate until feature complete
5. Run full suite (`make check`)
6. Fix any failures or warnings
7. Commit when all tests pass with zero warnings

**Always:**
- ✅ Run tests after every code change
- ✅ Fix warnings immediately
- ✅ Keep tests passing continuously
- ✅ Add tests for new features
- ✅ Update tests when refactoring

**Never:**
- ❌ Commit with failing tests
- ❌ Commit with warnings present
- ❌ Skip tests after code changes
- ❌ Ignore test failures as "known issues"

## Quick Reference

**Essential commands:**

```bash
# Development - Targeted
pytest tests/unit/test_file.py -v           # Specific file
pytest -k "test_name" -v                    # Pattern match
pytest tests/unit/test_file.py::test_func   # Exact test

# Debugging
pytest -v --tb=short                        # Short traceback
pytest -l                                   # Show locals
pytest --pdb                                # Debug on failure
pytest -x                                   # Stop on first failure
pytest --lf                                 # Rerun last failed

# Coverage
pytest --cov=app --cov-report=html          # HTML report
pytest --cov=app --cov-report=term-missing  # Terminal report

# Verification
make check                                  # Full suite + quality
```

**Test quality checklist:**
- ✅ Run in isolation (no shared state)
- ✅ Deterministic (same result every time)
- ✅ Fast (mock slow operations)
- ✅ Document behavior (clear names)
- ✅ Test edge cases and errors
- ✅ Zero warnings in output
- ✅ >80% coverage on critical paths

---

**TL;DR: Zero warnings policy. Targeted tests during development. Full suite before commit. Mock external dependencies. Test behavior not implementation. >80% coverage on critical paths.**
