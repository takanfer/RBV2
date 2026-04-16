# Phase Gate Specifications

Defines the verification checklists that must pass before a phase is considered complete and the next phase can begin. Each gate is an exhaustive checklist with specific commands, expected outputs, and pass/fail criteria.

---

## Gate Report Template

After completing all tasks in a phase, the agent must produce a gate report in this format:

```markdown
# Phase {N} Gate Report

## Tasks Completed
| Task | Commit | Status |
|------|--------|--------|
| P{N}-T01 | abc1234 | PASS |
| P{N}-T02 | def5678 | PASS |

## Verification Results
| Check | Command | Expected | Actual | Status |
|-------|---------|----------|--------|--------|
| Linter | `ruff check src/` | 0 errors | 0 errors | PASS |
| Tests | `pytest` | All pass | 42/42 pass | PASS |

## Coverage
- Files created: {count}
- Tests written: {count}
- Lines of code: {count}

## Known Issues
{none, or list of issues with severity}

## Recommendation
PROCEED to Phase {N+1} / HOLD for {reason}
```

---

## Phase 0 Gate — Foundations

**Prerequisite:** Tasks P0-T01 through P0-T18 all marked `[x]`.

### Infrastructure Checks

| # | Check | Command | Expected Output |
|---|-------|---------|-----------------|
| 1 | Docker Compose starts | `docker compose -f docker/docker-compose.yml up -d` | All 4 services healthy |
| 2 | PostgreSQL accessible | `psql -h localhost -U postgres -d partners -c "SELECT 1"` | Returns 1 |
| 3 | ClickHouse accessible | `clickhouse-client --query "SELECT 1"` | Returns 1 |
| 4 | MinIO accessible | `mc alias set local http://localhost:9090 minioadmin minioadmin && mc ls local/` | Lists buckets |
| 5 | Redis accessible | `redis-cli ping` | PONG |

### Migration Checks

| # | Check | Command | Expected Output |
|---|-------|---------|-----------------|
| 6 | Migrations apply cleanly | `alembic upgrade head` | No errors, creates tables |
| 7 | Migration round-trip | `alembic downgrade base && alembic upgrade head` | No errors |
| 8 | Tenant table exists | `psql -c "\d tenant"` | Shows tenant table columns |
| 9 | RLS enabled on tenant-scoped tables | `psql -c "SELECT tablename, rowsecurity FROM pg_tables WHERE schemaname='public' AND rowsecurity=true"` | Lists source_system, user_account, audit_log, client, property, vendor, assessment |
| 10 | ClickHouse schema exists | Query `SHOW TABLES` | Database created |

### Service Checks

| # | Check | Command | Expected Output |
|---|-------|---------|-----------------|
| 11 | AuthZ check_access works | `pytest tests/unit/test_authz.py` | All tests pass |
| 12 | Tenant isolation verified | `pytest tests/integration/test_tenant_isolation.py` | Cross-tenant access denied |
| 13 | Engagement service works | `pytest tests/unit/test_engagement.py` | All tests pass |
| 14 | API starts | `uvicorn src.api.main:app --host 0.0.0.0 --port 8000` | Server starts, health check returns 200 |
| 15 | JWT middleware rejects invalid token | `curl -H "Authorization: Bearer invalid" http://localhost:8000/api/...` | 401 response |
| 16 | Audit logging works | Mutation → `SELECT * FROM audit_log` | Audit entries created |

### Code Quality Checks

| # | Check | Command | Expected Output |
|---|-------|---------|-----------------|
| 17 | Linter passes | `ruff check src/ tests/` | 0 errors |
| 18 | All tests pass | `pytest` | All pass |
| 19 | Validator passes | `python codegen/validate_docs.py` | 0 errors |
| 20 | Generated models match DDL | `python codegen/generate_models.py ... && diff` | No drift |

### Pattern Lock Checkpoint (P0-CK1 through P0-CK3)

| # | Check | Expected |
|---|-------|----------|
| 21 | Code Patterns reviewed against actual code | Written deviation report |
| 22 | Code Patterns Specification updated | Any new patterns added |
| 23 | Patterns locked | Specification committed, no further changes without ADR |

---

## Phase 1 Gate — Canonical Core

**Prerequisite:** Tasks P1-T01 through P1-T16 all marked `[x]`. Phase 0 gate passed.

### Schema Checks

