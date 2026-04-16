# Implementation Tasks

Task-level implementation checklist for all 7 phases of the RBv2 Multifamily Property Assessment Platform. Every task is derived from a specific source document — no invented work. This is a working document; update checkboxes and status as tasks complete.

**Companion to:** `Deployment_Roadmap.md` (phase-level reference)
**Governance:** `.cursor/rules/agent-behavior.mdc` applies to all implementation work

---

## Progress Summary

| Phase | Total | Done | In Progress | Not Started |
|-------|-------|------|-------------|-------------|
| 0 — Foundations | 18 | 0 | 0 | 18 |
| 0-CK — Post-Phase 0 Checkpoint | 3 | 0 | 0 | 3 |
| 1 — Canonical Core & Import | 20 | 0 | 0 | 20 |
| 2 — Temporal Unit Spine | 12 | 0 | 0 | 12 |
| 3 — Core Diagnostics | 25 | 0 | 0 | 25 |
| 4 — Workspace & Reporting | 18 | 0 | 0 | 18 |
| 5 — Client Portal & Longitudinal | 15 | 0 | 0 | 15 |
| 6 — Door Opener & Extensibility | 12 | 0 | 0 | 12 |
| **Total** | **123** | **0** | **0** | **123** |

---

## How To Use This Document

**For agents:** Before starting any task, read the listed Refs documents. Do not work from memory. Check that all "Depends on" tasks are marked complete before starting. When done, check the box and note the commit hash.

**For the user:** Track progress by scanning checkboxes. The Progress Summary table should be updated when tasks complete.

**Task format:**
- `What:` describes the deliverable
- `Files:` specific files/directories created or modified
- `Refs:` source documents and line numbers the agent must read
- `Depends on:` prerequisite tasks (or "none")
- `Done when:` testable acceptance criterion

---

## Phase 0 — Foundations

> Cursor rule: `phase-0-foundations.mdc`
> Services: AuthZ (3 ops), Engagement (6 ops)
> Source: spec_1 lines 1307-1311

- [ ] **P0-T01: Project skeleton and Python tooling**
  - What: Create monorepo structure, `pyproject.toml` with Python 3.11+, pytest, ruff config, `uv.lock`
  - Files: `pyproject.toml`, `.gitignore`, `src/__init__.py`, `src/shared/__init__.py`, `src/api/__init__.py`, `src/services/__init__.py`, `tests/__init__.py`, `tests/conftest.py`
  - Refs: `Project_Skeleton_Specification.md` §2 (lines 56-186, repo structure), §5.1 (lines 274-290, pyproject.toml)
  - Depends on: none
  - Done when: `uv sync` succeeds, `ruff check` runs clean, `pytest` discovers test directory

- [ ] **P0-T02: Docker Compose local dev stack**
  - What: Create `docker-compose.yml` with PostgreSQL 16, ClickHouse, MinIO, and Redis for local development
  - Files: `docker/docker-compose.yml`, `docker/docker-compose.test.yml`
  - Refs: `Infrastructure_Specification.md` (Docker Compose service definitions, ports, images), `Project_Skeleton_Specification.md` §5.2 (lines 292-304), `phase-0-foundations.mdc` line 49, `ADR-008` (Docker Compose), `ADR-014` (Celery + Redis)
  - Depends on: P0-T01
  - Done when: `docker compose up` starts all 4 services (PG, CH, MinIO, Redis), health checks pass, can connect to each

- [ ] **P0-T03: Environment configuration**
  - What: Create `.env.example` and Pydantic Settings config module for all connection strings, Redis URL, and auth provider settings (issuer URL, audience, JWKS URL)
  - Files: `.env.example`, `src/shared/config/__init__.py`, `src/shared/config/settings.py`
  - Refs: `Infrastructure_Specification.md` (complete env var inventory, defaults, secrets boundary), `Code_Patterns_Specification.md` §9 (Pydantic Settings pattern), `phase-0-foundations.mdc` line 48 (Pydantic Settings, env vars), `Project_Skeleton_Specification.md` §2 (line 62, .env), `ADR-014` (Redis connection), `ADR-015` (auth provider config)
  - Depends on: P0-T01
  - Done when: Settings load from environment variables, all connection strings configurable, Redis URL and auth provider settings present

- [ ] **P0-T04: PostgreSQL connection factory**
  - What: SQLAlchemy Core engine and session factory with tenant context support
  - Files: `src/shared/db/__init__.py`, `src/shared/db/postgres.py`
  - Refs: `phase-0-foundations.mdc` line 40 (SQLAlchemy Core, not ORM), line 53 (tenant context via `SET app.current_tenant_id`)
  - Depends on: P0-T02, P0-T03
  - Done when: Can create engine, get session, set tenant context, execute queries against local PG

- [ ] **P0-T05: ClickHouse connection factory**
  - What: clickhouse-connect client factory
  - Files: `src/shared/db/clickhouse.py`
  - Refs: `phase-0-foundations.mdc` line 41 (clickhouse-connect)
  - Depends on: P0-T02, P0-T03
  - Done when: Can create client, execute queries against local ClickHouse

- [ ] **P0-T06: S3 storage wrapper**
  - What: boto3 wrapper for raw evidence storage, using MinIO for local dev
  - Files: `src/shared/storage/__init__.py`, `src/shared/storage/s3.py`
  - Refs: `phase-0-foundations.mdc` line 42 (boto3, MinIO)
  - Depends on: P0-T02, P0-T03
  - Done when: Can upload/download/list objects against local MinIO

- [ ] **P0-T07: Alembic initialization**
  - What: Set up Alembic for PostgreSQL migrations
  - Files: `db/postgresql/migrations/env.py`, `db/postgresql/migrations/alembic.ini`, `db/postgresql/migrations/versions/`
  - Refs: `phase-0-foundations.mdc` line 43 (Alembic for PG migrations), `Project_Skeleton_Specification.md` §2 (lines 83-89)
  - Depends on: P0-T04
  - Done when: `alembic upgrade head` and `alembic downgrade -1` run without error on empty database

- [ ] **P0-T08: Tenancy and identity migration**
  - What: Alembic migration for `tenant`, `user_account`, `audit_log` tables (3 tables) with RLS policies
  - Files: `db/postgresql/migrations/versions/001_tenancy_identity.py`
  - Refs: `Database_Schema_Specification.md` — `tenant` (line 166 heading, DDL line 171), `user_account` (line 187), `audit_log` (line 207). `phase-0-foundations.mdc` lines 51-56 (schema rules: tenant_id, RLS, uuid, timestamptz, bitemporal)
  - Depends on: P0-T07
  - Done when: Migration runs up/down cleanly, RLS policies enforced, tenant isolation verified

- [ ] **P0-T09: Raw evidence layer migration**
  - What: Alembic migration for Layer A tables: `source_system`, `source_ingestion`, `source_asset`, `source_record_raw`, `mapping_rule`, `mapping_review_queue` (6 tables)
  - Files: `db/postgresql/migrations/versions/002_raw_evidence_layer.py`
  - Refs: `Database_Schema_Specification.md` — Layer A section (lines 28-155). Tables: `source_system` (heading line 28, DDL line 33), `source_ingestion` (heading line 49, DDL line 54), `source_asset` (heading line 73, DDL line 78), `source_record_raw` (heading line 94, DDL line 99), `mapping_rule` (line 122), `mapping_review_queue` (line 142)
  - Depends on: P0-T08
  - Done when: Migration runs up/down cleanly, all 6 tables created with indexes

- [ ] **P0-T10: ClickHouse initial schema**
  - What: Versioned SQL migration creating the ClickHouse database and initial configuration
  - Files: `db/clickhouse/migrations/001_initial_schema.sql`
  - Refs: `phase-0-foundations.mdc` line 44 (CH migrations are versioned SQL, no Alembic), `Database_Schema_Specification.md` Layer C (line 2500)
  - Depends on: P0-T05
  - Done when: Migration runs, database exists, can create and query test table

- [ ] **P0-T11: Generate Pydantic models for Phase 0 tables**
  - What: Run `codegen/generate_models.py` to generate models for tenancy/identity and raw evidence tables, copy to `src/shared/models/`
  - Files: `src/shared/models/infrastructure.py`, `src/shared/models/raw_evidence.py`
  - Refs: `Project_Skeleton_Specification.md` §8 (lines 363-389, model generation pipeline), `rbv2-project.mdc` lines 148-153 (DDL-first pipeline)
  - Depends on: P0-T08, P0-T09
  - Done when: Generated models match DDL, import without error, all fields present

- [ ] **P0-T12: AuthZ service**
  - What: Implement AuthZ / Tenant Policy service with 3 operations: `check_access`, `get_tenant_context`, `enforce_row_filter`
  - Files: `src/services/authz/__init__.py`, `src/services/authz/service.py`, `src/services/authz/repository.py`
  - Refs: `Code_Patterns_Specification.md` §1 (service module structure), §3 (service function pattern), §4 (repository function pattern), §5 (exception pattern), `Service_Interface_Contracts.md` §1 (lines 36-72) — 3 operations, security model, scope levels
  - Depends on: P0-T04, P0-T08, P0-T11
  - Done when: All 3 operations implemented, tenant isolation enforced, error conditions handled

