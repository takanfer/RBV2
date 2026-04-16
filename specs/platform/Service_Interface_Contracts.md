# Service Interface Contracts

Protocol interfaces for all Phase 0–6 application services. Data shapes reference the generated Pydantic models in `src/shared/models/` (no local copies that can drift). Error conditions for every service.

**Source documents:**
- `spec_1` — §3 (architecture), §5.4 (pipeline), §6 (scoring), §7 (impact), §8 (contradictions), §9 (workspace), §10 (intake), §11.2 (client portal), §12 (reporting), §14 (longitudinal tracking), §15 (extensibility), §16 (security)
- `Database_Schema_Specification.md` — all table structures
- `Shared_Type_Definitions.md` / generated `src/shared/models/` — Pydantic model definitions
- `Data_Onramp_Specification.md` — import pipeline and mapping details
- `Door_Opener_Applicability_Matrix.md` — 65-item Door Opener scoring applicability

**Convention:** All services are Python modules in `src/services/<name>/`. Services communicate via direct Python imports (not HTTP) when running in the same process. FastAPI routes in `src/api/routes/` delegate to services.

---

## Pipeline Sequence

Services execute in a fixed pipeline order. Each service's output feeds the next.

```
Import & Mapping  →  Entity Resolution  →  Temporal State Builder  →  Metric Engine
                                                                          │
                                                          Scoring Engine  ←┘
                                                                │
                                                    Finding Compiler  ←┘
                                                                │
                                                      Impact Engine  ←┘
                                                                │
                                                Report Rendering  ←┘
```

Cross-cutting: Engagement Service (lifecycle), AuthZ (every call), Study & Snapshot (workspace).

---

## 1. AuthZ / Tenant Policy

**Phase:** 0  
**Directory:** `src/services/authz/`  
**Store:** PostgreSQL (Canonical OLTP)

### Responsibility

Enforces multi-tenant access control at every service boundary. All other services call AuthZ before reading or writing scoped data.

### Models (from `src/shared/models/infrastructure.py`)

- `Tenant` — consultant organization
- `Client` — property owner / client within a tenant
- `Portfolio` — group of properties within a client
- `UserAccount` — individual user with role and scope

### Interface

| Operation | Input | Output | Error Conditions |
|-----------|-------|--------|-----------------|
| `check_access` | user_id, resource_type, resource_id, action | `AccessDecision` (allow/deny + scopes) | `PermissionDenied`, `TenantMismatch` |
| `get_tenant_context` | user_id | `TenantContext` (tenant_id, client_ids, roles) | `UserNotFound`, `TenantSuspended` |
| `enforce_row_filter` | tenant_context, table_name | SQL filter clause for row-level security | `InvalidScope` |

### Security model (spec_1 §16.1)

| Scope Level | Entities |
|-------------|---------|
| Tenant (consultant org) | All data within the org |
| Client | Properties belonging to one client |
| Portfolio | Subset of a client's properties |
| Property | Single property |
| Assessment | Single assessment within a property |

RLS (row-level security) is enforced at the transactional layer. Client portal access uses restricted marts.

---

## 2. Engagement Service

**Phase:** 0  
**Directory:** `src/services/engagement/`  
**Reads:** PostgreSQL  
**Writes:** PostgreSQL

### Responsibility

Manages the assessment lifecycle: creating properties, creating assessments, configuring comp sets, tracking data coverage, and workflow state.

### Models (from `src/shared/models/assessment.py` + `asset.py`)

- `Assessment` — assessment configuration (type, date range, status)
- `AssessmentDataCoverage` — which data sources have been provided
- `Property` — the subject and comp properties

### Interface

| Operation | Input | Output | Error Conditions |
|-----------|-------|--------|-----------------|
| `create_assessment` | property_id, assessment_type, date_range | `Assessment` | `PropertyNotFound`, `OverlappingAssessment` |
| `update_assessment_status` | assessment_id, new_status | `Assessment` | `InvalidStatusTransition`, `AssessmentNotFound` |
| `get_assessment` | assessment_id | `Assessment` with coverage summary | `AssessmentNotFound`, `PermissionDenied` |
| `update_data_coverage` | assessment_id, source_type, coverage_status | `AssessmentDataCoverage` | `AssessmentNotFound` |
| `configure_comp_set` | assessment_id, comp_property_ids | `CompetitiveSet` | `TooFewComps`, `CompNotFound` |
| `get_run_status` | assessment_id | Pipeline stage + per-service completion | `AssessmentNotFound` |

