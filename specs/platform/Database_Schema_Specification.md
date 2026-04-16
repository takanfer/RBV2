# Database Schema Specification

Migration-ready DDL for the Multifamily Property Assessment Platform. Every table and column is sourced from the authoritative specification documents listed below.

**Source documents:**
- `spec_1_multifamily_property_assessment_platform.md` — entity model (§3–4), workspace (§9), longitudinal (§14), scoring (§6), impact (§7), contradictions (§8), intake (§10)
- `Complete_Data_Inventory.md` — 1,100+ field definitions across all data sources
- `Audit_Workbook_Specification.md` — audit data collection structure and field types
- `scoring_config.json` — 12 areas, 65 items, 315 sub-items

**Conventions:**
- All identifiers use `snake_case`
- Primary keys are `uuid` with `gen_random_uuid()` default
- Bitemporal columns: `valid_from`/`valid_to` (business time), `recorded_from`/`recorded_to` (system time)
- Timestamps: `timestamptz` for system events, `date` for business dates
- Multi-tenant scoping: `tenant_id` on all top-level entities
- Extension columns: `attributes jsonb not null default '{}'::jsonb` for sparse/vendor-specific fields
- JSONB arrays use `'[]'::jsonb` default; JSONB objects use `'{}'::jsonb` default

---

## PostgreSQL Schema

### Layer A — Raw Evidence Store

> Source: spec_1 §3.1 Layer A, §10 Data Intake

#### `source_system`

Registry of external systems from which data is imported.

```sql
create table source_system (
  source_system_id   uuid primary key default gen_random_uuid(),
  tenant_id          uuid not null,
  system_name        text not null,
  system_type        text not null,       -- pm, crm, ils, public_data, manual_capture, api
  vendor_name        text null,           -- Yardi, RealPage, Entrata, AppFolio, ResMan
  api_base_url       text null,
  adapter_type       text not null,       -- file_parser, api_connector, manual_form
  configuration      jsonb not null default '{}'::jsonb,
  is_active          boolean not null default true,
  created_at         timestamptz not null default now(),
  updated_at         timestamptz not null default now()
);
create index idx_source_system_tenant on source_system (tenant_id);
```

#### `source_ingestion`

Each import job / data pull event.

```sql
create table source_ingestion (
  ingestion_id       uuid primary key default gen_random_uuid(),
  source_system_id   uuid not null references source_system(source_system_id),
  assessment_id      uuid null,
  ingestion_type     text not null,       -- file_import, api_pull, manual_capture, public_data
  status             text not null default 'pending',  -- pending, processing, review, complete, failed
  file_count         integer not null default 0,
  record_count       integer null,
  idempotency_key    text null,
  started_at         timestamptz null,
  completed_at       timestamptz null,
  error_detail       jsonb null,
  created_at         timestamptz not null default now(),
  created_by         uuid null
);
create index idx_source_ingestion_system on source_ingestion (source_system_id);
create index idx_source_ingestion_assessment on source_ingestion (assessment_id);
```

#### `source_asset`

Raw files, pages, photos, transcripts — preserved with provenance and hash.

```sql
create table source_asset (
  asset_id           uuid primary key default gen_random_uuid(),
  ingestion_id       uuid not null references source_ingestion(ingestion_id),
  asset_type         text not null,       -- csv, xlsx, pdf, json, html, photo, video, audio, transcript, form_submission
  original_filename  text null,
  mime_type          text null,
  file_size_bytes    bigint null,
  content_hash       text not null,       -- SHA-256
  storage_path       text not null,       -- S3 key
  metadata           jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_source_asset_ingestion on source_asset (ingestion_id);
create unique index idx_source_asset_hash on source_asset (content_hash);
```

#### `source_record_raw`

Parsed records from source assets before canonicalization.

```sql
create table source_record_raw (
  record_id          uuid primary key default gen_random_uuid(),
  asset_id           uuid not null references source_asset(asset_id),
  ingestion_id       uuid not null references source_ingestion(ingestion_id),
  record_type        text not null,       -- rent_roll, move_event, work_order, lead, lease, ...
  source_row_number  integer null,
  raw_data           jsonb not null,
  mapping_status     text not null default 'unmapped',  -- unmapped, auto_mapped, review_needed, mapped, rejected
  mapping_confidence numeric(5,4) null,
  canonical_entity   text null,           -- target canonical table name
  canonical_id       uuid null,           -- FK to canonical entity once mapped
  created_at         timestamptz not null default now()
);
create index idx_source_record_raw_asset on source_record_raw (asset_id);
create index idx_source_record_raw_ingestion on source_record_raw (ingestion_id);
create index idx_source_record_raw_mapping on source_record_raw (mapping_status);
```

#### `mapping_rule`

Reusable column mapping rules for transforming source records to canonical entities.

```sql
create table mapping_rule (
  rule_id            uuid primary key default gen_random_uuid(),
  source_system_id   uuid not null references source_system(source_system_id),
  source_record_type text not null,
  source_column      text not null,
  target_table       text not null,
  target_column      text not null,
  transform_expr     text null,           -- optional transformation expression
  is_active          boolean not null default true,
  created_at         timestamptz not null default now(),
  created_by         uuid null
);
create index idx_mapping_rule_system on mapping_rule (source_system_id, source_record_type);
```

#### `mapping_review_queue`

Items requiring human review during import mapping.

```sql
create table mapping_review_queue (
  review_id          uuid primary key default gen_random_uuid(),
  ingestion_id       uuid not null references source_ingestion(ingestion_id),
  record_id          uuid null references source_record_raw(record_id),
  review_type        text not null,       -- unmapped_column, low_confidence, ambiguous_entity, duplicate_suspect
  description        text not null,
  suggested_mapping  jsonb null,
  resolution         text null,           -- approved, modified, rejected, deferred
  resolved_by        uuid null,
  resolved_at        timestamptz null,
  created_at         timestamptz not null default now()
);
create index idx_mapping_review_ingestion on mapping_review_queue (ingestion_id);
create index idx_mapping_review_status on mapping_review_queue (resolution) where resolution is null;
```

---

### Layer B — Canonical Operational Model

#### Domain 1: Tenancy and Identity

> Source: spec_1 §16.1, M27

##### `tenant`

Consultant organization — top-level multi-tenant boundary.

```sql
create table tenant (
  tenant_id          uuid primary key default gen_random_uuid(),
  org_name           text not null,
  slug               text not null unique,
  settings           jsonb not null default '{}'::jsonb,
  is_active          boolean not null default true,
  created_at         timestamptz not null default now(),
  updated_at         timestamptz not null default now()
);
```

##### `user_account`

Platform users (consultants, clients, admins).

```sql
create table user_account (
  user_id            uuid primary key default gen_random_uuid(),
  tenant_id          uuid not null references tenant(tenant_id),
  email              text not null,
  display_name       text not null,
  role               text not null,       -- admin, consultant, analyst, client_viewer
  auth_provider_id   text null,
  is_active          boolean not null default true,
  created_at         timestamptz not null default now(),
  updated_at         timestamptz not null default now(),
  unique (tenant_id, email)
);
create index idx_user_account_tenant on user_account (tenant_id);
```

##### `audit_log`

Tracks all manual overrides and significant actions for auditability.

```sql
create table audit_log (
  log_id             uuid primary key default gen_random_uuid(),
  tenant_id          uuid not null,
  user_id            uuid null references user_account(user_id),
  action             text not null,
  entity_type        text not null,
  entity_id          uuid not null,
  before_value       jsonb null,
  after_value        jsonb null,
  reason             text null,
  created_at         timestamptz not null default now()
);
create index idx_audit_log_entity on audit_log (entity_type, entity_id);
create index idx_audit_log_tenant on audit_log (tenant_id, created_at);
```

---

#### Domain 2: Asset Hierarchy

> Source: spec_1 §3.2 domain 1, §3.3, §4.1; CDI §0

##### `client`

```sql
create table client (
  client_id          uuid primary key default gen_random_uuid(),
  tenant_id          uuid not null references tenant(tenant_id),
  client_name        text not null,
  contact_name       text null,
  contact_phone      text null,
  contact_email      text null,
  attributes         jsonb not null default '{}'::jsonb,
  is_active          boolean not null default true,
  created_at         timestamptz not null default now(),
  updated_at         timestamptz not null default now()
);
create index idx_client_tenant on client (tenant_id);
```

##### `portfolio`

Optional grouping of properties under a client.

```sql
create table portfolio (
  portfolio_id       uuid primary key default gen_random_uuid(),
  client_id          uuid not null references client(client_id),
  portfolio_name     text not null,
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_portfolio_client on portfolio (client_id);
```

##### `property`

Subject or competitor property master.

```sql
create table property (
  property_id        uuid primary key default gen_random_uuid(),
  tenant_id          uuid not null references tenant(tenant_id),
  client_id          uuid null references client(client_id),
  portfolio_id       uuid null references portfolio(portfolio_id),
  property_name      text not null,
  street_address     text not null,
  city               text not null,
  state              text not null,
  zip_code           text not null,
  total_units        integer null,
  year_built         integer null,
  property_class     text null,           -- A, B, C, D
  building_type      text null,           -- high_rise, mid_rise, garden, townhome, mixed
  buildings_count    integer null,
  stories            integer null,
  total_sqft         integer null,
  lot_size           text null,
  parking_spaces     integer null,
  parking_type       text null,           -- none, open, carport, covered, garage
  is_subject         boolean not null default true,
  latitude           numeric(10,7) null,
  longitude          numeric(10,7) null,
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now(),
  updated_at         timestamptz not null default now()
);
create index idx_property_tenant on property (tenant_id);
create index idx_property_client on property (client_id);
```

##### `building`

Building / section / phase within a property.

```sql
create table building (
  building_id        uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  parent_building_id uuid null references building(building_id),
  building_label     text not null,
  building_type      text null,           -- building, section, phase, tower
  stories            integer null,
  unit_count         integer null,
  has_elevator       boolean null,
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_building_property on building (property_id);
```

##### `floor_plan`

Canonical floor plan / unit type.

```sql
create table floor_plan (
  floor_plan_id      uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  plan_code          text not null,
  plan_name          text null,
  bedrooms           numeric(4,1) not null,
  bathrooms          numeric(4,1) not null,
  sqft               integer null,
  base_market_rent   numeric(12,2) null,
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now(),
  unique (property_id, plan_code)
);
create index idx_floor_plan_property on floor_plan (property_id);
```

##### `unit`

Durable unit identity — stable surrogate key surviving renumbers and migrations.

```sql
create table unit (
  unit_id            uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  unit_natural_key   text not null,
  created_at         timestamptz not null default now(),
  retired_at         timestamptz null,
  unique (property_id, unit_natural_key)
);
create index idx_unit_property on unit (property_id);
```

##### `unit_version`

Time-bounded physical/configuration attributes of a unit.

```sql
create table unit_version (
  unit_version_id    uuid primary key default gen_random_uuid(),
  unit_id            uuid not null references unit(unit_id),
  valid_from         date not null,
  valid_to           date null,
  building_id        uuid null references building(building_id),
  floor_plan_id      uuid null references floor_plan(floor_plan_id),
  floor_label        text null,
  unit_label         text not null,
  floorplan_code     text null,
  bedrooms           numeric(4,1) null,
  bathrooms          numeric(4,1) null,
  sqft               integer null,
  finish_package     text null,
  attributes         jsonb not null default '{}'::jsonb,
  recorded_from      timestamptz not null default now(),
  recorded_to        timestamptz null
);
create index idx_unit_version_unit on unit_version (unit_id);
create index idx_unit_version_valid on unit_version (unit_id, valid_from, valid_to);
```

##### `unit_existence_interval`

When the unit physically exists and is rentable / non-rentable.