- [ ] **P0-T13: Engagement service**
  - What: Implement Engagement service with 6 operations: `create_assessment`, `update_assessment_status`, `get_assessment`, `update_data_coverage`, `configure_comp_set`, `get_run_status`
  - Files: `src/services/engagement/__init__.py`, `src/services/engagement/service.py`, `src/services/engagement/repository.py`
  - Refs: `Code_Patterns_Specification.md` §1 (service module structure), §3 (service function pattern), §4 (repository function pattern), §5 (exception pattern), `Service_Interface_Contracts.md` §2 (lines 75-109) — 6 operations, assessment types, status lifecycle
  - Depends on: P0-T04, P0-T08, P0-T11, P0-T12
  - Done when: All 6 operations implemented, status transitions validated, error conditions handled

- [ ] **P0-T14: FastAPI app and API routes**
  - What: Create FastAPI app entry point with JWT auth middleware and route modules for AuthZ and Engagement services
  - Files: `src/api/main.py`, `src/api/dependencies/__init__.py`, `src/api/dependencies/auth.py`, `src/api/routes/__init__.py`, `src/api/routes/auth.py`, `src/api/routes/engagements.py`
  - Refs: `Code_Patterns_Specification.md` §2 (route function pattern), §5 (exception pattern), §10 (FastAPI app initialization), `API_Design_Specification.md` (URL patterns, pagination, error envelope, OpenAPI rules), `Authentication_Middleware_Specification.md` (JWT claims, dependency chain, CORS, error codes), `phase-0-foundations.mdc` line 47 (FastAPI, `src/api/main.py`), `ADR-015` (JWT middleware validates tokens, extracts user_id), `Service_Interface_Contracts.md` cross-cutting error categories (lines 490-501), audit logging (line 505)
  - Depends on: P0-T12, P0-T13
  - Done when: API starts, JWT middleware validates tokens and rejects invalid ones, routes return correct responses, OpenAPI docs render, error categories return correct HTTP codes

- [ ] **P0-T15: CI workflow and Phase 0 tests**
  - What: GitHub Actions CI workflow + tests for migrations, tenant isolation, S3 integration, Celery task execution, JWT auth
  - Files: `.github/workflows/ci.yml`, `tests/unit/test_authz.py`, `tests/unit/test_engagement.py`, `tests/integration/test_migrations.py`, `tests/integration/test_s3.py`, `tests/integration/test_celery.py`, `tests/unit/test_auth_middleware.py`
  - Refs: `Code_Patterns_Specification.md` §6 (test pattern), `Project_Skeleton_Specification.md` §7.1 (lines 333-343, CI steps), `phase-0-foundations.mdc` lines 62-65 (testing rules)
  - Depends on: P0-T12, P0-T13, P0-T14, P0-T16, P0-T17
  - Done when: CI pipeline runs ruff check + ruff format + pytest, all tests pass, migration up/down tested, tenant isolation tested, S3 integration tested, Celery task dispatch/execution tested, JWT validation tested

- [ ] **P0-T16: Celery worker and Redis connection**
  - What: Set up Celery app configuration, Redis connection, and worker entry point. Define a sample task to verify the pipeline works.
  - Files: `src/worker.py`, `src/shared/celery_app.py`
  - Refs: `Code_Patterns_Specification.md` §8 (Celery task pattern), `ADR-014` (Celery + Redis architecture, task patterns, worker entry point), `phase-0-foundations.mdc` line 49 (Celery + Redis)
  - Depends on: P0-T02 (Redis in Docker Compose), P0-T03 (Redis URL in settings)
  - Done when: Celery worker starts, connects to Redis, can dispatch and execute a test task, task result is retrievable

- [ ] **P0-T17: Auth provider integration**
  - What: Select and configure managed auth provider (Auth0, Clerk, or Cognito). Set up tenant/org, create test users with roles matching `user_account.role` enum (admin, consultant, analyst, client_viewer). Configure JWT issuer/audience.
  - Files: `.env.example` (auth provider settings), documentation of provider setup steps
  - Refs: `Authentication_Middleware_Specification.md` (JWT claims schema, JWKS caching, token validation), `ADR-015` (managed auth provider, JWT validation, role mapping, provider selection criteria), `Database_Schema_Specification.md` — `user_account.role` enum (line 192)
  - Depends on: P0-T03
  - Done when: Auth provider configured, test users created for each role, JWTs can be obtained for test users, JWT contains `sub` (user ID) claim, role resolved from `user_account` table per Authentication_Middleware_Specification.md

- [ ] **P0-T18: Audit logging service**
  - What: Implement audit logging to `audit_log` table for all state-changing operations. Log user_id, action, entity_type, entity_id, old/new values, timestamp.
  - Files: `src/shared/audit.py`
  - Refs: `Code_Patterns_Specification.md` §7 (audit log helper pattern), `Observability_Specification.md` (audit logging rules, what gets audited), `Database_Schema_Specification.md` — `audit_log` (line 207), `Service_Interface_Contracts.md` line 505 (audit logging cross-cutting), `spec_1` Phase 0 item 4 (line 1311: "Implement audit logging and version registries")
  - Depends on: P0-T08 (audit_log table), P0-T04 (PG connection), P0-T12 (AuthZ service), P0-T13 (Engagement service)
  - Done when: All AuthZ and Engagement service mutations produce audit log entries, log entries are queryable by entity

---

## Post-Phase 0 Checkpoint — Pattern Lock

> Source: `agent_drift_prevention_strategy` plan, Option C (Hybrid)
> Purpose: Review Phase 0 output, update Code Patterns Specification with anything learned, lock patterns before Phase 1

**Prerequisite:** All Phase 0 tasks (P0-T01 through P0-T18) complete.

- [ ] **P0-CK1: Review Phase 0 code against Code Patterns Specification**
  - What: Read every file produced in Phase 0 (`src/services/authz/`, `src/services/engagement/`, `src/api/routes/`, `src/api/dependencies/`, `src/shared/audit.py`, `src/shared/config/`, `src/shared/db/`, `src/shared/storage/`, `src/worker.py`, `src/shared/celery_app.py`). Compare against each of the 10 patterns in `Code_Patterns_Specification.md`. Document any deviations or patterns that emerged but were not specified.
  - Files: (read-only review)
  - Refs: `Code_Patterns_Specification.md` (all 10 patterns)
  - Depends on: P0-T01 through P0-T18
  - Done when: Written report lists every deviation and every emergent pattern, with specific file:line citations

- [ ] **P0-CK2: Update Code Patterns Specification**
  - What: Incorporate any new patterns discovered during Phase 0 review into `Code_Patterns_Specification.md`. Correct any patterns that proved impractical during implementation. This is the last opportunity to modify the specification before it is locked.
  - Files: `Code_Patterns_Specification.md`
  - Refs: P0-CK1 review output
  - Depends on: P0-CK1
  - Done when: `Code_Patterns_Specification.md` accurately reflects the patterns in the Phase 0 codebase, with no unexplained deviations

- [ ] **P0-CK3: Validate documentation alignment and lock patterns**
  - What: Run `codegen/validate_docs.py` to confirm all documentation is still consistent after any updates. Confirm 0 errors. After validation, the Code Patterns Specification is locked — no further changes without explicit user approval.
  - Files: (validation run, no writes)
  - Refs: `codegen/validate_docs.py`
  - Depends on: P0-CK2
  - Done when: `validate_docs.py` reports 0 errors, `pytest codegen/test_validate_docs.py` passes, user confirms lock

---

## Phase 1 — Canonical Core and Import Framework

> Cursor rule: `phase-1-canonical-core.mdc`
> Services: Import & Mapping (8 ops), Entity Resolution (5 ops)
> Source: spec_1 lines 1313-1318

**Prerequisite:** All Phase 0 tasks complete AND Post-Phase 0 Checkpoint complete (P0-CK1 through P0-CK3 — Code Patterns Specification reviewed and locked).

- [ ] **P1-T01: Asset domain migration**
  - What: Alembic migration for Asset Hierarchy tables (13 tables) with RLS policies and indexes
  - Files: `db/postgresql/migrations/versions/003_asset_domain.py`
  - Refs: `Database_Schema_Specification.md` — Asset Hierarchy (13 tables per verification summary line 2826). Cross-ref spec_1 §3.2 Domain 1 (line 244)
  - Depends on: P0-T08, P0-CK3 (pattern lock)
  - Done when: All 13 asset tables created, FK constraints correct, indexes match DDL, RLS policies applied

- [ ] **P1-T02: Resident and Lease domain migration**
  - What: Alembic migration for Resident & Lease tables (10 tables)
  - Files: `db/postgresql/migrations/versions/004_resident_lease_domain.py`
  - Refs: `Database_Schema_Specification.md` — Resident & Lease (10 tables per line 2827). Cross-ref spec_1 §3.2 Domain 2 (line 245)
  - Depends on: P1-T01
  - Done when: All 10 tables created, FK constraints correct, indexes match DDL

- [ ] **P1-T03: Operations domain migration**
  - What: Alembic migration for Operations tables (15 tables)
  - Files: `db/postgresql/migrations/versions/005_operations_domain.py`
  - Refs: `Database_Schema_Specification.md` — Operations (15 tables per line 2828). Cross-ref spec_1 §3.2 Domain 3 (line 246)
  - Depends on: P1-T01
  - Done when: All 15 tables created, FK constraints correct, indexes match DDL

- [ ] **P1-T04: Demand domain migration**
  - What: Alembic migration for Demand (Leasing & CRM) tables (9 tables)
  - Files: `db/postgresql/migrations/versions/006_demand_domain.py`
  - Refs: `Database_Schema_Specification.md` — Demand (9 tables per line 2829). Cross-ref spec_1 §3.2 Domain 4 (line 247)
  - Depends on: P1-T01
  - Done when: All 9 tables created, FK constraints correct, indexes match DDL

