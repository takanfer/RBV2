# Deployment Roadmap

Complete deployment roadmap for the RBv2 Multifamily Property Assessment Platform. Every claim in this document cites a specific source file. Nothing is elaborated beyond what the source documents state.

> **Authority:** This document is the authoritative source for phase scope. It defines which services, DDL domains, and capabilities belong to each phase. If `Implementation_Tasks.md` conflicts with this document, this document wins.

**Supersedes:** `Version 6/Working Docs/Planning Docs/Remaining_Work_Plan.md` (V6 Google Apps Script system -- deprecated, reference only)

---

## Current State

All pre-implementation documentation is complete. The platform is ready for Phase 0 implementation.

### Verified Documentation Inventory

Every file below was confirmed to exist on disk as of 2026-04-13.

**Scoring and Analytical Domain**

| File | Verified Content | Source Verification |
|------|-----------------|---------------------|
| `Scoring_Weights_Final_Update.json` | 12 area weights (`aw__` keys), 65 item weights (`iw__` keys), 315 sub-item point budgets (`sp__` keys) | Grep counts: `aw__` = 12, `iw__` = 65, `sp__` = 315 |
| `Scoring_Model_Specification.md` | "Defines the complete structure and methodology of what the analytical engine scores, organized into 12 operational areas. This is the specification for Layer 1 (Scoring) of the Analytical Engine." (line 1) | Read line 1-3 |
| `Scoring_Model_Workbook.html` | Tier definitions and sub-item point budgets (HTML format) | File exists, 45,898 bytes |
| `Computation_Rules_Workbook.html` | Computation method, data source, input format per scored item (HTML format) | File exists, 71,358 bytes |
| `Computation_Rules_DATA.json` | Machine-readable extraction: area/item/type/source/method/format structure | Read lines 1-10: JSON array with area, items, name, type, source, method, format fields |
| `Scoring_Thresholds_Calibration.md` | "Defines the specific benchmark values that map raw inputs to 0-10 scores for all Data-type and Comparative-type items." (line 1) | Read line 1-3 |
| `scoring_config.json` | 12 areas (grep `"number":` = 12), structured with items containing type, weight, source, thresholds, sub-items | Read lines 1-15, grep count verified |
| `Analytical_Engine_Specification.md` | Pre-Computation (BADS) + 5 structured layers (Scoring, Cohort Profiling, Correlative Diagnostics, Emergent Pattern Detection, Unified Impact Summary) + AI Analysis Layer (advisory only) | Grep for `^## Layer\|^## Pre-Computation\|^## AI Analysis` returns 6 headings at lines 94, 145, 217, 278, 335, 371 |
| `Basic_Analytic_Data_Set.md` | "Standard property performance KPIs" -- Total: 124 KPIs (line 301: `**Total** | **124**`) | Read lines 1-15, grep confirmed |
| `Analytical_Question_Inventory.md` | Diagnostic questions across 16 categories (grep `^## [0-9]` returns 16 headings: Vacancy & Turnover through Cohort Profiling & Pattern Recognition) | Grep confirmed 16 categories |

**Data Collection Domain**

| File | Verified Content | Source Verification |
|------|-----------------|---------------------|
| `Complete_Data_Inventory.md` | "Every data field collected across all sources." Two data streams: PM Data Set and Audit Data Set. 1,100+ fields. (lines 1-9) | Read lines 1-15 |
| `Audit_Workbook_Specification.md` | "The single authoritative document for everything the auditor collects across both assessment types." Two workflows: Door Opener and Full Engagement. (lines 1-14) | Read lines 1-15 |

**Platform Architecture**