### Assessment types

| Type | Badge | Data Sources |
|------|-------|-------------|
| `door_opener` | Public data only | Listings, websites, social, reputation, comp observations |
| `full_engagement` | Full access | All door opener data + PM exports + site visit + mystery shop + interviews |

---

## 3. Import & Mapping Service

**Phase:** 1  
**Directory:** `src/services/import_mapping/`  
**Reads:** PostgreSQL (Canonical OLTP), S3 (Raw Evidence)  
**Writes:** S3 (Raw Evidence), PostgreSQL (Canonical OLTP)

### Responsibility

File parsing, vendor adapter execution, column mapping, validation, and the mapping review queue. Detailed pipeline in `Data_Onramp_Specification.md`.

### Models (from `src/shared/models/raw_evidence.py`)

- `SourceSystem` — registered vendor/source
- `SourceIngestion` — import job
- `SourceAsset` — raw file preserved in S3
- `SourceRecordRaw` — parsed rows awaiting mapping
- `MappingRule` — column mapping definitions
- `MappingReviewQueue` — items needing human review

### Interface

| Operation | Input | Output | Error Conditions |
|-----------|-------|--------|-----------------|
| `create_ingestion` | source_system_id, assessment_id, files | `SourceIngestion` | `SourceSystemNotFound`, `UnsupportedFileType` |
| `upload_asset` | ingestion_id, file_bytes, filename, mime_type | `SourceAsset` | `DuplicateHash` (idempotent), `StorageError` |
| `parse_asset` | asset_id | list of `SourceRecordRaw` | `ParseError`, `UnsupportedFormat` |
| `apply_mappings` | ingestion_id | mapping results (auto/review counts) | `NoMappingRules`, `SchemaValidationError` |
| `get_review_queue` | ingestion_id | list of `MappingReviewQueue` items | `IngestionNotFound` |
| `resolve_review_item` | review_id, resolution, mapping_override | `MappingReviewQueue` | `ReviewItemNotFound`, `InvalidResolution` |
| `finalize_ingestion` | ingestion_id | `SourceIngestion` with status=complete | `UnresolvedReviewItems`, `IngestionAlreadyFinalized` |
| `register_source_system` | tenant_id, system_name, vendor_name, adapter_type | `SourceSystem` | `DuplicateSystem` |

### Mapping status lifecycle

`unmapped` → `auto_mapped` → `mapped`  
`unmapped` → `review_needed` → `mapped` | `rejected`

### Review types

`unmapped_column`, `low_confidence`, `ambiguous_entity`, `duplicate_suspect`

---

## 4. Entity Resolution Service

**Phase:** 1  
**Directory:** `src/services/entity_resolution/`  
**Reads:** PostgreSQL  
**Writes:** PostgreSQL

### Responsibility

Resolves identity matches across sources: unit aliases/renumbering, resident duplicates, agent name variants, vendor name variants.

### Models (from `src/shared/models/asset.py`)

- `UnitAlias` — cross-system unit identity mapping
- `Unit` — canonical unit entity

### Interface

| Operation | Input | Output | Error Conditions |
|-----------|-------|--------|-----------------|
| `resolve_unit_aliases` | property_id, source_records | list of `UnitAlias` with confidence | `PropertyNotFound` |
| `get_aliases_for_unit` | unit_id | list of `UnitAlias` | `UnitNotFound` |
| `override_match` | alias_id, confirmed_unit_id, reviewer_id | `UnitAlias` with `reviewer_override=True` | `AliasNotFound`, `UnitNotFound` |
| `find_duplicates` | entity_type, property_id | list of candidate duplicate pairs with scores | `UnsupportedEntityType` |
| `merge_entities` | entity_type, keep_id, merge_id | merged entity | `MergeConflict`, `EntityNotFound` |

### Resolution strategy

