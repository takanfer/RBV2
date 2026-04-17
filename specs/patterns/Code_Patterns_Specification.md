# Code Patterns Specification

Defines the exact code patterns every agent must follow when implementing any service, route, repository, test, or infrastructure module. This document contains literal code templates. Deviating from these patterns requires explicit user approval and a documented reason.

**Sources:**
- `Project_Skeleton_Specification.md` — service directory structure (lines 117-165), naming conventions §4 (lines 232-273), testing §6 (lines 314-334)
- `Service_Interface_Contracts.md` — 15 services, operation signatures, error categories (lines 490-501), audit logging (line 505)
- `API_Design_Specification.md` — URL patterns, response shapes, error format, pagination
- `Authentication_Middleware_Specification.md` — dependency chain, CurrentUser, TenantContext
- `Observability_Specification.md` — structured logging, correlation IDs, audit logging
- `Infrastructure_Specification.md` — environment variables, Pydantic Settings
- `phase-0-foundations.mdc` — SQLAlchemy Core (line 48), Pydantic Settings (line 54), testing rules (lines 68-73), code quality (lines 75-80)
- `ADR-002-api-framework.md` — FastAPI, Pydantic-native schemas, dependency injection
- `ADR-014-task-queue.md` — Celery tasks co-located with services (line 45)
- `rbv2-project.mdc` — DDL-first pipeline (lines 146-155), working principles (lines 157-165)

---

## 1. Service Module Structure

Source: `Project_Skeleton_Specification.md` lines 117-165

Every service follows this directory layout:

```
src/services/{service_name}/
    __init__.py          # Re-exports public functions from service.py
    service.py           # Business logic — orchestrates repository calls, validation, audit
    repository.py        # Database access — SQLAlchemy Core queries only
    exceptions.py        # Service-specific exception classes
    tasks.py             # Celery tasks (only if the service has async operations)
```

### `__init__.py` Pattern

```python
from src.services.engagement.service import (
    create_assessment,
    get_assessment,
    update_assessment_status,
)
```

Re-export only the public interface. No logic in `__init__.py`.

---

## 2. Route Function Pattern

Source: `API_Design_Specification.md`, `ADR-002-api-framework.md` line 22

File location: `src/api/routes/{domain}.py`

```python
from fastapi import APIRouter, Depends, Query
from uuid import UUID

from src.api.dependencies.auth import get_current_user, get_tenant_context
from src.api.dependencies.db import get_db
from src.services.engagement import service as engagement_service
from src.shared.models.assessment import Assessment, AssessmentCreate
from src.api.schemas.pagination import PaginatedResponse

router = APIRouter(prefix="/api/engagements", tags=["engagements"])


@router.post(
    "/assessments",
    response_model=Assessment,
    status_code=201,
    summary="Create a new assessment",
)
async def create_assessment(
    body: AssessmentCreate,
    tenant: TenantContext = Depends(get_tenant_context),
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await engagement_service.create_assessment(db, tenant, user, body)


@router.get(
    "/assessments",
    response_model=PaginatedResponse[Assessment],
    status_code=200,
    summary="List assessments",
)
async def list_assessments(
    tenant: TenantContext = Depends(get_tenant_context),
    db: AsyncSession = Depends(get_db),
    page_size: int = Query(default=50, ge=1, le=200),
    cursor: str | None = Query(default=None),
    status: str | None = Query(default=None),
):
    return await engagement_service.list_assessments(
        db, tenant, page_size=page_size, cursor=cursor, status=status
    )
```

### Rules

- Every route function receives dependencies via `Depends()`.
- Route functions contain zero business logic. They call one service function and return its result.
- `tenant: TenantContext = Depends(get_tenant_context)` is the standard auth dependency (sets RLS automatically).
- Use `get_current_user` only when the route does not need full tenant scoping (rare).
- All parameters must have type hints.
- All route decorators must include `response_model`, `status_code`, and `summary`. Tags are set once on the `APIRouter` constructor, not repeated on individual route decorators.

---

## 3. Service Function Pattern

Source: `Service_Interface_Contracts.md` operation signatures, `Observability_Specification.md` audit logging

File location: `src/services/{name}/service.py`