- [ ] **P1-T05: Listing and Marketing domain migration**
  - What: Alembic migration for Listing & Marketing tables (13 tables)
  - Files: `db/postgresql/migrations/versions/007_listing_marketing_domain.py`
  - Refs: `Database_Schema_Specification.md` — Listing & Marketing (13 tables per line 2830)
  - Depends on: P1-T01
  - Done when: All 13 tables created, FK constraints correct, indexes match DDL

- [ ] **P1-T06: Market and Competition domain migration**
  - What: Alembic migration for Market & Competition tables (6 tables)
  - Files: `db/postgresql/migrations/versions/008_market_competition_domain.py`
  - Refs: `Database_Schema_Specification.md` — Market & Competition (6 tables per line 2831). Cross-ref spec_1 §3.2 Domain 5 (line 248)
  - Depends on: P1-T01
  - Done when: All 6 tables created, FK constraints correct, indexes match DDL

- [ ] **P1-T07: Field Evidence domain migration**
  - What: Alembic migration for Mystery Shop & Field Evidence (4 tables) + Technology Stack (2 tables) + Staffing & Programs (5 tables)
  - Files: `db/postgresql/migrations/versions/009_field_evidence_domain.py`
  - Refs: `Database_Schema_Specification.md` — Mystery Shop & Field Evidence (4, line 2832), Technology Stack (2, line 2833), Staffing & Programs (5, line 2835)
  - Depends on: P1-T01, P1-T02
  - Done when: All 11 tables created, FK constraints correct, indexes match DDL

- [ ] **P1-T08: Assessment and Deliverables domain migration**
  - What: Alembic migration for Assessment & Deliverables tables (15 tables) + Scoring Configuration (5 tables)
  - Files: `db/postgresql/migrations/versions/010_assessment_scoring_domain.py`
  - Refs: `Database_Schema_Specification.md` — Assessment & Deliverables (15, line 2834), Scoring Configuration (5, line 2836). Cross-ref spec_1 §3.2 Domain 6 (line 249)
  - Depends on: P1-T01, P1-T02, P1-T03
  - Done when: All 20 tables created, FK constraints correct, indexes match DDL

- [ ] **P1-T09: Workspace domain migration**
  - What: Alembic migration for Workspace (Studies/Reports) tables (10 tables: study, saved_query, result_snapshot, study_item, comparison_board, annotation, evidence_bundle, report, report_section, report_render)
  - Files: `db/postgresql/migrations/versions/011_workspace_domain.py`
  - Refs: `Database_Schema_Specification.md` — Domain 11 (line 2135). Tables: study, saved_query, result_snapshot, study_item, comparison_board, annotation, evidence_bundle, report, report_section, report_render (10 tables).
  - Depends on: P1-T08
  - Done when: All 10 Domain 11 tables created, FK constraints correct, indexes match DDL

- [ ] **P1-T10: Regenerate all Pydantic models**
  - What: Run `codegen/generate_models.py` against full DDL, copy all 14 domain modules to `src/shared/models/`
  - Files: All 14 files in `src/shared/models/` (asset.py, lease.py, operations.py, demand.py, marketing.py, competitive.py, field_evidence.py, assessment.py, scoring_config.py, workspace.py, infrastructure.py, raw_evidence.py, intake_snapshot.py, clickhouse_facts.py)
  - Refs: `Project_Skeleton_Specification.md` §8.1 (lines 372-389, 14 domain modules), `rbv2-project.mdc` lines 148-153
  - Depends on: P1-T01 through P1-T09
  - Done when: All 14 modules generated, 125 models total, 1,393 fields (per `Shared_Type_Definitions.md` lines 12-13)

- [ ] **P1-T11: Import framework core — file upload and raw storage**
  - What: Implement file upload to S3, `source_asset` creation with SHA-256 hash, `source_record_raw` parsing
  - Files: `src/services/import_mapping/__init__.py`, `src/services/import_mapping/service.py`, `src/services/import_mapping/repository.py`
  - Refs: `Service_Interface_Contracts.md` §3 — operations `upload_asset` (line 137), `parse_asset` (line 138), `create_ingestion` (line 136). `Data_Onramp_Specification.md` §3 (lines 68-97, ingestion pipeline), `phase-1-canonical-core.mdc` lines 47-51 (import framework rules)
  - Depends on: P0-T06, P0-T09, P1-T10
  - Done when: Files upload to S3, source_asset records created with SHA-256, records parsed to source_record_raw, duplicate hash detection works

- [ ] **P1-T12: Column mapping engine**
  - What: Implement `apply_mappings` operation — auto-mapping with confidence scoring, review routing
  - Files: `src/services/import_mapping/mapping.py` (or within service.py)
  - Refs: `Service_Interface_Contracts.md` §3 — `apply_mappings` (line 139). `Data_Onramp_Specification.md` §7 (lines 179-223, column mapping rules, mapping lifecycle, review queue). `phase-1-canonical-core.mdc` lines 58-59 (confidence thresholds: 0.8 auto-detect, 0.7 record-level)
  - Depends on: P1-T11
  - Done when: Mapping rules applied, high-confidence records auto-mapped, low-confidence sent to review, mapping status lifecycle correct

- [ ] **P1-T13: Review queue**
  - What: Implement `get_review_queue` and `resolve_review_item` operations
  - Files: within `src/services/import_mapping/`
  - Refs: `Service_Interface_Contracts.md` §3 — `get_review_queue` (line 140), `resolve_review_item` (line 141). `Data_Onramp_Specification.md` §7.3 (lines 212-223, review types and resolutions)
  - Depends on: P1-T12
  - Done when: Review items retrievable by ingestion, all 4 review types handled, all 4 resolution options work, `finalize_ingestion` blocks if unresolved items exist

- [ ] **P1-T14: Yardi vendor adapter**
  - What: Implement Yardi adapter implementing `VendorAdapter` protocol
  - Files: `src/services/import_mapping/adapters/__init__.py`, `src/services/import_mapping/adapters/yardi.py`
  - Refs: `Data_Onramp_Specification.md` §4 (lines 124-136, vendor adapters — Yardi). `phase-1-canonical-core.mdc` lines 55-59 (connector rules, adapter protocol)
  - Depends on: P1-T12
  - Done when: Yardi rent roll, work order, and lease exports parse correctly, column mappings produce canonical entities

- [ ] **P1-T15: RealPage, Entrata, AppFolio, ResMan adapters**
  - What: Implement remaining 4 vendor adapters
  - Files: `src/services/import_mapping/adapters/realpage.py`, `src/services/import_mapping/adapters/entrata.py`, `src/services/import_mapping/adapters/appfolio.py`, `src/services/import_mapping/adapters/resman.py`
  - Refs: `Data_Onramp_Specification.md` §4 (lines 128-134, vendor table). `phase-1-canonical-core.mdc` lines 55-59
  - Depends on: P1-T14
  - Done when: Each adapter handles its vendor's export formats, column mappings produce canonical entities

- [ ] **P1-T16: Entity Resolution service**
  - What: Implement Entity Resolution with 5 operations: `resolve_unit_aliases`, `get_aliases_for_unit`, `override_match`, `find_duplicates`, `merge_entities`
  - Files: `src/services/entity_resolution/__init__.py`, `src/services/entity_resolution/service.py`, `src/services/entity_resolution/repository.py`
  - Refs: `Service_Interface_Contracts.md` §4 (lines 156-188) — 5 operations, resolution strategy. `phase-1-canonical-core.mdc` lines 63-67 (resolution rules: alias first, fuzzy matching, confidence thresholds)
  - Depends on: P1-T10, P1-T11
  - Done when: All 5 operations implemented, deterministic → fuzzy → review pipeline works, match_method/confidence/reviewer_override stored

- [ ] **P1-T17: Source system registration and finalization**
  - What: Implement `register_source_system` and `finalize_ingestion` operations
  - Files: within `src/services/import_mapping/`
  - Refs: `Service_Interface_Contracts.md` §3 — `register_source_system` (line 143), `finalize_ingestion` (line 142)
  - Depends on: P1-T13
  - Done when: Source systems register correctly, finalization blocks on unresolved items, status transitions complete

- [ ] **P1-T18: Import and Entity Resolution API routes**
  - What: FastAPI route modules for Import & Mapping and Entity Resolution services
  - Files: `src/api/routes/imports.py`, `src/api/routes/entity_resolution.py`
  - Refs: `Service_Interface_Contracts.md` cross-cutting error categories (lines 490-501)
  - Depends on: P1-T11 through P1-T17
  - Done when: All import and resolution operations exposed via API, error conditions return correct HTTP codes

- [ ] **P1-T19: Golden property test fixture**
  - What: Create test dataset for one property: rent roll, leases, work orders, vacancy cycles, mystery shop, financials
  - Files: `tests/fixtures/golden_property/` (multiple fixture files)
  - Refs: `Project_Skeleton_Specification.md` §6.2 (lines 317-319, golden property description)
  - Depends on: P1-T10
  - Done when: Complete test dataset exists, can be loaded into canonical tables