1. Deterministic matching (exact natural key match)
2. Scored fuzzy matching (Levenshtein, phonetic, domain rules)
3. Below-threshold matches → `mapping_review_queue`
4. All matches store `match_method`, `match_confidence`, `reviewer_override`

---

## 5. Temporal State Builder

**Phase:** 2  
**Directory:** `src/services/temporal_state/`  
**Reads:** PostgreSQL (Canonical OLTP)  
**Writes:** PostgreSQL (Canonical OLTP), ClickHouse (Analytical Warehouse)

### Responsibility

Materializes the dense temporal spine: `fact_unit_day`, vacancy cycles, make-ready cycles, and all interval-based facts.

### Models

- From `src/shared/models/asset.py`: `Unit`, `UnitVersion`, `UnitExistenceInterval`
- From `src/shared/models/lease.py`: `Lease`, `LeaseInterval`
- From `src/shared/models/operations.py`: `VacancyCycle`, `MakeReadyCycle`
- From `src/shared/models/clickhouse_facts.py`: `FactUnitDay`, `FactLeaseInterval`, `FactVacancyCycle`

### Interface

| Operation | Input | Output | Error Conditions |
|-----------|-------|--------|-----------------|
| `build_unit_day_spine` | property_id, date_range | row count of materialized `fact_unit_day` | `PropertyNotFound`, `NoExistenceIntervals` |
| `rebuild_vacancy_cycles` | property_id | list of `VacancyCycle` | `PropertyNotFound` |
| `rebuild_make_ready_cycles` | property_id | list of `MakeReadyCycle` | `PropertyNotFound` |
| `get_unit_day` | unit_id, day_date | `FactUnitDay` | `UnitNotFound`, `DateOutOfRange` |
| `refresh_after_ingestion` | assessment_id, changed_unit_ids | refresh summary | `AssessmentNotFound` |

### `fact_unit_day` construction (spec_1 §3.3, lines 359-368)

For each unit with an existence interval:
1. Generate one row per day
2. Join effective intervals from leases, notices, make-ready, listings, field audits
3. Carry forward last-known state only where logically valid
4. Mark unknowns explicitly when evidence is missing
5. Store source coverage flags

---

## 6. Metric Engine

**Phase:** 3  
**Directory:** `src/services/metric_engine/`  
**Reads:** ClickHouse (Analytical Warehouse)  
**Writes:** ClickHouse

### Responsibility

Computes KPIs from fact tables (124 metrics in the Basic Analytic Data Set). Atomic measures that feed the Scoring Engine.

### Models

- From `src/shared/models/scoring_config.py`: `MetricRegistry`
- From `src/shared/models/clickhouse_facts.py`: all fact tables

### Interface

| Operation | Input | Output | Error Conditions |
|-----------|-------|--------|-----------------|
| `compute_metrics` | assessment_id, domain_filter (optional) | dict of metric_name → value + metadata | `AssessmentNotFound`, `InsufficientData` |
| `get_metric_value` | assessment_id, metric_name, scope | metric value + confidence + coverage | `MetricNotRegistered`, `ScopeNotAvailable` |
| `register_metric` | metric definition | `MetricRegistry` | `DuplicateMetric` |
| `list_metrics` | domain filter | list of `MetricRegistry` | None |
| `validate_inputs` | assessment_id, package_name | input coverage report | `PackageNotFound` |

### Metric components

Every metric returns:
- `metric_value` — the computed number
- `confidence_score` — how trustworthy the result is
- `coverage_score` — evidence completeness
- `evidence_count` — supporting data points
- `benchmark_basis` — what the metric is compared against

---

## 7. Scoring Engine

**Phase:** 3  
**Directory:** `src/services/scoring_engine/`  
**Reads:** ClickHouse, PostgreSQL (Metadata & Rule Registry)  
**Writes:** PostgreSQL, ClickHouse

### Responsibility

Applies scoring rubric to metric values, produces `score_result` rows. Implements the 12-area, 65-item, 315-sub-item scoring structure.

### Models

- From `src/shared/models/assessment.py`: `ScoreResult`, `Scorecard`
- From `src/shared/models/scoring_config.py`: `ScoringRubricVersion`, `BenchmarkVersion`

### Interface

