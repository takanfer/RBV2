# Database Schema Specification

Source documents: `spec_1_multifamily_property_assessment_platform.md`

**Conventions:** lowercase snake_case for all identifiers.

---

## PostgreSQL Schema

### Layer A — Raw Evidence Store

#### `source_asset`

```sql
create table source_asset (
    source_asset_id  uuid primary key default gen_random_uuid(),
    tenant_id        uuid not null,
    file_name        text not null,
    mime_type        text,
    created_at       timestamptz not null default now(),
    updated_at       timestamptz not null default now()
);
```

### Layer B — Canonical Operational Model

#### Domain 1: Tenancy

##### `property`

```sql
create table property (
    property_id   uuid primary key default gen_random_uuid(),
    tenant_id     uuid not null,
    name          text not null,
    address       text,
    unit_count    integer,
    valid_from    timestamptz not null default now(),
    valid_to      timestamptz not null default 'infinity',
    created_at    timestamptz not null default now(),
    updated_at    timestamptz not null default now()
);
```

##### `user_account`

```sql
create table user_account (
    user_account_id  uuid primary key default gen_random_uuid(),
    tenant_id        uuid not null,
    email            text not null,
    role             text not null,  -- admin, consultant, analyst, client_viewer, client_user, viewer
    created_at       timestamptz not null default now(),
    updated_at       timestamptz not null default now()
);
```

### Layer C — Analytical Facts (ClickHouse)

#### `fact_unit_day`

```sql
CREATE TABLE fact_unit_day (
    property_id      String,
    unit_id          String,
    day              Date,
    status           LowCardinality(String),
    rent             Nullable(Float64)
) ENGINE = MergeTree()
ORDER BY (property_id, unit_id, day);
```

### Layer C — Longitudinal Facts (ClickHouse)

#### `fact_score_snapshot`

```sql
CREATE TABLE fact_score_snapshot (
    property_id      String,
    snapshot_date    Date,
    area_id          UInt8,
    score            Float64
) ENGINE = MergeTree()
ORDER BY (property_id, snapshot_date, area_id);
```

## Verification Summary

### PostgreSQL Table Count

| Domain | Tables |
|--------|--------|
| Raw Evidence | 1 |
| Tenancy | 2 |
| **Total** | **3** |

### ClickHouse Table Count

| Group | Tables |
|-------|--------|
| Analytical Facts | 2 |
| **Total** | **2** |

### Cross-Reference to spec_1 Sections

| Table | spec_1 Section |
|-------|---------------|
| source_asset | §1.1 |
| property | §1.2 |
| user_account | §1.2 |