- [ ] **P1-T20: Phase 1 integration tests**
  - What: Tests for adapters, entity resolution, E2E import pipeline, review queue
  - Files: `tests/unit/test_import_mapping.py`, `tests/unit/test_entity_resolution.py`, `tests/integration/test_import_pipeline.py`
  - Refs: `phase-1-canonical-core.mdc` lines 76-79 (testing rules). `phase-0-foundations.mdc` line 60 (migration tests)
  - Depends on: P1-T14 through P1-T19
  - Done when: Adapter tests with sample files pass, resolution scenarios tested (exact, alias, fuzzy, new, override), E2E import pipeline tested, review queue tested

---

## Phase 2 — Temporal Unit Spine

> Cursor rule: `phase-2-temporal-spine.mdc`
> Service: Temporal State Builder (5 ops)
> Source: spec_1 lines 1320-1325

**Prerequisite:** All Phase 1 tasks complete (canonical schemas deployed, import framework functional, entity resolution working, at least one PM connector operational).

- [ ] **P2-T01: Occupancy interval resolver**
  - What: Derive occupancy intervals from `lease` + `lease_interval` tables
  - Files: `src/services/temporal_state/__init__.py`, `src/services/temporal_state/resolvers/__init__.py`, `src/services/temporal_state/resolvers/occupancy.py`
  - Refs: `phase-2-temporal-spine.mdc` line 46 (occupancy from lease + lease_interval). `Service_Interface_Contracts.md` §5 (lines 191-227)
  - Depends on: P1-T02, P1-T10
  - Done when: Occupancy intervals derived correctly from lease data, gaps between leases produce vacant intervals

- [ ] **P2-T02: Notice interval resolver**
  - What: Derive notice intervals from lease notice dates
  - Files: `src/services/temporal_state/resolvers/notice.py`
  - Refs: `phase-2-temporal-spine.mdc` line 47
  - Depends on: P2-T01
  - Done when: Notice periods correctly extracted from lease data

- [ ] **P2-T03: Readiness interval resolver**
  - What: Derive readiness intervals from `make_ready_cycle` phase dates
  - Files: `src/services/temporal_state/resolvers/readiness.py`
  - Refs: `phase-2-temporal-spine.mdc` line 48
  - Depends on: P1-T03
  - Done when: Readiness state transitions (not_ready → make_ready → ready_show → ready_lease) derived from cycle dates

- [ ] **P2-T04: Listing interval resolver**
  - What: Derive listing intervals from `listing_observation` records
  - Files: `src/services/temporal_state/resolvers/listing.py`
  - Refs: `phase-2-temporal-spine.mdc` line 49
  - Depends on: P1-T05
  - Done when: Marketing state (unlisted → listed → application_pending → leased) derived from observations

- [ ] **P2-T05: Pricing interval resolver**
  - What: Derive pricing intervals from `lease_interval` rent fields and `listing_observation` asking rents
  - Files: `src/services/temporal_state/resolvers/pricing.py`
  - Refs: `phase-2-temporal-spine.mdc` line 50
  - Depends on: P2-T01, P2-T04
  - Done when: Asking rent, effective rent, and concession values resolve per day from lease and listing data

- [ ] **P2-T06: fact_unit_day materialization logic**
  - What: Implement `build_unit_day_spine` and `get_unit_day` — one row per unit per day, joining all interval resolvers, carry-forward rules, evidence coverage, contradiction flags
  - Files: `src/services/temporal_state/service.py`, `src/services/temporal_state/repository.py`
  - Refs: `phase-2-temporal-spine.mdc` lines 38-42 (temporal modeling rules), `Service_Interface_Contracts.md` §5 lines 213-226 (5 operations including `get_unit_day` at line 216, construction steps)
  - Depends on: P2-T01 through P2-T05
  - Done when: Every unit with an existence interval has a row for every day, no gaps, unknowns marked explicitly, contradictions flagged, `get_unit_day` returns single day for a unit

- [ ] **P2-T07: Vacancy cycle construction**
  - What: Implement `rebuild_vacancy_cycles` — build cycles from move-out to move-in with derived fields
  - Files: within `src/services/temporal_state/`
  - Refs: `phase-2-temporal-spine.mdc` lines 55-59 (cycle construction rules), `Database_Schema_Specification.md` — `vacancy_cycle` (line 878)
  - Depends on: P2-T06
  - Done when: Vacancy cycles span move-out to move-in, `days_vacant`/`prior_rent`/`new_rent`/`vacancy_cost` derived, still-vacant units have NULL end

- [ ] **P2-T08: Make-ready cycle construction**
  - What: Implement `rebuild_make_ready_cycles` — full turnover pipeline with phase boundaries
  - Files: within `src/services/temporal_state/`
  - Refs: `phase-2-temporal-spine.mdc` lines 57-59 (make-ready pipeline: notice → move-out → ... → move-in), `Database_Schema_Specification.md` — `make_ready_cycle` (line 846)
  - Depends on: P2-T06
  - Done when: Make-ready cycles track all phases, `make_ready_scope` values correct, linked to prior/new lease IDs

- [ ] **P2-T09: ClickHouse fact table migrations**
  - What: Create 3 ClickHouse tables: `fact_unit_day`, `fact_lease_interval`, `fact_vacancy_cycle`
  - Files: `db/clickhouse/migrations/002_phase2_fact_tables.sql`
  - Refs: `Database_Schema_Specification.md` — `fact_unit_day` (line 2512), `fact_lease_interval` (line 2541), `fact_vacancy_cycle` (line 2564). `phase-2-temporal-spine.mdc` lines 64-66 (ordering keys)
  - Depends on: P0-T10
  - Done when: All 3 tables created with correct MergeTree engines and ordering keys

- [ ] **P2-T10: ClickHouse materialization pipeline**
  - What: Implement PG → CH materialization for all 3 fact tables, including `refresh_after_ingestion`
  - Files: within `src/services/temporal_state/`
  - Refs: `phase-2-temporal-spine.mdc` lines 63-69 (materialization rules), `Service_Interface_Contracts.md` §5 — `refresh_after_ingestion` (line 217)
  - Depends on: P2-T06, P2-T09
  - Done when: `build_unit_day_spine` populates ClickHouse, `refresh_after_ingestion` incrementally updates affected rows

- [ ] **P2-T11: Temporal State Builder API routes**
  - What: FastAPI routes for all 5 Temporal State Builder operations
  - Files: `src/api/routes/temporal.py`
  - Refs: `Service_Interface_Contracts.md` §5 (lines 211-217)
  - Depends on: P2-T06 through P2-T10
  - Done when: All 5 operations exposed via API

- [ ] **P2-T12: Phase 2 tests**
  - What: Tests for spine, vacancy cycles, make-ready cycles, ClickHouse row counts, edge cases (no events, overlapping intervals, offline units)
  - Files: `tests/unit/test_temporal_state.py`, `tests/integration/test_temporal_materialization.py`
  - Refs: `phase-2-temporal-spine.mdc` lines 73-77 (testing rules)
  - Depends on: P2-T10, P2-T11
  - Done when: All test scenarios pass including edge cases, CH row counts match expected

---

## Phase 3 — Core Diagnostics

> Cursor rule: `phase-3-core-diagnostics.mdc`
> Services: Metric Engine (5 ops), Scoring Engine (4 ops), Finding Compiler (4 ops), Impact Engine (3 ops)
> Source: spec_1 lines 1327-1339

**Prerequisite:** All Phase 2 tasks complete (`fact_unit_day` materialized, cycles built, ClickHouse populated).

- [ ] **P3-T01: Metric registry infrastructure**
  - What: Implement `MetricRegistry` with `register_metric`, `list_metrics`, `validate_inputs` operations
  - Files: `src/services/metric_engine/__init__.py`, `src/services/metric_engine/service.py`, `src/services/metric_engine/repository.py`, `src/services/metric_engine/registry.py`
  - Refs: `Service_Interface_Contracts.md` §6 (lines 230-264) — registry operations + 5 metric components. `phase-3-core-diagnostics.mdc` lines 44-48
  - Depends on: P2-T10
  - Done when: Metrics can be registered, listed, and input validation works

- [ ] **P3-T02: Benchmark registry**
  - What: Implement benchmark registration and lookup for metric comparison
  - Files: within `src/services/metric_engine/`
  - Refs: `phase-3-core-diagnostics.mdc` line 15 (benchmark registry), `Service_Interface_Contracts.md` §6 line 263 (`benchmark_basis` component)
  - Depends on: P3-T01
  - Done when: Benchmarks registered per metric, retrievable for scoring comparison

- [ ] **P3-T03: KPI computation — vacancy and turnover metrics**
  - What: Implement KPIs for vacancy/turnover domain from the 124 Basic Analytic Data Set
  - Files: `src/services/metric_engine/packages/vacancy_turnover.py`
  - Refs: `Basic_Analytic_Data_Set.md` (124 KPIs total, line 301). `phase-3-core-diagnostics.mdc` line 46 (metrics read from ClickHouse)
  - Depends on: P3-T01, P3-T02
  - Done when: Vacancy/turnover KPIs compute from ClickHouse facts, return all 5 components

- [ ] **P3-T04: KPI computation — make-ready and maintenance metrics**
  - What: Implement KPIs for make-ready/maintenance domain
  - Files: `src/services/metric_engine/packages/make_ready_maintenance.py`
  - Refs: `Basic_Analytic_Data_Set.md`, `Analytical_Engine_Specification.md` Pre-Computation layer (line 94)
  - Depends on: P3-T01, P3-T02
  - Done when: Make-ready/maintenance KPIs compute correctly

