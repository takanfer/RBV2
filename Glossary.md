# Glossary

Standardized terminology for the Multifamily Property Assessment Platform. Every definition sourced from existing specification documents; source cited in parentheses.

---

## Scoring Terms

**Area** — One of 12 top-level scoring categories. Each area has a configurable weight (summing to 100% across all areas) and contains multiple items. (Scoring Model Specification, Design Principle 6)

**Item** — A scorable element within an area. Each item uses exactly one input type (Data, Checklist, or Comparative) and produces a 0–10 score. Item weights within an area sum to 100%. (Scoring Model Specification, Design Principle 6)

**Sub-item** — A component within a Checklist item. Sub-items share a 100-point budget per item. Sub-items are either Y/N (binary) or Tiered (multi-level). (Scoring Model Specification, Design Principle 5)

**Area Weight** — The percentage contribution of an area to the overall asset score. All 12 area weights sum to 100%. User-configurable. (Scoring Model Specification, Design Principle 6)

**Item Weight** — The percentage contribution of an item to its area score. Item weights within each area sum to 100%. User-configurable. (Scoring Model Specification, Design Principle 6)

**Sub-item Points** — The point value assigned to a sub-item within a checklist item's 100-point budget. All sub-item points within a checklist item sum to 100. (Scoring Model Specification, Design Principle 5)

**Data (input type)** — Continuous numerical values from PM systems, CRM, or financial reports. Scored by comparing the raw value against calibrated benchmark thresholds using piecewise linear interpolation to produce a 0–10 score. 20 items use this type. (Scoring Model Specification, Input Types)

**Checklist (input type)** — Human-derived evaluations from audit observations or management interviews. Each checklist item's sub-items share a 100-point budget. Total points earned / 100 × 10 = item score (0–10). 38 items use this type. (Scoring Model Specification, Input Types)

**Comparative (input type)** — Metrics or observations evaluated relative to a competitive set. The subject property's value is compared to the comp set average; the difference/ratio is mapped to a 0–10 score via calibrated thresholds. 7 items use this type. (Scoring Model Specification, Input Types)

**Y/N (Binary)** — A checklist sub-item sub-type. Presence = full point value; Absence = 0. (Scoring Model Specification, Input Types)

**Tiered** — A checklist sub-item sub-type. Multi-level categorical rating (e.g., Excellent/Good/Fair/Poor, or value ranges). Each tier maps to a percentage of the sub-item's point value. (Scoring Model Specification, Input Types)

**100-point budget** — The rule that each checklist item's sub-items share exactly 100 points. Points earned / 100 × 10 = the item's 0–10 score. (Scoring Model Specification, Design Principle 5)

**Piecewise linear interpolation** — The scoring function used for Data and Comparative items. Four breakpoints (Excellent, Good, Concern, Poor) define score anchors at 10.0, 7.5, 5.0, and 2.5 respectively. Values between breakpoints are linearly interpolated; values beyond Poor extrapolate toward 0. (Scoring Thresholds Calibration, Scoring Function)

**Overall asset score** — The weighted average of 12 area scores. Range: 0–10. (Scoring Model Specification, Rollup)

**Area score** — The weighted average of item scores within an area. Range: 0–10. (Scoring Model Specification, Rollup)

**Item score** — A single 0–10 score for one scoring item, produced by the item's input type method. (Scoring Model Specification, Rollup)

**Coverage percentage** — The percentage of items within an area that have sufficient data to be scored. Missing items are excluded from the weighted average, not scored as zero. (Scoring Model Specification, Rollup)

**Variance-based scoring** — The method used for Area 8 (Financials). Each line item is scored by comparing actual performance against the owner's stated financial targets/budget. Revenue: higher actual vs budget scores favorably. Expenses: lower actual vs budget scores favorably. (Scoring Model Specification, Financials Scoring)

**Threshold direction** — Indicates whether higher or lower raw values are favorable for a Data/Comparative item. Three types: Higher is better (↑), Lower is better (↓), Proximity (≈). (Scoring Thresholds Calibration, Scoring Function)

---

## Comparative Scoring Methods

