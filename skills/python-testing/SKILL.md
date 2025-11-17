---
name: python-testing
description: Python-specific testing practices with pytest, fixtures, mocking, async testing, coverage configuration, and uv execution rules. Activate when working with pytest files, conftest.py, test directories, pyproject.toml testing configuration, or Python test-related tasks.
---

# Python Testing Practices

Python-specific testing patterns and best practices using pytest, complementing general testing-workflow skill.

## CRITICAL: UV Execution Rules

**NEVER use `-m` flag with uv run:**

```bash
# ✅ CORRECT - UV pytest execution
uv run pytest
uv run pytest -v
uv run pytest tests/unit/ -v
uv run pytest --cov=app --cov-report=html

# ❌ WRONG - Never add -m flag
# ❌ uv run -m pytest
# ❌ uv run -m pytest -v
```

**Always use `uv run pytest` directly** (never call pytest directly in uv projects).

---

## Pytest Fixtures

### Fixture Scopes

Pytest fixtures support different scopes for setup/teardown control:

```python
@pytest.fixture(scope="session")
def database_connection():
    """Created once per test session - expensive setup."""
    connection = setup_expensive_database()
    yield connection
    connection.cleanup()


@pytest.fixture(scope="module")
def api_client():
    """Created once per test module."""
    return APIClient(config="test")


@pytest.fixture(scope="class")
def service_instance():
    """Created once per test class."""
    return Service()


@pytest.fixture(scope="function")  # Default
def user():
    """Created for each test function - isolated."""
    return User(email="test@example.com")
```

### Fixture Setup and Teardown

Use `yield` pattern for setup/teardown with proper cleanup:

```python
@pytest.fixture
def database():
    """Fixture with setup and teardown."""
    # Setup
    db = Database(":memory:")
    db.initialize()
    db.create_schema()

    # Provide to test
    yield db

    # Teardown
    db.close()


@pytest.fixture
def mock_file(tmp_path):
    """Create temporary file that auto-cleans up."""
    temp_file = tmp_path / "test.txt"
    temp_file.write_text("test data")
    yield temp_file
    # Cleanup automatic with tmp_path
```

### Fixture Dependency Injection

Fixtures can depend on other fixtures:

```python
@pytest.fixture
def database():
    """Base database fixture."""
    db = Database(":memory:")
    db.initialize()
    yield db
    db.close()


@pytest.fixture
def user_service(database):
    """Service depending on database fixture."""
    return UserService(database)


@pytest.fixture
def authenticated_user(user_service):
    """User depending on service fixture."""
    user = user_service.create_user(
        username="testuser",
        email="test@example.com",
        password="secure"
    )
    yield user
    user_service.delete_user(user.id)
```

---

## conftest.py Patterns

### Central Fixture Location

Place shared fixtures in `conftest.py` at appropriate levels:

```
tests/
├── conftest.py              # Session/module level fixtures
├── unit/
│   ├── conftest.py          # Unit-specific fixtures
│   └── test_*.py
└── integration/
    ├── conftest.py          # Integration-specific fixtures
    └── test_*.py
```

### Example conftest.py

```python
# tests/conftest.py
import pytest
from app.services import UserService
from app.database import Database


@pytest.fixture(scope="session")
def database_connection():
    """Database connection for entire session."""
    db = Database(":memory:")
    db.initialize()
    db.run_migrations()
    yield db
    db.close()


@pytest.fixture
def user_service(database_connection):
    """UserService with test database."""
    return UserService(database_connection)


@pytest.fixture
def sample_user_data():
    """Standard user data for tests."""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "secure123",
        "age": 25
    }


@pytest.fixture
def temp_config_file(tmp_path):
    """Create temporary config file."""
    config_file = tmp_path / "config.json"
    config_file.write_text('{"setting": "value"}')
    return config_file
```

---

## Parametrized Testing

### Basic Parametrization

Use `@pytest.mark.parametrize` for multiple test inputs:

```python
import pytest


@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("", ""),
    ("MiXeD", "MIXED"),
])
def test_uppercase(input, expected):
    """Test uppercase conversion with multiple inputs."""
    assert input.upper() == expected
```

### Multiple Parameters

```python
@pytest.mark.parametrize("method,expected_status", [
    ("GET", 200),
    ("POST", 201),
    ("PUT", 200),
    ("DELETE", 204),
])
def test_http_methods(client, method, expected_status):
    """Test different HTTP methods."""
    response = client.request(method, "/api/resource")
    assert response.status_code == expected_status
```

### Parametrized Fixtures

```python
@pytest.mark.parametrize("user_role", ["admin", "user", "guest"])
def test_permission_levels(user_role):
    """Test different user permission levels."""
    user = User(role=user_role)
    assert user.can_access_dashboard() == (user_role in ["admin", "user"])
```

---

## Async Testing

### Marking Async Tests

Use `@pytest.mark.asyncio` decorator:

```python
import pytest


@pytest.mark.asyncio
async def test_async_fetch_data():
    """Test async data fetching."""
    result = await fetch_data_async("user123")
    assert result is not None
    assert result["id"] == "user123"


@pytest.mark.asyncio
async def test_concurrent_requests():
    """Test multiple concurrent async operations."""
    results = await asyncio.gather(
        fetch_user(1),
        fetch_user(2),
        fetch_user(3),
    )
    assert len(results) == 3
```

### Async Fixtures

```python
@pytest.fixture
async def async_client():
    """Async HTTP client fixture."""
    client = AsyncHTTPClient()
    await client.connect()
    yield client
    await client.disconnect()


@pytest.mark.asyncio
async def test_api_call(async_client):
    """Test with async fixture."""
    response = await async_client.get("/api/users")
    assert response.status_code == 200
```

---

## Mocking Patterns

### Mock Objects and Patching

```python
from unittest.mock import Mock, patch, MagicMock
import pytest


def test_send_email_success():
    """Test email sending with mocked SMTP."""
    # Create mock object
    mock_smtp = Mock()

    with patch("smtplib.SMTP", return_value=mock_smtp):
        result = send_email("test@example.com", "Subject", "Body")

    # Verify mock was called correctly
    mock_smtp.send_message.assert_called_once()
    assert result is True


def test_api_call_with_mock():
    """Test API call with mocked response."""
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"status": "ok"}

        result = fetch_api_data()

        mock_get.assert_called_once_with("https://api.example.com/data")
        assert result["status"] == "ok"
```

### Fixture-Based Mocking

```python
@pytest.fixture
def mock_database():
    """Provide mocked database."""
    with patch("app.database.Database") as mock_db:
        mock_db.return_value.query.return_value = {"id": 1, "name": "Test"}
        yield mock_db


def test_user_service_with_mock(mock_database):
    """Test service with mocked database dependency."""
    service = UserService(mock_database.return_value)
    user = service.get_user(1)
    assert user["name"] == "Test"


@pytest.fixture
def mock_api_client():
    """Provide mocked API client."""
    with patch("app.client.APIClient") as mock:
        mock.return_value.get.return_value = {"status": "ok"}
        mock.return_value.post.return_value = {"id": 123}
        yield mock
```

### Spy on Real Objects

```python
from unittest.mock import MagicMock


def test_spy_on_method():
    """Spy on actual method calls."""
    obj = RealObject()
    obj.method = MagicMock(side_effect=obj.method)

    result = obj.method("arg1")

    obj.method.assert_called_once_with("arg1")
    assert result == expected_value
```

---

## Exception Testing

### Testing with Context Managers

```python
import pytest
from app.exceptions import UserNotFoundError, ValidationError


def test_exception_raised():
    """Test that correct exception is raised."""
    with pytest.raises(UserNotFoundError) as exc_info:
        user_service.get_user("nonexistent_id")

    assert "nonexistent_id" in str(exc_info.value)


def test_validation_error():
    """Test validation error with message check."""
    user_data = {
        "username": "testuser",
        "email": "invalid-email",  # Invalid format
        "age": 25
    }

    with pytest.raises(ValidationError) as exc_info:
        user_service.create_user(user_data)

    assert "email" in str(exc_info.value)


def test_exception_type_matching():
    """Test matching specific exception type."""
    with pytest.raises((ValueError, TypeError)):
        process_data(None)
```

---

## pyproject.toml Configuration

### Complete Pytest Configuration

```toml
[tool.pytest.ini_options]
# Test discovery
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

# Output and behavior
addopts = [
    "-v",
    "--strict-markers",
    "--tb=short",
    "--cov=app",
    "--cov-report=term-missing",
    "--cov-report=html",
]

# Custom markers
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
    "asyncio: marks tests as async tests",
]

# Filter warnings as errors
filterwarnings = [
    "error",
    "ignore::DeprecationWarning:setuptools",  # Ignore specific warnings if needed
]
```

### Coverage Configuration

```toml
[tool.coverage.run]
source = ["app"]
omit = [
    "*/tests/*",
    "*/migrations/*",
    "*/__init__.py",
    "*/__main__.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
    "class .*\\bProtocol\\):",
    "@(abc\\.)?abstractmethod",
]
min_coverage = 80
```

---

## Makefile Integration

### Test Targets

```makefile
.PHONY: test test-unit test-integration test-coverage test-quick

# Run all tests
test:
	uv run pytest

# Unit tests only
test-unit:
	uv run pytest tests/unit/ -v

# Integration tests
test-integration:
	uv run pytest tests/integration/ -v

# Quick tests (skip slow)
test-quick:
	uv run pytest -m "not slow" -v

# Coverage report
test-coverage:
	uv run pytest --cov=app --cov-report=html --cov-report=term
	@echo "Coverage report: htmlcov/index.html"

# Watch mode (requires pytest-watch)
test-watch:
	uv run ptw tests/unit/

# Full test suite with all checks
check: test lint type-check
	@echo "All checks passed!"
```

---

## Development Dependencies Installation

### Installing with UV

```bash
# Core testing
uv add --dev pytest pytest-cov pytest-asyncio

# Mocking
uv add --dev pytest-mock

# Performance testing
uv add --dev pytest-benchmark

# Test data generation
uv add --dev faker factory-boy

# HTTP mocking
uv add --dev responses

# Watch mode (optional)
uv add --dev pytest-watch

# Parallel execution (optional)
uv add --dev pytest-xdist
```