```python
import logging
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.audit import audit_log
from src.shared.models.assessment import Assessment, AssessmentCreate
from src.services.engagement import repository as repo
from src.services.engagement.exceptions import (
    AssessmentNotFound,
    InvalidStatusTransition,
)
from src.api.dependencies.auth import CurrentUser, TenantContext

logger = logging.getLogger(__name__)


async def create_assessment(
    db: AsyncSession,
    tenant: TenantContext,
    user: CurrentUser,
    data: AssessmentCreate,
) -> Assessment:
    assessment = await repo.insert_assessment(db, tenant.tenant_id, data)
    await audit_log(
        db,
        tenant_id=tenant.tenant_id,
        user_id=user.user_id,
        action="create_assessment",
        entity_type="assessment",
        entity_id=assessment.assessment_id,
        after_value=assessment.model_dump(),
    )
    await db.commit()
    logger.info(
        "Assessment created",
        extra={"entity_type": "assessment", "entity_id": str(assessment.assessment_id)},
    )
    return assessment


async def get_assessment(
    db: AsyncSession,
    tenant: TenantContext,
    assessment_id: UUID,
) -> Assessment:
    assessment = await repo.get_assessment_by_id(db, tenant.tenant_id, assessment_id)
    if assessment is None:
        raise AssessmentNotFound(assessment_id)
    return assessment


async def update_assessment_status(
    db: AsyncSession,
    tenant: TenantContext,
    user: CurrentUser,
    assessment_id: UUID,
    new_status: str,
) -> Assessment:
    before = await get_assessment(db, tenant, assessment_id)
    if not _is_valid_transition(before.status, new_status):
        raise InvalidStatusTransition(before.status, new_status)
    updated = await repo.update_assessment_status(
        db, tenant.tenant_id, assessment_id, new_status
    )
    await audit_log(
        db,
        tenant_id=tenant.tenant_id,
        user_id=user.user_id,
        action="update_assessment_status",
        entity_type="assessment",
        entity_id=assessment_id,
        before_value=before.model_dump(),
        after_value=updated.model_dump(),
    )
    await db.commit()
    return updated
```

### Rules

- Service functions always receive `db: AsyncSession` as the first parameter.
- Service functions always receive `tenant: TenantContext` as the second parameter.
- Service functions that mutate data receive `user: CurrentUser` for audit logging.
- Service functions raise service-specific exceptions (not HTTP exceptions).
- Service functions call `audit_log()` for every mutation, then `await db.commit()` to commit the write and audit log atomically.
- Service functions use `logger.info()` for state transitions, `logger.error()` for unexpected failures.
- Service functions never import FastAPI (no `Request`, `Response`, `HTTPException`).
- Service functions own the transaction boundary. Repositories and audit helpers execute statements but never commit.

---

## 4. Repository Function Pattern

Source: `phase-0-foundations.mdc` line 48 (SQLAlchemy Core, not ORM)

File location: `src/services/{name}/repository.py`

```python
from uuid import UUID

from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.models.assessment import Assessment, AssessmentCreate


async def get_assessment_by_id(
    db: AsyncSession, tenant_id: UUID, assessment_id: UUID
) -> Assessment | None:
    from src.shared.db.tables import assessment_table

    stmt = select(assessment_table).where(
        assessment_table.c.tenant_id == tenant_id,
        assessment_table.c.assessment_id == assessment_id,
    )
    row = (await db.execute(stmt)).first()
    return Assessment.model_validate(dict(row._mapping)) if row else None


async def insert_assessment(
    db: AsyncSession, tenant_id: UUID, data: AssessmentCreate
) -> Assessment:
    from src.shared.db.tables import assessment_table

    values = data.model_dump()
    values["tenant_id"] = tenant_id
    stmt = insert(assessment_table).values(**values).returning(assessment_table)
    row = (await db.execute(stmt)).first()
    return Assessment.model_validate(dict(row._mapping))


async def list_assessments(
    db: AsyncSession,
    tenant_id: UUID,
    page_size: int,
    cursor_id: UUID | None,
    status: str | None,
) -> tuple[list[Assessment], int]:
    from src.shared.db.tables import assessment_table
    from sqlalchemy import func

    base = select(assessment_table).where(
        assessment_table.c.tenant_id == tenant_id,
    )
    if status:
        base = base.where(assessment_table.c.status == status)
    if cursor_id:
        base = base.where(assessment_table.c.assessment_id > cursor_id)

    total = (await db.execute(select(func.count()).select_from(base.subquery()))).scalar()
    rows = (await db.execute(base.order_by(assessment_table.c.assessment_id).limit(page_size))).all()
    items = [Assessment.model_validate(dict(r._mapping)) for r in rows]
    return items, total
```

