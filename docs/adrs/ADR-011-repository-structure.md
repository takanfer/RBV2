# ADR-011: Monorepo

**Status:** Accepted  
**Date:** 2026-04-04  
**Decides:** Repository structure

## Decision

All platform code lives in a single monorepo.

## Rationale

- The platform has 11 named application services that share entity types, scoring structures, and database schemas. Keeping them together enables atomic cross-service changes.
- Shared Pydantic models in `src/shared/models/` are imported directly by all services — no package distribution overhead.
- Multiple Cursor agents working in parallel benefit from a single repo: they see the same types, the same schemas, and the same Cursor rules.
- CI can scope builds and tests to changed directories for efficiency.

## Implications

- Backend Python code in `src/`
- Frontend TypeScript code in `frontend/`
- Database migrations in `db/`
- Specifications and governance in `docs/`
- All Cursor rules in `.cursor/rules/`
