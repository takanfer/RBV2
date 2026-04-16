# Data Onramp Specification

How data enters the Multifamily Property Assessment Platform: intake channels, file formats, vendor adapters, column mapping, entity resolution, review queue, and the raw evidence pipeline.

**Source documents:**
- `spec_1` §10 (Data intake and ingestion), §3.1 Layer A (Raw evidence), §5.4 (Engine pipeline)
- `Complete_Data_Inventory.md` — two streams, 12 PM categories, 8 field audit templates, 9 upload schemas
- `Audit_Workbook_Specification.md` — observation and interview data collection
- `Database_Schema_Specification.md` — Layer A tables (`source_system`, `source_ingestion`, `source_asset`, `source_record_raw`, `mapping_rule`, `mapping_review_queue`)

---

## 1. Two Data Streams

All 1,100+ fields enter the platform through exactly two streams.

### Stream 1: PM Data Set — What the Property Provides

System exports and operational reports uploaded by the property or pulled from their PM software and CRM. The consultant does not create this data — they ingest it.

| Category | CDI Section | Target Canonical Tables | Typical Format |
|----------|------------|------------------------|----------------|
| Rent Roll | §1.1 | `lease`, `unit_version` | XLSX, CSV |
| Move-In/Move-Out | §1.2 | `move_event` | XLSX, CSV |
| Lease Renewals | §1.3 | `renewal_offer` | XLSX, CSV |
| Work Orders | §1.4 | `work_order`, `work_order_line_item` | XLSX, CSV |
| Vacancy | §1.5 | `vacancy_cycle` | XLSX, CSV |
| T12 Financials | §1.6 | `budget_actual_line` | XLSX, CSV, PDF |
| Lease Charges | §1.7 | `lease_charge` | XLSX, CSV |
| Lease Detail | §1.8 | `lease` | XLSX, CSV |
| Traffic/Leads | §1.9 | `lead`, `lead_event` | XLSX, CSV |
| Lease Expirations | §1.10 | `lease` (derived) | XLSX, CSV |
| Delinquency | §1.11 | `delinquency_snapshot` | XLSX, CSV |
| Renewal Offers | §1.12 | `renewal_offer` | XLSX, CSV |
| CRM Lead Activity | §2 | `lead_event` | XLSX, CSV |

**Vendor systems:** Yardi, RealPage, Entrata, AppFolio, ResMan. The platform does not hard-code vendor-specific tables — vendor adapters normalize into a stable canonical model.

### Stream 2: Audit Data Set — What the Field Team Captures

Everything collected by the consultant/auditor through the unified audit platform: desk research, site observation, mystery shops, interviews, competitive research, and technology assessment.

| Category | CDI Sections | Target Canonical Tables | Collection Method |
|----------|-------------|------------------------|-------------------|
| Property profile | §3.1–3.24 | `property`, `property_amenity`, `unit_amenity`, `market_context`, `website_observation`, `social_observation`, `reputation_observation`, `listing_content_assessment`, `listing_photo_assessment`, + JSONB snapshots | Desk research + on-site |
| Mystery shop | §4 | `mystery_shop` | Secret shopper |
| Competitive analysis | §5 | `comp_listing_observation`, `comp_property_observation`, `comp_marketing_assessment` | Desk research + comp tours |
| Field audit templates | §6.1–6.8 | `vacant_unit_audit`, `resident_interview`, `listing_observation`, `lead_event` | On-site interviews/observation |
| Financial data | §9 | `budget_actual_line` | Owner interview |
| Technology assessment | §11 | `tech_platform`, `tech_summary` | On-site assessment |
| Condition observations | §10 | `unit_condition_observation`, `property_condition_observation`, `capital_asset_observation`, `back_of_house_observation`, `fire_safety_observation` | On-site inspection |

---

## 2. Intake Channels

The platform accepts four ingestion patterns (spec_1 §10.1):