```sql
create table unit_existence_interval (
  interval_id        uuid primary key default gen_random_uuid(),
  unit_id            uuid not null references unit(unit_id),
  valid_from         date not null,
  valid_to           date null,
  existence_status   text not null,       -- active, offline_reno, model, demolished, combined, split
  rentable_flag      boolean not null,
  reason_code        text null,
  recorded_from      timestamptz not null default now(),
  recorded_to        timestamptz null
);
create index idx_unit_existence_unit on unit_existence_interval (unit_id);
create index idx_unit_existence_valid on unit_existence_interval (unit_id, valid_from, valid_to);
```

##### `unit_alias`

Maps source keys and historical labels to canonical `unit_id`.

```sql
create table unit_alias (
  alias_id           uuid primary key default gen_random_uuid(),
  unit_id            uuid not null references unit(unit_id),
  source_system_id   uuid null references source_system(source_system_id),
  alias_key          text not null,
  alias_type         text not null,       -- source_key, prior_label, marketing_label
  valid_from         date null,
  valid_to           date null,
  match_method       text null,
  match_confidence   numeric(5,4) null,
  reviewer_override  boolean not null default false,
  created_at         timestamptz not null default now()
);
create index idx_unit_alias_unit on unit_alias (unit_id);
create index idx_unit_alias_key on unit_alias (alias_key, source_system_id);
```

##### `calendar_day`

Dense date dimension shared across all facts.

```sql
create table calendar_day (
  day_date           date primary key,
  day_of_week        smallint not null,
  day_of_month       smallint not null,
  day_of_year        smallint not null,
  week_of_year       smallint not null,
  month              smallint not null,
  quarter            smallint not null,
  year               smallint not null,
  is_weekend         boolean not null,
  is_month_end       boolean not null
);
```

##### `property_amenity`

Building-level amenities (CDI §3.2 — ~40 Y/N amenity fields).

```sql
create table property_amenity (
  amenity_id         uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  assessment_id      uuid null,
  amenity_category   text not null,       -- core, premium, convenience, recreation, pet, dining, event, parking
  amenity_name       text not null,
  is_present         boolean null,
  source             text null,           -- listing, website, google_maps, on_site
  verification       text null,           -- confirmed, corrected, added, not_available
  created_at         timestamptz not null default now()
);
create index idx_property_amenity_property on property_amenity (property_id);
```

##### `unit_amenity`

Unit-level amenities (CDI §3.4 — ~30 Y/N fields).

```sql
create table unit_amenity (
  amenity_id         uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  assessment_id      uuid null,
  amenity_category   text not null,       -- kitchen, bathroom, laundry, climate, flooring, storage, tech, other
  amenity_name       text not null,
  is_present         boolean null,
  source             text null,
  verification       text null,
  created_at         timestamptz not null default now()
);
create index idx_unit_amenity_property on unit_amenity (property_id);
```

##### `market_context`

Submarket data for a property assessment (CDI §3.3).

```sql
create table market_context (
  context_id         uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  assessment_id      uuid null,
  submarket_name     text null,
  submarket_vacancy_pct numeric(6,3) null,
  submarket_avg_rent_psf numeric(10,2) null,
  yoy_rent_growth_pct numeric(6,3) null,
  new_supply_units   integer null,
  employment_growth_pct numeric(6,3) null,
  population_growth_pct numeric(6,3) null,
  median_household_income numeric(12,2) null,
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_market_context_property on market_context (property_id);
```

---

#### Domain 3: Resident and Lease

> Source: spec_1 §3.2 domain 2, §3.4; CDI §1.1–1.3, §1.7–1.8, §1.10–1.12

##### `resident`

```sql
create table resident (
  resident_id        uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  resident_name      text null,
  household_id       uuid null,
  contact_email      text null,
  contact_phone      text null,
  source_system_id   uuid null references source_system(source_system_id),
  source_key         text null,
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_resident_property on resident (property_id);
```

##### `lease`

Lease master record.

```sql
create table lease (
  lease_id           uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  unit_id            uuid not null references unit(unit_id),
  resident_id        uuid null references resident(resident_id),
  lease_type         text null,           -- new, renewal, transfer, mtm
  lease_start        date not null,
  lease_end          date null,
  lease_term_months  integer null,
  execution_date     date null,
  monthly_rent       numeric(12,2) null,
  market_rent        numeric(12,2) null,
  security_deposit   numeric(12,2) null,
  concession_type    text null,
  concession_monthly numeric(12,2) null,
  concession_start   date null,
  concession_end     date null,
  leasing_agent      text null,
  move_in_date       date null,
  notice_date        date null,
  expected_move_out  date null,
  actual_move_out    date null,
  move_out_reason    text null,
  occupancy_status   text null,           -- occupied, notice, vacant, leased_not_moved_in
  source_ingestion_id uuid null,
  attributes         jsonb not null default '{}'::jsonb,
  recorded_from      timestamptz not null default now(),
  recorded_to        timestamptz null,
  created_at         timestamptz not null default now()
);
create index idx_lease_unit on lease (unit_id);
create index idx_lease_property on lease (property_id);
create index idx_lease_resident on lease (resident_id);
create index idx_lease_dates on lease (lease_start, lease_end);
```

##### `lease_interval`

Active coverage periods for a lease (bitemporal).

```sql
create table lease_interval (
  interval_id        uuid primary key default gen_random_uuid(),
  lease_id           uuid not null references lease(lease_id),
  unit_id            uuid not null references unit(unit_id),
  valid_from         date not null,
  valid_to           date null,
  monthly_rent       numeric(12,2) null,
  effective_rent     numeric(12,2) null,
  concession_value   numeric(12,2) null,
  interval_status    text not null,       -- active, notice, expired, mtm
  recorded_from      timestamptz not null default now(),
  recorded_to        timestamptz null
);
create index idx_lease_interval_lease on lease_interval (lease_id);
create index idx_lease_interval_unit on lease_interval (unit_id, valid_from, valid_to);
```

##### `lease_charge`

Per-lease recurring charges (CDI §1.7 — charge codes).

```sql
create table lease_charge (
  charge_id          uuid primary key default gen_random_uuid(),
  lease_id           uuid not null references lease(lease_id),
  unit_id            uuid not null references unit(unit_id),
  charge_code        text not null,
  charge_description text null,
  monthly_amount     numeric(12,2) not null,
  effective_from     date null,
  effective_to       date null,
  created_at         timestamptz not null default now()
);
create index idx_lease_charge_lease on lease_charge (lease_id);
create index idx_lease_charge_unit on lease_charge (unit_id);
```

##### `lease_event`

Lifecycle events on a lease (spec_1 §3.4).

```sql
create table lease_event (
  event_id           uuid primary key default gen_random_uuid(),
  lease_id           uuid not null references lease(lease_id),
  event_type         text not null,       -- signed, activated, renewed, amended, terminated, expired, mtm_started
  event_date         date not null,
  details            jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_lease_event_lease on lease_event (lease_id);
```

##### `notice_event`

Move-out notices.

```sql
create table notice_event (
  event_id           uuid primary key default gen_random_uuid(),
  lease_id           uuid not null references lease(lease_id),
  unit_id            uuid not null references unit(unit_id),
  notice_date        date not null,
  expected_move_out  date null,
  notice_type        text null,           -- resident_ntv, property_non_renewal, lease_break
  reason             text null,
  created_at         timestamptz not null default now()
);
create index idx_notice_event_lease on notice_event (lease_id);
```

##### `move_event`

Move-in and move-out events (CDI §1.2).

```sql
create table move_event (
  event_id           uuid primary key default gen_random_uuid(),
  lease_id           uuid null references lease(lease_id),
  unit_id            uuid not null references unit(unit_id),
  resident_id        uuid null references resident(resident_id),
  event_type         text not null,       -- move_in, move_out
  event_date         date not null,
  rent_amount        numeric(12,2) null,
  reason             text null,
  source_ingestion_id uuid null,
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_move_event_unit on move_event (unit_id);
create index idx_move_event_lease on move_event (lease_id);
```

##### `renewal_offer`

Renewal offers sent to residents (CDI §1.12).

```sql
create table renewal_offer (
  offer_id           uuid primary key default gen_random_uuid(),
  lease_id           uuid not null references lease(lease_id),
  unit_id            uuid not null references unit(unit_id),
  resident_id        uuid null references resident(resident_id),
  offer_date         date not null,
  current_rent       numeric(12,2) null,
  offered_rent       numeric(12,2) null,
  offered_term       text null,
  outcome            text null,           -- accepted, declined, counter, pending, no_response
  accepted_date      date null,
  incentive_offered  text null,
  incentive_value    numeric(12,2) null,
  competitor_offer   numeric(12,2) null,
  resident_sentiment text null,           -- happy, neutral, unhappy, at_risk
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_renewal_offer_lease on renewal_offer (lease_id);
create index idx_renewal_offer_unit on renewal_offer (unit_id);
```

##### `payment_event`

Rent payments and related transactions.

```sql
create table payment_event (
  event_id           uuid primary key default gen_random_uuid(),
  lease_id           uuid not null references lease(lease_id),
  unit_id            uuid not null references unit(unit_id),
  payment_date       date not null,
  amount             numeric(12,2) not null,
  payment_type       text not null,       -- rent, late_fee, utility, pet, parking, other
  payment_method     text null,
  created_at         timestamptz not null default now()
);
create index idx_payment_event_lease on payment_event (lease_id);
```

##### `delinquency_snapshot`

Outstanding balances by aging bucket (CDI §1.11).

```sql
create table delinquency_snapshot (
  snapshot_id        uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  unit_id            uuid not null references unit(unit_id),
  resident_id        uuid null references resident(resident_id),
  snapshot_date      date not null,
  current_balance    numeric(12,2) null,
  bucket_0_30        numeric(12,2) null,
  bucket_31_60       numeric(12,2) null,
  bucket_61_90       numeric(12,2) null,
  bucket_90_plus     numeric(12,2) null,
  last_payment_date  date null,
  collections_status text null,
  eviction_filed     boolean null,
  created_at         timestamptz not null default now()
);
create index idx_delinquency_unit on delinquency_snapshot (unit_id, snapshot_date);
create index idx_delinquency_property on delinquency_snapshot (property_id, snapshot_date);
```

---

#### Domain 4: Operations

> Source: spec_1 §3.2 domain 3, §4.3; CDI §1.4, §3.20

##### `staff_member`

On-site staff.

```sql
create table staff_member (
  staff_id           uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  staff_name         text not null,
  role               text null,           -- property_manager, assistant_manager, leasing_agent, maintenance_tech, other
  tenure_months      integer null,
  certifications     text null,
  is_active          boolean not null default true,
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_staff_property on staff_member (property_id);
```

##### `vendor`

External service providers.

```sql
create table vendor (
  vendor_id          uuid primary key default gen_random_uuid(),
  tenant_id          uuid not null references tenant(tenant_id),
  vendor_name        text not null,
  vendor_type        text null,
  contact_info       jsonb not null default '{}'::jsonb,
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_vendor_tenant on vendor (tenant_id);
```

##### `work_order`

Maintenance and make-ready tasks (CDI §1.4).

```sql
create table work_order (
  work_order_id      uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  unit_id            uuid null references unit(unit_id),
  work_order_number  text null,
  category           text not null,
  sub_category       text null,
  description        text null,
  priority           text null,
  status             text not null,       -- open, in_progress, complete, cancelled
  assigned_to        text null,
  vendor_id          uuid null references vendor(vendor_id),
  cost               numeric(12,2) null,
  date_created       date not null,
  date_completed     date null,
  is_make_ready      boolean not null default false,
  source_ingestion_id uuid null,
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_work_order_property on work_order (property_id);
create index idx_work_order_unit on work_order (unit_id);
create index idx_work_order_status on work_order (status);
```

##### `work_order_line_item`

Cost breakdown for a work order.

```sql
create table work_order_line_item (
  line_item_id       uuid primary key default gen_random_uuid(),
  work_order_id      uuid not null references work_order(work_order_id),
  cost_category      text not null,       -- cleaning, painting, flooring, appliance, other
  description        text null,
  amount             numeric(12,2) not null,
  created_at         timestamptz not null default now()
);
create index idx_wo_line_work_order on work_order_line_item (work_order_id);
```

