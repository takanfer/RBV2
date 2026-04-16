# Project Skeleton Specification

Locked technical decisions, monorepo structure, naming conventions, toolchain, testing strategy, and CI/CD for the Multifamily Property Assessment Platform.

**Authority:** Every decision in this document is locked by an accepted ADR (see `docs/adrs/`). Changes require a new superseding ADR.

---

## 1. Technology Stack

### 1.1 Backend

| Component | Technology | ADR |
|-----------|-----------|-----|
| Language | Python 3.11+ | ADR-001 |
| API Framework | FastAPI (async, Pydantic-native, auto OpenAPI) | ADR-002 |
| PostgreSQL Access | SQLAlchemy Core (expression language, not ORM) | ADR-003 |
| ClickHouse Access | clickhouse-connect (official Python driver) | ADR-003 |
| Migrations (PostgreSQL) | Alembic | ADR-004 |
| Package Manager | uv | ADR-005 |
| Testing | pytest + pytest-asyncio + pytest-mock + testcontainers | ADR-006 |
| Lint / Format | ruff (replaces black, isort, flake8) | ADR-007 |
| Local Dev Infrastructure | Docker Compose | ADR-008 |

### 1.2 Frontend

| Component | Technology | ADR |
|-----------|-----------|-----|
| Framework | Next.js (App Router) | ADR-009 |
| Language | TypeScript (strict mode) | ADR-009 |
| Styling | Tailwind CSS | ADR-009 |
| Component Library | shadcn/ui | ADR-009 |
| Data Tables | TanStack Table | ADR-009 |
| Charts | Recharts (standard) / D3 (custom) | ADR-009 |
| Data Fetching | TanStack Query | ADR-009 |
| Forms / Validation | React Hook Form + Zod | ADR-009 |
| Mobile Field Capture | PWA (offline service workers) | ADR-010 |

### 1.3 Infrastructure

| Component | Technology | ADR |
|-----------|-----------|-----|
| Cloud Provider | AWS (not multi-cloud) | ADR-013 |
| PostgreSQL | RDS PostgreSQL or Aurora PostgreSQL | ADR-013 |
| ClickHouse | ClickHouse Cloud on AWS | ADR-013 |
| Object Storage | S3 | ADR-013 |
| Containers | ECS (Fargate) | ADR-013 |
| Secrets | Secrets Manager | ADR-013 |
| DNS / CDN | Route 53 / CloudFront | ADR-013 |
| Monitoring | CloudWatch | ADR-013 |
| Repository | Monorepo (single repo for all platform code) | ADR-011 |
| CI/CD | GitHub Actions | ADR-012 |

---

## 2. Repository Structure