**Comparative Method A (Pricing Proximity)** — Scores based on absolute deviation of a price ratio from 1.0. Breakpoints: ≤3% Excellent, ≤7% Good, ≤12% Concern, ≤18% Poor. Used for all Pricing vs Comps sub-items. (Scoring Thresholds Calibration, Comparative)

**Comparative Method B (Ratio, higher better)** — Scores based on the ratio of subject value to comp set average. Breakpoints: ≥1.20 Excellent, 1.00 Good, 0.80 Concern, 0.60 Poor. Used for Amenity Count, Mystery Shop, Resident Services, Resident Events vs Comps. (Scoring Thresholds Calibration, Comparative)

**Comparative Method C (Point difference)** — Scores based on the difference between subject and comp set values. Two calibrations: Occupancy (+3/0/−3/−6 pp) and Reputation (+0.5/0.0/−0.3/−0.7 points). (Scoring Thresholds Calibration, Comparative)

**Percentage point difference (pp)** — The unit used for Occupancy vs Comps scoring under Method C. Measures the gap between subject and comp set occupancy rates in percentage points (e.g., subject at 95% vs comp average at 92% = +3 pp). Distinct from a percentage of the base value. (Scoring Thresholds Calibration, Method C — Occupancy)

**Comparative Method D (Custom matrix)** — A two-dimensional scoring matrix for Resident Mobile App vs Comps. Rows: subject has/doesn't have app. Columns: comp adoption rate ranges (0–20%, 20–50%, 50–80%, 80–100%). (Scoring Thresholds Calibration, Comparative)

---

## Analytical Engine Terms

**Layer 1 — Scoring (The Report Card)** — Produces a comprehensive performance grade: overall asset score, 12 area scores, and 65 item-level scores. Deterministic and fully auditable. (Analytical Engine Specification, Layer 1)

**Layer 2 — Cohort Profiling (The Pattern Finder)** — Ranks 16 entity types by performance, groups them into top/middle/bottom cohorts, and profiles what each tier shares. Data absence is treated as a diagnostic signal. (Analytical Engine Specification, Layer 2)

**Layer 3 — Correlative Diagnostics (The Root Cause Engine)** — Answers 400+ predefined diagnostic questions from the Analytical Question Inventory. Classifies answers as strength/weakness/neutral/data-insufficient. Deductive. (Analytical Engine Specification, Layer 3)

