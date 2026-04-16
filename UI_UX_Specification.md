# UI/UX Specification

Defines the structural framework for the platform's user interfaces: module inventory, user roles, data dependencies per view, user flows, and access boundaries. Visual design, component specifications, wireframes, interaction patterns, and responsive breakpoints will be defined during Phase 4 implementation.

**Sources:**
- `spec_1` §11.1 (consultant workspace modules, lines 1038-1051), §11.2 (client portal modules, lines 1054-1064), §16.1 (security/access, lines 1227-1233)
- `Service_Interface_Contracts.md` — all 15 service interfaces define what operations each module calls
- `Database_Schema_Specification.md` — DDL for `user_account` (role enum, line 192), workspace objects (lines 2139-2267), report objects (lines 2269-2322)

---

## User Roles

Source: `user_account.role` (DDL line 192)

| Role | Access Scope | Portal |
|------|-------------|--------|
| `admin` | Full platform administration, tenant management | Consultant workspace |
| `consultant` | Full workspace access within tenant/client scope | Consultant workspace |
| `analyst` | Workspace access, may be scoped to specific assessments | Consultant workspace |
| `client_viewer` | Read-only access to approved outputs only | Client portal |

Access enforcement: every service call passes through AuthZ (Service §1) which validates tenant, client, property, and assessment scope.

---

## Portal Architecture

The platform has two distinct portals with different audiences, data access, and module sets.

### Consultant Workspace (Phases 0-4)

Target users: `admin`, `consultant`, `analyst`

### Client Portal (Phase 5)

Target users: `client_viewer`

**Design constraint** (spec_1 §11.2, line 1063-1064): Clients must never see consultant-only working notes, draft hypotheses, or unrestricted underlying PII. The client portal is a curated window on approved outputs.

---

## Consultant Workspace Modules

Source: spec_1 §11.1, lines 1040-1048

### Module 1: Engagement Cockpit

**Purpose:** Property overview, assessment lifecycle, source coverage, run status.

**Service dependencies:**
- Engagement Service (§2) — assessment CRUD, status transitions
- Import & Mapping Service (§3) — source coverage status
- AuthZ (§1) — scoping

**Data objects:**
- `assessment` (status, scope window, site visit date)
- `assessment_data_coverage` (domain coverage percentages)
- `analysis_run` (run status, timestamps)
- `property`, `portfolio`, `client`

**User flows (to be designed):**
- Create/open assessment
- View assessment status and progress
- Monitor data coverage gaps
- Trigger analysis runs

---

### Module 2: Import Center

**Purpose:** Upload, map, validate, and monitor data ingestion.

**Service dependencies:**
- Import & Mapping Service (§3) — file upload, mapping, validation
- Entity Resolution Service (§4) — resolution queue
- Engagement Service (§2) — coverage update

**Data objects:**
- `raw_import_batch` (file metadata, status)
- `import_row` (per-row validation)
- `mapping_config` (source-to-canonical mapping)
- `import_validation_result` (errors, warnings)

**User flows (to be designed):**
- Upload file and select source type
- Map columns to canonical fields
- Review validation results
- Resolve entity matches
- Monitor ingestion progress

---

### Module 3: Field Capture

**Purpose:** Unit walks, mystery shops, common-area observations, competitor captures.

**Service dependencies:**
- Import & Mapping Service (§3) — structured capture ingestion
- Entity Resolution Service (§4) — unit/property matching

**Data objects:**
- `unit_condition_observation` (field condition per unit)
- `field_validation` (PM claim vs field reality)
- `mystery_shop` (leasing interaction assessment)
- `vacant_unit_audit` (vacant unit inspection)
- `resident_interview` (resident feedback)
- `back_of_house_observation`, `capital_asset_observation`, `fire_safety_observation` (planned additions per DDL §10)

**User flows (to be designed):**
- Select property/unit for observation
- Fill structured capture form (per Audit Workbook §5-§6 templates)
- Attach photos
- Submit and validate
- Mobile-responsive layout required (Audit Workbook line 189)

---

### Module 4: Diagnostic Hub

**Purpose:** Scorecards, findings, contradictions, impact summaries.

**Service dependencies:**
- Scoring Engine (§7) — scorecard results
- Finding Compiler (§8) — findings by domain/severity
- Impact Engine (§9) — financial impact estimates
- Contradiction detection (within Finding Compiler)

**Data objects:**
- `scorecard`, `score_result` (area/item/sub-item scores)
- `finding` (evidence-backed diagnostic findings)
- `contradiction` (cross-source conflicts)
- `impact_estimate` (financial impact per finding)
- `recommendation` (structured recommendations)

**User flows (to be designed):**
- View overall scorecard with drill-down to area → item → sub-item
- Browse findings by domain, severity, or scoring area
- View contradiction detail with source evidence
- View impact summaries with assumption traces
- Navigate from finding → evidence → source data

---

### Module 5: Analysis Lab

**Purpose:** Guided pivots, SQL, drilldowns, compare views.

**Service dependencies:**
- Study & Snapshot Service (§10) — saved queries, snapshots
- Metric Engine (§6) — computed metrics and KPIs

**Data objects:**
- `saved_query` (reusable query definitions)
- `result_snapshot` (frozen query results)
- ClickHouse materialized views (analytical layer)