| File | Verified Content | Source Verification |
|------|-----------------|---------------------|
| `spec_1_multifamily_property_assessment_platform.md` | 30 must-have requirements (M1-M30), 7 should-have requirements (S1-S7), 4-layer data model (A-D, line 182), 6-domain entity model (line 240-249), 7 phases (0-6, lines 1307-1358), 5 milestones (lines 1370-1403) | Grep counts: `M[0-9]` = 30, `S[0-9]` = 7. Section headings confirmed at cited lines. |
| `Database_Schema_Specification.md` | 110 PostgreSQL tables (lowercase `create table` count = 110) + 15 ClickHouse tables (uppercase `CREATE TABLE` count = 15) = 125 total | Grep counts verified |
| `Shared_Type_Definitions.md` | "Total models: 125, Total fields: 1393" (lines 12-13). Generated from DDL. 14 domain modules. | Read lines 1-20 |
| `Project_Skeleton_Specification.md` | Monorepo structure, 11 named services (lines 190-206), naming conventions, testing strategy, CI/CD | Read lines 190-224 |
| `Service_Interface_Contracts.md` | "Protocol interfaces for all Phase 0–6 application services." (line 1). Pipeline sequence + 15 service contracts. Phase summary table at lines 702-712 covers Phases 0-6. | Read lines 1-11, 700-713 |
| `Data_Onramp_Specification.md` | "Two Data Streams" (line 13), "four ingestion patterns" (line 57), vendor adapters, column mapping, review queue | Read confirmed at cited lines |
| `Glossary.md` | "Standardized terminology for the Multifamily Property Assessment Platform. Every definition sourced from existing specification documents." (line 1) | Read lines 1-15 |

**Agent Drift Prevention (Code Pattern Enforcement)**

| File | Verified Content | Source Verification |
|------|-----------------|---------------------|
| `Code_Patterns_Specification.md` | 18 literal code templates: service module structure, route functions, service functions, repository functions, exceptions, tests, audit logging, Celery tasks, Pydantic Settings, FastAPI app initialization, PostgreSQL connection factory, get_db dependency, ClickHouse client factory, table definitions, S3 wrapper, Celery app factory, worker entry point, auth routes | File created, read in full |
| `API_Design_Specification.md` | URL conventions, HTTP methods, cursor-based pagination, error envelope shape, filtering/sorting, auth header, OpenAPI rules | File created, read in full |
| `Authentication_Middleware_Specification.md` | JWT claims schema (6 claims), 8-step middleware flow, FastAPI dependency chain, JWKS caching, CORS config, 8 error response codes | File created, read in full |
| `Infrastructure_Specification.md` | 22 environment variables, Docker Compose services, S3 bucket key structure, secrets management boundary, production AWS topology, ECS service definitions | File created, read in full |
| `Observability_Specification.md` | Structured JSON log format (5 required + 8 optional fields), log level policy, correlation ID propagation, health check contract (4 checks), audit log schema, 9 production metrics | File created, read in full |

**Governance Layer**

| Artifact | Verified Content |
|----------|-----------------|
| `docs/adrs/` | 16 ADR files: ADR-001 through ADR-016 + README.md. ADR-014 (Celery + Redis), ADR-015 (AWS Cognito), ADR-016 (WeasyPrint + python-pptx) added for workflow orchestration, authentication, and report rendering. |
| `.cursor/rules/rbv2-project.mdc` | 21-document authoritative hierarchy, scoring constraints, tech stack, naming conventions, working principles including "DDL is the source of truth" (lines 1-171, read in full) |
| `.cursor/rules/phase-0-foundations.mdc` | Phase 0 implementation rules: what to build, technology constraints, schema rules, testing rules, what NOT to build (lines 1-89, read in full) |
| `.cursor/rules/phase-1-canonical-core.mdc` | Phase 1 implementation rules: canonical entities, import framework, connector rules, entity resolution rules, idempotency (lines 1-87, read in full) |
| `codegen/generate_models.py` | DDL-to-Pydantic generation script using sqlglot parser (file exists, confirmed) |
| `codegen/test_ddl.sql` | Test DDL for 4 Asset domain tables (file exists, confirmed) |
| `codegen/expected_asset.py` | Hand-written answer key for generation validation (file exists, confirmed) |
| `codegen/output/` | 14 generated `.py` domain modules + Shared_Type_Definitions.md + VERIFICATION_REPORT.txt (ls confirmed 16 files) |

### Deprecated (in `DEPRECATED/` folder)