- [ ] **P3-T05: KPI computation — leasing, listing, pricing, competitive, condition metrics**
  - What: Implement remaining domain KPIs (leasing/CRM, listing quality, pricing/revenue, competitive position, property condition)
  - Files: `src/services/metric_engine/packages/leasing_crm.py`, `src/services/metric_engine/packages/listing_quality.py`, `src/services/metric_engine/packages/pricing_revenue.py`, `src/services/metric_engine/packages/competitive_position.py`, `src/services/metric_engine/packages/property_condition.py`
  - Refs: `Basic_Analytic_Data_Set.md`, `phase-3-core-diagnostics.mdc` line 16 (7 domain packages)
  - Depends on: P3-T01, P3-T02
  - Done when: All 124 KPIs computable, all 5 metric components returned per KPI

- [ ] **P3-T06: compute_metrics and get_metric_value operations**
  - What: Implement `compute_metrics` and `get_metric_value` operations for Metric Engine
  - Files: within `src/services/metric_engine/service.py`
  - Refs: `Service_Interface_Contracts.md` §6 — `compute_metrics` (line 250), `get_metric_value` (line 251)
  - Depends on: P3-T03 through P3-T05
  - Done when: Both operations work, domain filtering supported, error conditions handled

- [ ] **P3-T07: Scoring engine — Data item scorer (piecewise linear interpolation)**
  - What: Implement scoring for 20 Data items via piecewise linear interpolation with 4 breakpoints
  - Files: `src/services/scoring_engine/__init__.py`, `src/services/scoring_engine/service.py`, `src/services/scoring_engine/repository.py`, `src/services/scoring_engine/scorers/data_scorer.py`
  - Refs: `phase-3-core-diagnostics.mdc` line 53 (Data items, interpolation, 4 breakpoints, direction). `Scoring_Thresholds_Calibration.md` (breakpoint values). `scoring_config.json` (machine-readable structure)
  - Depends on: P3-T06
  - Done when: All 20 Data items score correctly via interpolation, direction (↑/↓) handled, breakpoint edge cases tested

- [ ] **P3-T08: Scoring engine — Checklist item scorer (100-point budget)**
  - What: Implement scoring for 38 Checklist items via sub-item point budget system
  - Files: `src/services/scoring_engine/scorers/checklist_scorer.py`
  - Refs: `phase-3-core-diagnostics.mdc` line 54 (Checklist: 100-point budget, Y/N, tiered, points/100 × 10). `Scoring_Weights_Final_Update.json` (315 `sp__` sub-item budgets)
  - Depends on: P3-T06
  - Done when: All 38 Checklist items score correctly, sub-item points sum to 100 per item verified, Y/N and tiered scoring both work

- [ ] **P3-T09: Scoring engine — Comparative item scorer**
  - What: Implement scoring for 7 Comparative items (subject vs comp set average)
  - Files: `src/services/scoring_engine/scorers/comparative_scorer.py`
  - Refs: `phase-3-core-diagnostics.mdc` line 55 (Comparative: same interpolation vs comp average). `Scoring_Thresholds_Calibration.md`
  - Depends on: P3-T07
  - Done when: All 7 Comparative items score correctly, comp set average computed, interpolation applied

- [ ] **P3-T10: Scoring engine — weight hierarchy and aggregation**
  - What: Implement three-level weighting (sub-item → item → area → overall), configurable weights, missing-data exclusion
  - Files: `src/services/scoring_engine/aggregation.py`
  - Refs: `phase-3-core-diagnostics.mdc` lines 56-58 (weighting rules, missing data exclusion). `Scoring_Weights_Final_Update.json` (12 `aw__`, 65 `iw__`, 315 `sp__`)
  - Depends on: P3-T07, P3-T08, P3-T09
  - Done when: Weights load from config, item weights sum to 100% per area, area weights sum to 100%, missing items excluded (not zeroed), coverage tracked

- [ ] **P3-T11: Scoring engine — ScoreResult and Scorecard operations**
  - What: Implement `score_assessment`, `score_domain`, `get_scorecard`, `compare_scorecards`
  - Files: within `src/services/scoring_engine/service.py`
  - Refs: `Service_Interface_Contracts.md` §7 (lines 267-314) — 4 operations, ScoreResult fields (lines 294-299), three views (lines 309-313). `phase-3-core-diagnostics.mdc` lines 60-61
  - Depends on: P3-T10
  - Done when: All 4 operations work, ScoreResult stores all 9 fields, three views (performance/confidence/scope) available

- [ ] **P3-T12: Finding Compiler — diagnostic rule framework**
  - What: Implement finding compilation framework: package execution, status returns (PASS/WATCH/FAIL/OUT_OF_SCOPE), evidence linking
  - Files: `src/services/finding_compiler/__init__.py`, `src/services/finding_compiler/service.py`, `src/services/finding_compiler/repository.py`
  - Refs: `Service_Interface_Contracts.md` §8 (lines 317-356) — `compile_findings` (line 337), finding fields (lines 344-346). `phase-3-core-diagnostics.mdc` lines 65-68
  - Depends on: P3-T06
  - Done when: Framework can execute rule packages, return correct statuses, link findings to evidence

- [ ] **P3-T13: Finding Compiler — finding graph**
  - What: Implement `get_finding_graph` — nodes (findings, units, agents, listings) and edges (evidence links)
  - Files: within `src/services/finding_compiler/`
  - Refs: `Service_Interface_Contracts.md` §8 — `get_finding_graph` (line 339), `get_findings_by_domain` (line 340). `phase-3-core-diagnostics.mdc` line 67
  - Depends on: P3-T12
  - Done when: Finding graph connects findings to entities via evidence links, domain filtering works

- [ ] **P3-T14: Contradiction engine**
  - What: Implement `detect_contradictions` — PM-vs-field and cross-source mismatch detection
  - Files: within `src/services/finding_compiler/` (contradiction detection is part of Finding Compiler per contract)
  - Refs: `Service_Interface_Contracts.md` §8 — `detect_contradictions` (line 338), contradiction record (lines 350-356). `phase-3-core-diagnostics.mdc` lines 72-74
  - Depends on: P3-T12
  - Done when: Contradictions detected between sources, records include source A/B, matching rule, type, severity, evidence links, trust penalty

- [ ] **P3-T15: Domain package — vacancy/turnover**
  - What: Implement vacancy/turnover diagnostic package with rules, findings, and evidence linking
  - Files: `src/services/finding_compiler/packages/vacancy_turnover.py`
  - Refs: `phase-3-core-diagnostics.mdc` lines 85-89 (domain package rules). `Analytical_Question_Inventory.md` (diagnostic question categories)
  - Depends on: P3-T12, P3-T03
  - Done when: Package generates findings with evidence from vacancy/turnover metrics

- [ ] **P3-T16: Domain package — make-ready/maintenance**
  - What: Implement make-ready/maintenance diagnostic package
  - Files: `src/services/finding_compiler/packages/make_ready_maintenance.py`
  - Refs: same as P3-T15
  - Depends on: P3-T12, P3-T04
  - Done when: Package generates findings from make-ready/maintenance metrics

- [ ] **P3-T17: Domain package — leasing/CRM**
  - What: Implement leasing/CRM diagnostic package
  - Files: `src/services/finding_compiler/packages/leasing_crm.py`
  - Refs: `phase-3-core-diagnostics.mdc` line 85 (7 domain packages from spec_1 lines 1329-1336)
  - Depends on: P3-T12, P3-T05
  - Done when: Package generates findings from leasing/CRM metrics

- [ ] **P3-T18: Domain packages — listing quality, pricing/revenue, competitive position, property condition**
  - What: Implement remaining 4 domain diagnostic packages
  - Files: `src/services/finding_compiler/packages/listing_quality.py`, `src/services/finding_compiler/packages/pricing_revenue.py`, `src/services/finding_compiler/packages/competitive_position.py`, `src/services/finding_compiler/packages/property_condition.py`
  - Refs: `phase-3-core-diagnostics.mdc` line 85 (7 domain packages from spec_1 lines 1329-1336)
  - Depends on: P3-T12, P3-T05
  - Done when: All 4 packages generate findings from their respective metrics

- [ ] **P3-T19: Impact Engine — model catalog and core operations**
  - What: Implement Impact Engine with 3 operations: `estimate_impacts`, `get_impact_summary`, `simulate_optimal_budget`
  - Files: `src/services/impact_engine/__init__.py`, `src/services/impact_engine/service.py`, `src/services/impact_engine/repository.py`
  - Refs: `Service_Interface_Contracts.md` §9 (lines 360-400) — 3 operations, ImpactEstimate output format (lines 390-395), double-counting prevention (lines 397-399)
  - Depends on: P3-T12
  - Done when: All 3 operations implemented, ImpactEstimate returns low/base/high with formula trace

- [ ] **P3-T20: Impact Engine — 10 reusable impact models**
  - What: Implement all 10 impact models: vacancy_loss, avoidable_turn_delay, below_market_rent_loss, concession_leakage, retention_failure_cost, collections_loss_risk, maintenance_overspend, vendor_rework_cost, marketing_waste, pricing_misposition_cost
  - Files: `src/services/impact_engine/models/` (one file per model or grouped)
  - Refs: `Service_Interface_Contracts.md` §9 line 386 (10 model names). `phase-3-core-diagnostics.mdc` line 78
  - Depends on: P3-T19
  - Done when: All 10 models compute impacts, double-counting prevented via `impact_family_id`