| Operation | Input | Output | Error Conditions |
|-----------|-------|--------|-----------------|
| `score_assessment` | assessment_id, rubric_version_id | `Scorecard` with all `ScoreResult` rows | `AssessmentNotFound`, `RubricNotFound`, `MetricsNotComputed` |
| `score_domain` | assessment_id, area_number, rubric_version_id | list of `ScoreResult` for one area | `AreaNotFound` |
| `get_scorecard` | assessment_id | `Scorecard` summary | `ScorecardNotFound` |
| `compare_scorecards` | assessment_ids | comparative scorecard | `MismatchedRubricVersions` |

### Score architecture (spec_1 §6.1)

Every `ScoreResult` stores:
- `metric_value`, `normalized_score` (0–100)
- `weight`, `weighted_score`
- `benchmark_type`, `benchmark_reference`
- `confidence_score`, `coverage_score`
- `grade_letter` (A through F, metadata-driven bands)

### Score hierarchy

```
Atomic metric → indicator score → domain score → assessment summary
```

### Three separate views (spec_1 §6.4)

| View | What it measures |
|------|-----------------|
| Performance score | How good/bad the operation is |
| Confidence score | How trustworthy the conclusion is |
| Scope flag | Whether this domain was eligible |

---

## 8. Finding Compiler

**Phase:** 3  
**Directory:** `src/services/finding_compiler/`  
**Reads:** ClickHouse, PostgreSQL (Metadata & Rule Registry)  
**Writes:** PostgreSQL

### Responsibility

Generates findings from diagnostic rule packages, detects contradictions, produces the finding graph that connects units, agents, listings, and impacts.

### Models

- From `src/shared/models/assessment.py`: `Finding`, `Contradiction`
- From `src/shared/models/scoring_config.py`: `DiagnosticPackage`

### Interface

| Operation | Input | Output | Error Conditions |
|-----------|-------|--------|-----------------|
| `compile_findings` | assessment_id, package_ids (optional) | list of `Finding` | `AssessmentNotFound`, `PackageNotFound` |
| `detect_contradictions` | assessment_id | list of `Contradiction` | `AssessmentNotFound` |
| `get_finding_graph` | assessment_id | finding graph (nodes + edges + evidence links) | `NoFindings` |
| `get_findings_by_domain` | assessment_id, area_number | list of `Finding` for one domain | `AssessmentNotFound` |

### Diagnostic package statuses (spec_1 §5.5)

Every package returns one of: `PASS`, `WATCH`, `FAIL`, `OUT_OF_SCOPE`

Plus: `coverage_pct`, `confidence_score`, `evidence_count`, `benchmark_basis`, `financial_impact_status`

### Contradiction record (spec_1 §8)

Each contradiction includes:
- source A and source B
- matching rule
- contradiction type and severity
- evidence links
- affected domains
- trust penalty multiplier

---

## 9. Impact Engine

**Phase:** 3  
**Directory:** `src/services/impact_engine/`  
**Reads:** ClickHouse, PostgreSQL (Metadata & Rule Registry)  
**Writes:** PostgreSQL

### Responsibility

Quantifies financial impact of findings. Produces low/base/high dollar estimates with formula traces and assumption audit trails.

### Models

- From `src/shared/models/assessment.py`: `ImpactEstimate`
- From `src/shared/models/scoring_config.py`: `ImpactModelCatalog`

### Interface

| Operation | Input | Output | Error Conditions |
|-----------|-------|--------|-----------------|
| `estimate_impacts` | assessment_id, finding_ids (optional) | list of `ImpactEstimate` | `AssessmentNotFound`, `FindingNotFound` |
| `get_impact_summary` | assessment_id | aggregated impact by domain | `NoImpactEstimates` |
| `simulate_optimal_budget` | assessment_id, constraints | budget allocation with projected ROI | `InsufficientFindings` |

### Impact model catalog (spec_1 §7.1)

Reusable models: `vacancy_loss`, `avoidable_turn_delay`, `below_market_rent_loss`, `concession_leakage`, `retention_failure_cost`, `collections_loss_risk`, `maintenance_overspend`, `vendor_rework_cost`, `marketing_waste`, `pricing_misposition_cost`