### Rules

- Repository functions use **SQLAlchemy Core** (select, insert, update, delete from `sqlalchemy`). Never use ORM session methods like `session.add()` or `session.query()`.
- Every query includes `tenant_id` in its WHERE clause (RLS is a defense-in-depth backup, not the primary filter).
- Repository functions return Pydantic models (via `model_validate`), not raw Row objects.
- Repository functions never raise HTTP exceptions. They return `None` for not-found (the service layer raises the exception).
- Repository functions take `db: AsyncSession` as the first parameter and `tenant_id: UUID` as the second.
- Repository functions never call `db.commit()` or `db.rollback()`. The service layer manages the transaction.

---

## 5. Exception Pattern

Base class location: `src/services/base_exceptions.py`

```python
class ServiceError(Exception):
    """Base class for all service-layer exceptions."""
    status_code: int = 500
    code: str = "internal_error"

    def __init__(self, message: str, detail: dict | None = None):
        self.message = message
        self.detail = detail or {}
        super().__init__(message)
```

Service-specific exceptions location: `src/services/{name}/exceptions.py`

```python
from uuid import UUID
from src.services.base_exceptions import ServiceError


class AssessmentNotFound(ServiceError):
    status_code = 404
    code = "assessment_not_found"

    def __init__(self, assessment_id: UUID):
        super().__init__(
            message=f"Assessment with ID {assessment_id} not found",
            detail={"assessment_id": str(assessment_id)},
        )


class InvalidStatusTransition(ServiceError):
    status_code = 409
    code = "invalid_status_transition"

    def __init__(self, current_status: str, target_status: str):
        super().__init__(
            message=f"Cannot transition from {current_status} to {target_status}",
            detail={"current_status": current_status, "target_status": target_status},
        )
```

### Exception Handler (in `src/api/main.py`)

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.services.base_exceptions import ServiceError


@app.exception_handler(ServiceError)
async def service_error_handler(request: Request, exc: ServiceError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "detail": exc.detail,
            }
        },
    )
```

### Rules

- All service exceptions inherit from `ServiceError`.
- `ServiceError` is defined once in `src/services/base_exceptions.py` and imported by all services.
- Each service defines its own exceptions in `exceptions.py`.
- Exception `code` values follow the format from `API_Design_Specification.md`: lowercase snake_case.
- The FastAPI exception handler in `main.py` catches `ServiceError` and converts it to the standard error envelope.

---

## 6. Test Pattern

Source: `Project_Skeleton_Specification.md` §6 (lines 314-334), `phase-0-foundations.mdc` lines 68-73

### Unit Test

File location: `tests/unit/test_{service_name}.py`

```python
import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from src.services.engagement.service import create_assessment, get_assessment
from src.services.engagement.exceptions import AssessmentNotFound
from src.shared.models.assessment import AssessmentCreate


@pytest.fixture
def mock_db():
    return AsyncMock()


@pytest.fixture
def tenant_context():
    from src.api.dependencies.auth import TenantContext
    return TenantContext(
        tenant_id=uuid4(),
        client_ids=[uuid4()],
        role="consultant",
        scopes=["full"],
    )


@pytest.fixture
def current_user(tenant_context):
    from src.api.dependencies.auth import CurrentUser
    return CurrentUser(
        user_id=uuid4(),
        tenant_id=tenant_context.tenant_id,
        email="test@example.com",
        role="consultant",
        display_name="Test User",
    )


@pytest.mark.asyncio
async def test_create_assessment(mock_db, tenant_context, current_user):
    data = AssessmentCreate(property_id=uuid4(), assessment_type="FULL_ENGAGEMENT")
    # ... mock repo, call service, assert result ...