All 6 files confirmed present in `DEPRECATED/` via ls:

| File | Why Deprecated |
|------|---------------|
| `data_dictionary.json` (161,159 bytes) | Superseded by DDL + generated Shared_Type_Definitions |
| `DDL_VERIFICATION_REPORT.txt` (131,419 bytes) | One-time verification artifact |
| `DDL_DEEP_VERIFICATION_REPORT.txt` (9,580 bytes) | One-time verification artifact |
| `Gemini_Prompt_Cross_Source_Analysis.md` (11,621 bytes) | One-time analysis |
| `Scoring_Items_List-Deprecated.md` (15,812 bytes) | Superseded by Scoring_Model_Specification |
| `Scoring_Model_Specification-Deprecated.md` (33,242 bytes) | Superseded by current version |

### Documentation Gaps

All previously identified documentation gaps have been closed:

- `Report_Template_Specification.md` — report composition model, rendering pipeline, 7+ standard templates (structural framework; template content to be defined during Phase 4)
- `Door_Opener_Applicability_Matrix.md` — 11 of 65 items scorable from public data, strict interpretation
- `UI_UX_Specification.md` — module inventory, user roles, data dependencies, user flows, access boundaries (structural framework; visual design and component specs to be defined during Phase 4)
- `Code_Patterns_Specification.md` — 18 literal code templates preventing pattern drift across agent sessions
- `API_Design_Specification.md` — REST API conventions (URL patterns, pagination, error shapes, auth headers)
- `Authentication_Middleware_Specification.md` — JWT claims, FastAPI dependency chain, tenant resolution flow, CORS
- `Infrastructure_Specification.md` — environment variables, Docker Compose, S3 bucket structure, secrets management, production topology
- `Observability_Specification.md` — structured logging, correlation IDs, health checks, audit logging, monitoring metrics

---

## Governance Model

Source: `rbv2-project.mdc` lines 151-170 (Model Generation Pipeline, Working Principles)

### DDL-First Pipeline

The DDL in `Database_Schema_Specification.md` is the single source of truth for all data structures (rbv2-project.mdc line 169: "DDL is the source of truth").

Pipeline (rbv2-project.mdc lines 153-159):
1. DDL is written/modified in `Database_Schema_Specification.md`
2. `codegen/generate_models.py` parses the DDL and generates Pydantic models
3. Generated `.py` files are copied to `src/shared/models/`
4. All services import from `src/shared/models/` -- no hand-written models
5. `Shared_Type_Definitions.md` is the human-readable reference generated alongside the models

### Phase-Specific Cursor Rules

Rules exist for all 7 phases (0-6). Each phase-specific `.mdc` file defines scope, authoritative references, implementation rules, testing requirements, and what NOT to build.

---

## Implementation Phases

Source: `spec_1` lines 1305-1358. Reproduced verbatim below -- no elaboration, no reordering, no invented workstreams.

### Phase 0 -- Foundations

> Source: spec_1 lines 1307-1311

1. Establish tenancy, identity, auth, and property/assessment model.
2. Stand up object storage, PostgreSQL, analytical warehouse, and workflow orchestration.
3. Create source registry, ingestion job model, and raw evidence store.
4. Implement audit logging and version registries.

**Services built in this phase:** AuthZ, Engagement (Service_Interface_Contracts.md line 706)

**Authentication provider:** AWS Cognito (ADR-015). Handles user login, registration, password management, and JWT issuance. The platform validates Cognito-issued JWTs and enforces authorization via the AuthZ service.

**Relevant cursor rule:** `phase-0-foundations.mdc`

---

### Phase 1 -- Canonical core and import framework

> Source: spec_1 lines 1313-1318

1. Build canonical asset, lease, resident, vendor, and staff schemas.
2. Build file import framework with schema mapping UI and review queue.
3. Implement first connectors for PM exports, CRM exports, and manual field forms.
4. Add entity resolution and alias mapping.
5. Persist coverage metadata and source provenance.

**Services built in this phase:** Import & Mapping, Entity Resolution (Service_Interface_Contracts.md line 707)