| Channel | Examples | `ingestion_type` |
|---------|---------|------------------|
| **File import** | PM exports (rent roll XLSX, T12 CSV), CRM exports, budget PDFs | `file_import` |
| **API pull** | Where vendor APIs are available and authorized | `api_pull` |
| **Manual structured capture** | Field audits, mystery shops, interviews, observations via forms | `manual_capture` |
| **Public-data collection** | Listings, websites, social profiles, competitor observations | `public_data` |

---

## 3. Ingestion Pipeline

```
Receive file / API / form / web capture
        │
        ▼
Store raw asset + SHA-256 hash + metadata  ──▶  source_asset (S3)
        │
        ▼
Parse into source records                  ──▶  source_record_raw
        │
        ▼
Run schema mapping + validation
        │
        ├──▶ High confidence?  ──▶  Normalize to canonical entities
        │
        └──▶ Low confidence?   ──▶  mapping_review_queue
        │
        ▼
Resolve identities and aliases             ──▶  unit_alias, entity matching
        │
        ▼
Build intervals and event facts
        │
        ▼
Materialize dense facts and marts          ──▶  fact_unit_day, etc.
        │
        ▼
Run diagnostics + publish assessment refresh
```

### Pipeline database flow

1. **`source_system`** — registered source (PM system, CRM, manual form, etc.)
2. **`source_ingestion`** — each import job, tracked from pending → processing → review → complete/failed
3. **`source_asset`** — raw file preserved in S3 with SHA-256 hash and provenance
4. **`source_record_raw`** — parsed rows from the file, stored as JSONB, awaiting mapping
5. **`mapping_rule`** — reusable column mapping rules per source system and record type
6. **`mapping_review_queue`** — items needing human review before canonicalization

---

## 4. Connector Registry

Each connector in the registry declares (spec_1 §10.3):

| Property | Description |
|----------|-------------|
| `adapter_type` | `file_parser`, `api_connector`, or `manual_form` |
| `source_record_type` | What type of data it produces (e.g., `rent_roll`, `work_order`, `lead`) |
| Extraction schema | Column definitions for the expected input |
| Mapping rules | Default column→column mappings to canonical tables |
| Idempotency key | How to detect re-imports of the same data |
| Quality checks | Validation rules run before canonicalization |
| Required review steps | Which steps need human sign-off |

### Vendor adapters

Each PM system has its own adapter that lands data into the stable canonical model:

| Vendor | `vendor_name` | Notes |
|--------|--------------|-------|
| Yardi | `Yardi` | Most common; Report 55 for charge codes |
| RealPage | `RealPage` | Separate rent roll and lease detail exports |
| Entrata | `Entrata` | API-friendly; combined exports possible |
| AppFolio | `AppFolio` | Smaller portfolios |
| ResMan | `ResMan` | Growing market share |

New vendor adapters are added without changing application code — the connector registry is data-driven.

---

## 5. Upload Schemas (CDI §7)

Exact column definitions for the 9 upload templates that the platform ingests from PM exports and field data:

| Template | CDI §7 | Columns | Target Tables |
|----------|--------|---------|---------------|
| Rent Roll Appendix | §7.1 | 31 | `lease`, `unit_version`, `lease_charge` |
| Current Vacancy Snapshot | §7.2 | 32 | `vacancy_cycle`, `vacant_unit_audit` |
| Vacancy Timeline | §7.3 | 23 | `vacancy_cycle`, `make_ready_cycle` |
| Turnover Records | §7.4 | 26 | `move_event`, `work_order` |
| Listing Assessment | §7.5 | 18 | `listing_observation` |
| Recent Move-In Detail | §7.6 | 34 | `move_event`, `lead_event` |
| T12 Financial Statement | §7.7 | 21 | `budget_actual_line` |
| Lead Activity Log | §7.8 | 13 | `lead`, `lead_event` |
| Charge Code Detail | §7.9 | 6 | `lease_charge` |

---