@pytest.mark.asyncio
async def test_get_assessment_not_found(mock_db, tenant_context):
    with pytest.raises(AssessmentNotFound):
        await get_assessment(mock_db, tenant_context, uuid4())
```

### Integration Test

File location: `tests/integration/test_{service_name}.py`

```python
import pytest
from uuid import uuid4


@pytest.mark.asyncio
async def test_assessment_lifecycle(db_session):
    """End-to-end: create -> update status -> get."""
    # Uses real PostgreSQL via testcontainers
    # db_session fixture from tests/conftest.py
    pass
```

### Rules

- Unit tests mock the database (`AsyncMock` for `db`).
- Integration tests use real databases via testcontainers (configured in `tests/conftest.py`).
- Test file names: `test_{service_name}.py` (`Project_Skeleton_Specification.md` §6.3, line 330).
- Every service operation must have at least one unit test for the success path and one for each error condition.
- Use `@pytest.fixture` decorators for all test setup. No setup/teardown methods.
- Use `@pytest.mark.asyncio` for all async tests.
- Shared fixtures (db_session, tenant_factory, user_factory) live in `tests/conftest.py`.

---

## 7. Audit Log Helper Pattern

Source: `Observability_Specification.md`, `Database_Schema_Specification.md` lines 207-220

File location: `src/shared/audit.py`

```python
from uuid import UUID, uuid4
from typing import Any

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession


async def audit_log(
    db: AsyncSession,
    *,
    tenant_id: UUID,
    user_id: UUID | None,
    action: str,
    entity_type: str,
    entity_id: UUID,
    before_value: dict[str, Any] | None = None,
    after_value: dict[str, Any] | None = None,
    reason: str | None = None,
) -> None:
    from src.shared.db.tables import audit_log_table

    stmt = insert(audit_log_table).values(
        log_id=uuid4(),
        tenant_id=tenant_id,
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        before_value=before_value,
        after_value=after_value,
        reason=reason,
    )
    await db.execute(stmt)
```

### Rules

- All keyword arguments after `db` are keyword-only (enforced by `*`).
- `before_value` and `after_value` are the output of `model.model_dump()`.
- `user_id` is `None` for system-triggered actions (e.g., scheduled scoring runs).
- The audit helper does NOT commit. The calling service function manages the transaction.

---

## 8. Celery Task Pattern

Source: `ADR-014-task-queue.md` lines 28-32, 45

File location: `src/services/{name}/tasks.py`

```python
import logging

from src.shared.celery_app import celery_app
from src.shared.db.postgres import get_async_session
from src.shared.observability import correlation_id_var

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def run_import_pipeline(self, ingestion_id: str, correlation_id: str | None = None):
    """Long-running import pipeline task."""
    if correlation_id:
        correlation_id_var.set(correlation_id)

    logger.info("Import pipeline started", extra={"task_id": self.request.id, "ingestion_id": ingestion_id})

    try:
        # Synchronous wrapper around async service calls
        import asyncio
        asyncio.run(_run_import_pipeline_async(ingestion_id))
    except Exception as exc:
        logger.error("Import pipeline failed", extra={"task_id": self.request.id, "ingestion_id": ingestion_id, "exc_info": str(exc)})
        raise self.retry(exc=exc)

    logger.info("Import pipeline completed", extra={"task_id": self.request.id, "ingestion_id": ingestion_id})
