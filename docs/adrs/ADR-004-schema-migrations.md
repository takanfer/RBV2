# ADR-004: Alembic

**Status:** Accepted  
**Date:** 2026-04-04  
**Decides:** Schema migration tool for PostgreSQL

## Decision

Alembic manages all PostgreSQL schema migrations.

## Rationale

- Paired with SQLAlchemy Core — auto-generates migration diffs from table metadata
- Versioned migration chain ensures every environment applies the same changes in the same order
- Supports both upgrade and downgrade paths
- Production-proven at scale

## Implications

- All PostgreSQL schema changes go through Alembic migrations — no manual DDL in production
- Migration files live in `db/postgresql/migrations/versions/`
- ClickHouse migrations use separate versioned SQL scripts in `db/clickhouse/migrations/` (ClickHouse does not support transactional DDL the same way, so Alembic is not used for ClickHouse)
