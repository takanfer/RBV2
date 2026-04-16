# Code Patterns Specification

Defines the exact code patterns every agent must follow when implementing any service, route, repository, test, or infrastructure module. This document contains literal code templates. Deviating from these patterns requires explicit user approval and a documented reason.

**Sources:**
- `Project_Skeleton_Specification.md` — service directory structure (lines 117-165), naming conventions §4 (lines 232-273), testing §6 (lines 314-334)
- `Service_Interface_Contracts.md` — 15 services, operation signatures, error categories (lines 490-501), audit logging (line 505)
- `API_Design_Specification.md` — URL patterns, response shapes, error format, pagination
- `Authentication_Middleware_Specification.md` — dependency chain, CurrentUser, TenantContext
- `Observability_Specification.md` — structured logging, correlation IDs, audit logging
- `Infrastructure_Specification.md` — environment variables, Pydantic Settings
- `phase-0-foundations.mdc` — SQLAlchemy Core (line 42), Pydantic Settings (line 48), testing rules (lines 62-67), code quality (lines 69-74)
- `ADR-002-api-framework.md` — FastAPI, Pydantic-native schemas, dependency injection
- `ADR-014-task-queue.md` — Celery tasks co-located with services (line 45)
- `rbv2-project.mdc` — DDL-first pipeline (lines 145-154), working principles (lines 156-164)

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
- All route decorators must include `response_model`, `status_code`, `summary`, and `tags`.

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

Source: `phase-0-foundations.mdc` line 42 (SQLAlchemy Core, not ORM)

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

Source: `Project_Skeleton_Specification.md` §6 (lines 314-334), `phase-0-foundations.mdc` lines 62-67

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

Source: `phase-0-foundations.mdc` line 48, `Infrastructure_Specification.md`

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