```

### Rules

- Celery tasks are co-located with their service in `tasks.py` (ADR-014 line 45).
- Tasks accept the `correlation_id` parameter and set it in context for log propagation.
- Tasks use `bind=True` for access to `self.request.id` and `self.retry()`.
- Tasks log start, completion, and failure at `INFO`/`ERROR` level.
- Long-running operations (import, scoring, report rendering) are Celery tasks. Short-lived operations are synchronous (ADR-014 lines 28-31).

---

## 9. Pydantic Settings Pattern

Source: `phase-0-foundations.mdc` line 54, `Infrastructure_Specification.md`

File location: `src/shared/config/settings.py`

```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@localhost:5432/partners"
    database_pool_size: int = 5
    database_max_overflow: int = 10

    clickhouse_host: str = "localhost"
    clickhouse_port: int = 8123
    clickhouse_database: str = "partners"
    clickhouse_user: str = "default"
    clickhouse_password: str = ""

    s3_endpoint_url: str = "http://localhost:9090"
    s3_access_key: str = "minioadmin"
    s3_secret_key: str = "minioadmin"
    s3_bucket_evidence: str = "partners-evidence"
    s3_bucket_reports: str = "partners-reports"

    redis_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/1"

    auth_issuer_url: str = ""
    auth_audience: str = ""
    auth_jwks_url: str = ""
    cognito_user_pool_id: str = ""
    cognito_region: str = ""
    cognito_app_client_id: str = ""

    log_level: str = "INFO"
    log_format: str = "json"
    environment: str = "development"
    cors_allowed_origins: str = "http://localhost:3000"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
```

### Rules

- One `Settings` class, one `settings` instance, imported everywhere.
- All env vars have local-dev defaults so the app starts with just `docker compose up` and no `.env` file.
- Auth variables have empty-string defaults and are validated at middleware initialization, not at settings load.
- Never access environment variables via the `os` module directly. Always go through `settings`.

---

## 10. FastAPI App Initialization Pattern

File location: `src/api/main.py`

```python
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.shared.config.settings import settings
from src.api.middleware.logging import LoggingMiddleware
from src.api.middleware.correlation import CorrelationMiddleware
from src.api.routes import auth, engagements
from src.services.base_exceptions import ServiceError


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize DB pools, validate settings
    yield
    # Shutdown: close DB pools


app = FastAPI(
    title="Partners Platform API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(CorrelationMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ServiceError)
async def service_error_handler(request, exc: ServiceError):
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message, "detail": exc.detail}},
    )


app.include_router(auth.router)
app.include_router(engagements.router)
```

### Rules

- Middleware order matters: CorrelationMiddleware first (sets correlation_id), then LoggingMiddleware (uses it), then CORS.
- The `ServiceError` exception handler is registered on the app, catching all service exceptions uniformly.
- Route modules are included via `app.include_router()` at the bottom.
- The `lifespan` context manager handles startup/shutdown (DB pool initialization, cleanup).

---

## 11. PostgreSQL Connection Factory

Source: `phase-0-foundations.mdc` line 48 (SQLAlchemy Core), `Infrastructure_Specification.md`

File location: `src/shared/db/postgres.py`

```python
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.shared.config.settings import settings

_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def get_engine() -> AsyncEngine:
    global _engine
    if _engine is None:
        _engine = create_async_engine(
            settings.database_url,
            pool_size=settings.database_pool_size,
            max_overflow=settings.database_max_overflow,
            echo=False,
        )
    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    global _session_factory
    if _session_factory is None:
        _session_factory = async_sessionmaker(
            get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
        )
    return _session_factory


async def dispose_engine() -> None:
    global _engine, _session_factory
    if _engine is not None:
        await _engine.dispose()
        _engine = None
        _session_factory = None
```

### Rules

- One engine per process. Created lazily on first use.
- `expire_on_commit=False` because we use SQLAlchemy Core (no ORM identity map to expire).
- `dispose_engine()` is called from the FastAPI lifespan shutdown handler.
- Pool size and overflow are sourced from `Settings` (§9), not hardcoded.
- The `database_url` must use the `postgresql+asyncpg://` scheme for async support.

---

## 12. get_db Dependency and Tenant Context

Source: `Authentication_Middleware_Specification.md`, `phase-0-foundations.mdc` line 63

File location: `src/api/dependencies/db.py`

```python
from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.db.postgres import get_session_factory


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    factory = get_session_factory()
    async with factory() as session:
        yield session
```

Tenant context injection (in `src/api/dependencies/auth.py`, called by `get_tenant_context`):

```python
async def _set_tenant_context(db: AsyncSession, tenant_id: str) -> None:
    await db.execute(text(f"SET app.current_tenant_id = '{tenant_id}'"))
```

This is called within the `get_tenant_context` dependency after JWT validation, before the route handler runs. It enables RLS policies for the entire request.