### Output format (spec_1 §7.4)

Every `ImpactEstimate` returns:
- Low / base / high dollars
- Annualized equivalent
- Per-unit or per-incident breakdown
- Formula trace + assumption trace
- Confidence

### Double-counting prevention (spec_1 §7.3)

Related impacts grouped under `impact_family_id` with `primary_driver_share` and `contributing_driver_share`. Portfolio/assessment totals sum only net attributable amounts.

---

## 10. Study & Snapshot Service

**Phase:** 4  
**Directory:** `src/services/study_snapshot/`  
**Reads:** ClickHouse, S3 (Raw Evidence)  
**Writes:** PostgreSQL

### Responsibility

Manages the investigative workspace: saved queries, frozen snapshots, studies, comparison boards, annotations, and evidence bundles.

### Models (from `src/shared/models/workspace.py`)

- `Study` — named investigation container
- `StudyItem` — link between study and artifacts
- `SavedQuery` — reusable query with parameters
- `ResultSnapshot` — frozen output with data hash and rule versions
- `ComparisonBoard` — side-by-side layout
- `Annotation` — consultant notes
- `EvidenceBundle` — curated export set

### Interface

| Operation | Input | Output | Error Conditions |
|-----------|-------|--------|-----------------|
| `create_study` | assessment_id, name, description | `Study` | `AssessmentNotFound` |
| `save_query` | query definition, parameters, chart_spec | `SavedQuery` | `InvalidQuery` |
| `take_snapshot` | saved_query_id | `ResultSnapshot` (frozen with versions) | `QueryNotFound`, `ExecutionError` |
| `add_to_study` | study_id, item_type, item_id | `StudyItem` | `StudyNotFound`, `ItemNotFound` |
| `create_comparison` | study_id, snapshot_ids | `ComparisonBoard` | `SnapshotCountMismatch` |
| `annotate` | target_type, target_id, text | `Annotation` | `TargetNotFound` |
| `create_evidence_bundle` | study_id, item_ids | `EvidenceBundle` | `StudyNotFound` |
| `export_bundle` | bundle_id, format | file bytes | `BundleNotFound`, `UnsupportedFormat` |

### Snapshot semantics (spec_1 §9.2)

A snapshot preserves: source data version, transformation version, rule version, benchmark version, result payload, chart spec, query definition, filters, creation timestamp, creator. Allows the consultant to return weeks later and see the exact same result.

---

## 11. Report Rendering Service

**Phase:** 4  
**Directory:** `src/services/report_rendering/`  
**Reads:** PostgreSQL, ClickHouse  
**Writes:** PostgreSQL, S3

### Responsibility

Generates reports from system objects (scorecards, findings, snapshots, evidence). Template-based composition with brand themes, rendered to PDF/HTML.

### Models (from `src/shared/models/assessment.py`)

- `Report` — report metadata
- `ReportSection` — individual sections with data bindings
- `ReportRender` — rendered artifact (PDF, HTML)

### Interface

| Operation | Input | Output | Error Conditions |
|-----------|-------|--------|-----------------|
| `create_report` | assessment_id, template_id | `Report` | `AssessmentNotFound`, `TemplateNotFound` |
| `add_section` | report_id, section_type, data_binding | `ReportSection` | `ReportNotFound`, `InvalidBinding` |
| `render_report` | report_id, output_format | `ReportRender` with storage_path | `ReportIncomplete`, `RenderError` |
| `get_report` | report_id | `Report` with sections | `ReportNotFound` |
| `list_templates` | assessment_type | list of available templates | None |

### Standard templates (spec_1 §12.2)

- Full assessment report
- Executive summary
- Vacancy / turnover deep dive
- Leasing effectiveness deep dive
- Competitive market analysis
- Progress tracking report
- Door opener report

### Rendering pipeline (spec_1 §12.4)

1. Query bound data and images
2. Render structured markdown/HTML sections
3. Apply brand theme and layout
4. Render to PDF and presentation-ready outputs
5. Store rendered artifact and section manifest

---

## Cross-Cutting Error Categories

All services share these error patterns:

| Category | Examples | Handling |
|----------|---------|---------|
| **Not Found** | `AssessmentNotFound`, `UnitNotFound`, `PropertyNotFound` | Return 404 at API layer |
| **Permission** | `PermissionDenied`, `TenantMismatch` | Return 403 at API layer |
| **Validation** | `SchemaValidationError`, `InvalidQuery`, `InvalidResolution` | Return 400 with detail |
| **State** | `InvalidStatusTransition`, `UnresolvedReviewItems` | Return 409 (conflict) |
| **Upstream** | `MetricsNotComputed`, `NoFindings`, `InsufficientData` | Return 422 with prerequisite guidance |
| **Infrastructure** | `StorageError`, `RenderError`, `ExecutionError` | Return 500, log, alert |

### Audit logging

All write operations create an `AuditLog` entry (from `src/shared/models/infrastructure.py`) with: user_id, action, entity_type, entity_id, before/after payload, timestamp.

---

## 12. Client Portal Service

**Phase:** 5  
**Directory:** `src/services/client_portal/`  
**Reads:** PostgreSQL (approved outputs, assessments, reports), ClickHouse (trend facts)  
**Writes:** PostgreSQL (client preferences, portal audit log)

### Responsibility

Serves the curated, approved-only client view. Clients see approved results, recommendations, score trends, and selected reports without exposing consultant-only tools, working notes, draft hypotheses, or unrestricted underlying PII (spec_1 §11.2, line 1064).

### Models

- From `src/shared/models/assessment.py`: `Assessment`, `Scorecard`, `ScoreResult`, `Finding`, `ImpactEstimate`, `Recommendation`, `Report`, `ReportRender`
- From `src/shared/models/clickhouse_facts.py`: `FactAssessmentScore`, `FactAssessmentFinding`, `FactRecommendationStatus`

### Interface

| Operation | Input | Output | Error Conditions |
|-----------|-------|--------|-----------------|
| `get_executive_overview` | client_id, property_id | overall scores, trends, top findings, financial opportunity | `PropertyNotFound`, `NoApprovedAssessments` |
| `get_domain_scorecard` | assessment_id, area_number | domain-level scorecard with item scores | `AssessmentNotFound`, `AreaNotFound`, `NotApproved` |
| `get_finding_detail` | finding_id | evidence-backed finding with recommendations | `FindingNotFound`, `NotApproved` |
| `get_progress_tracking` | property_id | cross-assessment score and recommendation tracking | `PropertyNotFound`, `InsufficientAssessments` |
| `get_report_library` | client_id, property_id | list of delivered reports and exports | `PropertyNotFound` |
| `get_limited_explore` | client_id, property_id, filter_spec | pre-approved filters and comparisons only | `PropertyNotFound`, `FilterNotAllowed` |
| `get_score_trends` | property_id, area_number (optional) | score trajectories across assessments | `PropertyNotFound`, `InsufficientAssessments` |

### Client portal modules (spec_1 §11.2, lines 1055-1061)

1. Executive overview — overall scores, trends, top findings, financial opportunity
2. Domain scorecards — leasing, vacancy, pricing, retention, etc.
3. Finding detail — evidence-backed issues and recommendations
4. Progress tracking — across assessments, by domain and recommendation
5. Report library — delivered reports and exports
6. Limited explore — pre-approved filters and comparisons only

### Access control

Every operation enforces:
- Client can only see their own properties
- Only approved/published outputs are returned — draft, in_progress, or consultant-only data is excluded
- PII masking applied per tenant policy

---

## 13. Trend & Trajectory Service

**Phase:** 5  
**Directory:** `src/services/trend_trajectory/`  
**Reads:** PostgreSQL (assessments, scores, findings, recommendations), ClickHouse (all fact tables)  
**Writes:** ClickHouse (trend marts), PostgreSQL (recommendation status updates)

### Responsibility

Builds longitudinal tracking infrastructure: trend marts, recurring finding detection, recommendation adoption tracking, and property trajectory analysis across multiple assessments.

### Models

- From `src/shared/models/clickhouse_facts.py`: `FactAssessmentScore`, `FactAssessmentFinding`, `FactRecommendationStatus`, `FactPropertyKpiPeriod`, `FactUnitChronicity`
- From `src/shared/models/assessment.py`: `Recommendation`

