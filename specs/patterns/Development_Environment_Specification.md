# Development Environment Specification

Provides the exact Docker Compose configuration, Alembic workflow, ClickHouse migration process, and local development setup steps. This document complements `Infrastructure_Specification.md` (which defines what services exist) with the implementation-ready details of how to run them locally.

---

## Sources

- `Infrastructure_Specification.md` — Service definitions, ports, env vars, S3 bucket structure
- `Project_Skeleton_Specification.md` lines 70–71 — `docker/docker-compose.yml`, `docker/docker-compose.test.yml`
- `phase-0-foundations.mdc` lines 46–57 — Technology constraints
- `Implementation_Tasks.md` — P0-T02 (Docker Compose), P0-T07 (Alembic), P0-T10 (ClickHouse schema)
- `Database_Schema_Specification.md` — All DDL (110 PostgreSQL tables, 15 ClickHouse tables)

---

## 1. Docker Compose — Local Development

File: `docker/docker-compose.yml`

```yaml
services:
  postgres:
    image: postgres:16
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: partners
    volumes:
      - pg_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 3s
      retries: 5

  clickhouse:
    image: clickhouse/clickhouse-server
    ports:
      - "8123:8123"
      - "9000:9000"
    volumes:
      - ch_data:/var/lib/clickhouse
    healthcheck:
      test: ["CMD", "clickhouse-client", "--query", "SELECT 1"]
      interval: 5s
      timeout: 3s
      retries: 5

  minio:
    image: minio/minio
    ports:
      - "9090:9000"
      - "9091:9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    command: server /data --console-address ":9001"
    volumes:
      - minio_data:/data
    healthcheck:
      test: ["CMD", "mc", "ready", "local"]
      interval: 5s
      timeout: 3s
      retries: 5

  redis:
    image: redis:7
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

volumes:
  pg_data:
  ch_data:
  minio_data:
```

Source: `Infrastructure_Specification.md` lines 23–28 (service names, images, ports).

### Notes

- Python services (FastAPI, Celery worker) run on the host, not in containers, for fast iteration.
- MinIO maps container port 9000 to host port 9090 to avoid conflict with ClickHouse native port 9000.
- MinIO console is available at `http://localhost:9091`.
- All data is persisted in named Docker volumes. Run `docker compose down -v` to reset all data.

---

## 2. Docker Compose — CI Test Stack

File: `docker/docker-compose.test.yml`

```yaml
services:
  postgres-test:
    image: postgres:16
    ports:
      - "5433:5432"
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: partners_test
    tmpfs:
      - /var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 3s
      timeout: 2s
      retries: 10

  clickhouse-test:
    image: clickhouse/clickhouse-server
    ports:
      - "8124:8123"
      - "9001:9000"
    tmpfs:
      - /var/lib/clickhouse
    healthcheck:
      test: ["CMD", "clickhouse-client", "--query", "SELECT 1"]
      interval: 3s
      timeout: 2s
      retries: 10

  minio-test:
    image: minio/minio
    ports:
      - "9092:9000"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    command: server /data
    tmpfs:
      - /data

  redis-test:
    image: redis:7
    ports:
      - "6380:6379"
    tmpfs:
      - /data
```

### Notes

- All test services use different host ports to allow concurrent dev and CI runs.
- `tmpfs` mounts ensure no data persists between test runs. Each CI run starts clean.
- CI workflow starts the test stack, waits for health checks, runs migrations, then executes tests.

---

## 3. Alembic Workflow (PostgreSQL Migrations)

### Directory Structure

Source: `Project_Skeleton_Specification.md` lines 84–89.

```
db/
  postgresql/
    migrations/
      env.py               # Alembic environment configuration
      alembic.ini           # Alembic settings (points to env.py)
      versions/             # Migration files
        001_tenancy_identity.py
        002_raw_evidence_layer.py
        003_asset_domain.py
        004_resident_lease_domain.py
        ...
```

### Migration Naming Convention

Migrations are manually numbered with a 3-digit prefix:

```
{NNN}_{descriptive_name}.py
```

Phase 0 migrations: `001_` through `004_`.
Phase 1 migrations: `005_` through `013_`.
Phase 2+ migrations continue sequentially.

