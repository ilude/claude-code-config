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

**Pre-Commit Requirements:**
- ✅ All tests pass
- ✅ Zero warnings
- ✅ No linting errors
- ✅ No type errors
- ✅ Code formatted

**Never commit with:**
- ❌ Failing tests
- ❌ Any warnings
- ❌ Linting errors
- ❌ Unformatted code

```bash
# ✅ Required outcome
uv run pytest
# All tests passed, no warnings

# ❌ Unacceptable
uv run pytest
# Tests passed but with warnings
```

## Testing Strategy

**During Development:**
- Run targeted tests for fast iteration
- Fix issues immediately

**Before Commit:**
- Run full suite (`make check`)
- Fix all warnings/errors
- Note: May run 1500+ tests

## Test Organization

```
project/
├── tests/
│   ├── unit/              # Fast, isolated
│   ├── integration/       # External dependencies
│   └── fixtures/conftest.py
```

**Naming:**
- Files: `test_*.py` or `*_test.py`
- Functions: `test_*`
- Classes: `Test*`

## Coverage Requirements

**Standards:** >80% coverage, focus on behavior

**Test these:**
- Business logic, algorithms
- Edge cases, boundary conditions
- Error handling
- Integration points, APIs
- Security-critical paths

**Skip these:**
- Trivial getters/setters
- Private implementation details
- Third-party internals
- Simple data classes

## Test Structure - AAA Pattern

```python
# ✅ GOOD
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

```python
# conftest.py
@pytest.fixture
def db_connection():
    conn = create_test_database()
    yield conn
    conn.close()

@pytest.fixture
def sample_user():
    return User(email="test@example.com", name="Test User")

# test_file.py
def test_save_user(db_connection, sample_user):
    save_user(db_connection, sample_user)
    assert user_exists(db_connection, sample_user.email)
```

**Scopes:** `function` (default), `class`, `module`, `session`

## Parametrized Tests

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

## Mocking

```python
from unittest.mock import Mock, patch

# Mock external API
@patch('module.requests.get')
def test_api_call(mock_get):
    mock_get.return_value.json.return_value = {"status": "ok"}
    result = fetch_data()
    assert result["status"] == "ok"

# Dependency injection for testability
class UserService:
    def __init__(self, db_connection):
        self.db = db_connection

def test_get_user():
    mock_db = Mock()
    mock_db.query.return_value = {"id": 1, "name": "Test"}
    service = UserService(mock_db)
    assert service.get_user(1)["name"] == "Test"
```

## Integration Testing

```python
@pytest.fixture(scope="module")
def test_database():
    db = create_test_database()
    run_migrations(db)
    yield db
    drop_test_database(db)

def test_user_operations(test_database):
    user = create_user(test_database, email="test@example.com")
    assert user.id is not None
    assert get_user(test_database, user.id).email == "test@example.com"
```

## TDD Pattern Example

```python
# 1. Write failing test
def test_calculate_discount():
    result = calculate_discount(price=100, discount_percent=10)
    assert result == 90

# 2. Implement
def calculate_discount(price, discount_percent):
    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount must be between 0 and 100")
    return price - (price * discount_percent / 100)
```

## Test Configuration

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

```python
@pytest.mark.slow
def test_expensive_operation():
    result = process_large_dataset()
    assert result.success

# Run fast tests only
pytest -m "not slow"
```

## Development Workflow

1. Write/modify code
2. Run targeted tests
3. Fix issues immediately
4. Run full suite (`make check`)
5. Commit when zero warnings

**Always:**
- ✅ Test after every change
- ✅ Fix warnings immediately
- ✅ Add tests for new features

**Never:**
- ❌ Commit with failures/warnings
- ❌ Skip tests after changes
- ❌ Ignore failures as "known issues"

## Essential Commands

```bash
# Development - Targeted
pytest tests/unit/test_file.py -v           # Specific file
pytest -k "test_name" -v                    # Pattern match
pytest tests/unit/test_file.py::test_func   # Exact test
pytest -v --tb=short                        # Cleaner errors

# Debugging
pytest -l                                   # Show locals
pytest --pdb                                # Debug on failure
pytest -x                                   # Stop on first failure
pytest --lf                                 # Rerun last failed

# Coverage
pytest --cov=app --cov-report=html          # HTML report
pytest --cov=app --cov-report=term-missing  # Terminal report

# Verification
make check                                  # Full suite + quality
uv run pytest                               # All tests
uv run black --check app/ tests/            # Format check
uv run isort --check app/ tests/            # Import order
uv run flake8 app/ tests/                   # Linting
uv run mypy app/ tests/                     # Type check
```

## Test Quality Checklist

- ✅ Run in isolation (no shared state)
- ✅ Deterministic (same result every time)
- ✅ Fast (mock slow operations)
- ✅ Clear names document behavior
- ✅ Test edge cases and errors
- ✅ Zero warnings in output
- ✅ >80% coverage on critical paths

---

**TL;DR: Zero warnings policy. Targeted tests during development. Full suite before commit. Mock external dependencies. Test behavior not implementation. >80% coverage on critical paths.**
