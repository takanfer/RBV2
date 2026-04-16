# Report Template Specification

Defines the report composition model, rendering pipeline, section types, data binding interface, and the initial set of standard templates. Template content (section ordering, specific data bindings, narrative templates, chart specs) will be defined during Phase 4 implementation.

**Sources:**
- `spec_1` §12 (lines 1066-1114) — report model, standard deliverables, custom reports, rendering pipeline
- `Service_Interface_Contracts.md` §11 — Report Rendering Service interface and standard template list
- `Database_Schema_Specification.md` — `report` (line 2274), `report_section` (line 2292), `report_render` (line 2312)

---

## Report Composition Model

Source: spec_1 §12.1, lines 1070-1084

A report is composed of:
- **Template** — defines the structure, section ordering, and default data bindings
- **Section definitions** — individual content blocks within the report
- **Data bindings** — connections from sections to system data (scorecards, findings, metrics, snapshots)
- **Narratives** — text content, either template-generated or manually written by the consultant
- **Charts / tables** — visual representations bound to data
- **Appended evidence** — supporting documents, screenshots, raw data excerpts

Each section can be sourced from:
- Scorecards
- Findings
- Saved queries
- Snapshots
- Manual commentary
- Recommendation sets

---

## Section Types

Source: `report_section.section_type` (DDL line 2295)

| Section Type | Description |
|-------------|-------------|
| `scorecard` | Area or overall scorecard with scores, grades, and weights |
| `finding` | Evidence-backed finding with severity, domain, and evidence links |
| `saved_query` | Results from a saved analytical query |
| `snapshot` | Frozen result snapshot with version provenance |
| `commentary` | Manual consultant-written narrative |
| `recommendation` | Structured recommendation with priority, owner, status, expected impact |

### Section data structure (DDL lines 2292-2304)

Each `report_section` stores:
- `section_type` — one of the types above
- `sort_order` — position within the report
- `title` — section heading
- `content` — JSONB payload (structure varies by section type)
- `data_bindings` — JSONB specifying which system data to query
- `narrative` — optional text narrative
- `chart_spec` — optional JSONB chart/visualization specification

---

## Render Formats

Source: `report_render.format` (DDL line 2315)

| Format | Use Case |
|--------|----------|
| `pdf` | Primary client deliverable |
| `html` | Web-viewable version, client portal |
| `pptx` | Presentation-ready format |

---

## Rendering Pipeline

Source: spec_1 §12.4, lines 1109-1114

1. Query bound data and images from PostgreSQL/ClickHouse/S3
2. Render structured markdown/HTML sections
3. Apply brand theme and layout
4. Render to PDF and presentation-ready outputs
5. Store rendered artifact and section manifest in S3

The `report_render` record stores: `format`, `storage_path` (S3 location), `section_manifest` (JSONB listing all sections included), `rendered_at`, `rendered_by`.

---

## Report Types

Source: `report.report_type` (DDL line 2278)

| Report Type | Assessment Type | Source |
|-------------|----------------|--------|
| `full_assessment` | Full Engagement | spec_1 §12.2 |
| `executive_summary` | Full Engagement | spec_1 §12.2 |
| `vacancy_deep_dive` | Full Engagement | spec_1 §12.2 |
| `leasing_deep_dive` | Full Engagement | spec_1 §12.2 |
| `competitive_analysis` | Both | spec_1 §12.2 |
| `progress_tracking` | Full Engagement | spec_1 §12.2 |
| `door_opener` | Door Opener | spec_1 §12.2 |
| `custom` | Either | spec_1 §12.3 |

This list is extensible. Additional report types can be added by registering a new template and adding the type to the `report.report_type` enum.

---

## Standard Templates

Source: spec_1 §12.2, lines 1088-1095; Service_Interface_Contracts.md lines 472-478

The following 7 templates are the MVP deliverables. Section content, ordering, data bindings, narrative templates, and chart specifications for each will be defined during Phase 4 implementation.

### 1. Full Assessment Report

Complete property assessment covering all 12 scoring areas, findings, recommendations, and financial impact analysis. Primary client deliverable for a Full Engagement assessment.

### 2. Executive Summary

Condensed overview: overall score, top findings, key recommendations, total financial opportunity. Designed for ownership/executive audience.

### 3. Vacancy / Turnover Deep Dive

Focused analysis on Area 1 (Vacancy/Occupancy) and Area 9 (Maintenance & Turnovers): vacancy cycles, make-ready performance, turnover costs, chronic vacancy units.

### 4. Leasing Effectiveness Deep Dive

Focused analysis on Area 3 (Leasing Performance): conversion funnel, mystery shop results, lead management, tour quality, training assessment.

### 5. Competitive Market Analysis

Focused analysis on Area 11 (Competitive Position) and pricing comparisons: comp set profiling, pricing position, amenity comparison, reputation benchmarking.

### 6. Progress Tracking Report

Cross-assessment comparison: score changes by area, recommendation adoption status, recurring vs resolved findings, before/after impact analysis. Requires at least two assessments for the same property.

### 7. Door Opener Report

Public-data-only assessment report covering the 11 scorable items from `Door_Opener_Applicability_Matrix.md` across Areas 2, 4, and 11. Designed as a sales/initial diagnostic tool.

---

## Custom Report Creation

Source: spec_1 §12.3, lines 1097-1105

The consultant can create ad hoc report sections by selecting:
- A result set or snapshot
- A visual spec
- A narrative template
- Optional custom written commentary

Custom reports use `report_type = 'custom'` and are composed from any combination of section types. This allows reports beyond the standard templates without requiring new template definitions.

---

## Extensibility

New templates can be added at any time by:
1. Defining a new `report_type` value
2. Creating a template definition (section ordering, default data bindings, default narrative templates)
3. Registering it via the Report Rendering Service's `list_templates` operation

No schema changes required. The `report`, `report_section`, and `report_render` tables support arbitrary templates through their JSONB `content`, `data_bindings`, `chart_spec`, and `section_manifest` fields.