**Design constraint** (spec_1 §11.1, lines 1050-1051): The UI should expose depth without forcing power users into raw SQL for routine work. Guided exploration covers common investigations; SQL remains available for edge cases.

**User flows (to be designed):**
- Select a guided analysis (pre-built pivot)
- Build a custom query with filters
- Execute and view results
- Save query for reuse
- Freeze result as snapshot

---

### Module 6: Studies

**Purpose:** Saved investigations, boards, annotations, exports.

**Service dependencies:**
- Study & Snapshot Service (§10) — all study operations

**Data objects:**
- `study` (named investigation container)
- `study_item` (links to snapshots, findings, annotations, comparisons)
- `comparison_board` (side-by-side layout)
- `annotation` (consultant notes on evidence)
- `evidence_bundle` (curated export set)

**User flows (to be designed):**
- Create/open a study
- Add snapshots, findings, comparisons to study
- Open comparison board with side-by-side results
- Annotate evidence cells
- Build evidence bundle for export

**Study workflow** (spec_1 §9.3, lines 949-956):
1. Run an analysis
2. Freeze it as a snapshot
3. Add related snapshots to a study
4. Open a comparison board inside the study
5. Annotate the evidence
6. Promote selected artifacts into a report section

---

### Module 7: Report Composer

**Purpose:** Template selection, section editing, evidence insertion.

**Service dependencies:**
- Report Rendering Service (§11) — report CRUD, section management, rendering

**Data objects:**
- `report` (report metadata, type, status)
- `report_section` (sections with data bindings)
- `report_render` (rendered artifacts: PDF, HTML, PPTX)

**User flows (to be designed):**
- Select report template
- Add/reorder sections
- Bind sections to data (scorecards, findings, snapshots, evidence)
- Write/edit narrative text
- Configure chart specifications
- Preview and render report
- Export rendered artifact

See `Report_Template_Specification.md` for template details and section types.

---

### Module 8: Assessment Compare

**Purpose:** Longitudinal score, finding, and recommendation tracking.

**Service dependencies:**
- Trend & Trajectory Service (§13) — trend data, recurring findings, recommendation tracking

**Data objects:**
- `fact_assessment_score` (score trajectories)
- `fact_assessment_finding` (finding persistence)
- `fact_recommendation_status` (recommendation adoption)
- `fact_property_kpi_period` (KPI trends)
- `fact_unit_chronicity` (chronic vacancy tracking)

**Prerequisite:** At least two assessments for the same property.

**User flows (to be designed):**
- Select assessments to compare
- View score change by area/item
- View recurring vs resolved findings
- Track recommendation adoption status
- Before/after impact comparison

---

## Client Portal Modules

Source: spec_1 §11.2, lines 1055-1061

### Module 1: Executive Overview

**Purpose:** Overall scores, trends, top findings, financial opportunity.

**Service dependencies:**
- Client Portal Service (§12) — curated approved outputs

**Data access:** Read-only, approved outputs only.

---

### Module 2: Domain Scorecards

**Purpose:** Leasing, vacancy, pricing, retention, etc.

**Data access:** Scorecard and score_result records marked as client-approved.

---

### Module 3: Finding Detail

**Purpose:** Evidence-backed issues and recommendations.

**Data access:** Findings included in approved reports only.

---

### Module 4: Progress Tracking

**Purpose:** Cross-assessment tracking by domain and recommendation.

**Data access:** Trend data for assessments where client has access.

---

### Module 5: Report Library

**Purpose:** Delivered reports and exports.

**Data access:** Rendered reports marked as delivered.

---

### Module 6: Limited Explore

**Purpose:** Pre-approved filters and comparisons only.

**Design constraint:** No raw SQL, no unrestricted pivots. Only pre-configured exploration paths approved by the consultant.

---

## Security Boundaries

Source: spec_1 §16.1, lines 1227-1233

| Boundary | Enforcement |
|----------|-------------|
| Tenant isolation | Every query scoped by `tenant_id` (AuthZ) |
| Client data separation | Client users can only see their property data |
| Consultant vs client content | Client portal excludes: working notes, draft hypotheses, unrestricted PII |
| Role-based permissions | `admin` > `consultant` > `analyst` > `client_viewer` |
| Row-level access | Transactional layer enforced |
| PII handling | Tagged and masked per role |
| Encryption | In transit and at rest |

---

## Extensibility

New modules can be added without restructuring. The service layer (15 services) provides the operational interface; the UI is a presentation layer over those service operations. New modules register their service dependencies and data objects following the same pattern as above.

---

## Open Design Decisions

The following require design decisions during Phase 4 implementation:

1. **Layout framework** — overall workspace navigation structure (sidebar, tabs, etc.)
2. **Component library** — which UI component framework/library to use
3. **Responsive strategy** — breakpoints, mobile-specific layouts (especially for Field Capture)
4. **Visualization library** — chart rendering for diagnostics, comparisons, scorecards
5. **Real-time updates** — whether assessment runs, imports, etc. use polling or WebSocket
6. **Theming / branding** — brand theme system for reports and client portal
7. **Accessibility** — WCAG compliance level
8. **State management** — client-side state architecture (per Next.js patterns)
