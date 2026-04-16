# ADR-006: pytest

**Status:** Accepted  
**Date:** 2026-04-04  
**Decides:** Testing framework for all backend code

## Decision

pytest is the testing framework for all Python tests.

## Rationale

- De facto standard for Python testing
- Fixture system for composable test setup (database sessions, test data, mock services)
- Plugin ecosystem: pytest-asyncio (async tests), pytest-mock (mocking), testcontainers (real database containers)
- Parameterized tests for scoring threshold validation across multiple input values
- Clear assertion introspection for debugging failures

## Implications

- Test configuration in `pyproject.toml` under `[tool.pytest.ini_options]`
- Shared fixtures in `tests/conftest.py`
- Golden property test data in `tests/fixtures/golden_property/`
- Integration tests use testcontainers for real PostgreSQL and ClickHouse instances