- [ ] **P3-T21: ClickHouse score and finding fact tables**
  - What: Create ClickHouse migrations for `fact_score_result` and `fact_finding_impact`
  - Files: `db/clickhouse/migrations/003_phase3_score_finding_facts.sql`
  - Refs: `Database_Schema_Specification.md` — core analytical facts (lines 2500-2718, 10 tables total for core)
  - Depends on: P0-T10
  - Done when: Tables created with correct engines and ordering keys

- [ ] **P3-T22: Phase 3 API routes**
  - What: FastAPI routes for Metric Engine, Scoring Engine, Finding Compiler, Impact Engine
  - Files: `src/api/routes/metrics.py`, `src/api/routes/scoring.py`, `src/api/routes/findings.py`, `src/api/routes/impacts.py`
  - Refs: `Service_Interface_Contracts.md` §6-9, cross-cutting error categories (lines 490-501)
  - Depends on: P3-T06, P3-T11, P3-T13, P3-T19
  - Done when: All 16 operations (5+4+4+3) exposed via API with correct error handling

- [ ] **P3-T23: Scoring engine tests**
  - What: Tests for all 3 input types, interpolation, checklist budget, weight sums, missing data
  - Files: `tests/unit/test_scoring_engine.py`
  - Refs: `phase-3-core-diagnostics.mdc` lines 93-97 (testing rules)
  - Depends on: P3-T11
  - Done when: Interpolation tested at/between breakpoints, checklist budgets verified (sum to 100), weights verified (sum to 100%), missing data excluded correctly

- [ ] **P3-T24: Finding and contradiction tests**
  - What: Tests for finding compilation, contradiction detection, finding graph
  - Files: `tests/unit/test_finding_compiler.py`, `tests/unit/test_contradiction_engine.py`
  - Refs: `phase-3-core-diagnostics.mdc` lines 98-99
  - Depends on: P3-T14, P3-T15 through P3-T18
  - Done when: Findings compile with evidence links, contradictions detected from known conflicting data

- [ ] **P3-T25: Impact engine tests**
  - What: Tests for impact estimation, double-counting prevention, budget simulation
  - Files: `tests/unit/test_impact_engine.py`
  - Refs: `phase-3-core-diagnostics.mdc` line 99 (double-counting prevention test)
  - Depends on: P3-T20
  - Done when: Related impacts don't sum beyond net attributable amount, all 10 models tested

---

## Phase 4 — Workspace and Reporting

> Cursor rule: `phase-4-workspace-reporting.mdc`
> Services: Study & Snapshot (8 ops), Report Rendering (5 ops)
> Source: spec_1 lines 1341-1346

**Prerequisite:** All Phase 3 tasks complete (full diagnostic pipeline operational).

- [ ] **P4-T01: Frontend project setup**
  - What: Initialize Next.js App Router project with TypeScript, Tailwind CSS, shadcn/ui, TanStack Table, Recharts, TanStack Query, React Hook Form + Zod
  - Files: `frontend/package.json`, `frontend/tsconfig.json`, `frontend/next.config.js`, `frontend/tailwind.config.ts`, `frontend/src/`
  - Refs: `Project_Skeleton_Specification.md` §1.2 (lines 25-37, frontend stack)
  - Depends on: P0-T14
  - Done when: Next.js dev server starts, TypeScript compiles, Tailwind works, shadcn/ui components available

- [ ] **P4-T02: Study & Snapshot service**
  - What: Implement Study & Snapshot service with 8 operations: `create_study`, `save_query`, `take_snapshot`, `add_to_study`, `create_comparison`, `annotate`, `create_evidence_bundle`, `export_bundle`
  - Files: `src/services/study_snapshot/__init__.py`, `src/services/study_snapshot/service.py`, `src/services/study_snapshot/repository.py`
  - Refs: `Service_Interface_Contracts.md` §10 (lines 403-439) — 8 operations, snapshot semantics. `phase-4-workspace-reporting.mdc` lines 41-47
  - Depends on: P1-T09, P1-T10
  - Done when: All 8 operations implemented, snapshot preserves all required version fields, evidence bundles export

- [ ] **P4-T03: Report Rendering service**
  - What: Implement Report Rendering service with 5 operations: `create_report`, `add_section`, `render_report`, `get_report`, `list_templates`
  - Files: `src/services/report_rendering/__init__.py`, `src/services/report_rendering/service.py`, `src/services/report_rendering/repository.py`
  - Refs: `Service_Interface_Contracts.md` §11 (lines 443-487) — 5 operations, rendering pipeline. `phase-4-workspace-reporting.mdc` lines 59-67 (report rendering rules)
  - Depends on: P1-T09, P1-T10
  - Done when: All 5 operations implemented, reports compose from section types, rendering pipeline produces output

- [ ] **P4-T04: Report template definitions**
  - What: Define 7 standard report templates + custom report type
  - Files: `src/services/report_rendering/templates/` (template definition files)
  - Refs: `Report_Template_Specification.md` — 7 standard templates, section types, render formats. `phase-4-workspace-reporting.mdc` lines 62-63 (report_type and section_type enums)
  - Depends on: P4-T03
  - Done when: All 7 templates registered, `list_templates` returns them, custom report type works

- [ ] **P4-T05: PDF rendering pipeline**
  - What: Implement PDF output from report sections with brand theme
  - Files: within `src/services/report_rendering/`
  - Refs: `phase-4-workspace-reporting.mdc` lines 65-67 (rendering pipeline steps), `Report_Template_Specification.md` render formats
  - Depends on: P4-T04
  - Done when: PDF renders from bound data, sections include scorecards/findings/narratives/charts, stored in S3

- [ ] **P4-T06: HTML and PPTX rendering**
  - What: Implement HTML and PPTX output formats
  - Files: within `src/services/report_rendering/`
  - Refs: `Report_Template_Specification.md` render formats (pdf, html, pptx)
  - Depends on: P4-T05
  - Done when: Both HTML and PPTX formats produce valid output files

- [ ] **P4-T07: Workspace and report API routes**
  - What: FastAPI routes for Study & Snapshot and Report Rendering services
  - Files: `src/api/routes/workspace.py`, `src/api/routes/reports.py`
  - Refs: `Service_Interface_Contracts.md` §10-11
  - Depends on: P4-T02, P4-T03
  - Done when: All 13 operations (8+5) exposed via API

- [ ] **P4-T08: UI — Engagement Cockpit module**
  - What: Property overview, assessment lifecycle, source coverage, run status
  - Files: `frontend/src/app/workspace/` (cockpit pages)
  - Refs: `UI_UX_Specification.md` — Module 1: Engagement Cockpit (service deps: Engagement, Import & Mapping, AuthZ)
  - Depends on: P4-T01, P0-T14
  - Done when: Assessment list/detail views render, status visible, coverage gaps shown

- [ ] **P4-T09: UI — Import Center module**
  - What: Upload, map, validate, and monitor data ingestion
  - Files: `frontend/src/app/workspace/import/` (import pages)
  - Refs: `UI_UX_Specification.md` — Module 2: Import Center (service deps: Import & Mapping, Entity Resolution)
  - Depends on: P4-T01, P1-T18
  - Done when: File upload works, mapping review UI functional, ingestion progress visible

- [ ] **P4-T10: UI — Field Capture module**
  - What: Unit walks, mystery shops, observations, competitor captures (mobile-responsive)
  - Files: `frontend/src/app/workspace/field-capture/` (capture forms)
  - Refs: `UI_UX_Specification.md` — Module 3: Field Capture (mobile responsive per Audit Workbook line 189)
  - Depends on: P4-T01
  - Done when: Structured capture forms render, photo attachment works, mobile-responsive layout

- [ ] **P4-T11: UI — Diagnostic Hub module**
  - What: Scorecards, findings, contradictions, impact summaries with drilldown
  - Files: `frontend/src/app/workspace/diagnostics/` (diagnostic pages)
  - Refs: `UI_UX_Specification.md` — Module 4: Diagnostic Hub (service deps: Scoring Engine, Finding Compiler, Impact Engine)
  - Depends on: P4-T01, P3-T22
  - Done when: Scorecard drilldown (area → item → sub-item), finding browser, contradiction detail, impact summaries render

- [ ] **P4-T12: UI — Analysis Lab module**
  - What: Guided pivots, SQL access, drilldowns, compare views
  - Files: `frontend/src/app/workspace/analysis/` (analysis pages)
  - Refs: `UI_UX_Specification.md` — Module 5: Analysis Lab. `phase-4-workspace-reporting.mdc` lines 71-74 (analysis lab rules)
  - Depends on: P4-T01, P4-T02
  - Done when: Guided exploration works, SQL available for edge cases, results saveable as queries/snapshots

- [ ] **P4-T13: UI — Studies module**
  - What: Saved investigations, comparison boards, annotations, evidence bundles
  - Files: `frontend/src/app/workspace/studies/` (study pages)
  - Refs: `UI_UX_Specification.md` — Module 6: Studies. `phase-4-workspace-reporting.mdc` lines 49-57 (study workflow)
  - Depends on: P4-T01, P4-T02
  - Done when: Study creation, snapshot adding, comparison boards, annotations, and evidence bundle export all functional

- [ ] **P4-T14: UI — Report Composer module**
  - What: Template selection, section editing, evidence insertion, preview, render, export
  - Files: `frontend/src/app/workspace/reports/` (report pages)
  - Refs: `UI_UX_Specification.md` — Module 7: Report Composer
  - Depends on: P4-T01, P4-T03, P4-T05
  - Done when: Template selection works, sections addable/reorderable, narrative editing, chart config, preview and render to PDF/HTML/PPTX