```
/
├── pyproject.toml                    # Python deps, pytest config, ruff config
├── uv.lock                          # Locked Python deps (committed)
├── .env                             # Local connection strings (not committed)
├── .env.example                     # Template with local-dev defaults (committed)
├── .github/
│   └── workflows/
│       ├── ci.yml                   # Lint + test on push
│       └── deploy.yml               # Build + migrate + deploy on merge to main
├── .cursor/
│   └── rules/                       # Cursor project rules (.mdc files)
├── docker/
│   ├── docker-compose.yml           # Local data stack (PG, CH, MinIO, Redis)
│   └── docker-compose.test.yml      # CI integration DBs
├── docs/
│   ├── adrs/                        # Architecture Decision Records
│   ├── spec_1_multifamily_property_assessment_platform.md
│   ├── Complete_Data_Inventory.md
│   ├── Audit_Workbook_Specification.md
│   ├── Scoring_Model_Specification.md
│   ├── Database_Schema_Specification.md
│   ├── Shared_Type_Definitions.md
│   ├── Project_Skeleton_Specification.md
│   ├── Data_Onramp_Specification.md
│   └── Service_Interface_Contracts.md
├── db/
│   ├── postgresql/
│   │   └── migrations/
│   │       ├── env.py               # Alembic environment
│   │       ├── alembic.ini
│   │       └── versions/            # Alembic migration files
│   └── clickhouse/
│       └── migrations/              # Versioned ClickHouse SQL (not Alembic)
├── src/
│   ├── __init__.py
│   ├── shared/
│   │   ├── __init__.py
│   │   ├── models/                  # Pydantic v2 models (generated from DDL)
│   │   │   ├── __init__.py
│   │   │   ├── asset.py
│   │   │   ├── lease.py
│   │   │   ├── operations.py
│   │   │   ├── demand.py
│   │   │   ├── marketing.py
│   │   │   ├── competitive.py
│   │   │   ├── field_evidence.py
│   │   │   ├── assessment.py
│   │   │   ├── scoring_config.py
│   │   │   ├── workspace.py
│   │   │   ├── infrastructure.py
│   │   │   ├── raw_evidence.py
│   │   │   ├── intake_snapshot.py
│   │   │   └── clickhouse_facts.py
│   │   ├── db/                      # Shared connection factories
│   │   │   ├── __init__.py
│   │   │   ├── postgres.py          # SQLAlchemy Core engine/session
│   │   │   └── clickhouse.py        # clickhouse-connect client
│   │   ├── config/
│   │   │   ├── __init__.py
│   │   │   └── settings.py          # Pydantic Settings (single Settings class)
│   │   ├── storage/
│   │   │   ├── __init__.py
│   │   │   └── s3.py                # S3/MinIO client factory
│   │   ├── audit.py                 # Audit log helper (insert-only, never commits)
│   │   ├── celery_app.py            # Celery application factory
│   │   └── sdk/                     # Extension SDK (Phase 6)
│   │       ├── __init__.py
│   │       ├── connector_sdk.py     # Vendor adapter registration
│   │       ├── package_sdk.py       # Diagnostic package registration
│   │       ├── rubric_sdk.py        # Rubric version registration
│   │       └── fact_grain_sdk.py    # ClickHouse fact grain registration
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI app initialization, lifespan, exception handlers
│   │   ├── dependencies/            # FastAPI dependency injection
│   │   │   ├── __init__.py
│   │   │   ├── auth.py              # get_current_user, get_tenant_context
│   │   │   └── db.py                # get_db session dependency
│   │   └── routes/                  # FastAPI routers
│   │       ├── __init__.py
│   │       └── ...                  # One module per domain
│   ├── services/
│   │   ├── __init__.py
│   │   ├── base_exceptions.py       # ServiceError base class (all services import)
│   │   ├── engagement/              # Engagement Service
│   │   │   ├── __init__.py
│   │   │   ├── service.py
│   │   │   └── repository.py
│   │   ├── import_mapping/          # Import & Mapping Service
│   │   │   ├── __init__.py
│   │   │   ├── service.py
│   │   │   ├── repository.py
│   │   │   ├── mapping.py
│   │   │   └── tasks.py
│   │   ├── entity_resolution/       # Entity Resolution Service
│   │   │   ├── __init__.py
│   │   │   ├── service.py
│   │   │   └── repository.py
│   │   ├── temporal_state/          # Temporal State Builder
│   │   │   ├── __init__.py
│   │   │   ├── service.py
│   │   │   └── repository.py
│   │   ├── metric_engine/           # Metric Engine
│   │   │   ├── __init__.py
│   │   │   ├── service.py
│   │   │   ├── repository.py
│   │   │   └── registry.py
│   │   ├── scoring_engine/          # Scoring Engine
│   │   │   ├── __init__.py
│   │   │   ├── service.py
│   │   │   ├── repository.py
│   │   │   └── aggregation.py
│   │   ├── finding_compiler/        # Finding Compiler
│   │   │   ├── __init__.py
│   │   │   ├── service.py
│   │   │   └── repository.py
│   │   ├── impact_engine/           # Impact Engine
│   │   │   ├── __init__.py
│   │   │   ├── service.py
│   │   │   └── repository.py
│   │   ├── study_snapshot/          # Study & Snapshot Service
│   │   │   ├── __init__.py
│   │   │   ├── service.py
│   │   │   └── repository.py
│   │   ├── report_rendering/        # Report Rendering Service
│   │   │   ├── __init__.py
│   │   │   ├── service.py
│   │   │   └── repository.py
│   │   ├── client_portal/           # Client Portal Service
│   │   │   ├── __init__.py
│   │   │   ├── service.py
│   │   │   └── repository.py
│   │   ├── trend_trajectory/        # Trend & Trajectory Service
│   │   │   ├── __init__.py
│   │   │   ├── service.py
│   │   │   └── repository.py
│   │   ├── door_opener/             # Door Opener Service
│   │   │   ├── __init__.py
│   │   │   ├── service.py
│   │   │   └── repository.py
│   │   └── authz/                   # AuthZ / Tenant Policy
│   │       ├── __init__.py
│   │       ├── service.py
│   │       └── repository.py
│   ├── scoring_config/
│   │   └── scoring_config.json      # Machine-readable scoring rubric
│   └── worker.py                    # Celery worker entry point
├── frontend/
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.js
│   ├── tailwind.config.ts
│   └── src/
│       ├── app/                     # Next.js App Router pages
│       ├── components/
│       │   └── ui/                  # shadcn/ui components
│       ├── hooks/
│       ├── lib/
│       └── types/
├── tests/
│   ├── __init__.py
│   ├── conftest.py                  # Shared pytest fixtures
│   ├── fixtures/
│   │   └── golden_property/         # Golden property test data
│   ├── unit/                        # Fast isolated tests
│   └── integration/                 # Tests with real DB (testcontainers)
└── codegen/
    ├── generate_models.py           # DDL-to-Pydantic generation script
    ├── validate_docs.py             # Cross-reference documentation validator
    ├── test_ddl.sql                 # Test fixtures for generator
    └── expected_asset.py            # Answer key for test fixtures
```