### Rules

- `get_db` yields a single session per request (FastAPI dependency lifecycle).
- The session is NOT committed inside `get_db`. Service functions own the transaction boundary (§3).
- Tenant context is set via `SET app.current_tenant_id` on the PostgreSQL session, enabling RLS.
- Use parameterized queries for all data operations, but `SET` is a session variable assignment (not a data query) and uses string formatting.

---

## 13. ClickHouse Client Factory

Source: `phase-0-foundations.mdc` line 49 (clickhouse-connect), `Infrastructure_Specification.md`

File location: `src/shared/db/clickhouse.py`

```python
import clickhouse_connect
from clickhouse_connect.driver import Client

from src.shared.config.settings import settings

_client: Client | None = None


def get_clickhouse_client() -> Client:
    global _client
    if _client is None:
        _client = clickhouse_connect.get_client(
            host=settings.clickhouse_host,
            port=settings.clickhouse_port,
            database=settings.clickhouse_database,
            username=settings.clickhouse_user,
            password=settings.clickhouse_password,
        )
    return _client


def close_clickhouse_client() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None
```

### Rules

- One client per process. Created lazily on first use.
- `close_clickhouse_client()` is called from the FastAPI lifespan shutdown handler.
- ClickHouse is read-heavy. Most writes are bulk inserts from ETL pipelines (Celery tasks), not request-scoped.
- All connection parameters come from `Settings` (§9).
- ClickHouse does not use SQLAlchemy. All queries use the `clickhouse_connect` client API directly.

---

## 14. SQLAlchemy Core Table Definitions

Source: `Database_Schema_Specification.md`, `phase-0-foundations.mdc` line 48

File location: `src/shared/db/tables.py`

```python
import sqlalchemy as sa

metadata = sa.MetaData()

tenant_table = sa.Table(
    "tenant",
    metadata,
    sa.Column("tenant_id", sa.dialects.postgresql.UUID, primary_key=True),
    sa.Column("name", sa.Text, nullable=False),
    sa.Column("slug", sa.Text, nullable=False, unique=True),
    sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
)

user_account_table = sa.Table(
    "user_account",
    metadata,
    sa.Column("user_id", sa.dialects.postgresql.UUID, primary_key=True),
    sa.Column("tenant_id", sa.dialects.postgresql.UUID, sa.ForeignKey("tenant.tenant_id"), nullable=False),
    sa.Column("email", sa.Text, nullable=False),
    sa.Column("role", sa.Text, nullable=False),
    sa.Column("display_name", sa.Text),
    sa.Column("auth_provider_id", sa.Text),
    sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
)

audit_log_table = sa.Table(
    "audit_log",
    metadata,
    sa.Column("log_id", sa.dialects.postgresql.UUID, primary_key=True),
    sa.Column("tenant_id", sa.dialects.postgresql.UUID, sa.ForeignKey("tenant.tenant_id"), nullable=False),
    sa.Column("user_id", sa.dialects.postgresql.UUID),
    sa.Column("action", sa.Text, nullable=False),
    sa.Column("entity_type", sa.Text, nullable=False),
    sa.Column("entity_id", sa.dialects.postgresql.UUID, nullable=False),
    sa.Column("before_value", sa.dialects.postgresql.JSONB),
    sa.Column("after_value", sa.dialects.postgresql.JSONB),
    sa.Column("reason", sa.Text),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
)
```

### Rules

- One shared `metadata` object. All tables are defined in this file.
- Table objects are hand-written to match the DDL in `Database_Schema_Specification.md` exactly. Column names, types, and constraints must be verified against the DDL.
- This file is NOT generated by `codegen/generate_models.py`. The generator produces Pydantic models, not SQLAlchemy table definitions.
- Add tables incrementally as each migration creates them: Phase 0 adds Domain 1 + Layer A + Phase 0 Domain 2/10 tables; Phase 1 adds Domains 2-13.
- Repository functions import specific tables from this module (see §4).

---

## 15. S3 Storage Wrapper

Source: `phase-0-foundations.mdc` line 50 (boto3, MinIO), `Infrastructure_Specification.md`

File location: `src/shared/storage/s3.py`