- [ ] **P4-T15: Evidence bundle export pipeline**
  - What: Export curated evidence bundles in selected formats
  - Files: within `src/services/study_snapshot/`
  - Refs: `Service_Interface_Contracts.md` §10 — `export_bundle` (line 435)
  - Depends on: P4-T02
  - Done when: Bundles export with all referenced artifacts, multiple formats supported

- [ ] **P4-T16: Phase 4 backend tests**
  - What: Tests for Study & Snapshot workflow, snapshot immutability, report rendering, custom reports, export formats
  - Files: `tests/unit/test_study_snapshot.py`, `tests/unit/test_report_rendering.py`, `tests/integration/test_report_pipeline.py`
  - Refs: `phase-4-workspace-reporting.mdc` lines 78-84 (testing rules)
  - Depends on: P4-T02, P4-T03, P4-T05, P4-T06
  - Done when: Full workflow test passes, snapshots immutable, all 7 templates render, PDF/HTML/PPTX valid

- [ ] **P4-T17: OpenAPI type generation for frontend**
  - What: Generate TypeScript types from FastAPI OpenAPI spec for frontend consumption
  - Files: `frontend/src/types/` (generated types)
  - Refs: `Project_Skeleton_Specification.md` §4.3 (line 257, API types generated from OpenAPI)
  - Depends on: P4-T07
  - Done when: TypeScript types match API schema, imported by frontend components

- [ ] **P4-T18: Consultant pilot validation**
  - What: End-to-end validation: create assessment → import data → run diagnostics → investigate in workspace → generate report
  - Files: none (validation task)
  - Refs: `Deployment_Roadmap.md` Phase 4 step 5 (line 192, "Pilot with consultant on live engagements")
  - Depends on: P4-T08 through P4-T16
  - Done when: Full engagement workflow completes end-to-end in the platform

---

## Phase 5 — Client Portal and Longitudinal Tracking

> Cursor rule: `phase-5-client-portal.mdc`
> Services: Client Portal (7 ops), Trend & Trajectory (8 ops)
> Source: spec_1 lines 1348-1352

**Prerequisite:** All Phase 4 tasks complete (workspace functional, at least one full assessment completed).

- [ ] **P5-T01: Trend mart ClickHouse migrations**
  - What: Create 5 longitudinal ClickHouse tables: `fact_assessment_score`, `fact_assessment_finding`, `fact_recommendation_status`, `fact_property_kpi_period`, `fact_unit_chronicity`
  - Files: `db/clickhouse/migrations/004_phase5_trend_marts.sql`
  - Refs: `Database_Schema_Specification.md` — `fact_assessment_score` (line 2731), `fact_assessment_finding` (line 2750), `fact_recommendation_status` (line 2769), `fact_property_kpi_period` (line 2787), `fact_unit_chronicity` (line 2804). `phase-5-client-portal.mdc` lines 57-62 (ordering keys)
  - Depends on: P0-T10
  - Done when: All 5 tables created with correct engines and ordering keys

- [ ] **P5-T02: Trend & Trajectory service — trend mart materialization**
  - What: Implement `build_trend_marts` — materialize trend data per-property after assessment completion
  - Files: `src/services/trend_trajectory/__init__.py`, `src/services/trend_trajectory/service.py`, `src/services/trend_trajectory/repository.py`
  - Refs: `Service_Interface_Contracts.md` §13 (lines 557-597) — `build_trend_marts` (line 577). `phase-5-client-portal.mdc` line 56
  - Depends on: P5-T01
  - Done when: Trend marts populate after assessment, row counts correct per table

- [ ] **P5-T03: Trend & Trajectory service — trajectory and detection operations**
  - What: Implement remaining 7 operations: `get_score_trajectory`, `detect_recurring_findings`, `get_recommendation_status`, `update_recommendation_status`, `compare_assessments`, `get_property_trajectory`, `detect_chronic_units`
  - Files: within `src/services/trend_trajectory/`
  - Refs: `Service_Interface_Contracts.md` §13 (lines 578-584). `phase-5-client-portal.mdc` lines 63-65 (recurring findings, chronic units, assessment comparison rules)
  - Depends on: P5-T02
  - Done when: All 7 operations work, recurring finding detection correct, chronic unit thresholds configurable, cross-property comparison blocked

- [ ] **P5-T04: Recommendation tracking**
  - What: Implement recommendation status management with validated transitions and verification evidence
  - Files: within `src/services/trend_trajectory/`
  - Refs: `phase-5-client-portal.mdc` lines 69-72 (recommendation tracking rules). `Service_Interface_Contracts.md` §13 lines 594-596 (recommendation structure)
  - Depends on: P5-T03
  - Done when: Status transitions validated, invalid transitions rejected, verification evidence stored

- [ ] **P5-T05: Client Portal service**
  - What: Implement Client Portal with 7 operations: `get_executive_overview`, `get_domain_scorecard`, `get_finding_detail`, `get_progress_tracking`, `get_report_library`, `get_limited_explore`, `get_score_trends`
  - Files: `src/services/client_portal/__init__.py`, `src/services/client_portal/service.py`, `src/services/client_portal/repository.py`
  - Refs: `Service_Interface_Contracts.md` §12 (lines 509-553) — 7 operations, access control rules. `phase-5-client-portal.mdc` lines 48-52
  - Depends on: P5-T02
  - Done when: All 7 operations work, only approved outputs returned, PII masking applied, client scoped to own properties

- [ ] **P5-T06: Portal and trend API routes**
  - What: FastAPI routes for Client Portal and Trend & Trajectory services
  - Files: `src/api/routes/portal.py`, `src/api/routes/trends.py`
  - Refs: `Service_Interface_Contracts.md` §12-13
  - Depends on: P5-T03, P5-T05
  - Done when: All 15 operations (7+8) exposed via API

- [ ] **P5-T07: UI — Client Portal: Executive Overview**
  - What: Overall scores, trends, top findings, financial opportunity
  - Files: `frontend/src/app/portal/` (portal pages)
  - Refs: `UI_UX_Specification.md` — Client Portal Module 1
  - Depends on: P4-T01, P5-T05
  - Done when: Executive overview renders with scores, trends, and financial opportunity

- [ ] **P5-T08: UI — Client Portal: Domain Scorecards**
  - What: Per-domain scorecard views for clients
  - Files: `frontend/src/app/portal/scorecards/`
  - Refs: `UI_UX_Specification.md` — Client Portal Module 2
  - Depends on: P5-T07
  - Done when: Domain scorecards render from approved assessment data

- [ ] **P5-T09: UI — Client Portal: Finding Detail and Progress Tracking**
  - What: Evidence-backed findings, recommendations, and cross-assessment progress tracking
  - Files: `frontend/src/app/portal/findings/`, `frontend/src/app/portal/progress/`
  - Refs: `UI_UX_Specification.md` — Client Portal Modules 3-4
  - Depends on: P5-T07
  - Done when: Finding detail views render, progress tracking shows cross-assessment changes

- [ ] **P5-T10: UI — Client Portal: Report Library and Limited Explore**
  - What: Delivered reports list and pre-approved exploration filters
  - Files: `frontend/src/app/portal/reports/`, `frontend/src/app/portal/explore/`
  - Refs: `UI_UX_Specification.md` — Client Portal Modules 5-6. `phase-5-client-portal.mdc` line 51 (no raw SQL, pre-approved only)
  - Depends on: P5-T07
  - Done when: Report library lists delivered reports, limited explore enforces pre-approved filters only

- [ ] **P5-T11: UI — Assessment Compare module (consultant workspace)**
  - What: Longitudinal score, finding, and recommendation tracking across assessments
  - Files: `frontend/src/app/workspace/compare/`
  - Refs: `UI_UX_Specification.md` — Consultant workspace Module 8: Assessment Compare
  - Depends on: P4-T01, P5-T03
  - Done when: Score changes, recurring vs resolved findings, recommendation adoption visible

- [ ] **P5-T12: Client portal access control tests**
  - What: Tests that client users cannot see consultant-only data, drafts, or other clients' data
  - Files: `tests/unit/test_client_portal.py`
  - Refs: `phase-5-client-portal.mdc` lines 76-77 (portal isolation tests)
  - Depends on: P5-T05
  - Done when: All access control scenarios tested and pass

- [ ] **P5-T13: Trend and trajectory tests**
  - What: Tests for trend mart materialization, recurring findings, chronic units, recommendation transitions, assessment comparison
  - Files: `tests/unit/test_trend_trajectory.py`, `tests/integration/test_trend_marts.py`
  - Refs: `phase-5-client-portal.mdc` lines 78-83 (testing rules)
  - Depends on: P5-T03, P5-T04
  - Done when: Recurring finding detection tested (1 assessment, 2 matching, 2 different), chronic unit thresholds tested, invalid transitions rejected, cross-property comparison returns error

- [ ] **P5-T14: Recommendation tracking tests**
  - What: Tests for all valid status transitions, verification evidence storage, invalid transition rejection
  - Files: `tests/unit/test_recommendation_tracking.py`
  - Refs: `phase-5-client-portal.mdc` lines 80-81
  - Depends on: P5-T04
  - Done when: All transition paths tested, completed→open rejected, evidence stored per update