**Relevant cursor rule:** `phase-1-canonical-core.mdc`

---

### Phase 2 -- Temporal unit spine

> Source: spec_1 lines 1320-1325

1. Build `unit`, `unit_version`, `unit_existence_interval`, and alias model.
2. Implement interval resolvers for occupancy, notice, readiness, listing, and pricing.
3. Materialize `fact_unit_day`.
4. Build vacancy cycle and make-ready cycle facts.
5. Validate against sample properties with units that had no events.

**Services built in this phase:** Temporal State Builder (Service_Interface_Contracts.md line 708)

**Cursor rule:** `phase-2-temporal-spine.mdc` (created)

---

### Phase 3 -- Core diagnostics

> Source: spec_1 lines 1327-1339

1. Implement metric registry and benchmark registry.
2. Ship domain packages for:
   - vacancy/turnover
   - make-ready/maintenance
   - leasing/CRM
   - listing quality
   - pricing/revenue
   - competitive position
   - property condition
3. Implement contradiction engine.
4. Implement scorecards and impact model catalog.
5. Build evidence-backed finding compiler.

**Services built in this phase:** Metric Engine, Scoring Engine, Finding Compiler, Impact Engine (Service_Interface_Contracts.md line 709)

**Cursor rule:** `phase-3-core-diagnostics.mdc` (created)

**Note:** The Analytical Engine Specification defines a 5-layer architecture (Pre-Computation + Layers 1-5 + AI Advisory Layer) that maps to this phase's deliverables. The Scoring Engine implements Layer 1; domain packages + contradiction engine implement Layers 2-3; the impact model catalog aligns with Layer 5. The Analytical Engine Specification should be read alongside spec_1 Phase 3 for implementation detail.

---

### Phase 4 -- Workspace and reporting

> Source: spec_1 lines 1341-1346

1. Build diagnostic hub and drilldown pages.
2. Build studies, snapshots, comparison boards, and annotations.
3. Build report template system and rendering pipeline.
4. Add export formats and evidence bundles.
5. Pilot with consultant on live engagements.

**Services built in this phase:** Study & Snapshot, Report Rendering (Service_Interface_Contracts.md line 710)

**Prerequisites created:** `Report_Template_Specification.md` (structural framework), `UI_UX_Specification.md` (structural framework). Template content and visual design to be defined during implementation.

**Cursor rule:** `phase-4-workspace-reporting.mdc` (created)

---

### Phase 5 -- Client portal and longitudinal tracking

> Source: spec_1 lines 1348-1352

1. Build client portal with approved scorecards, findings, trends, and report library.
2. Add recommendation tracking and follow-up assessment compare views.
3. Build trend marts and recurring finding logic.
4. Add property trajectory dashboards.

**Services built in this phase:** Client Portal, Trend & Trajectory (Service_Interface_Contracts.md §12-13)

**Cursor rule:** `phase-5-client-portal.mdc` (created)

---

### Phase 6 -- Door opener and extensibility

> Source: spec_1 lines 1354-1358

1. Add `DOOR_OPENER` assessment type and applicability matrix.
2. Add public listing/marketing collection workflow.
3. Add additional diagnostic packages for public-data-only analyses.
4. Publish connector SDK / package SDK for future extensions.

**Services built in this phase:** Door Opener, Extension SDK (Service_Interface_Contracts.md §14-15)

**Prerequisite created:** `Door_Opener_Applicability_Matrix.md` — 11 of 65 items scorable from public data.

**Cursor rule:** `phase-6-door-opener.mdc` (created)

---

### Suggested delivery team

> Source: spec_1 lines 1360-1366

- 1 product-minded architect / tech lead
- 2 full-stack engineers
- 1 data engineer / analytics engineer
- 1 front-end engineer
- 1 QA / data validation analyst
- Consultant as domain owner for rubric and output validation

---

## Service-to-Phase Map

Source: Service_Interface_Contracts.md lines 702-712 (Phase Summary table). Reproduced verbatim.