---

## Import Error Solutions

### Issue: Tests Can't Import App Modules

**Solution 1: Ensure __init__.py exists**

```
tests/
├── __init__.py  # Important!
├── conftest.py
└── unit/
    ├── __init__.py
    └── test_*.py
```

**Solution 2: Add to conftest.py**

```python
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
```

**Solution 3: Use pyproject.toml**

```toml
[tool.pytest.ini_options]
pythonpath = ["src"]
```

---

## Deleted File Handling

### Skip Module-Level When Imports Fail

Move `pytest.skip()` BEFORE imports to prevent collection errors:

```python
# tests/removed_feature_test.py
import pytest

pytest.skip("Module removed - feature deleted", allow_module_level=True)

from deleted_module import Something  # Won't be evaluated
```

---

## Warnings as Errors Policy

### Enforce Clean Test Output

Treat all warnings as errors in tests:

```bash
# Run tests with warnings as errors
uv run pytest -W error

# Run with specific warning filters
uv run pytest -W error::DeprecationWarning
```

### Configuration in pyproject.toml

```toml
[tool.pytest.ini_options]
filterwarnings = ["error"]
```

### Handle Expected Warnings

```python
import warnings
import pytest


def test_deprecated_function():
    """Test deprecated function with expected warning."""
    with pytest.warns(DeprecationWarning):
        deprecated_function()


def test_suppress_specific_warning():
    """Test while ignoring specific warning."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        function_that_warns()
```

---

## User Deletion Handling

### Test Database User Cleanup

When tests create users, ensure cleanup:

```python
@pytest.fixture
def created_user(user_service):
    """Create test user with automatic cleanup."""
    user = user_service.create_user(
        username="testuser",
        email="test@example.com",
        password="secure"
    )

    yield user

    # Cleanup - delete after test
    user_service.delete_user(user.id)


def test_user_operations(created_user):
    """Test operations on created user."""
    assert created_user.id is not None
    # User automatically deleted after test
```

### Handle User Onboarding Flow

```python
@pytest.fixture
def onboarded_user(user_service):
    """Create and fully onboard test user."""
    user = user_service.create_user(
        username="newuser",
        email="new@example.com",
        password="secure"
    )

    # Complete onboarding
    user_service.set_profile(user.id, name="Test User")
    user_service.verify_email(user.id)

    yield user

    # Cleanup
    user_service.delete_user(user.id)
```

---

## Common Testing Patterns

### Arrange-Act-Assert

```python
def test_create_user_success(user_service):
    """Test successful user creation."""
    # Arrange - Set up test data
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "age": 25
    }

    # Act - Execute functionality
    user = user_service.create_user(user_data)

    # Assert - Verify results
    assert user is not None
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.age == 25
```

### Database Integration

```python
@pytest.fixture(scope="module")
def test_database():
    """Provide test database for integration tests."""
    db = Database("test.db")
    db.migrate()
    yield db
    db.close()


def test_user_repository_integration(test_database):
    """Test user repository with real database."""
    repo = UserRepository(test_database)

    # Create
    user = repo.create(username="testuser", email="test@example.com")
    assert user.id is not None

    # Retrieve
    retrieved = repo.get(user.id)
    assert retrieved.username == "testuser"

    # Update
    retrieved.email = "updated@example.com"
    repo.update(retrieved)

    # Verify
    updated = repo.get(user.id)
    assert updated.email == "updated@example.com"
```

### Test Markers and Organization

```python
@pytest.mark.slow
def test_expensive_operation():
    """Long-running test - can be skipped."""
    pass


@pytest.mark.integration
def test_database_integration():
    """Integration test with external service."""
    pass


@pytest.mark.asyncio
@pytest.mark.slow
def test_async_integration():
    """Async integration test."""
    pass


# Run commands:
# uv run pytest -m "not slow"          # Skip slow tests
# uv run pytest -m integration         # Only integration
# uv run pytest -m "integration and not slow"  # Filter multiple
```

---

## Edge Case Testing

### Common Edge Cases

```python
def test_edge_cases():
    """Test edge cases comprehensively."""
    calculator = Calculator()

    # Empty input
    assert calculator.sum([]) == 0

    # Single item
    assert calculator.sum([5]) == 5

    # Negative numbers
    assert calculator.sum([-1, -2, -3]) == -6

    # Mixed positive/negative
    assert calculator.sum([10, -5, 3]) == 8

    # Large numbers
    assert calculator.sum([10**10, 10**10]) == 2 * 10**10

    # Zero
    assert calculator.sum([0, 0, 0]) == 0
```

### None Value Handling

```python
def test_none_handling(service):
    """Test handling of None values."""
    # None input raises error
    with pytest.raises(ValueError):
        service.process(None)

    # None in list gets filtered
    result = service.process_list([1, None, 3])
    assert result == [1, 3]
```

---

**Note:** For general testing principles and strategies not specific to Python, see the testing-workflow skill.