---

## 3. Application Services

The platform has 11 named application services (spec_1 §2, reference architecture diagram lines 131-142). Phases 5-6 add 4 more services (Client Portal, Trend & Trajectory, Door Opener, Extension SDK) defined in `Service_Interface_Contracts.md` §12-15. Each lives in `src/services/<name>/` with a consistent internal layout.

| # | Service | Directory | Responsibility |
|---|---------|-----------|---------------|
| 1 | Engagement Service | `engagement/` | Assessment lifecycle, comp set management, workflow state |
| 2 | Import & Mapping Service | `import_mapping/` | File parsing, vendor adapters, column mapping, review queue |
| 3 | Entity Resolution Service | `entity_resolution/` | Unit alias matching, source key dedup, merge/split |
| 4 | Temporal State Builder | `temporal_state/` | Materializes `fact_unit_day`, vacancy cycles, make-ready cycles |
| 5 | Metric Engine | `metric_engine/` | Computes KPIs from fact tables (124 Basic Analytic Data Set) |
| 6 | Scoring Engine | `scoring_engine/` | Applies scoring rubric to metrics → score_result rows |
| 7 | Finding Compiler | `finding_compiler/` | Generates findings from rule packages |
| 8 | Impact Engine | `impact_engine/` | Financial impact estimation, simulated optimal budget |
| 9 | Study & Snapshot Service | `study_snapshot/` | Saved investigations, comparison boards, annotations, exports |
| 10 | Report Rendering Service | `report_rendering/` | Report generation, section assembly, PDF/HTML rendering |
| 11 | AuthZ / Tenant Policy | `authz/` | Multi-tenant access control, row-level security |

### Service internal layout

Each service follows the same pattern:

```
src/services/<name>/
├── __init__.py
├── service.py          # Business logic (pure Python, no DB imports)
└── repository.py       # DB queries (SQLAlchemy Core for PG, clickhouse-connect for CH)
```