| Phase | Services Built | Milestone |
|-------|---------------|-----------|
| 0 | AuthZ, Engagement | Tenancy, identity, assessment lifecycle |
| 1 | Import & Mapping, Entity Resolution | PM/CRM files ingest, unit identity resolves |
| 2 | Temporal State Builder | `fact_unit_day` materializes, every unit queryable for every day |
| 3 | Metric Engine, Scoring Engine, Finding Compiler, Impact Engine | Full diagnostic pipeline produces scored findings with $ impact |
| 4 | Study & Snapshot, Report Rendering | Workspace investigations, report generation |
| 5 | Client Portal, Trend & Trajectory | Client-facing approved outputs, longitudinal tracking, recommendation adoption |
| 6 | Door Opener, Extension SDK | Public-data-only assessments, connector/package extensibility framework |

---

## DDL Scope Per Phase

Derived from spec_1 Phase definitions, Service Interface Contracts, and Database Schema Specification domain structure.

| Phase | DDL Scope | Source |
|-------|-----------|--------|
| 0 | **PostgreSQL:** Domain 1 — tenant, user_account, audit_log (tenancy + identity). Raw evidence store (Layer&nbsp;A) — source_system, source_ingestion, source_asset, source_record_raw, mapping_rule, mapping_review_queue. Domain 2 partial — client, portfolio, property (property model per spec_1 line 1308). Domain 10 partial — assessment, assessment_data_coverage (assessment model per spec_1 line 1308). | spec_1 line 1308 "tenancy, identity, auth, and property/assessment model"; line 1310 "source registry, ingestion job model, and raw evidence store" |
| 1 | **PostgreSQL:** Remaining Domain 2 (building, floor_plan, unit, unit_version, unit_existence_interval, unit_alias, calendar_day, property_amenity, unit_amenity, market_context). Domains 3-9 (Resident/Lease, Operations, Demand, Listing/Marketing, Market/Competition, Mystery Shop, Technology Stack). Domain 12 (Staffing). Domain 13 (Scoring Configuration). | spec_1 line 1314 "Build canonical asset, lease, resident, vendor, and staff schemas" |
| 2 | **ClickHouse:** fact_unit_day, fact_lease_interval, fact_lead_funnel_event, fact_listing_observation, fact_marketing_presence_day, fact_comp_listing_observation (temporal facts). | spec_1 line 1322 "Materialize fact_unit_day" + related temporal facts |
| 3 | **PostgreSQL:** Remaining Domain 10 (analysis_run, scorecard, score_result, finding, impact_estimate, contradiction, recommendation). **ClickHouse:** fact_score_result, fact_finding_impact, fact_assessment_score, fact_assessment_finding, fact_recommendation_status, fact_property_kpi_period, fact_unit_chronicity (score/finding/impact facts). | spec_1 lines 1327-1339 (core diagnostics + scorecards + findings) |
| 4 | **PostgreSQL:** Domain 11 (study, saved_query, result_snapshot, study_item, comparison_board, annotation, evidence_bundle, report, report_section, report_render). | spec_1 lines 1341-1346 (workspace and reporting) |
| 5-6 | No new DDL expected. Uses existing tables. | spec_1 lines 1348-1358 (client portal + door opener use existing models) |

---

## Milestones

Source: spec_1 lines 1370-1403. Reproduced verbatim.

### Milestone 1 -- Ingestion and temporal foundation

**Exit criteria:**
- PM and CRM files ingest successfully
- raw evidence preserved
- unit identity and dense unit-day state are working
- analyst can query every unit for every day in scope

### Milestone 2 -- Autonomous first-wave diagnostics

**Exit criteria:**
- core domain packages run automatically
- scorecards and findings generate with evidence links
- contradiction engine identifies PM vs field mismatches
- impact engine produces quantified opportunity estimates

### Milestone 3 -- Consultant workbench

**Exit criteria:**
- studies, snapshots, comparison boards, and ad hoc analysis are functional
- consultant can build a full engagement inside the platform
- exports are stable and reproducible

### Milestone 4 -- Client-ready deliverables