### Interface

| Operation | Input | Output | Error Conditions |
|-----------|-------|--------|-----------------|
| `build_trend_marts` | property_id, assessment_id | materialization summary (rows per trend table) | `AssessmentNotFound`, `PropertyNotFound` |
| `get_score_trajectory` | property_id, area_number (optional) | score values across assessments with dates | `PropertyNotFound`, `InsufficientAssessments` |
| `detect_recurring_findings` | property_id | list of findings that persist across assessments with recurrence count | `PropertyNotFound` |
| `get_recommendation_status` | property_id, assessment_id (optional) | recommendation adoption tracking by domain | `PropertyNotFound` |
| `update_recommendation_status` | recommendation_id, new_status, verification_evidence | updated `Recommendation` | `RecommendationNotFound`, `InvalidStatusTransition` |
| `compare_assessments` | assessment_id_a, assessment_id_b | side-by-side score, finding, and recommendation comparison | `AssessmentNotFound`, `DifferentProperties` |
| `get_property_trajectory` | property_id | dashboard data: KPI trends, score trends, chronic issues, recommendation progress | `PropertyNotFound` |
| `detect_chronic_units` | property_id | list of `FactUnitChronicity` records (chronic vacancy, recurring issues, repeat turnover) | `PropertyNotFound` |

### Trend-ready ClickHouse tables (spec_1 §14.2, lines 1177-1182; DDL lines 2731-2813)

- `fact_assessment_score` (line 2731) — score trajectories per area per assessment
- `fact_assessment_finding` (line 2750) — finding persistence, recurrence detection
- `fact_recommendation_status` (line 2769) — recommendation adoption tracking
- `fact_property_kpi_period` (line 2787) — period-level KPIs for trend analysis
- `fact_unit_chronicity` (line 2804) — chronic vacancy, recurring issue, repeat turnover per unit

### Recommendation structure (spec_1 §14.3, lines 1192-1201; DDL line 2111)

Each recommendation is a structured object with: domain, target_entity_type, target_entity_id, priority (critical/high/medium/low), title, description, expected_impact, owner, due_date, status (open/in_progress/completed/deferred/rejected), verification_evidence.

---

## 14. Door Opener Service

**Phase:** 6  
**Directory:** `src/services/door_opener/`  
**Reads:** PostgreSQL (assessments, canonical entities), ClickHouse (fact tables), S3 (raw evidence)  
**Writes:** PostgreSQL (door opener assessment records, scores, findings)

### Responsibility

Implements the `DOOR_OPENER` assessment type: a public-data-only assessment that scores the 11 applicable items identified in `Door_Opener_Applicability_Matrix.md`, runs public-data diagnostic packages, and produces a door opener report.

### Models

- From `src/shared/models/assessment.py`: `Assessment` (with `assessment_type = 'door_opener'`), `Scorecard` (with `scorecard_type = 'door_opener'`), `ScoreResult`, `Finding`, `Report` (with `report_type = 'door_opener'`)

### Interface

| Operation | Input | Output | Error Conditions |
|-----------|-------|--------|-----------------|
| `create_door_opener_assessment` | property_id, date_range | `Assessment` with type `door_opener` | `PropertyNotFound` |
| `get_applicable_items` | assessment_id | list of 11 scorable items from applicability matrix | `AssessmentNotFound`, `NotDoorOpener` |
| `score_door_opener` | assessment_id, rubric_version_id | `Scorecard` with scores for applicable items only | `AssessmentNotFound`, `NotDoorOpener`, `InsufficientPublicData` |
| `run_public_data_packages` | assessment_id | list of findings from public-data diagnostic packages | `AssessmentNotFound`, `NotDoorOpener` |
| `generate_door_opener_report` | assessment_id, template_id | `Report` with door opener sections | `AssessmentNotFound`, `NotDoorOpener` |
| `upgrade_to_full_engagement` | assessment_id | `Assessment` with type changed to `full_engagement`, preserving all door opener data | `AssessmentNotFound`, `NotDoorOpener`, `AlreadyUpgraded` |

### Applicability matrix (from `Door_Opener_Applicability_Matrix.md`)