**Conventions:**
- `service.py` contains business logic and orchestration. It accepts and returns Pydantic models from `src/shared/models/`.
- `repository.py` contains all database access. Queries use SQLAlchemy Core expression language for PostgreSQL and clickhouse-connect for ClickHouse.
- Services may call each other via direct Python imports (not HTTP) when running in the same process.
- FastAPI route handlers in `src/api/routes/` delegate to services; they do not contain business logic.

---

## 4. Naming Conventions

### 4.1 Python

| Element | Convention | Example |
|---------|-----------|---------|
| Modules | `snake_case` | `import_mapping`, `metric_engine` |
| Classes | `PascalCase` | `UnitVersion`, `ScoreResult` |
| Functions | `snake_case` | `compute_vacancy_days` |
| Constants | `UPPER_SNAKE` | `MAX_RETRY_COUNT` |
| Pydantic models | `PascalCase`, one per DB table | `Property`, `FactUnitDay` |
| Test files | `test_*.py` | `test_scoring_engine.py` |

### 4.2 Database

| Element | Convention | Example |
|---------|-----------|---------|
| Tables | `snake_case` | `unit_version`, `fact_unit_day` |
| Columns | `snake_case` | `lease_start`, `monthly_rent` |
| Primary keys | `<table_singular>_id` | `property_id`, `lease_id` |
| Foreign keys | Same name as referenced PK | `property_id references property(property_id)` |
| Indexes | `idx_<table>_<columns>` | `idx_lease_unit` |
| ClickHouse facts | `fact_<entity>_<grain>` | `fact_unit_day`, `fact_lease_interval` |

### 4.3 Frontend

| Element | Convention | Example |
|---------|-----------|---------|
| Components | `PascalCase` files, named exports | `ScoreCard.tsx` |
| Hooks | `use<Name>` | `useAssessment` |
| API types | Generated from FastAPI OpenAPI spec | `Property`, `ScoreResult` |

### 4.4 Domain terminology

These terms are locked and must be used consistently across all code and documentation:

| Correct | Incorrect alternatives |
|---------|----------------------|
| Area → Item → Sub-item | dimension, category, metric |
| Data / Checklist / Comparative (input types) | Benchmark, Metric |
| Good / Fair / Poor / Critical (condition ratings) | End of Life |
| 12 areas, 65 items, 315 sub-items | any other counts |

---

## 5. Configuration

### 5.1 `pyproject.toml`

Single configuration file at repo root for all Python tooling:

```toml
[project]
name = "partners-platform"
requires-python = ">=3.11"

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"

[tool.ruff]
target-version = "py311"
line-length = 120
```

### 5.2 Docker Compose (local development)

File: `docker/docker-compose.yml`

| Service | Image | Purpose |
|---------|-------|---------|
| postgres | `postgres:16` | Canonical OLTP store |
| clickhouse | `clickhouse/clickhouse-server` | Analytical warehouse |
| minio | `minio/minio` | S3-compatible object storage |
| redis | `redis:7` | Celery message broker and result backend (ADR-014) |

Python services run on the host (not in containers) for fast iteration. Connect via `.env` connection strings.

Test stack (`docker/docker-compose.test.yml`) provides isolated DBs for CI integration tests.

---

## 6. Testing Strategy

### 6.1 Test categories

| Category | Location | Dependencies | Speed |
|----------|---------|-------------|-------|
| Unit | `tests/unit/` | None (mocked) | Fast |
| Integration | `tests/integration/` | Real PG + CH (testcontainers) | Slower |

### 6.2 Golden property

`tests/fixtures/golden_property/` contains a complete test dataset for one property: rent roll, leases, work orders, vacancy cycles, mystery shop, financials, and scored results. Used for end-to-end validation of the analytical pipeline.

### 6.3 Test conventions