##### `work_order_status_event`

Status transitions for work orders.

```sql
create table work_order_status_event (
  event_id           uuid primary key default gen_random_uuid(),
  work_order_id      uuid not null references work_order(work_order_id),
  status             text not null,
  event_date         timestamptz not null,
  notes              text null,
  created_at         timestamptz not null default now()
);
create index idx_wo_status_work_order on work_order_status_event (work_order_id);
```

##### `make_ready_cycle`

Canonical unit turn cycle with phase boundaries (spec_1 §4.3).

```sql
create table make_ready_cycle (
  cycle_id           uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  unit_id            uuid not null references unit(unit_id),
  move_out_date      date null,
  notice_date        date null,
  make_ready_start   date null,
  make_ready_complete date null,
  ready_observed     date null,
  first_listing_date date null,
  first_tour_date    date null,
  first_showing_date date null,
  application_date   date null,
  lease_signed_date  date null,
  move_in_date       date null,
  prior_lease_id     uuid null references lease(lease_id),
  new_lease_id       uuid null references lease(lease_id),
  total_turn_days    integer null,
  make_ready_scope   text null,           -- standard, heavy, full_renovation
  total_cost         numeric(12,2) null,
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_make_ready_unit on make_ready_cycle (unit_id);
create index idx_make_ready_property on make_ready_cycle (property_id);
```

##### `vacancy_cycle`

Canonical turnover cycle from move-out to move-in (spec_1 §3.3 key tables).

```sql
create table vacancy_cycle (
  cycle_id           uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  unit_id            uuid not null references unit(unit_id),
  vacancy_start      date not null,
  vacancy_end        date null,
  days_vacant        integer null,
  prior_rent         numeric(12,2) null,
  new_rent           numeric(12,2) null,
  vacancy_cost       numeric(12,2) null,
  make_ready_cycle_id uuid null references make_ready_cycle(cycle_id),
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_vacancy_cycle_unit on vacancy_cycle (unit_id);
create index idx_vacancy_cycle_property on vacancy_cycle (property_id);
```

##### `unit_condition_observation`

Field condition observations per unit (CDI §10.1, AWS §5G).

```sql
create table unit_condition_observation (
  observation_id     uuid primary key default gen_random_uuid(),
  assessment_id      uuid not null,
  unit_id            uuid not null references unit(unit_id),
  observation_date   date not null,
  observer_id        uuid null references user_account(user_id),
  flooring           text null,           -- excellent, good, fair, poor
  walls_paint        text null,
  kitchen_cabinets   text null,
  kitchen_appliances text null,
  bathroom_fixtures  text null,
  windows_blinds     text null,
  doors_hardware     text null,
  lighting_fixtures  text null,
  hvac_in_unit       text null,
  overall_cleanliness text null,
  general_finish     text null,           -- dated, acceptable, updated, modern
  cleanliness_acceptable boolean null,
  odor_present       boolean null,
  pest_evidence      boolean null,
  water_damage       boolean null,
  appliances_functional boolean null,
  windows_blinds_intact boolean null,
  hvac_operational   boolean null,
  ready_to_show      boolean null,
  condition_notes    text null,
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_unit_condition_unit on unit_condition_observation (unit_id);
create index idx_unit_condition_assessment on unit_condition_observation (assessment_id);
```

##### `field_validation`

Field observations that validate or contradict PM data.

```sql
create table field_validation (
  validation_id      uuid primary key default gen_random_uuid(),
  assessment_id      uuid not null,
  entity_type        text not null,
  entity_id          uuid not null,
  field_name         text not null,
  pm_value           text null,
  field_value        text null,
  is_match           boolean null,
  severity           text null,           -- info, warning, contradiction
  notes              text null,
  created_at         timestamptz not null default now()
);
create index idx_field_validation_assessment on field_validation (assessment_id);
create index idx_field_validation_entity on field_validation (entity_type, entity_id);
```

##### `budget_actual_line`

Monthly financial line items — budget and actuals (CDI §1.6, §3.23–3.24).

```sql
create table budget_actual_line (
  line_id            uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  assessment_id      uuid null,
  line_category      text not null,       -- revenue, expense, capital
  line_item          text not null,
  period_month       date not null,
  budget_amount      numeric(14,2) null,
  actual_amount      numeric(14,2) null,
  per_unit_amount    numeric(12,2) null,
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_budget_actual_property on budget_actual_line (property_id, period_month);
```

##### `property_condition_observation`

Overall property condition during site visit (AWS §5C).

```sql
create table property_condition_observation (
  observation_id     uuid primary key default gen_random_uuid(),
  assessment_id      uuid not null,
  property_id        uuid not null references property(property_id),
  observation_date   date not null,
  overall_condition  text null,           -- excellent, good, fair, poor, critical
  common_areas       text null,
  exterior_presentation text null,
  amenities_condition text null,
  issues_count       integer null,
  issues_detail      text null,
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_prop_condition_assessment on property_condition_observation (assessment_id);
```

##### `capital_asset_observation`

Capital asset condition per system (AWS §5D, CDI §10.4).

```sql
create table capital_asset_observation (
  observation_id     uuid primary key default gen_random_uuid(),
  assessment_id      uuid not null,
  property_id        uuid not null references property(property_id),
  system_name        text not null,       -- roof, hvac, plumbing, electrical, siding, windows, parking, elevator, water_heater, fire_safety
  system_type        text null,
  condition_rating   text null,           -- good, fair, poor, critical
  install_year       integer null,
  last_service_date  date null,
  age_years          integer null,
  observation_notes  text null,
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_capital_asset_assessment on capital_asset_observation (assessment_id);
```

##### `deferred_maintenance_item`

Deferred maintenance observed during site visit (AWS §5E).

```sql
create table deferred_maintenance_item (
  item_id            uuid primary key default gen_random_uuid(),
  assessment_id      uuid not null,
  property_id        uuid not null references property(property_id),
  location           text null,
  description        text not null,
  affected_system    text null,
  severity           text null,           -- minor, moderate, major, critical
  estimated_cost     numeric(12,2) null,
  is_safety_hazard   boolean not null default false,
  photo_asset_id     uuid null references source_asset(asset_id),
  created_at         timestamptz not null default now()
);
create index idx_deferred_maint_assessment on deferred_maintenance_item (assessment_id);
```

##### `fire_safety_observation`

Fire / safety compliance (AWS §5F, CDI §10.5).

```sql
create table fire_safety_observation (
  observation_id     uuid primary key default gen_random_uuid(),
  assessment_id      uuid not null,
  property_id        uuid not null references property(property_id),
  fire_inspection_current boolean null,
  last_fire_inspection date null,
  open_violations    boolean null,
  violation_count    integer null,
  violation_details  text null,
  no_open_code_violations boolean null,
  ada_compliance_met boolean null,
  insurance_current  boolean null,
  reac_nspire_score  numeric(5,1) null,
  elevator_inspection_current boolean null,
  last_elevator_inspection date null,
  created_at         timestamptz not null default now()
);
create index idx_fire_safety_assessment on fire_safety_observation (assessment_id);
```

##### `back_of_house_observation`

Maintenance back-of-house inspection (AWS §5H, CDI §10.3).

```sql
create table back_of_house_observation (
  observation_id     uuid primary key default gen_random_uuid(),
  assessment_id      uuid not null,
  property_id        uuid not null references property(property_id),
  shop_organized     boolean null,
  parts_inventory_labeled boolean null,
  safety_equipment_present boolean null,
  fire_extinguisher_current boolean null,
  chemical_storage_compliant boolean null,
  vehicle_cart_condition text null,        -- good, fair, poor
  cleanliness        text null,           -- good, fair, poor
  created_at         timestamptz not null default now()
);
create index idx_back_of_house_assessment on back_of_house_observation (assessment_id);
```

---

#### Domain 5: Demand (Leasing & CRM)

> Source: spec_1 §3.2 domain 4, §4.2; CDI §1.9, §2, §3.13–3.18

##### `lead`

Prospect / lead record.

```sql
create table lead (
  lead_id            uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  prospect_id        text null,
  lead_created_date  date null,
  lead_source_id     uuid null,
  agent_id           uuid null references staff_member(staff_id),
  unit_type_interest text null,
  status             text null,
  attributes         jsonb not null default '{}'::jsonb,
  source_ingestion_id uuid null,
  created_at         timestamptz not null default now()
);
create index idx_lead_property on lead (property_id);
```

##### `lead_source`

Traffic source registry.

```sql
create table lead_source (
  source_id          uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  source_name        text not null,
  source_category    text null,           -- ils, website, walk_in, referral, broker, social, paid_digital
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_lead_source_property on lead_source (property_id);
```

##### `lead_event`

Individual interactions in the lead funnel (spec_1 §3.4).

```sql
create table lead_event (
  event_id           uuid primary key default gen_random_uuid(),
  lead_id            uuid not null references lead(lead_id),
  event_type         text not null,       -- contact, inquiry, tour_scheduled, tour_completed, tour_no_show, application, approved, denied, lease_signed, lost
  event_date         date not null,
  agent_id           uuid null references staff_member(staff_id),
  response_time_min  integer null,
  outcome            text null,
  reason_lost        text null,
  notes              text null,
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_lead_event_lead on lead_event (lead_id);
create index idx_lead_event_date on lead_event (event_date);
```

##### `communication_event`

Communication touches in lead nurturing.

```sql
create table communication_event (
  event_id           uuid primary key default gen_random_uuid(),
  lead_id            uuid null references lead(lead_id),
  resident_id        uuid null references resident(resident_id),
  property_id        uuid not null references property(property_id),
  channel            text not null,       -- phone, email, text, in_person, chat
  direction          text not null,       -- inbound, outbound
  event_date         timestamptz not null,
  notes              text null,
  created_at         timestamptz not null default now()
);
create index idx_comm_event_lead on communication_event (lead_id);
create index idx_comm_event_property on communication_event (property_id);
```

##### `tour_event`

Tour occurrences.

```sql
create table tour_event (
  event_id           uuid primary key default gen_random_uuid(),
  lead_id            uuid not null references lead(lead_id),
  property_id        uuid not null references property(property_id),
  agent_id           uuid null references staff_member(staff_id),
  tour_date          date not null,
  tour_type          text null,           -- in_person, virtual, self_guided
  outcome            text null,           -- completed, no_show, cancelled
  duration_minutes   integer null,
  units_shown        jsonb null,
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_tour_event_lead on tour_event (lead_id);
create index idx_tour_event_property on tour_event (property_id);
```

##### `application_event`

Lease application events.

```sql
create table application_event (
  event_id           uuid primary key default gen_random_uuid(),
  lead_id            uuid null references lead(lead_id),
  property_id        uuid not null references property(property_id),
  unit_id            uuid null references unit(unit_id),
  application_date   date not null,
  status             text not null,       -- submitted, screening, approved, denied, cancelled, withdrawn
  screening_score    text null,
  decision_date      date null,
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_application_event_property on application_event (property_id);
create index idx_application_event_lead on application_event (lead_id);
```

##### `agent`

Leasing agent (may be external brokerage).

```sql
create table agent (
  agent_id           uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  agent_name         text not null,
  agent_type         text null,           -- in_house, broker, hybrid
  is_active          boolean not null default true,
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_agent_property on agent (property_id);
```

##### `crm_assignment_interval`

Agent assignment periods for leads (spec_1 §4.2).

```sql
create table crm_assignment_interval (
  interval_id        uuid primary key default gen_random_uuid(),
  lead_id            uuid not null references lead(lead_id),
  agent_id           uuid not null references agent(agent_id),
  assigned_from      date not null,
  assigned_to        date null,
  created_at         timestamptz not null default now()
);
create index idx_crm_assignment_lead on crm_assignment_interval (lead_id);
```

##### `conversion_metric_snapshot`

Period conversion metrics (CDI §3.15).

