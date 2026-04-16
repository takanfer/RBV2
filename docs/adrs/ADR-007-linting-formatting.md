# ADR-007: ruff

**Status:** Accepted  
**Date:** 2026-04-04  
**Decides:** Linting and code formatting tool

## Decision

ruff handles all Python linting, formatting, and import sorting.

## Rationale

- Single tool replaces black (formatting), isort (import sorting), flake8 (linting), and pylint (static analysis)
- Rust-based — runs in milliseconds even on large codebases
- Built by Astral (same team as uv) — consistent tooling
- Supports all major lint rule sets (pyflakes, pycodestyle, isort, pep8-naming, etc.)

## Implications

- Configuration in `pyproject.toml` under `[tool.ruff]`
- Pre-commit hooks run `ruff check` and `ruff format`
- CI pipeline fails on any ruff violation
- No black, no isort, no flake8, no pylint installed separately