```python
from typing import BinaryIO

import boto3
from botocore.exceptions import ClientError

from src.shared.config.settings import settings

_s3_client = None


def _get_client():
    global _s3_client
    if _s3_client is None:
        _s3_client = boto3.client(
            "s3",
            endpoint_url=settings.s3_endpoint_url,
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
        )
    return _s3_client


def upload_file(
    bucket: str, key: str, body: BinaryIO, content_type: str = "application/octet-stream"
) -> str:
    _get_client().upload_fileobj(
        body, bucket, key, ExtraArgs={"ContentType": content_type}
    )
    return f"s3://{bucket}/{key}"


def download_file(bucket: str, key: str) -> bytes:
    response = _get_client().get_object(Bucket=bucket, Key=key)
    return response["Body"].read()


def file_exists(bucket: str, key: str) -> bool:
    try:
        _get_client().head_object(Bucket=bucket, Key=key)
        return True
    except ClientError:
        return False


def list_objects(bucket: str, prefix: str) -> list[str]:
    response = _get_client().list_objects_v2(Bucket=bucket, Prefix=prefix)
    return [obj["Key"] for obj in response.get("Contents", [])]
```

### Rules

- S3 client is created lazily. Local dev uses MinIO (S3-compatible) via `endpoint_url`.
- `upload_file` returns the full `s3://` URI for storage in database columns.
- All S3 operations are synchronous (boto3 default). For large uploads in request handlers, delegate to a Celery task.
- Bucket names come from `Settings` (§9). Key structure follows `Infrastructure_Specification.md` (e.g., `{tenant_id}/evidence/{assessment_id}/{filename}`).

---

## 16. Celery App Factory

Source: `ADR-014-task-queue.md`, `phase-0-foundations.mdc` line 56

File location: `src/shared/celery_app.py`

```python
from celery import Celery

from src.shared.config.settings import settings

celery_app = Celery(
    "partners",
    broker=settings.redis_url,
    backend=settings.celery_result_backend,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)

celery_app.autodiscover_tasks(
    [
        "src.services.engagement",
        "src.services.import_mapping",
        "src.services.temporal_state",
        "src.services.metric_engine",
        "src.services.scoring_engine",
        "src.services.finding_compiler",
        "src.services.impact_engine",
        "src.services.report_rendering",
    ]
)
```

### Rules

- One `celery_app` instance imported by all task modules.
- `autodiscover_tasks` lists all services that define `tasks.py` files. Update this list as new services are added in later phases.
- `task_acks_late=True` and `worker_prefetch_multiplier=1` ensure tasks are not lost if a worker crashes mid-execution.
- Broker and backend URLs come from `Settings` (§9).
- JSON serialization only (no pickle) for security and debuggability.

---

## 17. Worker Entry Point

Source: `ADR-014-task-queue.md`, `phase-0-foundations.mdc` line 56

File location: `src/worker.py`

```python
from src.shared.celery_app import celery_app  # noqa: F401
```

Started via: `celery -A src.worker worker --loglevel=info`

### Rules

- The worker entry point imports the celery app, which triggers `autodiscover_tasks`.
- The file contains only the import. No additional logic.
- The `# noqa: F401` suppresses the unused-import lint warning (the import has the side effect of registering tasks).

---

## 18. Auth Routes

Source: `Authentication_Middleware_Specification.md`, `API_Design_Specification.md`

File location: `src/api/routes/auth.py`

```python
from fastapi import APIRouter, Depends

from src.api.dependencies.auth import get_current_user, CurrentUser

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.get(
    "/me",
    response_model=CurrentUser,
    status_code=200,
    summary="Get current authenticated user",
)
async def get_me(
    user: CurrentUser = Depends(get_current_user),
):
    return user
```

### Rules

- `GET /api/auth/me` is the only auth route in the platform API. Login/registration are handled by AWS Cognito (ADR-015).
- This endpoint validates that the JWT is valid and returns the decoded user identity.
- Used by the frontend to confirm authentication state on page load.
- The `CurrentUser` model is defined in `src/api/dependencies/auth.py` and contains: `user_id`, `tenant_id`, `email`, `role`, `display_name`.
