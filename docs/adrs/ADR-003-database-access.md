# ADR-003: SQLAlchemy Core + clickhouse-connect

**Status:** Accepted  
**Date:** 2026-04-04  
**Decides:** Database access libraries for PostgreSQL and ClickHouse

## Decision

- **PostgreSQL:** SQLAlchemy Core (SQL expression language, not the ORM layer)
- **ClickHouse:** clickhouse-connect (official Python driver)

## Rationale

### SQLAlchemy Core (PostgreSQL)
- SQL expression language provides composability and type safety without ORM abstraction overhead
- The platform's explicit schema design (bitemporal tables, JSONB extensions, RLS) benefits from direct SQL control
- Full compatibility with Alembic for migration auto-generation
- Async support via `asyncpg` dialect when needed

### clickhouse-connect (ClickHouse)
- Official ClickHouse Python driver maintained by ClickHouse Inc.
- Native protocol support for high-throughput inserts (fact_unit_day materialization)
- Query results as Python dictionaries or pandas DataFrames
- Connection pooling and session management built in

## Implications

- No Django ORM, no SQLModel, no raw asyncpg without SQLAlchemy
- Database queries live in `repository.py` files within each service
- Shared connection factories in `src/shared/db/`