```sql
create table conversion_metric_snapshot (
  snapshot_id        uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  assessment_id      uuid null,
  period_label       text not null,       -- last_30d, last_90d, last_6m, last_12m
  total_leads        integer null,
  total_tours        integer null,
  total_no_shows     integer null,
  total_applications integer null,
  total_leases       integer null,
  avg_days_lead_tour numeric(8,2) null,
  avg_days_tour_app  numeric(8,2) null,
  avg_days_app_lease numeric(8,2) null,
  created_at         timestamptz not null default now()
);
create index idx_conversion_property on conversion_metric_snapshot (property_id);
```

---

#### Domain 6: Listing and Marketing

> Source: spec_1 §4.4; CDI §3.7–3.12; AWS §2D–2E

##### `marketing_channel`

Marketing channel registry.

```sql
create table marketing_channel (
  channel_id         uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  channel_name       text not null,
  channel_type       text not null,       -- ils, social, paid_digital, traditional, referral, email, website
  platform_url       text null,
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_marketing_channel_property on marketing_channel (property_id);
```

##### `campaign`

Marketing campaigns.

```sql
create table campaign (
  campaign_id        uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  channel_id         uuid null references marketing_channel(channel_id),
  campaign_name      text not null,
  start_date         date null,
  end_date           date null,
  budget             numeric(12,2) null,
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_campaign_property on campaign (property_id);
```

##### `campaign_spend`

Spend tracking per campaign period.

```sql
create table campaign_spend (
  spend_id           uuid primary key default gen_random_uuid(),
  campaign_id        uuid not null references campaign(campaign_id),
  period_month       date not null,
  amount             numeric(12,2) not null,
  created_at         timestamptz not null default now()
);
create index idx_campaign_spend_campaign on campaign_spend (campaign_id);
```

##### `website_observation`

Website quality audit (CDI §3.7, AWS §2D).

```sql
create table website_observation (
  observation_id     uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  assessment_id      uuid null,
  observation_date   date not null,
  website_url        text null,
  website_exists     boolean null,
  mobile_responsive  boolean null,
  live_chat          boolean null,
  contact_form       boolean null,
  floor_plans        boolean null,
  photo_gallery      boolean null,
  unit_availability  boolean null,
  virtual_tours      boolean null,
  online_application boolean null,
  tour_scheduling    boolean null,
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_website_obs_property on website_observation (property_id);
```

##### `social_observation`

Social media presence audit (CDI §3.9, AWS §2C).

```sql
create table social_observation (
  observation_id     uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  assessment_id      uuid null,
  platform           text not null,       -- facebook, instagram, tiktok, linkedin, youtube
  profile_url        text null,
  is_active          boolean null,
  follower_count     integer null,
  post_frequency     text null,           -- daily, 2_3x_week, weekly, bi_weekly, monthly, rarely, never
  observation_date   date not null,
  created_at         timestamptz not null default now()
);
create index idx_social_obs_property on social_observation (property_id);
```

##### `reputation_observation`

Online review platform observations (CDI §3.8, AWS §2A).

```sql
create table reputation_observation (
  observation_id     uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  assessment_id      uuid null,
  platform           text not null,       -- google, yelp, apartments_com, apartment_ratings, facebook, zillow
  platform_url       text null,
  profile_exists     boolean null,
  review_score       numeric(3,1) null,
  review_count       integer null,
  reviews_last_90d   integer null,
  observation_date   date not null,
  created_at         timestamptz not null default now()
);
create index idx_reputation_obs_property on reputation_observation (property_id);
```

##### `google_business_observation`

Google Business Profile audit (AWS §2B).

```sql
create table google_business_observation (
  observation_id     uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  assessment_id      uuid null,
  gmb_claimed        boolean null,
  gmb_optimized      boolean null,
  observation_date   date not null,
  created_at         timestamptz not null default now()
);
create index idx_gmb_obs_property on google_business_observation (property_id);
```

##### `listing`

Canonical listing record — links a unit/floor plan to a marketing channel.

```sql
create table listing (
  listing_id         uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  unit_id            uuid null references unit(unit_id),
  floor_plan_id      uuid null references floor_plan(floor_plan_id),
  channel_id         uuid null references marketing_channel(channel_id),
  platform           text not null,
  listing_url        text null,
  first_listed_date  date null,
  delisted_date      date null,
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_listing_property on listing (property_id);
create index idx_listing_unit on listing (unit_id);
```

##### `listing_observation`

Point-in-time observations of a subject listing (spec_1 §3.3 key tables; CDI §6.7).

```sql
create table listing_observation (
  observation_id     uuid primary key default gen_random_uuid(),
  listing_id         uuid null references listing(listing_id),
  property_id        uuid not null references property(property_id),
  unit_id            uuid null references unit(unit_id),
  assessment_id      uuid null,
  platform           text not null,
  observation_date   date not null,
  asking_rent        numeric(12,2) null,
  concession_displayed boolean null,
  concession_amount  numeric(12,2) null,
  photo_count        integer null,
  photo_quality      numeric(4,1) null,   -- 1-10
  description_quality numeric(4,1) null,  -- 1-10
  description_word_count integer null,
  floor_plan_available boolean null,
  virtual_tour_available boolean null,
  amenities_listed   boolean null,
  pricing_accurate   boolean null,
  matches_availability boolean null,
  contact_info_accurate boolean null,
  listing_url        text null,
  notes              text null,
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_listing_obs_property on listing_observation (property_id);
create index idx_listing_obs_unit on listing_observation (unit_id);
create index idx_listing_obs_date on listing_observation (observation_date);
```

##### `listing_photo_assessment`

Photo quality assessment for listings (CDI §3.12).

```sql
create table listing_photo_assessment (
  assessment_photo_id uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  assessment_id      uuid null,
  hero_image_present boolean null,
  exterior_shots_count integer null,
  living_room_shown  boolean null,
  kitchen_shown      boolean null,
  bedrooms_shown     boolean null,
  bathrooms_shown    boolean null,
  features_shown     boolean null,
  pool_photo         boolean null,
  fitness_photo      boolean null,
  clubhouse_photo    boolean null,
  other_amenity_count integer null,
  total_amenities    integer null,
  amenities_photographed integer null,
  lifestyle_photos   integer null,
  professional_photographer boolean null,
  last_photo_update  date null,
  shows_actual_units text null,           -- yes, no, mix
  created_at         timestamptz not null default now()
);
create index idx_listing_photo_property on listing_photo_assessment (property_id);
```

##### `listing_content_assessment`

Content quality assessment for listings (CDI §3.11).

```sql
create table listing_content_assessment (
  content_id         uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  assessment_id      uuid null,
  platform_count     integer null,
  ils_coverage       text null,           -- both, one, neither
  posting_method     text null,           -- centralized_syndication, partial_syndication, manual
  syndication_tool   text null,
  update_frequency   text null,           -- real_time, daily, weekly, manual
  usp_mentioned      boolean null,
  neighborhood_context boolean null,
  call_to_action     boolean null,
  contact_info_clear boolean null,
  floor_plans_on_listing boolean null,
  unit_specs_accurate boolean null,
  amenities_fully_listed boolean null,
  pet_policy_stated  boolean null,
  lease_terms_mentioned boolean null,
  pricing_consistent boolean null,
  availability_accurate boolean null,
  photos_match_condition boolean null,
  specials_updated   boolean null,
  created_at         timestamptz not null default now()
);
create index idx_listing_content_property on listing_content_assessment (property_id);
```

##### `listing_asset`

Photos, floor plans, video associated with a listing.

```sql
create table listing_asset (
  asset_id           uuid primary key default gen_random_uuid(),
  listing_id         uuid not null references listing(listing_id),
  asset_type         text not null,       -- photo, floor_plan, video, virtual_tour
  storage_path       text null,
  quality_score      numeric(4,1) null,
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_listing_asset_listing on listing_asset (listing_id);
```

##### `marketing_observation`

Property-level marketing observations over time (spec_1 §3.4).

```sql
create table marketing_observation (
  observation_id     uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  assessment_id      uuid null,
  observation_date   date not null,
  observation_type   text not null,       -- website, social, brand, channel_presence
  data               jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_marketing_obs_property on marketing_observation (property_id);
```

---

#### Domain 7: Market and Competition

> Source: spec_1 §3.2 domain 5, §4.5; CDI §5

##### `competitive_set`

Named comp set for a property assessment.

```sql
create table competitive_set (
  comp_set_id        uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  assessment_id      uuid null,
  set_name           text not null,
  valid_from         date null,
  valid_to           date null,
  created_at         timestamptz not null default now()
);
create index idx_comp_set_property on competitive_set (property_id);
```

##### `competitive_set_member`

Links competitor properties to a comp set.

```sql
create table competitive_set_member (
  member_id          uuid primary key default gen_random_uuid(),
  comp_set_id        uuid not null references competitive_set(comp_set_id),
  competitor_property_id uuid not null references property(property_id),
  distance_miles     numeric(6,2) null,
  created_at         timestamptz not null default now()
);
create index idx_comp_member_set on competitive_set_member (comp_set_id);
```

##### `comp_floorplan`

Competitor floor plan / unit type observations.

```sql
create table comp_floorplan (
  comp_floorplan_id  uuid primary key default gen_random_uuid(),
  competitor_property_id uuid not null references property(property_id),
  unit_type          text null,
  bedrooms           numeric(4,1) null,
  bathrooms          numeric(4,1) null,
  sqft               integer null,
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_comp_floorplan_property on comp_floorplan (competitor_property_id);
```

##### `comp_listing_observation`

Competitor unit/floorplan pricing observations (CDI §5.11; spec_1 §3.3 key tables).

```sql
create table comp_listing_observation (
  observation_id     uuid primary key default gen_random_uuid(),
  competitor_property_id uuid not null references property(property_id),
  comp_floorplan_id  uuid null references comp_floorplan(comp_floorplan_id),
  assessment_id      uuid null,
  observation_date   date not null,
  bedrooms           numeric(4,1) null,
  bathrooms          numeric(4,1) null,
  unit_type          text null,
  sqft               integer null,
  asking_rent        numeric(12,2) null,
  rent_per_sqft      numeric(8,2) null,
  floor              text null,
  is_available       boolean null,
  private_outdoor    boolean null,
  concession_amount  numeric(12,2) null,
  days_listed        integer null,
  confidence_score   numeric(5,4) null,
  notes              text null,
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_comp_listing_property on comp_listing_observation (competitor_property_id);
create index idx_comp_listing_date on comp_listing_observation (observation_date);
```

##### `comp_property_observation`

Competitor property-level observations.

```sql
create table comp_property_observation (
  observation_id     uuid primary key default gen_random_uuid(),
  competitor_property_id uuid not null references property(property_id),
  assessment_id      uuid null,
  observation_date   date not null,
  occupancy_rate_pct numeric(6,3) null,
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_comp_prop_obs_property on comp_property_observation (competitor_property_id);
```

##### `comp_marketing_assessment`

Analyst-assessed 0-10 scores for competitor marketing (CDI §5.9).

```sql
create table comp_marketing_assessment (
  assessment_score_id uuid primary key default gen_random_uuid(),
  competitor_property_id uuid not null references property(property_id),
  assessment_id      uuid null,
  platform_coverage  numeric(4,1) null,
  photo_quality      numeric(4,1) null,
  content_quality    numeric(4,1) null,
  listing_accuracy   numeric(4,1) null,
  website_quality    numeric(4,1) null,
  social_marketing   numeric(4,1) null,
  partnership_referral numeric(4,1) null,
  created_at         timestamptz not null default now()
);
create index idx_comp_marketing_property on comp_marketing_assessment (competitor_property_id);
```

---

#### Domain 8: Mystery Shop and Field Evidence

> Source: spec_1 §3.3 key tables; CDI §4; AWS §4

##### `mystery_shop`

Structured mystery shop evaluation (subject or competitor).