- [ ] **P5-T15: Portal end-to-end validation**
  - What: Validate client user experience: login → view scores → view findings → track progress → download reports
  - Files: none (validation task)
  - Refs: `Deployment_Roadmap.md` Milestone 4 exit criteria (lines 291-296)
  - Depends on: P5-T07 through P5-T10
  - Done when: Client can access all 6 portal modules with only approved content visible

---

## Phase 6 — Door Opener and Extensibility

> Cursor rule: `phase-6-door-opener.mdc`
> Services: Door Opener (6 ops), Extension SDK (6 ops)
> Source: spec_1 lines 1354-1358

**Prerequisite:** All Phase 5 tasks complete (client portal operational, full assessment lifecycle validated).

- [ ] **P6-T01: Door Opener service — assessment and applicability**
  - What: Implement `create_door_opener_assessment` and `get_applicable_items` — 11 of 65 items from applicability matrix
  - Files: `src/services/door_opener/__init__.py`, `src/services/door_opener/service.py`, `src/services/door_opener/repository.py`
  - Refs: `Service_Interface_Contracts.md` §14 (lines 600-652) — `create_door_opener_assessment` (line 620), `get_applicable_items` (line 621). `Door_Opener_Applicability_Matrix.md` (11 items across 3 areas). `phase-6-door-opener.mdc` lines 47-50 (11 item list)
  - Depends on: P3-T11
  - Done when: Door opener assessment creates with type `door_opener`, applicable items return exactly 11 items

- [ ] **P6-T02: Door Opener service — scoring and diagnostics**
  - What: Implement `score_door_opener` and `run_public_data_packages` — score only applicable items, non-applicable as OUT_OF_SCOPE
  - Files: within `src/services/door_opener/`
  - Refs: `Service_Interface_Contracts.md` §14 — `score_door_opener` (line 622), `run_public_data_packages` (line 623). `phase-6-door-opener.mdc` line 51 (non-applicable → OUT_OF_SCOPE)
  - Depends on: P6-T01
  - Done when: Only 11 items scored, remaining 54 return OUT_OF_SCOPE, coverage metadata shows scope clearly

- [ ] **P6-T03: Door Opener service — report generation and upgrade**
  - What: Implement `generate_door_opener_report` and `upgrade_to_full_engagement`
  - Files: within `src/services/door_opener/`
  - Refs: `Service_Interface_Contracts.md` §14 — `generate_door_opener_report` (line 624), `upgrade_to_full_engagement` (line 625). `phase-6-door-opener.mdc` line 52 (upgrade preserves data)
  - Depends on: P6-T02, P4-T03
  - Done when: Door opener report generates with only scored areas, upgrade changes assessment type preserving all data

- [ ] **P6-T04: Public data collection workflow**
  - What: Implement public data ingestion for door opener: ILS listings, review platforms, property website, social, Google Business, app stores
  - Files: within `src/services/door_opener/` or `src/services/import_mapping/adapters/`
  - Refs: `phase-6-door-opener.mdc` lines 56-63 (public data sources). `Service_Interface_Contracts.md` §14 lines 636-643 (data sources)
  - Depends on: P1-T11
  - Done when: Public data sources ingest via structured capture, mapped to canonical entities

- [ ] **P6-T05: Door Opener API routes**
  - What: FastAPI routes for all 6 Door Opener operations
  - Files: `src/api/routes/door_opener.py`
  - Refs: `Service_Interface_Contracts.md` §14 (lines 618-625)
  - Depends on: P6-T01 through P6-T03
  - Done when: All 6 operations exposed via API

- [ ] **P6-T06: Extension SDK — connector registration**
  - What: Implement `register_connector` and `validate_connector` for adding new vendor adapters
  - Files: `src/shared/sdk/__init__.py`, `src/shared/sdk/connector_sdk.py`
  - Refs: `Service_Interface_Contracts.md` §15 (lines 655-683) — `register_connector` (line 670), `validate_connector` (line 671). `phase-6-door-opener.mdc` lines 69-70
  - Depends on: P1-T11
  - Done when: Connectors register with required properties, validation checks adapter protocol compliance against test files

- [ ] **P6-T07: Extension SDK — diagnostic package registration**
  - What: Implement `register_diagnostic_package` and `validate_package`
  - Files: `src/shared/sdk/package_sdk.py`
  - Refs: `Service_Interface_Contracts.md` §15 — `register_diagnostic_package` (line 672), `validate_package` (line 673). `phase-6-door-opener.mdc` line 71
  - Depends on: P3-T01
  - Done when: Packages register with metric/benchmark/rule/formula/template definitions, validation checks completeness

- [ ] **P6-T08: Extension SDK — rubric versioning**
  - What: Implement `register_rubric_version` with weight-sum validation
  - Files: `src/shared/sdk/rubric_sdk.py`
  - Refs: `Service_Interface_Contracts.md` §15 — `register_rubric_version` (line 674). `phase-6-door-opener.mdc` line 73 (weight sum validation)
  - Depends on: P3-T10
  - Done when: Rubric versions register, area weights validated (sum to 100%), item weights validated (sum to 100% per area), sub-item points validated (sum to 100 per checklist item)

- [ ] **P6-T09: Extension SDK — fact grain registration**
  - What: Implement `register_fact_grain` — generates ClickHouse DDL and migration file for new fact tables
  - Files: `src/shared/sdk/fact_grain_sdk.py`
  - Refs: `Service_Interface_Contracts.md` §15 — `register_fact_grain` (line 675). `phase-6-door-opener.mdc` line 72 (new fact grain)
  - Depends on: P0-T10
  - Done when: Fact grain definitions produce valid ClickHouse DDL, migration files generated

- [ ] **P6-T10: Extension SDK API routes**
  - What: FastAPI routes for all 6 SDK operations
  - Files: `src/api/routes/sdk.py`
  - Refs: `Service_Interface_Contracts.md` §15 (lines 668-675)
  - Depends on: P6-T06 through P6-T09
  - Done when: All 6 operations exposed via API

- [ ] **P6-T11: Door Opener tests**
  - What: Tests for applicability matrix enforcement, scoring only applicable items, report generation, upgrade path
  - Files: `tests/unit/test_door_opener.py`
  - Refs: `phase-6-door-opener.mdc` lines 78-81 (testing rules)
  - Depends on: P6-T01 through P6-T03
  - Done when: Only 11 items scored, 54 return OUT_OF_SCOPE, door opener report covers scored areas only, upgrade preserves all data

- [ ] **P6-T12: Extension SDK tests**
  - What: Tests for connector/package/rubric registration and validation, weight sum rejection, fact grain DDL generation
  - Files: `tests/unit/test_extension_sdk.py`
  - Refs: `phase-6-door-opener.mdc` lines 82-84 (testing rules)
  - Depends on: P6-T06 through P6-T09
  - Done when: New connector registers and validates, new package registers and validates, invalid weight sums rejected, fact grain DDL generated correctly

---

## Conventions

**Marking tasks complete:**
```markdown
- [x] **P0-T01: Project skeleton** — abc1234
```

**Marking tasks in progress:**
```markdown
- [~] **P0-T02: Docker Compose** — agent: session-xyz
```

**Marking tasks blocked:**
```markdown
- [!] **P1-T14: Yardi adapter** — waiting on sample Yardi export files
```

Status markers follow `execution-protocol.mdc`: `[ ]` pending, `[~]` in progress, `[x]` complete (with commit hash), `[!]` blocked (with reason).

---

## Authoritative References

| Document | What Tasks Cite It For |
|----------|----------------------|
| `phase-0-foundations.mdc` through `phase-6-door-opener.mdc` | Phase scope, rules, what NOT to build |
| `Code_Patterns_Specification.md` | Exact code templates for services, routes, repos, exceptions, tests, Celery tasks |
| `API_Design_Specification.md` | REST API conventions (URL patterns, pagination, error shapes, OpenAPI) |
| `Authentication_Middleware_Specification.md` | JWT claims, FastAPI dependency chain, tenant resolution, CORS |
| `Infrastructure_Specification.md` | Environment variables, Docker Compose, S3 buckets, secrets, production topology |
| `Observability_Specification.md` | Structured logging, correlation IDs, health checks, audit logging, monitoring |
| `Service_Interface_Contracts.md` | All 85 service operations across 15 services |
| `Database_Schema_Specification.md` | 110 PG tables, 15 CH tables, DDL line numbers |
| `Project_Skeleton_Specification.md` | Repo structure, tech stack, testing strategy, CI/CD |
| `Data_Onramp_Specification.md` | Import pipeline, vendor adapters, column mapping, review queue |
| `Report_Template_Specification.md` | 7 report templates, rendering pipeline, section types |
| `UI_UX_Specification.md` | 8 workspace modules, 6 portal modules |
| `Door_Opener_Applicability_Matrix.md` | 11 of 65 items scorable from public data |
| `Scoring_Weights_Final_Update.json` | 12 area weights, 65 item weights, 315 sub-item budgets |
| `Scoring_Thresholds_Calibration.md` | Piecewise linear interpolation breakpoints |
| `scoring_config.json` | Machine-readable scoring structure |
| `Basic_Analytic_Data_Set.md` | 124 KPIs |
| `Analytical_Engine_Specification.md` | 5-layer architecture |
| `Analytical_Question_Inventory.md` | 16 diagnostic question categories |
| `docs/adrs/ADR-014` | Celery + Redis task queue for pipeline orchestration |
| `docs/adrs/ADR-015` | Managed auth provider, JWT validation, role mapping |
| `docs/adrs/ADR-016` | WeasyPrint + python-pptx for report rendering |