**Layer 4 — Emergent Pattern Detection (The System's Own Observations)** — Surfaces patterns, anomalies, and relationships that nobody predefined. Uses statistical outlier detection, unexpected correlation discovery, temporal anomaly detection, cluster analysis, distribution analysis, and cross-entity anomaly detection. Inductive. (Analytical Engine Specification, Layer 4)

**Layer 5 — Unified Impact Summary (The Action Plan)** — Aggregates findings from Layers 1–4 only into a single prioritized, actionable summary. AI layer output is explicitly excluded. Deduplicates, tags, and ranks findings by financial impact. (Analytical Engine Specification, Layer 5)

**AI Analysis Layer (Advisory Only)** — Provides independent AI-generated interpretive analysis of all data and all structured layer outputs. Produces agreement confirmations, disagreement flags, supplementary observations, and investigation prompts. Does not write into any structured layer or the Impact Summary. The consultant decides whether to promote any AI observation into the formal deliverable. (Analytical Engine Specification, AI Analysis Layer)

**Trust Model** — Structured Layers 1–5 are the "record of truth" (deterministic, auditable, reproducible). The AI Analysis Layer is the "second opinion" (probabilistic, interpretive, advisory). The consultant is the "final arbiter" (human judgment, client context). (Analytical Engine Specification, AI Analysis Layer — Trust Model)

**BADS (Basic Analytic Data Set)** — A pre-computation enrichment step that derives 124 standard property performance KPIs from normalized data and benchmarks each against industry standards. Not an analytical layer. Not a gate — analytical layers can access any normalized field directly. (Analytical Engine Specification, BADS)

**Enriched data pool** — The unified data surface all analytical layers read from: 1,100+ normalized fields from PM Data Set, Audit Data Set, and CRM, plus 124 BADS-computed KPIs and benchmarks. (Analytical Engine Specification, Layer 1 — Input)

**Simulated Optimal Budget** — A property-specific "what-if" proforma representing optimal financial performance achievable based on the engine's findings. Not a generic industry benchmark. Generated after Layers 1–4 complete. Three-column output: Actual vs Owner's Budget vs Optimal. Structure mirrors Area 8 (Financials): Revenue, Expenses, Bottom Line, Capital. (Analytical Engine Specification, Simulated Optimal Budget)

**Assessment-level date range variable** — A configurable date range set once per engagement. All date-range-dependent items use this variable rather than hardcoded periods. Stored in assessment metadata. (Scoring Model Specification, Design Principle 9; Analytical Engine Specification, Date Range Variable)

**Confidence modifiers** — A planned mechanism (not yet defined) for how data contradiction density affects score trust. Modifies confidence in scores, not the scores themselves. (Analytical Engine Specification, Layer 1 — Scoring Methods)

**Diagnostic package** — A versioned bundle of analysis logic for a specific domain/topic. Includes inputs, grain, features, benchmarks, scores, findings, contradiction logic, impact models, recommendations, narratives, chart specs. (spec_1_multifamily_property_assessment_platform.md, Section 5.2)

**Finding** — A discrete analytical conclusion produced by any of Layers 1–5. Tagged with source layer(s), performance issue, financial impact estimate, and priority. (Analytical Engine Specification, Layer 5)

**Cohort** — A performance grouping (top/middle/bottom) assigned to entities in Layer 2. Thresholds defined per entity type. (Analytical Engine Specification, Layer 2)

**Entity types (16)** — Leasing Agents, Units, Unit Types, Floors, Floor Plans, Buildings, Individual Leasing Deals, Concessions, Individual Listings, Individual Tours, Traffic Sources, Vendors, Residents, Competitors, Marketing Channels, Technology Platforms. (Analytical Engine Specification, Layer 2)

---

## Data Architecture Terms

**PM Data Set (Stream 1)** — System exports and operational reports uploaded by the property or pulled from their PM software and CRM. The consultant does not create this data — they ingest it. Documented in CDI Sections 1, 2, and 7. (Complete Data Inventory, Data Collection Architecture)

**Audit Data Set (Stream 2)** — Everything collected by the consultant/auditor during the engagement through one unified audit platform. Includes property profile, mystery shops, competitive analysis, unit walks, interviews, listing assessments, leasing observations, and compliance checks. Documented in CDI Sections 3, 4, 5, 6, 8, and 10. (Complete Data Inventory, Data Collection Architecture)

**CRM** — Customer Relationship Management system data. Lead activity logs sourced from the property's CRM or PM system's CRM module. (Complete Data Inventory, Section 2)

**Canonical schema** — A source-agnostic data model where the same field semantics apply regardless of which PM system (Yardi, RealPage, Entrata, AppFolio, etc.) the data originated from. (spec_1_multifamily_property_assessment_platform.md, Section 3; Analytical Engine Specification, Normalization)

**Normalized fields** — Source data transformed to the canonical schema: standardized field names, types, formats, and semantics. The foundation for all analytical processing. (Analytical Engine Specification, Normalization)

**Bitemporal history** — A modeling approach using both effective time (when something was true in the real world) and record time (when the system learned about it). (spec_1_multifamily_property_assessment_platform.md, Section 3.2)

**fact_unit_day** — The core analytical spine: a dense daily state table with one row per unit per day. Built from lease, notice, make-ready, listing, field observation, and manual intervals. Enables cross-domain temporal analysis. (spec_1_multifamily_property_assessment_platform.md, Section 3.3)

---

## Platform & Tech Stack Terms

**PostgreSQL** — The canonical application database. Stores operational data, workflow state, security, and bitemporal entities. Uses JSONB for sparse fields and row-level security (RLS) for multi-tenant access. (spec_1_multifamily_property_assessment_platform.md, Section 3)

**ClickHouse** — The analytical warehouse. Stores dense analytical facts (e.g., fact_unit_day), pre-aggregated score marts, and supports fast slicing/benchmarking/trend queries. (spec_1_multifamily_property_assessment_platform.md, Section 3)

**Object storage** — Stores raw evidence files and frozen snapshots. Immutable, cheap, exportable. (spec_1_multifamily_property_assessment_platform.md, Section 3)

**Python analysis services** — The language and runtime for all analysis logic: parsing, analytics, rule engines, metric computation, scoring, report rendering. (spec_1_multifamily_property_assessment_platform.md, Section 3)

**Four-layer data model** — Layer A: Raw Evidence Store. Layer B: Canonical Operational Model. Layer C: Analytical Facts (ClickHouse). Layer D: Reproducible outputs. (spec_1_multifamily_property_assessment_platform.md, Section 3.1)

**Canonical operational model** — Layer B of the four-layer data model. The source-agnostic relational model in PostgreSQL where entities (units, leases, residents, vendors, staff, etc.) are stored with standardized semantics regardless of which PM system produced the data. (spec_1_multifamily_property_assessment_platform.md, Section 3.1 — Layer B)

**Analytical facts** — Layer C of the four-layer data model. Dense daily state tables (e.g., fact_unit_day) and pre-aggregated score marts stored in ClickHouse for fast slicing, benchmarking, and trend queries. (spec_1_multifamily_property_assessment_platform.md, Section 3.1 — Layer C)

**Reproducible outputs** — Layer D of the four-layer data model. Reports, assessment scorecards, comparison boards, and frozen snapshots. Immutable once generated; tied to specific data versions for auditability. (spec_1_multifamily_property_assessment_platform.md, Section 3.1 — Layer D)

---

## Assessment Terms

**Door Opener Assessment** — A public-data-only assessment for sales/initial diagnostics. Uses only data available without property access: online reputation, digital presence, website quality, listings, market context, building/unit amenities (from listings), and competitive research. Produces meaningful but scoped analysis. (Audit Workbook Specification, Overview; Complete Data Inventory, Section 0)

**Full Engagement Assessment** — A comprehensive assessment that adds site visit, mystery shops, management interviews, unit walks, back-of-house inspection, compliance checks, and all PM data to the Door Opener data. The full engagement builds upon (does not replace) door opener data. (Audit Workbook Specification, Overview)

**Workflow badge: [DOOR OPENER]** — Applied to audit workbook sections that use only public data sources. Sections 2A–2E, 10A–10K. Sections 3A–3E start as Door Opener (public data) and are verified on-site during Full Engagement. (Audit Workbook Specification, Section 1)

**Workflow badge: [FULL ENGAGEMENT]** — Applied to sections requiring property access, site visits, interviews, or PM data. Sections 4, 5, 6, 7, 8, 9, 10L, 11. (Audit Workbook Specification, Section 1)

**Workflow badge: [DOOR OPENER → VERIFIED ON-SITE]** — Applied to sections initially populated from public sources during door opener, then verified/corrected during site visit. Sections 3A, 3B, 3D, 3E. (Audit Workbook Specification, Section 1)

**Comp set** — The set of competitive properties selected for comparison against the subject property. Defined per assessment. All comps are mystery-toured using the same evaluation checklist as the subject. (Scoring Model Specification, Area 11; Complete Data Inventory, Section 0)

---

## Financial Terms

**GPR (Gross Potential Rent)** — The total rent revenue a property would generate if all units were occupied at market rent with no concessions or vacancies. (Scoring Model Specification, Area 8 — Revenue sub-items; Computation Rules Workbook)

**EGI (Effective Gross Income)** — Gross Potential Rent minus vacancy loss, concessions, and loss-to-lease, plus other income. The actual top-line revenue. (Scoring Model Specification, Area 8 — Revenue sub-items)

**NOI (Net Operating Income)** — Effective Gross Income minus Total Operating Expenses. The primary measure of property-level financial performance. (Scoring Model Specification, Area 8 — Bottom Line sub-items)

**Loss-to-Lease** — The difference between market rent (established from auditor-collected comp set data, not the property's internal rent matrix) and in-place rent, expressed as a percentage. (Computation Rules Workbook, Area 5; Scoring Thresholds Calibration, Area 5 Notes)

**PPSF (Price Per Square Foot)** — Rent divided by unit square footage. Used for standardized pricing comparisons across unit sizes. (Scoring Model Specification, Area 5; Area 11)

**Net Effective Rent** — The actual rent after accounting for concessions. Net Effective vs Asking Gap = (Asking Rent − Net Effective Rent) / Asking Rent. (Computation Rules Workbook, Area 5)

**Concession % of GPR** — Total free rent concession value divided by Gross Potential Rent. Concessions in this metric are free rent only — excludes waived fees, deposits, or non-rent incentives. (Computation Rules Workbook, Area 5)

**Owner-reported budget/targets** — Financial benchmarks provided by the property owner/client against which Area 8 (Financials) is scored. This is not an industry standard — it reflects the owner's specific expectations. (Scoring Model Specification, Financials Scoring)

**Rent Lift on Turnover** — The percentage increase in rent when a new resident replaces a departing one. (New lease rent − previous tenant rent) / previous tenant rent, averaged across all turnovers. (Computation Rules Workbook, Area 5)

---

## Scoring Areas (Quick Reference)

| # | Area | Weight | Question |
|---|------|--------|----------|
| 1 | Vacancy/Occupancy | 9% | Are units generating revenue? |
| 2 | Marketing | 8% | Is the property generating demand? |
| 3 | Leasing Performance | 8% | Is the team converting demand into leases? |
| 4 | Listings | 8% | Is the product positioned correctly? |
| 5 | Pricing | 8% | Is the property priced correctly? |
| 6 | Retention & Renewal | 8% | Are residents staying? |
| 7 | Operations | 8% | Is the property staffed and equipped to perform? |
| 8 | Financials | 9% | Is the property hitting its financial targets? |
| 9 | Maintenance & Turnovers | 8% | Are units maintained and turned efficiently? |
| 10 | Property Condition | 8% | What shape is the asset in? |
| 11 | Competitive Position | 10% | How does this property stack up? |
| 12 | Collections & Screening | 8% | Is the property screening well and collecting what it's owed? |

(Scoring Model Specification, Area Weights table and area section headers)

---

## Authoritative Document Hierarchy

When information conflicts, the document higher in this list wins. Full hierarchy defined in `.cursor/rules/rbv2-project.mdc`.

| Priority | Document | Source of Truth For |
|----------|----------|-------------------|
| 1 | `Scoring_Weights_Final_Update.json` | Locked-in weight values (12 area weights, 65 item weights, 315 sub-item points) |
| 2 | `Scoring_Model_Specification.md` | Scoring structure, methodology, design principles, area/item definitions |
| 3 | `Scoring_Model_Workbook.html` | Weight editing interface, sub-item point budgets, tier definitions |
| 4 | `Computation_Rules_Workbook.html` | Computation rules, data sources, formulas for every scored item |
| 5 | `Scoring_Thresholds_Calibration.md` | Raw-value-to-score thresholds for Data and Comparative items |
| 6 | `Analytical_Engine_Specification.md` | Engine architecture, layers, simulated optimal budget, date range variable |
| 6a | `Basic_Analytic_Data_Set.md` | 124 pre-computed KPIs, calculations, and benchmarks |
| 7 | `Complete_Data_Inventory.md` | Complete field inventory (1,100+ fields across all sources) |
| 8 | `Audit_Workbook_Specification.md` | Audit data collection instrument (field procedures, workflow badges) |
| 9 | `spec_1_multifamily_property_assessment_platform.md` | Platform requirements, tech stack, data architecture, domain model |
| 10 | `Project_Skeleton_Specification.md` | Locked tech stack, monorepo structure, naming conventions, testing, CI/CD |
| 11 | `Database_Schema_Specification.md` | Migration-ready DDL for all PostgreSQL (110 tables) and ClickHouse (15 fact tables) |
| 12 | `Shared_Type_Definitions.md` | Pydantic model reference — generated from DDL via `codegen/generate_models.py` (14 domain modules) |
| 13 | `Service_Interface_Contracts.md` | Service interfaces for 15 services (Phases 0-6), data shapes, error conditions |
| 14 | `Data_Onramp_Specification.md` | Two data streams, intake channels, vendor adapters, column mapping, review queue |
| 15 | `scoring_config.json` | Machine-readable scoring structure (12 areas, 65 items, 315 sub-items, weights, tiers) |