| # | Check | Command | Expected Output |
|---|-------|---------|-----------------|
| 1 | All PostgreSQL tables exist | `psql -c "SELECT count(*) FROM pg_tables WHERE schemaname='public'"` | 110 tables |
| 2 | ClickHouse temporal facts exist | Query `SHOW TABLES` in partners DB | Phase 2 fact tables present |
| 3 | All indexes created | `psql -c "SELECT count(*) FROM pg_indexes WHERE schemaname='public'"` | Matches DDL index count |
| 4 | All Pydantic models generated | `ls src/shared/models/*.py \| wc -l` | 14 modules |
| 5 | Model field count | `python -c "... count fields ..."` | 1,393 fields |

### Import Pipeline Checks

| # | Check | Expected |
|---|-------|----------|
| 6 | File upload to S3 works | Upload returns source_asset with SHA-256 hash |
| 7 | Duplicate detection works | Re-upload same file → rejected as duplicate |
| 8 | Column mapping applies | Mapped fields populate canonical tables |
| 9 | Review queue works | Unmapped columns appear in review queue |
| 10 | Entity resolution works | Unit aliases merge correctly |

### Temporal Spine Checks

| # | Check | Expected |
|---|-------|----------|
| 11 | Unit existence intervals created | unit_existence_interval records span full history |
| 12 | Lease intervals constructed | lease_interval records link to units correctly |
| 13 | Vacancy cycles computed | vacancy_cycle records match expected gaps |
| 14 | ClickHouse fact_unit_day populated | Daily grain records exist for assessment period |

### Code Quality (same as Phase 0)

| # | Check | Command | Expected Output |
|---|-------|---------|-----------------|
| 15 | Linter | `ruff check src/ tests/` | 0 errors |
| 16 | Tests | `pytest` | All pass |
| 17 | Validator | `python codegen/validate_docs.py` | 0 errors |

---

## Phase 2 Gate — Metric Engine

**Prerequisite:** Tasks P2-T01 through P2-T16 all marked `[x]`. Phase 1 gate passed.

### Metric Computation Checks

| # | Check | Expected |
|---|-------|----------|
| 1 | All 124 BADS KPIs computable (with sufficient data) | Metric engine returns values for all KPIs given complete test data |
| 2 | Zero-denominator handling | KPIs with zero denominators return NULL, not errors |
| 3 | Missing data coverage tracking | Coverage percentage per area computed correctly |
| 4 | Date range variable respected | KPIs use assessment date range, not hardcoded periods |
| 5 | Annualization correct | Short-period rates annualized per BADS Edge Case Rules |

### ClickHouse Fact Checks

| # | Check | Expected |
|---|-------|----------|
| 6 | fact_property_kpi_period populated | Period-grain KPIs materialized |
| 7 | Historical comparison works | Can query current vs prior period |

---

## Phase 3 Gate — Analytical Engine

**Prerequisite:** All Phase 3 tasks marked `[x]`. Phase 2 gate passed.

### Scoring Engine Checks

| # | Check | Expected |
|---|-------|----------|
| 1 | All 20 Data items score correctly | Piecewise linear interpolation matches Scoring_Algorithm_Specification.md |
| 2 | All 38 Checklist items score correctly | 100-point budget produces correct 0-10 scores |
| 3 | All 7 Comparative items score correctly | Methods A-D produce correct scores |
| 4 | Financial variance scoring works | Budget vs actual variance mapped to scores |
| 5 | Missing items excluded from average | Weights redistributed, coverage tracked |
| 6 | Area scores computed | Weighted average of item scores |
| 7 | Overall score computed | Weighted average of area scores |

### Layer Checks

| # | Check | Expected |
|---|-------|----------|
| 8 | Layer 2 (Cohort Profiling) | Cohort identification and percentile ranking |
| 9 | Layer 3 (Diagnostics) | Finding generation with evidence bundles |
| 10 | Layer 4 (Pattern Detection) | Cross-area pattern identification |
| 11 | Layer 5 (Impact Summary) | Prioritized impact estimates |

---

## Phases 4–6 Gates

Phase 4 (Workspace & Reporting), Phase 5 (Door Opener), and Phase 6 (Extensibility) follow the same pattern: all tasks complete, all tests pass, all specifications verified. Detailed gate checklists for these phases should be created at the start of each phase based on the task list and service contracts.

---

## Authoritative Sources

- `planning/Implementation_Tasks.md` — Task definitions and done-when criteria
- `Code_Patterns_Specification.md` — Code quality standards
- `Database_Schema_Specification.md` — DDL for schema verification
- `Scoring_Algorithm_Specification.md` — Scoring correctness criteria
- `Basic_Analytic_Data_Set.md` — 124 KPI definitions
- `BADS_Edge_Case_Rules.md` — Edge case handling rules