11 of 65 items scorable from public data across 3 areas:
- Area 2 (Marketing): Online Reputation, Digital/Social Presence, Website Quality
- Area 4 (Listings): Content Quality, Listing Accuracy
- Area 11 (Competitive Position): Pricing vs Comps, Amenity Count vs Comps, Reputation Score vs Comps, Resident Services vs Comps, Resident Events vs Comps, Resident Mobile App vs Comps

### Public data collection workflow

Door opener data comes from:
- ILS listings (Apartments.com, Zillow, etc.)
- Review platforms (Google, Yelp, ApartmentRatings, Facebook)
- Property website
- Social media profiles
- Google Business Profile
- App stores (resident mobile app)
- Comp property public data (same sources for comp set)

Per Audit Workbook §2 [DOOR OPENER] and §10A-10K [DOOR OPENER].

### Assessment type DDL support

- `assessment.assessment_type` supports `'door_opener'` (DDL line 1921)
- `scorecard.scorecard_type` supports `'door_opener'` (DDL line 1982)
- `report.report_type` supports `'door_opener'` (DDL line 2278)

---

## 15. Extension SDK

**Phase:** 6  
**Directory:** `src/shared/sdk/`  
**Reads:** PostgreSQL (registries), ClickHouse (semantic catalog)  
**Writes:** PostgreSQL (registry entries)

### Responsibility

Provides the framework for adding new data source connectors, diagnostic packages, scoring patterns, and entity domains without restructuring the core system (spec_1 §15, lines 1204-1223).

### Interface

| Operation | Input | Output | Error Conditions |
|-----------|-------|--------|-----------------|
| `register_connector` | connector definition (source system type, supported report types, column mappings, adapter class) | `SourceSystem` registry entry | `DuplicateConnector`, `InvalidAdapterProtocol` |
| `validate_connector` | connector_id | validation report (required methods, column coverage, test file results) | `ConnectorNotFound` |
| `register_diagnostic_package` | package definition (metric definitions, benchmark definitions, rule thresholds, impact formulas, output templates) | `DiagnosticPackage` registry entry | `DuplicatePackage`, `MissingMetrics` |
| `validate_package` | package_id | validation report (metric coverage, threshold completeness, formula validity) | `PackageNotFound` |
| `register_rubric_version` | rubric definition (area weights, item weights, sub-item budgets, thresholds) | `ScoringRubricVersion` | `InvalidWeights`, `WeightSumMismatch` |
| `register_fact_grain` | fact table definition (columns, ordering key, source entities) | ClickHouse DDL + migration file | `DuplicateGrain` |

### Connector SDK (spec_1 §15.1)

A new connector must:
1. Implement the `VendorAdapter` protocol from `Data_Onramp_Specification.md`
2. Declare supported report types and column mappings
3. Register source-specific attributes in the `SourceSystem` registry
4. Pass validation against sample test files

### Package SDK (spec_1 §15.2)

A new diagnostic package must provide:
- Metric definitions
- Benchmark definitions
- Rule thresholds
- Impact formulas
- Output templates

No schema rewrite required unless the new analysis introduces a truly new fact grain (spec_1 §15.2, line 1217).

### Rubric versioning (spec_1 §15.3)

Rubrics are metadata-driven. A new rubric version can be deployed independently of core entity tables. Weight sums are validated at registration time (area weights sum to 100%, item weights sum to 100% per area, sub-item points sum to 100 per checklist item).

---

## Phase Summary

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

## Authoritative References

- `spec_1` §3 (architecture), §5.4 (pipeline), §6 (scoring), §7 (impact), §8 (contradictions), §9 (workspace), §10 (intake), §11.2 (client portal), §12 (reporting), §14 (longitudinal tracking), §15 (extensibility), §16 (security)
- `Database_Schema_Specification.md` — table structures read/written by each service
- `Shared_Type_Definitions.md` — Pydantic model reference for all data shapes
- `Data_Onramp_Specification.md` — detailed import pipeline for Import & Mapping Service
- `scoring_config.json` — rubric structure for Scoring Engine
- `Door_Opener_Applicability_Matrix.md` — 65-item applicability matrix for Door Opener service
- `Audit_Workbook_Specification.md` — Door Opener workflow and data collection sections