```sql
create table mystery_shop (
  shop_id            uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  assessment_id      uuid not null,
  shop_date          date not null,
  agent_name         text null,
  is_subject         boolean not null default true,
  phone_friendly_greeting boolean null,
  phone_answered_timely boolean null,
  phone_enthusiasm   boolean null,
  phone_described_community boolean null,
  phone_qualifying_questions boolean null,
  phone_offered_incentives boolean null,
  phone_matched_needs boolean null,
  phone_scheduled_tour boolean null,
  phone_collected_info boolean null,
  phone_impression   numeric(4,1) null,
  phone_response_time numeric(8,2) null,
  phone_response_unit text null,          -- minutes, hours
  email_response_time numeric(8,2) null,
  email_response_unit text null,
  greeting_prompt    boolean null,
  greeting_eye_contact boolean null,
  greeting_handshake boolean null,
  greeting_asked_name boolean null,
  greeting_rapport   boolean null,
  greeting_refreshments boolean null,
  greeting_impression numeric(4,1) null,
  needs_move_timeline boolean null,
  needs_floor_plan   boolean null,
  needs_budget       boolean null,
  needs_lifestyle    boolean null,
  needs_most_important boolean null,
  needs_active_listening boolean null,
  needs_impression   numeric(4,1) null,
  wait_time_minutes  numeric(6,1) null,
  tour_duration_minutes numeric(6,1) null,
  tour_showed_unit   boolean null,
  tour_highlighted_features boolean null,
  tour_amenities     boolean null,
  tour_tailored      boolean null,
  tour_product_knowledge boolean null,
  tour_competitive_knowledge boolean null,
  tour_submarket_knowledge boolean null,
  tour_lease_terms   boolean null,
  tour_curb_appeal   boolean null,
  tour_fair_housing  boolean null,
  presentation_impression numeric(4,1) null,
  close_asked_lease  boolean null,
  close_overcame_objections boolean null,
  close_next_steps   boolean null,
  close_urgency      boolean null,
  close_pricing_info boolean null,
  closing_impression numeric(4,1) null,
  followup_received  boolean null,
  followup_personalized boolean null,
  followup_referenced_visit boolean null,
  followup_close_attempt boolean null,
  followup_impression numeric(4,1) null,
  followup_timing    text null,           -- same_day, next_day, within_48h, after_48h, never
  followup_method    text null,           -- phone, email, text, multiple, none
  fair_housing_no_discrimination boolean null,
  fair_housing_consistent boolean null,
  fair_housing_accommodations boolean null,
  fair_housing_impression numeric(4,1) null,
  condition_grounds  boolean null,
  condition_office   boolean null,
  condition_show_unit boolean null,
  condition_common_areas boolean null,
  condition_signage  boolean null,
  condition_impression numeric(4,1) null,
  overall_experience numeric(4,1) null,
  strengths          text null,
  gaps               text null,
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_mystery_shop_property on mystery_shop (property_id);
create index idx_mystery_shop_assessment on mystery_shop (assessment_id);
```

##### `vacant_unit_audit`

Field vacancy observation per unit (CDI §6.1, AWS §6A).

```sql
create table vacant_unit_audit (
  audit_id           uuid primary key default gen_random_uuid(),
  assessment_id      uuid not null,
  unit_id            uuid not null references unit(unit_id),
  property_id        uuid not null references property(property_id),
  observation_date   date not null,
  marketed           boolean null,
  like_kind_listing_date date null,
  marketed_date      date null,
  listing_platform   text null,
  listing_type       text null,
  representative_unit boolean null,
  last_refresh_date  date null,
  leasing_agent      text null,
  tours_scheduled    integer null,
  tours_completed    integer null,
  applications_received integer null,
  showing_method     text null,           -- self_guided, agent_led, virtual
  why_still_vacant   text null,
  concession_type    text null,
  concession_proactive boolean null,
  notes              text null,
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_vacant_audit_unit on vacant_unit_audit (unit_id);
create index idx_vacant_audit_assessment on vacant_unit_audit (assessment_id);
```

##### `resident_interview`

Resident interview data — move-in, turnover, renewal, lease-expiring (CDI §6.2–6.6, AWS §6B–6F).

```sql
create table resident_interview (
  interview_id       uuid primary key default gen_random_uuid(),
  assessment_id      uuid not null,
  unit_id            uuid not null references unit(unit_id),
  property_id        uuid not null references property(property_id),
  interview_type     text not null,       -- move_in, turnover, renewal, lease_expiring, recently_leased
  interview_date     date not null,
  resident_id        uuid null references resident(resident_id),
  data               jsonb not null default '{}'::jsonb,
  notes              text null,
  created_at         timestamptz not null default now()
);
create index idx_resident_interview_assessment on resident_interview (assessment_id);
create index idx_resident_interview_unit on resident_interview (unit_id);
```

##### `tour_observation`

Auditor shadow of a live tour (AWS §8).

```sql
create table tour_observation (
  observation_id     uuid primary key default gen_random_uuid(),
  assessment_id      uuid not null,
  property_id        uuid not null references property(property_id),
  observation_date   date not null,
  data               jsonb not null default '{}'::jsonb,
  notes              text null,
  created_at         timestamptz not null default now()
);
create index idx_tour_obs_assessment on tour_observation (assessment_id);
```

---

#### Domain 9: Technology Stack

> Source: CDI §3.22, §8; AWS §11

##### `tech_platform`

Technology platform used at the property.

```sql
create table tech_platform (
  platform_id        uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  assessment_id      uuid null,
  platform_name      text not null,
  annual_cost        numeric(12,2) null,
  staff_mobile_access boolean null,
  functions_handled  jsonb not null default '[]'::jsonb,
  capabilities       jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_tech_platform_property on tech_platform (property_id);
```

##### `tech_summary`

Aggregate technology stack assessment (CDI §3.22).

```sql
create table tech_summary (
  summary_id         uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  assessment_id      uuid null,
  total_annual_spend numeric(12,2) null,
  spend_per_unit     numeric(12,2) null,
  active_integrations integer null,
  staff_mobile_access boolean null,
  resident_app       boolean null,
  automation_level   text null,           -- high, moderate, low, minimal
  redundant_systems  text null,           -- none, some, many
  gaps_pain_points   text null,
  created_at         timestamptz not null default now()
);
create index idx_tech_summary_property on tech_summary (property_id);
```

---

#### Domain 10: Assessment and Deliverables

> Source: spec_1 §3.2 domain 6, §4.6, §6, §7, §8, §9, §14

##### `assessment`

Top-level assessment container.

```sql
create table assessment (
  assessment_id      uuid primary key default gen_random_uuid(),
  tenant_id          uuid not null references tenant(tenant_id),
  property_id        uuid not null references property(property_id),
  client_id          uuid null references client(client_id),
  assessment_type    text not null,       -- full_engagement, door_opener
  status             text not null default 'draft',  -- draft, in_progress, complete, archived
  date_range_start   date null,
  date_range_end     date null,
  site_visit_date    date null,
  comp_set_id        uuid null references competitive_set(comp_set_id),
  created_by         uuid null references user_account(user_id),
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now(),
  updated_at         timestamptz not null default now()
);
create index idx_assessment_property on assessment (property_id);
create index idx_assessment_tenant on assessment (tenant_id);
```

##### `assessment_data_coverage`

What data sources are available for an assessment (spec_1 §10.5).

```sql
create table assessment_data_coverage (
  coverage_id        uuid primary key default gen_random_uuid(),
  assessment_id      uuid not null references assessment(assessment_id),
  domain             text not null,       -- pm_data, crm, field_audit, mystery_shop, listings, financial, competitive
  source_system_id   uuid null references source_system(source_system_id),
  coverage_status    text not null,       -- full, partial, missing
  coverage_pct       numeric(5,2) null,
  notes              text null,
  created_at         timestamptz not null default now()
);
create index idx_assessment_coverage on assessment_data_coverage (assessment_id);
```

##### `analysis_run`

A diagnostic analysis execution against an assessment.

```sql
create table analysis_run (
  run_id             uuid primary key default gen_random_uuid(),
  assessment_id      uuid not null references assessment(assessment_id),
  rule_package_version text not null,
  benchmark_version  text null,
  transformation_version text null,
  status             text not null default 'pending',
  started_at         timestamptz null,
  completed_at       timestamptz null,
  created_at         timestamptz not null default now()
);
create index idx_analysis_run_assessment on analysis_run (assessment_id);
```

##### `scorecard`

Assessment scorecard — container for score results.

```sql
create table scorecard (
  scorecard_id       uuid primary key default gen_random_uuid(),
  assessment_id      uuid not null references assessment(assessment_id),
  analysis_run_id    uuid null references analysis_run(run_id),
  scorecard_type     text not null,       -- full, door_opener, domain
  overall_score      numeric(6,2) null,
  overall_grade      text null,
  version            text not null,
  created_at         timestamptz not null default now()
);
create index idx_scorecard_assessment on scorecard (assessment_id);
```

##### `score_result`

Individual score for an area/item/sub-item (spec_1 §6.1).

```sql
create table score_result (
  result_id          uuid primary key default gen_random_uuid(),
  scorecard_id       uuid not null references scorecard(scorecard_id),
  assessment_id      uuid not null references assessment(assessment_id),
  analysis_run_id    uuid null references analysis_run(run_id),
  scoring_level      text not null,       -- area, item, sub_item
  area_number        integer null,
  area_name          text null,
  item_name          text null,
  sub_item_name      text null,
  input_type         text null,           -- data, checklist, comparative
  metric_value       numeric(14,4) null,
  normalized_score   numeric(6,2) null,   -- 0-10
  weight             numeric(8,4) null,
  weighted_score     numeric(8,4) null,
  benchmark_type     text null,           -- operational_standard, competitive, internal_relative, predictive
  benchmark_reference text null,
  confidence_score   numeric(5,2) null,
  coverage_score     numeric(5,2) null,
  grade_letter       text null,
  scope_status       text null,           -- in_scope, out_of_scope
  evidence_count     integer null,
  version            text not null,
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_score_result_scorecard on score_result (scorecard_id);
create index idx_score_result_assessment on score_result (assessment_id);
create index idx_score_result_area on score_result (area_number, item_name);
```

##### `finding`

Diagnostic finding with evidence (spec_1 §5.6, §6).

```sql
create table finding (
  finding_id         uuid primary key default gen_random_uuid(),
  assessment_id      uuid not null references assessment(assessment_id),
  analysis_run_id    uuid null references analysis_run(run_id),
  finding_type       text not null,       -- metric_warning, contradiction, pattern, root_cause, composite
  domain             text not null,
  severity           text not null,       -- info, watch, warning, critical
  title              text not null,
  description        text not null,
  entity_type        text null,
  entity_id          uuid null,
  evidence_refs      jsonb not null default '[]'::jsonb,
  contributing_causes jsonb not null default '[]'::jsonb,
  confidence         numeric(5,2) null,
  rule_package_version text null,
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_finding_assessment on finding (assessment_id);
create index idx_finding_domain on finding (domain);
```

##### `impact_estimate`

Quantified financial impact of a finding (spec_1 §7).

```sql
create table impact_estimate (
  estimate_id        uuid primary key default gen_random_uuid(),
  finding_id         uuid not null references finding(finding_id),
  assessment_id      uuid not null references assessment(assessment_id),
  impact_model       text not null,       -- vacancy_loss, avoidable_turn_delay, below_market_rent, concession_leakage, retention_failure, collections_risk, maintenance_overspend, vendor_rework, marketing_waste, pricing_misposition
  impact_family_id   uuid null,
  primary_driver_share numeric(5,4) null,
  contributing_share numeric(5,4) null,
  low_estimate       numeric(14,2) null,
  base_estimate      numeric(14,2) null,
  high_estimate      numeric(14,2) null,
  annualized_amount  numeric(14,2) null,
  per_unit_amount    numeric(12,2) null,
  formula_trace      jsonb not null default '{}'::jsonb,
  assumption_trace   jsonb not null default '{}'::jsonb,
  confidence         numeric(5,2) null,
  created_at         timestamptz not null default now()
);
create index idx_impact_finding on impact_estimate (finding_id);
create index idx_impact_assessment on impact_estimate (assessment_id);
create index idx_impact_family on impact_estimate (impact_family_id);
```

