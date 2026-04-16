# ADR-005: uv

**Status:** Accepted  
**Date:** 2026-04-04  
**Decides:** Python package and project manager

## Decision

uv is the package manager for all Python dependency management.

## Rationale

- Rust-based resolver — 10-100x faster than pip/Poetry for dependency resolution
- pip-compatible — works with standard `pyproject.toml` and lockfiles
- Built by Astral (creators of ruff) — consistent tooling ecosystem
- Handles virtual environments, Python version management, and dependency locking in one tool
- Production-ready and actively maintained

## Implications

- `pyproject.toml` at repo root defines all dependencies
- `uv.lock` is checked into the repository
- CI and Docker builds use `uv sync` for reproducible installs
- No Poetry, no pip-tools, no conda