## 6. Field Audit Templates (CDI §6, Audit Workbook §6)

Row-per-unit worksheets where PM data is pre-populated and the auditor fills observation columns on-site.

| Template | Target | Pre-populated From | Auditor Captures | Target Table |
|----------|--------|-------------------|-----------------|--------------|
| 1: Vacancy Observations | Vacant units | PM: unit info, rent, dates | Marketing status, showing method, why vacant | `vacant_unit_audit` |
| 2: Move-In Interviews | Recent move-ins (30–90 days) | PM: unit, lease, rent | Agent, source, concession, timing | `resident_interview` |
| 3: Turnover Interviews | Recent move-outs (30–90 days) | PM: unit, dates, costs | Condition, scope, screening, agent | `resident_interview` |
| 4: Renewal Context | Expiring/MTM leases | PM: unit, rent, tenure | Contacted, offer, sentiment | `resident_interview` |
| 5: Lease Expiring Audit | Leases within 120 days | PM: unit, dates, rent | Contacted, sentiment, expected outcome | `resident_interview` |
| 6: Recently Leased | Leases signed 30–60 days | PM: unit, rent, concession | Method, source, agent | `resident_interview` |
| 7: Listing Assessment | Per ILS platform | None | Photo quality, accuracy, content | `listing_observation` |
| 8: CRM Lead Upload | Fallback lead data | None | Full lead lifecycle | `lead`, `lead_event` |

### PM pre-population

Templates 1–6 have columns pre-populated from PM data that is already in the canonical store. The auditor does not re-enter this data — the platform merges PM columns automatically when the template is rendered. Auditor-filled columns are observational data that cannot be obtained from system exports.

---

## 7. Column Mapping

### 7.1 Mapping rules

Each `mapping_rule` defines a transformation from source column to canonical column:

| Field | Purpose |
|-------|---------|
| `source_system_id` | Which vendor/system this rule applies to |
| `source_record_type` | Which upload category (rent_roll, work_order, etc.) |
| `source_column` | Column name in the source file |
| `target_table` | Canonical table to write to |
| `target_column` | Canonical column name |
| `transform_expr` | Optional transformation (type cast, date parse, value map, etc.) |

Mapping rules are reusable: once a Yardi rent roll mapping is configured for one property, it applies to all Yardi properties.

### 7.2 Mapping status lifecycle

Each `source_record_raw` row moves through:

```
unmapped → auto_mapped → mapped
                ↓
         review_needed → mapped | rejected
```

- **`unmapped`** — freshly parsed, no mapping attempted
- **`auto_mapped`** — mapping rules matched with high confidence
- **`review_needed`** — confidence below threshold, sent to review queue
- **`mapped`** — successfully written to canonical entity
- **`rejected`** — human reviewer rejected the record

### 7.3 Mapping review queue

Items in `mapping_review_queue` have a `review_type`:

| Type | When |
|------|------|
| `unmapped_column` | Source file has a column with no matching mapping rule |
| `low_confidence` | Mapping rule matched but confidence below threshold |
| `ambiguous_entity` | Record could map to multiple canonical entities |
| `duplicate_suspect` | Record appears to duplicate an existing canonical record |

Resolution options: `approved`, `modified`, `rejected`, `deferred`.

---

## 8. Entity Resolution

Critical matching problems (spec_1 §10.4):

| Problem | Example |
|---------|---------|
| Unit aliases / renumbering | Unit "101" renamed to "A-101" across PM systems |
| Resident duplicates | Same person with different name spellings |
| Agent name variants | "John Smith" in CRM vs "J. Smith" in mystery shop |
| Vendor name variants | "ABC Plumbing" vs "ABC Plumbing LLC" |
| Competitor identity | Partial address match from listing scrape |

### Resolution strategy