##### `contradiction`

Contradiction records between data sources (spec_1 §8).

```sql
create table contradiction (
  contradiction_id   uuid primary key default gen_random_uuid(),
  assessment_id      uuid not null references assessment(assessment_id),
  source_a_type      text not null,
  source_a_ref       uuid null,
  source_b_type      text not null,
  source_b_ref       uuid null,
  matching_rule      text not null,
  contradiction_type text not null,
  severity           text not null,       -- low, medium, high, critical
  affected_domains   jsonb not null default '[]'::jsonb,
  trust_penalty      numeric(5,4) null,
  evidence_links     jsonb not null default '[]'::jsonb,
  notes              text null,
  created_at         timestamptz not null default now()
);
create index idx_contradiction_assessment on contradiction (assessment_id);
```

##### `recommendation`

Structured recommendation from findings (spec_1 §14.3).

```sql
create table recommendation (
  recommendation_id  uuid primary key default gen_random_uuid(),
  finding_id         uuid null references finding(finding_id),
  assessment_id      uuid not null references assessment(assessment_id),
  domain             text not null,
  target_entity_type text null,
  target_entity_id   uuid null,
  priority           text not null,       -- critical, high, medium, low
  title              text not null,
  description        text not null,
  expected_impact    jsonb null,
  owner              text null,
  due_date           date null,
  status             text not null default 'open',  -- open, in_progress, completed, deferred, rejected
  verification_evidence jsonb null,
  created_at         timestamptz not null default now(),
  updated_at         timestamptz not null default now()
);
create index idx_recommendation_assessment on recommendation (assessment_id);
create index idx_recommendation_finding on recommendation (finding_id);
```

---

#### Domain 11: Workspace — Studies, Snapshots, Reports

> Source: spec_1 §9, §12

##### `study`

Named investigation container.

```sql
create table study (
  study_id           uuid primary key default gen_random_uuid(),
  assessment_id      uuid not null references assessment(assessment_id),
  study_name         text not null,
  description        text null,
  created_by         uuid null references user_account(user_id),
  created_at         timestamptz not null default now(),
  updated_at         timestamptz not null default now()
);
create index idx_study_assessment on study (assessment_id);
```

##### `saved_query`

Reusable query definition.

```sql
create table saved_query (
  query_id           uuid primary key default gen_random_uuid(),
  assessment_id      uuid null references assessment(assessment_id),
  study_id           uuid null references study(study_id),
  query_name         text not null,
  query_definition   jsonb not null,
  parameters         jsonb not null default '{}'::jsonb,
  filters            jsonb not null default '{}'::jsonb,
  chart_spec         jsonb null,
  created_by         uuid null references user_account(user_id),
  created_at         timestamptz not null default now()
);
create index idx_saved_query_assessment on saved_query (assessment_id);
create index idx_saved_query_study on saved_query (study_id);
```

##### `result_snapshot`

Frozen output of a query or diagnostic.

```sql
create table result_snapshot (
  snapshot_id        uuid primary key default gen_random_uuid(),
  saved_query_id     uuid null references saved_query(query_id),
  assessment_id      uuid null references assessment(assessment_id),
  study_id           uuid null references study(study_id),
  source_data_version text null,
  transformation_version text null,
  rule_package_version text null,
  benchmark_version  text null,
  result_payload     jsonb not null,
  chart_spec         jsonb null,
  sql_definition     text null,
  filters            jsonb not null default '{}'::jsonb,
  data_hash          text null,
  created_by         uuid null references user_account(user_id),
  created_at         timestamptz not null default now()
);
create index idx_snapshot_assessment on result_snapshot (assessment_id);
create index idx_snapshot_study on result_snapshot (study_id);
```

##### `study_item`

Links a study to snapshots, findings, notes, or comparisons.

```sql
create table study_item (
  item_id            uuid primary key default gen_random_uuid(),
  study_id           uuid not null references study(study_id),
  item_type          text not null,       -- snapshot, finding, annotation, comparison
  ref_id             uuid not null,
  sort_order         integer null,
  created_at         timestamptz not null default now()
);
create index idx_study_item_study on study_item (study_id);
```

##### `comparison_board`

Side-by-side layout of selected results.

```sql
create table comparison_board (
  board_id           uuid primary key default gen_random_uuid(),
  study_id           uuid null references study(study_id),
  assessment_id      uuid null references assessment(assessment_id),
  board_name         text not null,
  layout             jsonb not null default '{}'::jsonb,
  created_by         uuid null references user_account(user_id),
  created_at         timestamptz not null default now()
);
create index idx_comparison_board_study on comparison_board (study_id);
```

##### `annotation`

Consultant notes tied to evidence or result cells.

```sql
create table annotation (
  annotation_id      uuid primary key default gen_random_uuid(),
  entity_type        text not null,
  entity_id          uuid not null,
  note_text          text not null,
  created_by         uuid null references user_account(user_id),
  created_at         timestamptz not null default now(),
  updated_at         timestamptz not null default now()
);
create index idx_annotation_entity on annotation (entity_type, entity_id);
```

##### `evidence_bundle`

Curated set of rows, photos, listings, and findings for export.

```sql
create table evidence_bundle (
  bundle_id          uuid primary key default gen_random_uuid(),
  assessment_id      uuid not null references assessment(assessment_id),
  bundle_name        text not null,
  item_refs          jsonb not null default '[]'::jsonb,
  created_by         uuid null references user_account(user_id),
  created_at         timestamptz not null default now()
);
create index idx_evidence_bundle_assessment on evidence_bundle (assessment_id);
```

##### `report`

Report container.

```sql
create table report (
  report_id          uuid primary key default gen_random_uuid(),
  assessment_id      uuid not null references assessment(assessment_id),
  template_name      text not null,
  report_type        text not null,       -- full_assessment, executive_summary, vacancy_deep_dive, leasing_deep_dive, competitive_analysis, progress_tracking, door_opener, custom
  status             text not null default 'draft',
  created_by         uuid null references user_account(user_id),
  created_at         timestamptz not null default now(),
  updated_at         timestamptz not null default now()
);
create index idx_report_assessment on report (assessment_id);
```

##### `report_section`

Individual section within a report.

```sql
create table report_section (
  section_id         uuid primary key default gen_random_uuid(),
  report_id          uuid not null references report(report_id),
  section_type       text not null,       -- scorecard, finding, saved_query, snapshot, commentary, recommendation
  sort_order         integer not null,
  title              text null,
  content            jsonb not null default '{}'::jsonb,
  data_bindings      jsonb not null default '{}'::jsonb,
  narrative          text null,
  chart_spec         jsonb null,
  created_at         timestamptz not null default now()
);
create index idx_report_section_report on report_section (report_id);
```

##### `report_render`

Rendered output of a report.

```sql
create table report_render (
  render_id          uuid primary key default gen_random_uuid(),
  report_id          uuid not null references report(report_id),
  format             text not null,       -- pdf, html, pptx
  storage_path       text not null,
  section_manifest   jsonb not null default '[]'::jsonb,
  rendered_at        timestamptz not null default now(),
  rendered_by        uuid null references user_account(user_id)
);
create index idx_report_render_report on report_render (report_id);
```

---

#### Domain 12: Staffing, Training, Leasing Model

> Source: CDI §3.13, §3.14, §3.19; AWS §7A–7N

##### `staffing_snapshot`

Staffing and compensation snapshot per assessment (CDI §3.19).

```sql
create table staffing_snapshot (
  snapshot_id        uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  assessment_id      uuid null,
  data               jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_staffing_property on staffing_snapshot (property_id);
```

##### `leasing_model_snapshot`

Leasing model, compensation, and training data (CDI §3.13).

```sql
create table leasing_model_snapshot (
  snapshot_id        uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  assessment_id      uuid null,
  data               jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_leasing_model_property on leasing_model_snapshot (property_id);
```

##### `resident_event_program`

Resident event program data (CDI §3.5).

```sql
create table resident_event_program (
  program_id         uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  assessment_id      uuid null,
  data               jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_resident_event_property on resident_event_program (property_id);
```

##### `renewal_retention_snapshot`

Renewal process and retention program data (CDI §3.21).

```sql
create table renewal_retention_snapshot (
  snapshot_id        uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  assessment_id      uuid null,
  data               jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_renewal_retention_property on renewal_retention_snapshot (property_id);
```

##### `partnership_referral_snapshot`

Referral, broker, corporate relocation programs (CDI §3.10).

```sql
create table partnership_referral_snapshot (
  snapshot_id        uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  assessment_id      uuid null,
  data               jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now()
);
create index idx_partnership_property on partnership_referral_snapshot (property_id);
```

---

#### Domain 13: Scoring Configuration (Metadata)

> Source: scoring_config.json — 12 areas, 65 items, 315 sub-items

##### `scoring_rubric_version`

Versioned scoring configuration.

```sql
create table scoring_rubric_version (
  version_id         uuid primary key default gen_random_uuid(),
  version_label      text not null unique,
  is_active          boolean not null default false,
  config             jsonb not null,      -- full scoring_config.json content
  created_at         timestamptz not null default now()
);
```

##### `benchmark_version`

Versioned benchmark reference sets.

```sql
create table benchmark_version (
  version_id         uuid primary key default gen_random_uuid(),
  version_label      text not null,
  benchmark_type     text not null,       -- operational_standard, competitive, internal_relative
  data               jsonb not null,
  is_active          boolean not null default false,
  created_at         timestamptz not null default now()
);
```

##### `metric_registry`

Registry of all computed metrics.

```sql
create table metric_registry (
  metric_id          uuid primary key default gen_random_uuid(),
  metric_name        text not null unique,
  domain             text not null,
  grain              text not null,
  description        text null,
  formula            text null,
  required_inputs    jsonb not null default '[]'::jsonb,
  output_type        text not null,       -- numeric, percentage, currency, days, count, boolean
  version            text not null,
  created_at         timestamptz not null default now()
);
```

##### `diagnostic_package`

Versioned diagnostic analysis packages (spec_1 §5.2).

```sql
create table diagnostic_package (
  package_id         uuid primary key default gen_random_uuid(),
  package_name       text not null,       -- e.g., vacancy.turn_cycle, leasing.crm_response
  domain             text not null,
  version            text not null,
  required_inputs    jsonb not null default '[]'::jsonb,
  optional_inputs    jsonb not null default '[]'::jsonb,
  grain              text null,
  description        text null,
  is_active          boolean not null default true,
  created_at         timestamptz not null default now(),
  unique (package_name, version)
);
```

##### `impact_model_catalog`

Reusable financial impact model definitions (spec_1 §7.1).

```sql
create table impact_model_catalog (
  model_id           uuid primary key default gen_random_uuid(),
  model_name         text not null unique,
  formula            text not null,
  required_inputs    jsonb not null default '[]'::jsonb,
  optional_refinements jsonb not null default '[]'::jsonb,
  low_high_params    jsonb not null default '{}'::jsonb,
  double_count_rules jsonb not null default '[]'::jsonb,
  narrative          text null,
  version            text not null,
  created_at         timestamptz not null default now()
);
```

---

### Layer C — Analytical Facts (ClickHouse)

> Source: spec_1 §3.1 Layer C, §3.3, §14.2

All ClickHouse tables use `MergeTree` family engines with appropriate ordering keys for the analytical query patterns described in spec_1.

#### `fact_unit_day`

One row per unit per day of existence — the core state spine.