Source: `Implementation_Tasks.md` — P0-T08 (`001_`), P0-T09 (`002_`), P0-T09a (`003_`), P0-T09b (`004_`), P1-T01 (`005_`), etc.

### Migration File Template

Every migration file must follow this structure:

```python
"""NNN: Descriptive title.

Tables created: table_a, table_b, table_c
RLS policies: table_a, table_b (if tenant-scoped)
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = "NNN_descriptive_name"
down_revision = "NNN-1_previous_name"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create tables
    op.create_table(
        "table_name",
        sa.Column("id", UUID(), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        # ... columns from DDL ...
    )
    # Create indexes
    op.create_index("idx_table_name_column", "table_name", ["column"])
    # Enable RLS (for tenant-scoped tables)
    op.execute("ALTER TABLE table_name ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE table_name FORCE ROW LEVEL SECURITY")
    op.execute("""
        CREATE POLICY tenant_isolation ON table_name
        USING (tenant_id = current_setting('app.current_tenant_id')::uuid)
    """)


def downgrade() -> None:
    op.drop_table("table_name")
```

### Alembic Commands

| Command | Purpose |
|---------|---------|
| `alembic upgrade head` | Apply all pending migrations |
| `alembic downgrade -1` | Rollback the most recent migration |
| `alembic current` | Show current migration version |
| `alembic history` | Show migration history |

### Rules

1. Every migration must have a working `downgrade()` function.
2. All columns, constraints, and indexes from `Database_Schema_Specification.md` must be included.
3. RLS policies must be created for every tenant-scoped table (see RLS section in `Database_Schema_Specification.md`).
4. Never use `op.execute()` with dynamic user input.
5. Test migrations with `alembic upgrade head && alembic downgrade base && alembic upgrade head` to verify round-trip.

### `alembic.ini` Template

File: `db/postgresql/migrations/alembic.ini`

```ini
[alembic]
script_location = db/postgresql/migrations
sqlalchemy.url = postgresql+asyncpg://postgres:postgres@localhost:5432/partners

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

### `env.py` Template

File: `db/postgresql/migrations/env.py`

```python
import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

from src.shared.config.settings import settings

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_offline() -> None:
    context.configure(
        url=settings.database_url,
        target_metadata=None,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    context.configure(connection=connection, target_metadata=None)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    connectable = create_async_engine(settings.database_url)
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
```

### env.py Rules

- `env.py` reads the database URL from `Settings` (Code_Patterns_Specification.md §9), not from alembic.ini. The sqlalchemy.url key in alembic.ini is a fallback only.
- The async pattern (`create_async_engine` + `run_sync`) is required because the application uses `asyncpg`.
- `target_metadata=None` because we use hand-written migrations (not autogenerate).

---

## 4. ClickHouse Migrations

ClickHouse does not use Alembic. Migrations are versioned SQL files executed in order.

### Directory Structure

```
db/
  clickhouse/
    migrations/
      001_initial_schema.sql
      002_phase2_temporal_facts.sql
      003_phase3_score_finding_facts.sql
      ...
```

Source: `phase-0-foundations.mdc` line 52, `Implementation_Tasks.md` — P0-T10 (`001_`), P2-T14 (`002_`), P3-T21 (`003_`).

### Migration Execution

ClickHouse SQL files are executed by the application or a deployment script using `clickhouse-connect`:

```python
import clickhouse_connect

client = clickhouse_connect.get_client(host="localhost", port=8123, database="partners")

with open("db/clickhouse/migrations/001_initial_schema.sql") as f:
    for statement in f.read().split(";"):
        statement = statement.strip()
        if statement:
            client.command(statement)
```

### ClickHouse Table Engine and Partitioning

All ClickHouse fact tables use `ReplacingMergeTree` with:
- `ORDER BY` matching the primary query patterns
- Partitioning by date or assessment_id (depending on table)

Source: `Database_Schema_Specification.md` Layer C ClickHouse section.

---

## 5. MinIO Bucket Initialization

On first startup, the S3 evidence and reports buckets must be created in MinIO:

```bash
# Using the MinIO client (mc)
mc alias set local http://localhost:9090 minioadmin minioadmin
mc mb local/partners-evidence
mc mb local/partners-reports
```

Or programmatically in Python during app initialization:

```python
import boto3

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9090",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin",
)

