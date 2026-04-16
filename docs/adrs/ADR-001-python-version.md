# ADR-001: Python 3.11+

**Status:** Accepted  
**Date:** 2026-04-04  
**Decides:** Minimum Python version for all backend services

## Decision

Python 3.11 or higher is required for all backend code.

## Rationale

- Modern typing features (ParamSpec, TypeVarTuple, Self)
- Built-in `tomllib` for TOML config parsing
- Significant performance improvements over 3.10
- Exception groups for structured error handling
- Required by current versions of FastAPI, Pydantic v2, and SQLAlchemy 2.x