```sql
-- ClickHouse
CREATE TABLE fact_unit_day (
  property_id        UUID,
  unit_id            UUID,
  day_date           Date,
  unit_version_id    UUID,
  existence_status   LowCardinality(String),
  rentable_flag      UInt8,
  occupancy_state    LowCardinality(String),   -- occupied, notice, vacant, leased_not_moved_in, offline
  readiness_state    LowCardinality(String),   -- unknown, not_ready, make_ready, ready_show, ready_lease
  marketing_state    LowCardinality(String),   -- unlisted, listed, application_pending, leased
  active_lease_id    Nullable(UUID),
  active_listing_id  Nullable(UUID),
  days_vacant        Nullable(Int32),
  asking_rent        Nullable(Decimal(12,2)),
  effective_rent     Nullable(Decimal(12,2)),
  concession_value   Nullable(Decimal(12,2)),
  condition_score    Nullable(Decimal(5,2)),
  contradiction_flags String DEFAULT '[]',
  evidence_coverage  String DEFAULT '{}'
) ENGINE = MergeTree()
ORDER BY (property_id, unit_id, day_date);
```

#### `fact_lease_interval`

Denormalized lease interval facts for analytical queries.

```sql
-- ClickHouse
CREATE TABLE fact_lease_interval (
  property_id        UUID,
  unit_id            UUID,
  lease_id           UUID,
  interval_start     Date,
  interval_end       Nullable(Date),
  monthly_rent       Nullable(Decimal(12,2)),
  effective_rent     Nullable(Decimal(12,2)),
  concession_value   Nullable(Decimal(12,2)),
  lease_type         LowCardinality(String),
  resident_id        Nullable(UUID),
  bedrooms           Nullable(Decimal(4,1)),
  sqft               Nullable(Int32)
) ENGINE = MergeTree()
ORDER BY (property_id, unit_id, interval_start);
```

#### `fact_vacancy_cycle`

Denormalized vacancy cycle facts.

```sql
-- ClickHouse
CREATE TABLE fact_vacancy_cycle (
  property_id        UUID,
  unit_id            UUID,
  cycle_id           UUID,
  vacancy_start      Date,
  vacancy_end        Nullable(Date),
  days_vacant        Nullable(Int32),
  prior_rent         Nullable(Decimal(12,2)),
  new_rent           Nullable(Decimal(12,2)),
  vacancy_cost       Nullable(Decimal(12,2)),
  make_ready_days    Nullable(Int32),
  make_ready_cost    Nullable(Decimal(12,2))
) ENGINE = MergeTree()
ORDER BY (property_id, unit_id, vacancy_start);
```

#### `fact_work_order`

Work order facts for maintenance analytics.

```sql
-- ClickHouse
CREATE TABLE fact_work_order (
  property_id        UUID,
  unit_id            Nullable(UUID),
  work_order_id      UUID,
  category           LowCardinality(String),
  is_make_ready      UInt8,
  date_created       Date,
  date_completed     Nullable(Date),
  days_to_complete   Nullable(Int32),
  cost               Nullable(Decimal(12,2)),
  vendor_id          Nullable(UUID)
) ENGINE = MergeTree()
ORDER BY (property_id, date_created);
```

#### `fact_lead_funnel_event`

Lead funnel events for leasing analytics.

```sql
-- ClickHouse
CREATE TABLE fact_lead_funnel_event (
  property_id        UUID,
  lead_id            UUID,
  event_type         LowCardinality(String),
  event_date         Date,
  agent_id           Nullable(UUID),
  lead_source        Nullable(String),
  response_time_min  Nullable(Int32),
  outcome            Nullable(String)
) ENGINE = MergeTree()
ORDER BY (property_id, event_date);
```

#### `fact_listing_observation`

Listing observation facts.

```sql
-- ClickHouse
CREATE TABLE fact_listing_observation (
  property_id        UUID,
  unit_id            Nullable(UUID),
  observation_id     UUID,
  platform           LowCardinality(String),
  observation_date   Date,
  asking_rent        Nullable(Decimal(12,2)),
  photo_quality      Nullable(Decimal(4,1)),
  description_quality Nullable(Decimal(4,1)),
  days_on_market     Nullable(Int32)
) ENGINE = MergeTree()
ORDER BY (property_id, observation_date);
```

#### `fact_marketing_presence_day`

Daily marketing channel presence.

```sql
-- ClickHouse
CREATE TABLE fact_marketing_presence_day (
  property_id        UUID,
  channel_id         UUID,
  day_date           Date,
  is_active          UInt8,
  platform           LowCardinality(String),
  spend_daily        Nullable(Decimal(12,2))
) ENGINE = MergeTree()
ORDER BY (property_id, day_date);
```

#### `fact_comp_listing_observation`

Competitor listing observation facts.

```sql
-- ClickHouse
CREATE TABLE fact_comp_listing_observation (
  competitor_property_id UUID,
  observation_id     UUID,
  observation_date   Date,
  bedrooms           Nullable(Decimal(4,1)),
  sqft               Nullable(Int32),
  asking_rent        Nullable(Decimal(12,2)),
  rent_per_sqft      Nullable(Decimal(8,2)),
  is_available       Nullable(UInt8),
  concession_amount  Nullable(Decimal(12,2))
) ENGINE = MergeTree()
ORDER BY (competitor_property_id, observation_date);
```

#### `fact_score_result`

Score results for fast analytical slicing.

```sql
-- ClickHouse
CREATE TABLE fact_score_result (
  assessment_id      UUID,
  property_id        UUID,
  scorecard_id       UUID,
  scoring_level      LowCardinality(String),
  area_number        Nullable(Int32),
  area_name          Nullable(String),
  item_name          Nullable(String),
  normalized_score   Nullable(Decimal(6,2)),
  weighted_score     Nullable(Decimal(8,4)),
  confidence_score   Nullable(Decimal(5,2)),
  grade_letter       Nullable(String),
  version            String
) ENGINE = MergeTree()
ORDER BY (property_id, assessment_id, area_number);
```

#### `fact_finding_impact`

Finding + impact denormalized for analytical queries.

```sql
-- ClickHouse
CREATE TABLE fact_finding_impact (
  assessment_id      UUID,
  property_id        UUID,
  finding_id         UUID,
  finding_type       LowCardinality(String),
  domain             LowCardinality(String),
  severity           LowCardinality(String),
  impact_model       Nullable(String),
  base_estimate      Nullable(Decimal(14,2)),
  annualized_amount  Nullable(Decimal(14,2)),
  confidence         Nullable(Decimal(5,2))
) ENGINE = MergeTree()
ORDER BY (property_id, assessment_id);
```

### Layer C — Longitudinal Facts (ClickHouse)

> Source: spec_1 §14.2

#### `fact_assessment_score`

Score trajectories across assessments.

```sql
-- ClickHouse
CREATE TABLE fact_assessment_score (
  property_id        UUID,
  assessment_id      UUID,
  assessment_date    Date,
  area_number        Nullable(Int32),
  area_name          Nullable(String),
  overall_score      Nullable(Decimal(6,2)),
  grade_letter       Nullable(String),
  version            String
) ENGINE = MergeTree()
ORDER BY (property_id, assessment_date);
```

#### `fact_assessment_finding`

Finding persistence across assessments.

```sql
-- ClickHouse
CREATE TABLE fact_assessment_finding (
  property_id        UUID,
  assessment_id      UUID,
  assessment_date    Date,
  finding_id         UUID,
  domain             LowCardinality(String),
  severity           LowCardinality(String),
  is_recurring       UInt8,
  prior_finding_id   Nullable(UUID)
) ENGINE = MergeTree()
ORDER BY (property_id, assessment_date);
```

#### `fact_recommendation_status`

Recommendation adoption tracking.

```sql
-- ClickHouse
CREATE TABLE fact_recommendation_status (
  property_id        UUID,
  assessment_id      UUID,
  recommendation_id  UUID,
  domain             LowCardinality(String),
  priority           LowCardinality(String),
  status             LowCardinality(String),
  status_date        Date
) ENGINE = MergeTree()
ORDER BY (property_id, status_date);
```

#### `fact_property_kpi_period`

Period-level KPIs for trend analysis.

```sql
-- ClickHouse
CREATE TABLE fact_property_kpi_period (
  property_id        UUID,
  period_start       Date,
  period_end         Date,
  kpi_name           LowCardinality(String),
  kpi_value          Nullable(Decimal(14,4)),
  kpi_unit           LowCardinality(String)
) ENGINE = MergeTree()
ORDER BY (property_id, period_start, kpi_name);
```

#### `fact_unit_chronicity`

Chronic vacancy / issue tracking per unit.

```sql
-- ClickHouse
CREATE TABLE fact_unit_chronicity (
  property_id        UUID,
  unit_id            UUID,
  assessment_id      UUID,
  chronic_type       LowCardinality(String),  -- chronic_vacancy, recurring_issue, repeat_turnover
  duration_days      Nullable(Int32),
  cycle_count        Nullable(Int32),
  total_cost         Nullable(Decimal(14,2))
) ENGINE = MergeTree()
ORDER BY (property_id, unit_id);
```

---

## Verification Summary

### PostgreSQL Table Count

| Domain | Tables |
|--------|--------|
| Layer A — Raw Evidence | 6 |
| Tenancy & Identity | 3 |
| Asset Hierarchy | 13 |
| Resident & Lease | 10 |
| Operations | 15 |
| Demand (Leasing & CRM) | 9 |
| Listing & Marketing | 13 |
| Market & Competition | 6 |
| Mystery Shop & Field Evidence | 4 |
| Technology Stack | 2 |
| Assessment & Deliverables | 9 |
| Staffing & Programs | 5 |
| Scoring Configuration | 5 |
| Workspace (Studies/Reports) | 10 |
| **PostgreSQL Total** | **110** |

### ClickHouse Table Count

| Category | Tables |
|----------|--------|
| Core Analytical Facts | 10 |
| Longitudinal Facts | 5 |
| **ClickHouse Total** | **15** |

### Cross-Reference to spec_1 Sections

| spec_1 Section | Tables Covering It |
|---|---|
| §3.1 Layer A | source_system, source_ingestion, source_asset, source_record_raw |
| §3.2 Domain 1 (Asset) | client, portfolio, property, building, floor_plan, unit, unit_version, unit_existence_interval, unit_alias |
| §3.2 Domain 2 (Resident/Lease) | resident, lease, lease_interval, lease_charge, lease_event, notice_event, move_event, renewal_offer, payment_event, delinquency_snapshot |
| §3.2 Domain 3 (Operations) | staff_member, vendor, work_order, work_order_line_item, work_order_status_event, make_ready_cycle, vacancy_cycle, unit_condition_observation, field_validation, budget_actual_line |
| §3.2 Domain 4 (Demand) | lead, lead_source, lead_event, communication_event, tour_event, application_event, agent, crm_assignment_interval, conversion_metric_snapshot |
| §3.2 Domain 5 (Market) | competitive_set, competitive_set_member, comp_floorplan, comp_listing_observation, comp_property_observation, comp_marketing_assessment |
| §3.2 Domain 6 (Assessment) | assessment, assessment_data_coverage, analysis_run, scorecard, score_result, finding, impact_estimate, contradiction, recommendation |
| §3.3 Unit Spine | unit, unit_version, unit_existence_interval, unit_alias, calendar_day, fact_unit_day |
| §3.4 Event Facts | lease_event, notice_event, move_event, renewal_offer, payment_event, delinquency_snapshot, work_order, work_order_status_event, make_ready_cycle, lead_event, communication_event, tour_event, application_event, listing_observation, marketing_observation |
| §4.2 Leasing/CRM | lead, lead_source, agent, communication_event, tour_event, application_event, crm_assignment_interval |
| §4.3 Make-ready | make_ready_cycle, work_order, work_order_line_item, vendor, staff_member, unit_condition_observation, field_validation, budget_actual_line |
| §4.4 Listing/Marketing | marketing_channel, campaign, campaign_spend, website_observation, social_observation, listing, listing_observation, listing_asset, marketing_observation |
| §4.5 Competitive | competitive_set, competitive_set_member, comp_floorplan, comp_listing_observation, comp_property_observation, comp_marketing_assessment |
| §4.6 Assessment/Deliverable | assessment, scorecard, score_result, finding, impact_estimate, recommendation, report, report_section, report_render |
| §6 Scoring | score_result, scoring_rubric_version, metric_registry |
| §7 Financial Impact | impact_estimate, impact_model_catalog |
| §8 Contradictions | contradiction |
| §9 Workspace | study, saved_query, result_snapshot, study_item, comparison_board, annotation, evidence_bundle |
| §10 Data Intake | source_system, source_ingestion, source_asset, source_record_raw, mapping_rule, mapping_review_queue |
| §12 Reporting | report, report_section, report_render |
| §14 Longitudinal | fact_assessment_score, fact_assessment_finding, fact_recommendation_status, fact_property_kpi_period, fact_unit_chronicity |