for bucket in ["partners-evidence", "partners-reports"]:
    try:
        s3.create_bucket(Bucket=bucket)
    except s3.exceptions.BucketAlreadyOwnedByYou:
        pass
```

Source: `Infrastructure_Specification.md` lines 106–108 (bucket names).

---

## 6. Local Development Workflow

### Initial Setup

```bash
# 1. Clone the repository
git clone git@github-takanfer:takanfer/RBV2.git
cd RBv2

# 2. Install Python dependencies
uv sync

# 3. Start the data stack
docker compose -f docker/docker-compose.yml up -d

# 4. Wait for services to be healthy
docker compose -f docker/docker-compose.yml ps  # all should show "healthy"

# 5. Create MinIO buckets
mc alias set local http://localhost:9090 minioadmin minioadmin
mc mb local/partners-evidence
mc mb local/partners-reports

# 6. Run PostgreSQL migrations
alembic upgrade head

# 7. Run ClickHouse migrations
python -m src.shared.db.clickhouse_migrate  # (or equivalent script)

# 8. Copy .env.example to .env
cp .env.example .env

# 9. Start the API server
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# 10. Start the Celery worker (in a separate terminal)
celery -A src.shared.celery_app worker --loglevel=info
```

### Daily Development

```bash
# Start data stack (if not already running)
docker compose -f docker/docker-compose.yml up -d

# Run tests
pytest

# Run linter
ruff check src/ tests/

# Format code
ruff format src/ tests/

# Apply new migrations after pulling changes
alembic upgrade head
```

### Teardown

```bash
# Stop containers (preserve data)
docker compose -f docker/docker-compose.yml down

# Stop and delete all data
docker compose -f docker/docker-compose.yml down -v
```

---

## Authoritative Sources

- `Infrastructure_Specification.md` — Service definitions, ports, env vars, S3 structure, production topology
- `Project_Skeleton_Specification.md` — Repository structure, directory layout, CI/CD steps
- `phase-0-foundations.mdc` — Technology constraints (Alembic, ClickHouse migrations)
- `Implementation_Tasks.md` — Migration numbering per phase
- `Database_Schema_Specification.md` — All DDL for migrations

---

## 7. GitHub Actions CI Workflow

Source: `Project_Skeleton_Specification.md` §7.1 (lines 384-394)

File: `.github/workflows/ci.yml`

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - run: uv sync --frozen
      - run: uv run ruff check src/ tests/
      - run: uv run ruff format --check src/ tests/

  test-unit:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - run: uv sync --frozen
      - run: uv run pytest tests/unit/ -v

  test-integration:
    runs-on: ubuntu-latest
    needs: lint
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: partners_test
        ports:
          - 5432:5432
        options: >-
          --health-cmd "pg_isready -U postgres"
          --health-interval 5s
          --health-timeout 3s
          --health-retries 5
      clickhouse:
        image: clickhouse/clickhouse-server
        ports:
          - 8123:8123
        options: >-
          --health-cmd "clickhouse-client --query 'SELECT 1'"
          --health-interval 5s
          --health-timeout 3s
          --health-retries 5
      redis:
        image: redis:7
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 5s
          --health-timeout 3s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - run: uv sync --frozen
      - name: Run migrations
        env:
          DATABASE_URL: postgresql+asyncpg://postgres:postgres@localhost:5432/partners_test
        run: uv run alembic upgrade head
      - name: Run integration tests
        env:
          DATABASE_URL: postgresql+asyncpg://postgres:postgres@localhost:5432/partners_test
          CLICKHOUSE_HOST: localhost
          CLICKHOUSE_PORT: 8123
          REDIS_URL: redis://localhost:6379/0
        run: uv run pytest tests/integration/ -v
```

### Rules

- Lint runs first; test jobs depend on lint passing.
- Unit tests run without external services (all deps are mocked).
- Integration tests use GitHub Actions service containers (not testcontainers) for consistency.
- Branch protection on `main` requires CI to pass before merge.
- `uv sync --frozen` ensures reproducible installs from the lockfile.