- Shared fixtures in `tests/conftest.py`
- Each test file corresponds to a service or module: `test_<name>.py`
- Integration tests use testcontainers to spin up real PostgreSQL and ClickHouse instances
- pytest-asyncio for async test functions
- pytest-mock for dependency isolation

---

## 7. CI/CD

### 7.1 Continuous Integration (`.github/workflows/ci.yml`)

Triggered on every push:

1. `ruff check` — lint violations fail the build
2. `ruff format --check` — formatting violations fail the build
3. `pytest tests/unit/` — unit tests
4. `pytest tests/integration/` — integration tests (with testcontainers)
5. Matrix: runs against multiple Python versions

Branch protection: CI must pass before merge to `main`.

### 7.2 Continuous Deployment (`.github/workflows/deploy.yml`)

Triggered on merge to `main`:

1. Build Docker images
2. Run Alembic migrations against RDS PostgreSQL
3. Run ClickHouse migration scripts
4. Deploy to ECS (Fargate)
5. Docker layer caching for build speed

### 7.3 Prohibited

- No manual DDL in production (PostgreSQL migrations via Alembic only)
- No `--no-verify` or hook-skipping in CI
- No force push to `main`

---

## 8. Shared Models

All Pydantic v2 models live in `src/shared/models/` and are **generated** from the DDL in `Database_Schema_Specification.md` using `codegen/generate_models.py`.

**Do not hand-edit generated model files.** To change a model:
1. Update the DDL in `Database_Schema_Specification.md`
2. Run `python codegen/generate_models.py Database_Schema_Specification.md src/shared/models/`
3. Commit both the DDL change and the regenerated models

### 8.1 Domain modules

| Module | Tables | Description |
|--------|--------|-------------|
| `asset.py` | 11 | Property, building, unit, floor plan, amenities, market context |
| `lease.py` | 10 | Resident, lease, lease_charge, events, delinquency |
| `operations.py` | 15 | Work orders, vacancy cycles, condition observations, financials |
| `demand.py` | 9 | Leads, CRM events, conversion metrics |
| `marketing.py` | 13 | Listings, campaigns, website, social, reputation |
| `competitive.py` | 6 | Comp sets, comp listings, comp marketing |
| `field_evidence.py` | 4 | Mystery shop, vacant unit audit, interviews, tour observation |
| `assessment.py` | 12 | Assessment, scorecard, findings, impact, reports |
| `scoring_config.py` | 5 | Scoring rubric, benchmarks, metrics, diagnostic packages |
| `workspace.py` | 7 | Studies, saved queries, snapshots, annotations |
| `infrastructure.py` | 5 | Tenant, client, portfolio, user, audit log |
| `raw_evidence.py` | 6 | Source system, ingestion, raw records, mapping |
| `intake_snapshot.py` | 7 | Staffing, leasing model, tech platform, partnership snapshots |
| `clickhouse_facts.py` | 15 | All ClickHouse fact tables |

---

## 9. Key Constraints

1. **AI is advisory only** — AI does not write scores, findings, or the Impact Summary. The consultant is the final arbiter.
2. **Assessment-level date range variable** — All date-range-dependent metrics use the assessment's configured date range, not hardcoded trailing windows.
3. **Score != confidence** — Performance, evidence coverage, and certainty are stored separately.
4. **Diagnostics as versioned packages** — Each analytical domain ships as a package with inputs, metrics, rules, impact models, narratives, and recommendations.
5. **One engine, different scopes** — Full assessments and door openers use the same engine with an applicability matrix.

---

## Authoritative References

- `docs/adrs/ADR-001` through `ADR-016` — all locked technology decisions
- `spec_1_multifamily_property_assessment_platform.md` — platform requirements and service definitions
- `Database_Schema_Specification.md` — DDL (source of truth for all data structures)
- `scoring_config.json` — scoring rubric structure
- `.cursor/rules/rbv2-project.mdc` — cursor rules and naming conventions