1. **Deterministic matching first** — exact match on natural keys (unit number + property, SSN hash, etc.)
2. **Scored fuzzy matching** — Levenshtein, phonetic, and domain-specific rules for low-confidence matches
3. **Review thresholds** — matches below confidence threshold go to `mapping_review_queue`
4. **Always store provenance** — `unit_alias` records track `match_method`, `match_confidence`, and `reviewer_override`

### `unit_alias` table

The key entity resolution artifact. Every external identifier for a unit is stored with:
- `alias_key` — the external identifier value
- `alias_type` — `source_key`, `prior_label`, `marketing_label`
- `match_confidence` — 0.0000 to 1.0000
- `reviewer_override` — whether a human confirmed the match

---

## 9. Raw Evidence Preservation

All imported data is preserved immutably (spec_1 §3.1 Layer A):

| Object | Storage | Purpose |
|--------|---------|---------|
| Original file (CSV, XLSX, PDF, etc.) | S3 via `source_asset` | Immutable evidence with SHA-256 hash |
| Parsed records | `source_record_raw.raw_data` (JSONB) | Pre-mapping snapshot of each row |
| Mapping decisions | `mapping_rule` + `mapping_review_queue` | Audit trail of how data was mapped |

### Asset types supported

`source_asset.asset_type`: `csv`, `xlsx`, `pdf`, `json`, `html`, `photo`, `video`, `audio`, `transcript`, `form_submission`

### Immutability guarantee

- Raw assets in S3 are versioned and never overwritten
- `source_record_raw` rows are append-only
- Late-arriving corrected exports create new `source_ingestion` records; prior records remain for reproducibility (bitemporal model)

---

## 10. Coverage and Missingness

Missing data is modeled explicitly — not silently ignored (spec_1 §10.5):

| Mechanism | Table | Purpose |
|-----------|-------|---------|
| Assessment data coverage | `assessment_data_coverage` | Which data sources were provided for each assessment |
| Evidence coverage per fact | `fact_unit_day.evidence_coverage` | Per-day evidence quality flag |
| Score confidence | `score_result` (separate from score) | Prevents weak data masquerading as strong performance |

**Design rule:** "No listings" because the scrape failed is different from "no listings" because no listings exist. Coverage flags prevent this class of misinterpretation.

---

## 11. Derived Fields

The platform computes derived fields from PM data without requiring additional input (CDI §1.13):

| Field | Derivation |
|-------|------------|
| Floor / Building | Parsed from unit number |
| Holdover Status | Lease end vs. current date + occupancy |
| Net Effective Rent | Gross Rent − (Concession / Lease Term) |
| Loss-to-Lease | Market Rent − Gross Rent |
| Days Vacant / VDOM | Move-out → make-ready → listing → move-in date math |
| Vacancy Cost | Days Vacant × Daily Rent Loss |
| Acquisition Cost | Vacancy + Make-Ready + Concession + Fees |
| Delinquency Rate | Units with balance > 0 / Total occupied |
| Tenure | Move-in to move-out date |
| Turnover Costs | Aggregated from make-ready work orders by sub-category |

These are computed by the Metric Engine and Temporal State Builder services, not stored at ingestion time.

---

## 12. Platform KPIs for Ingestion (spec_1 "Gathering Results" §1, lines 1410-1417)

| KPI | Target |
|-----|--------|
| Import success rate by source | Track per vendor adapter |
| Mapping review rate | % of records requiring human review |
| Unit-day completeness rate | % of unit-days with complete evidence coverage |
| Ingestion latency | Time from file upload to canonical availability |

---

## Authoritative References

- `spec_1` §3.1 (Layer A), §5.4 (pipeline), §10 (intake), "Gathering Results" §1 (platform correctness KPIs, lines 1410-1417)
- `Complete_Data_Inventory.md` §1 (PM data), §2 (CRM), §6 (field audit), §7 (upload schemas)
- `Audit_Workbook_Specification.md` §6 (field templates), §9 (financial data)
- `Database_Schema_Specification.md` — Layer A tables
- `scoring_config.json` — scoring structure (coverage affects scoring confidence)