### CDI Section Coverage

| CDI Section | Tables Covering It |
|---|---|
| §0 Assessment Config | assessment |
| §1.1 Rent Roll | lease, lease_interval, unit_version |
| §1.2 Move-In/Out | move_event |
| §1.3 Renewals | renewal_offer |
| §1.4 Work Orders | work_order, work_order_line_item |
| §1.5 Vacancy | unit_existence_interval, vacancy_cycle |
| §1.6 T12 Financial | budget_actual_line |
| §1.7 Lease Charges | lease_charge |
| §1.8 Lease Detail | lease |
| §1.9 Traffic | lead, lead_event |
| §1.10 Expiration | lease (lease_end dates) |
| §1.11 Delinquency | delinquency_snapshot |
| §1.12 Renewal Offers | renewal_offer |
| §2 CRM/Lead | lead, lead_event |
| §3.1–3.2 Property/Amenities | property, property_amenity, unit_amenity |
| §3.3 Market Context | market_context |
| §3.5 Resident Events | resident_event_program |
| §3.7 Website | website_observation |
| §3.8 Reputation | reputation_observation |
| §3.9 Social/Digital | social_observation |
| §3.10 Partnerships | partnership_referral_snapshot |
| §3.11–3.12 Listings | listing_content_assessment, listing_photo_assessment |
| §3.13 Leasing Model | leasing_model_snapshot |
| §3.14–3.18 Tour/Lead Mgmt | tour_event, conversion_metric_snapshot |
| §3.19 Staffing | staffing_snapshot, staff_member |
| §3.20 Maintenance | work_order, property_condition_observation |
| §3.21 Renewal/Retention | renewal_retention_snapshot |
| §3.22 Technology | tech_platform, tech_summary |
| §3.23–3.24 Financials | budget_actual_line |
| §4 Mystery Shop | mystery_shop |
| §5 Competitive | comp_listing_observation, comp_floorplan, competitive_set, competitive_set_member |
| §6 Field Audit | vacant_unit_audit, resident_interview, unit_condition_observation |
| §10 Planned Additions | unit_condition_observation (readiness checklist), back_of_house_observation, capital_asset_observation, fire_safety_observation |

### Audit Workbook Section Coverage

| AWS Section | Tables Covering It |
|---|---|
| §2A Online Reputation | reputation_observation |
| §2B Google Business | google_business_observation |
| §2C Digital/Social | social_observation |
| §2D Website | website_observation |
| §2E Listing Audit | listing_observation, listing_content_assessment, listing_photo_assessment |
| §3A Building Amenities | property_amenity |
| §3B Unit Amenities | unit_amenity |
| §3C Market Context | market_context |
| §3D Resident Events | resident_event_program |
| §3E Resident Services | resident_event_program (services in jsonb) |
| §4 Mystery Shop | mystery_shop |
| §5A–5B Office/Model | assessment (attributes), tour_observation |
| §5C Property Condition | property_condition_observation |
| §5D Capital Asset | capital_asset_observation |
| §5E Deferred Maintenance | deferred_maintenance_item |
| §5F Fire/Safety | fire_safety_observation |
| §5G Unit Walks | unit_condition_observation |
| §5H Back-of-House | back_of_house_observation |
| §6A–6G Field Templates | vacant_unit_audit, resident_interview |
| §7 Management Interview | staffing_snapshot, leasing_model_snapshot, renewal_retention_snapshot |
| §8 Tour Observation | tour_observation |
| §9 Financial Data | budget_actual_line |
| §10 Competitive Set | competitive_set, competitive_set_member, comp_listing_observation, comp_marketing_assessment |
| §11 Technology | tech_platform, tech_summary |

---

## Row-Level Security (RLS) Policies

All tenant-scoped PostgreSQL tables must have RLS enabled and enforced. RLS provides defense-in-depth at the database layer: even if application code has a bug, one tenant's data cannot leak to another.

Source: `spec_1` §16.1 — "row-level access at the transactional layer"; `phase-0-foundations.mdc` — `SET app.current_tenant_id`.

### Mechanism

The auth middleware sets a PostgreSQL session variable on every request:

```sql
SET app.current_tenant_id = '<tenant_uuid>';
```

RLS policies reference this variable to filter rows automatically.

### Strategy

**Direct tenant tables** (7 tables with `tenant_id` column): Simple equality policy on `tenant_id`.

**Indirect tenant tables** (97 tables in PostgreSQL reachable via FK chains): These tables do not have their own `tenant_id` column. Two strategies exist:

1. **Join-based policies** — RLS WHERE clause joins to a parent table. PostgreSQL supports this but it can be expensive for deep chains.
2. **Denormalized `tenant_id`** — Add `tenant_id` to every tenant-scoped table at the DDL level. This is the recommended approach for performance.

**Recommended approach:** Denormalize `tenant_id` onto all tenant-scoped tables. This is a schema change that should be applied during Phase 0 migrations.

**Non-tenant tables** (global reference data, not RLS-enabled):
- `tenant` (the tenant table itself)
- `benchmark_version` — system-wide scoring benchmark versions
- `scoring_rubric_version` — system-wide rubric versions
- `metric_registry` — system-wide metric definitions
- `impact_model_catalog` — system-wide impact models
- `calendar_day` — utility calendar table
- `diagnostic_package` — system-wide diagnostic templates

**ClickHouse fact tables** (15 tables): Not RLS-enabled. ClickHouse does not support PostgreSQL RLS. Application-layer filtering via `enforce_row_filter` (see `Authorization_Model_Specification.md` §8) provides tenant isolation for analytical queries. All 15 fact tables have an `assessment_id` column that resolves to a tenant through the assessment→property→tenant chain; the application layer must filter explicitly.

### Policy Definitions — Direct Tenant Tables

Applied to the 7 tables with a `tenant_id` column: `source_system`, `user_account`, `audit_log`, `client`, `property`, `vendor`, `assessment`.

```sql
-- Template: repeat for each direct-tenant table
ALTER TABLE {table_name} ENABLE ROW LEVEL SECURITY;
ALTER TABLE {table_name} FORCE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON {table_name}
  USING (tenant_id = current_setting('app.current_tenant_id')::uuid);
```

Expanded for all 7:

```sql
-- source_system
ALTER TABLE source_system ENABLE ROW LEVEL SECURITY;
ALTER TABLE source_system FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON source_system
  USING (tenant_id = current_setting('app.current_tenant_id')::uuid);

-- user_account
ALTER TABLE user_account ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_account FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON user_account
  USING (tenant_id = current_setting('app.current_tenant_id')::uuid);

-- audit_log
ALTER TABLE audit_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_log FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON audit_log
  USING (tenant_id = current_setting('app.current_tenant_id')::uuid);

-- client
ALTER TABLE client ENABLE ROW LEVEL SECURITY;
ALTER TABLE client FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON client
  USING (tenant_id = current_setting('app.current_tenant_id')::uuid);

-- property
ALTER TABLE property ENABLE ROW LEVEL SECURITY;
ALTER TABLE property FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON property
  USING (tenant_id = current_setting('app.current_tenant_id')::uuid);

-- vendor
ALTER TABLE vendor ENABLE ROW LEVEL SECURITY;
ALTER TABLE vendor FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON vendor
  USING (tenant_id = current_setting('app.current_tenant_id')::uuid);

-- assessment
ALTER TABLE assessment ENABLE ROW LEVEL SECURITY;
ALTER TABLE assessment FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON assessment
  USING (tenant_id = current_setting('app.current_tenant_id')::uuid);
```

### Policy Definitions — Indirect Tenant Tables (After Denormalization)

Once `tenant_id` is denormalized onto all tenant-scoped tables, the same policy template applies:

```sql
ALTER TABLE {table_name} ENABLE ROW LEVEL SECURITY;
ALTER TABLE {table_name} FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON {table_name}
  USING (tenant_id = current_setting('app.current_tenant_id')::uuid);
```

### Indirect Tenant Tables Requiring `tenant_id` Denormalization

The following 97 tables (in PostgreSQL) are tenant-scoped through FK chains but do not currently have a `tenant_id` column. Each needs `tenant_id uuid not null` added, populated from the nearest parent with `tenant_id`, and an RLS policy applied:

**Via property (property_id → property.tenant_id):**
building, unit, unit_alias, unit_version, unit_amenity, unit_existence_interval, floor_plan, property_amenity, portfolio, competitive_set, market_context

**Via assessment (assessment_id → assessment.tenant_id):**
assessment_data_coverage, score_result, scorecard, finding, recommendation, contradiction, impact_estimate, evidence_bundle, result_snapshot, report, comparison_board, study, analysis_run, annotation, saved_query, source_ingestion, mapping_rule, mapping_review_queue, field_validation

**Via unit (unit_id → unit → property → tenant):**
vacancy_cycle, lease, move_event

**Via lease (lease_id → lease → unit → property → tenant):**
lease_interval, lease_charge, lease_event, notice_event, payment_event, renewal_offer, delinquency_snapshot

**Via source_ingestion (source_ingestion_id → source_ingestion → assessment → tenant):**
source_asset, source_record_raw

**Via assessment (deeper chains through assessment-scoped tables):**
resident, lead, lead_event, lead_source, campaign, campaign_spend, marketing_channel, marketing_observation, application_event, tour_event, tour_observation, mystery_shop, conversion_metric_snapshot, leasing_model_snapshot, staffing_snapshot, staff_member, renewal_retention_snapshot, resident_interview, resident_event_program, budget_actual_line, work_order, work_order_line_item, work_order_status_event, make_ready_cycle, listing, listing_observation, listing_asset, listing_content_assessment, listing_photo_assessment, reputation_observation, social_observation, google_business_observation, website_observation, partnership_referral_snapshot, fire_safety_observation, property_condition_observation, capital_asset_observation, deferred_maintenance_item, unit_condition_observation, back_of_house_observation, vacant_unit_audit, tech_platform, tech_summary, competitive_set_member, comp_property_observation, comp_listing_observation, comp_marketing_assessment, comp_floorplan, agent, crm_assignment_interval, communication_event, report_render, report_section, study_item, diagnostic_package

### Service Account Bypass

Service accounts (migrations, background tasks, system operations) must bypass RLS. Two approaches:

1. **BYPASSRLS role:** Create a PostgreSQL role with `BYPASSRLS` privilege for service connections.
2. **Separate connection pool:** Service accounts use a connection pool authenticated as the superuser or a BYPASSRLS role, separate from the application pool.

The application connection pool uses a role WITHOUT `BYPASSRLS`, ensuring RLS is always enforced for user-facing requests.

### Implementation Notes

1. `FORCE ROW LEVEL SECURITY` ensures RLS applies even to the table owner. Without FORCE, the table owner bypasses RLS.
2. The session variable `app.current_tenant_id` must be set BEFORE any query. If not set, the policy will fail (comparison against NULL), blocking all access. This is a safe default.
3. The `tenant_id` denormalization migration should be run as a Phase 0 task, populating `tenant_id` from parent FKs in a single migration.
4. After denormalization, add `NOT NULL` and a foreign key constraint: `REFERENCES tenant(tenant_id)`.
5. Add an index on `(tenant_id)` for every table that gets the denormalized column, to support RLS filter performance.