**Exit criteria:**
- standard report templates render professionally
- client portal exposes approved outputs
- assessment-to-assessment comparisons are visible

### Milestone 5 -- Door opener and recurring assessments

**Exit criteria:**
- public-data-only assessments work
- recurring assessments preserve trends and recommendation tracking
- new diagnostic packages can be added without reworking the data model

---

## Phase-to-Milestone Mapping

Derived from spec_1 phase steps and milestone exit criteria:

| Milestone | Phases Covered | Rationale |
|-----------|---------------|-----------|
| 1 | 0, 1, 2 | Milestone 1 exit criteria require ingestion (Phase 1) AND dense unit-day state (Phase 2). Phase 0 is foundational infrastructure. |
| 2 | 3 | Milestone 2 exit criteria map directly to Phase 3 deliverables (domain packages, scorecards, contradiction engine, impact engine). |
| 3 | 4 | Milestone 3 exit criteria map to Phase 4 deliverables (studies, snapshots, workspace, exports). |
| 4 | 4 (reporting) + 5 | Milestone 4 exit criteria require report templates (Phase 4) AND client portal (Phase 5). |
| 5 | 5, 6 | Milestone 5 exit criteria require trend tracking and recommendation adoption (Phase 5) AND door opener assessments and extensibility (Phase 6). |

---

## What to Do Next

Phase 0 can begin immediately. All prerequisite documentation for Phase 0 is complete per `phase-0-foundations.mdc` (lines 30-44: "Before writing any code, read these documents").

**Task-level implementation plan:** `Implementation_Tasks.md` contains 125 sequenced, dependency-aware tasks across all 7 phases with checkbox progress tracking. Use it as the working checklist for implementation.

**Post-Phase 0 checkpoint (mandatory before Phase 1):**

After Phase 0 is complete, a pattern-lock checkpoint must occur before any Phase 1 work begins. This is tracked as tasks P0-CK1 through P0-CK3 in `Implementation_Tasks.md`:

1. Review all Phase 0 code against `Code_Patterns_Specification.md` — confirm patterns were followed, identify any deviations or improvements
2. Update `Code_Patterns_Specification.md` with any patterns that emerged during Phase 0 that were not anticipated
3. Run `codegen/validate_docs.py` to confirm all documentation still aligns, then lock patterns — no further changes to `Code_Patterns_Specification.md` without explicit approval

---

## Authoritative References

| Document | What This Roadmap Cites It For |
|----------|-------------------------------|
| `spec_1` lines 1305-1403 | Phase definitions and milestone exit criteria |
| `Service_Interface_Contracts.md` lines 702-712 | Service-to-phase mapping |
| `rbv2-project.mdc` lines 148-164 | DDL-first pipeline and governance model |
| `phase-0-foundations.mdc` lines 30-44 | Phase 0 prerequisites |
| `phase-1-canonical-core.mdc` lines 24-35 | Phase 1 prerequisites |
| `Analytical_Engine_Specification.md` lines 94-415 | 5-layer engine architecture (context for Phase 3) |
| `Data_Onramp_Specification.md` lines 13, 57 | Two data streams, four intake channels |
| `Basic_Analytic_Data_Set.md` line 301 | 124 KPI count |
| `Analytical_Question_Inventory.md` | 16 diagnostic question categories |
| `Database_Schema_Specification.md` | 125 tables (110 PG + 15 CH), 1,393 columns |
| `Shared_Type_Definitions.md` lines 12-13 | 125 models, 1,393 fields, 14 domain modules |
| `Scoring_Weights_Final_Update.json` | 12 area weights, 65 item weights, 315 sub-item budgets |
| `Code_Patterns_Specification.md` | 18 code templates for agent consistency |
| `API_Design_Specification.md` | REST API conventions |
| `Authentication_Middleware_Specification.md` | JWT auth middleware patterns |
| `Infrastructure_Specification.md` | Environment, containers, S3, secrets, production topology |
| `Observability_Specification.md` | Logging, correlation IDs, health checks, audit, monitoring |
