# Shared Type Definitions

Pydantic v2 models generated from the DDL in `Database_Schema_Specification.md`.
These models live in `src/shared/models/` and are the canonical Python representation
of every database entity.

**Do not edit generated model files by hand.** Re-run `codegen/generate_models.py`
against the DDL to regenerate after schema changes.

---

**Total models:** 125
**Total fields:** 1394

## raw_evidence

Module: `src/shared/models/raw_evidence.py`

### `SourceSystem`

Table: `source_system` (11 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `source_system_id` | `UUID` | No | `uuid` |
| `tenant_id` | `UUID` | No | `uuid` |
| `system_name` | `str` | No | `text` |
| `system_type` | `str` | No | `text` |
| `vendor_name` | `str` | Yes | `text` |
| `api_base_url` | `str` | Yes | `text` |
| `adapter_type` | `str` | No | `text` |
| `configuration` | `dict[str, Any]` | No | `jsonb` |
| `is_active` | `bool` | No | `boolean` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |
| `updated_at` | `datetime.datetime` | No | `timestamptz` |

### `SourceIngestion`

Table: `source_ingestion` (13 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `ingestion_id` | `UUID` | No | `uuid` |
| `source_system_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | Yes | `uuid` |
| `ingestion_type` | `str` | No | `text` |
| `status` | `str` | No | `text` |
| `file_count` | `int` | No | `int` |
| `record_count` | `int` | Yes | `int` |
| `idempotency_key` | `str` | Yes | `text` |
| `started_at` | `datetime.datetime` | Yes | `timestamptz` |
| `completed_at` | `datetime.datetime` | Yes | `timestamptz` |
| `error_detail` | `dict[str, Any]` | Yes | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |
| `created_by` | `UUID` | Yes | `uuid` |

### `SourceAsset`

Table: `source_asset` (10 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `asset_id` | `UUID` | No | `uuid` |
| `ingestion_id` | `UUID` | No | `uuid` |
| `asset_type` | `str` | No | `text` |
| `original_filename` | `str` | Yes | `text` |
| `mime_type` | `str` | Yes | `text` |
| `file_size_bytes` | `int` | Yes | `bigint` |
| `content_hash` | `str` | No | `text` |
| `storage_path` | `str` | No | `text` |
| `metadata` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `SourceRecordRaw`

Table: `source_record_raw` (11 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `record_id` | `UUID` | No | `uuid` |
| `asset_id` | `UUID` | No | `uuid` |
| `ingestion_id` | `UUID` | No | `uuid` |
| `record_type` | `str` | No | `text` |
| `source_row_number` | `int` | Yes | `int` |
| `raw_data` | `dict[str, Any]` | No | `jsonb` |
| `mapping_status` | `str` | No | `text` |
| `mapping_confidence` | `Decimal` | Yes | `decimal(5, 4)` |
| `canonical_entity` | `str` | Yes | `text` |
| `canonical_id` | `UUID` | Yes | `uuid` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `MappingRule`

Table: `mapping_rule` (10 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `rule_id` | `UUID` | No | `uuid` |
| `source_system_id` | `UUID` | No | `uuid` |
| `source_record_type` | `str` | No | `text` |
| `source_column` | `str` | No | `text` |
| `target_table` | `str` | No | `text` |
| `target_column` | `str` | No | `text` |
| `transform_expr` | `str` | Yes | `text` |
| `is_active` | `bool` | No | `boolean` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |
| `created_by` | `UUID` | Yes | `uuid` |

### `MappingReviewQueue`

Table: `mapping_review_queue` (10 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `review_id` | `UUID` | No | `uuid` |
| `ingestion_id` | `UUID` | No | `uuid` |
| `record_id` | `UUID` | Yes | `uuid` |
| `review_type` | `str` | No | `text` |
| `description` | `str` | No | `text` |
| `suggested_mapping` | `dict[str, Any]` | Yes | `jsonb` |
| `resolution` | `str` | Yes | `text` |
| `resolved_by` | `UUID` | Yes | `uuid` |
| `resolved_at` | `datetime.datetime` | Yes | `timestamptz` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

---

## infrastructure

Module: `src/shared/models/infrastructure.py`

### `Tenant`

Table: `tenant` (7 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `tenant_id` | `UUID` | No | `uuid` |
| `org_name` | `str` | No | `text` |
| `slug` | `str` | No | `text` |
| `settings` | `dict[str, Any]` | No | `jsonb` |
| `is_active` | `bool` | No | `boolean` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |
| `updated_at` | `datetime.datetime` | No | `timestamptz` |

### `UserAccount`

Table: `user_account` (9 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `user_id` | `UUID` | No | `uuid` |
| `tenant_id` | `UUID` | No | `uuid` |
| `email` | `str` | No | `text` |
| `display_name` | `str` | No | `text` |
| `role` | `str` | No | `text` |
| `auth_provider_id` | `str` | Yes | `text` |
| `is_active` | `bool` | No | `boolean` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |
| `updated_at` | `datetime.datetime` | No | `timestamptz` |

### `AuditLog`

Table: `audit_log` (10 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `log_id` | `UUID` | No | `uuid` |
| `tenant_id` | `UUID` | No | `uuid` |
| `user_id` | `UUID` | Yes | `uuid` |
| `action` | `str` | No | `text` |
| `entity_type` | `str` | No | `text` |
| `entity_id` | `UUID` | No | `uuid` |
| `before_value` | `dict[str, Any]` | Yes | `jsonb` |
| `after_value` | `dict[str, Any]` | Yes | `jsonb` |
| `reason` | `str` | Yes | `text` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `Client`

Table: `client` (10 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `client_id` | `UUID` | No | `uuid` |
| `tenant_id` | `UUID` | No | `uuid` |
| `client_name` | `str` | No | `text` |
| `contact_name` | `str` | Yes | `text` |
| `contact_phone` | `str` | Yes | `text` |
| `contact_email` | `str` | Yes | `text` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `is_active` | `bool` | No | `boolean` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |
| `updated_at` | `datetime.datetime` | No | `timestamptz` |

### `Portfolio`

Table: `portfolio` (5 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `portfolio_id` | `UUID` | No | `uuid` |
| `client_id` | `UUID` | No | `uuid` |
| `portfolio_name` | `str` | No | `text` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

---

## asset

Module: `src/shared/models/asset.py`

### `Property`

Table: `property` (25 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `property_id` | `UUID` | No | `uuid` |
| `tenant_id` | `UUID` | No | `uuid` |
| `client_id` | `UUID` | Yes | `uuid` |
| `portfolio_id` | `UUID` | Yes | `uuid` |
| `property_name` | `str` | No | `text` |
| `street_address` | `str` | No | `text` |
| `city` | `str` | No | `text` |
| `state` | `str` | No | `text` |
| `zip_code` | `str` | No | `text` |
| `total_units` | `int` | Yes | `int` |
| `year_built` | `int` | Yes | `int` |
| `property_class` | `str` | Yes | `text` |
| `building_type` | `str` | Yes | `text` |
| `buildings_count` | `int` | Yes | `int` |
| `stories` | `int` | Yes | `int` |
| `total_sqft` | `int` | Yes | `int` |
| `lot_size` | `str` | Yes | `text` |
| `parking_spaces` | `int` | Yes | `int` |
| `parking_type` | `str` | Yes | `text` |
| `is_subject` | `bool` | No | `boolean` |
| `latitude` | `Decimal` | Yes | `decimal(10, 7)` |
| `longitude` | `Decimal` | Yes | `decimal(10, 7)` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |
| `updated_at` | `datetime.datetime` | No | `timestamptz` |

### `Building`

Table: `building` (10 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `building_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `parent_building_id` | `UUID` | Yes | `uuid` |
| `building_label` | `str` | No | `text` |
| `building_type` | `str` | Yes | `text` |
| `stories` | `int` | Yes | `int` |
| `unit_count` | `int` | Yes | `int` |
| `has_elevator` | `bool` | Yes | `boolean` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `FloorPlan`

Table: `floor_plan` (10 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `floor_plan_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `plan_code` | `str` | No | `text` |
| `plan_name` | `str` | Yes | `text` |
| `bedrooms` | `Decimal` | No | `decimal(4, 1)` |
| `bathrooms` | `Decimal` | No | `decimal(4, 1)` |
| `sqft` | `int` | Yes | `int` |
| `base_market_rent` | `Decimal` | Yes | `decimal(12, 2)` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `Unit`

Table: `unit` (5 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `unit_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `unit_natural_key` | `str` | No | `text` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |
| `retired_at` | `datetime.datetime` | Yes | `timestamptz` |

### `UnitVersion`

Table: `unit_version` (16 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `unit_version_id` | `UUID` | No | `uuid` |
| `unit_id` | `UUID` | No | `uuid` |
| `valid_from` | `datetime.date` | No | `date` |
| `valid_to` | `datetime.date` | Yes | `date` |
| `building_id` | `UUID` | Yes | `uuid` |
| `floor_plan_id` | `UUID` | Yes | `uuid` |
| `floor_label` | `str` | Yes | `text` |
| `unit_label` | `str` | No | `text` |
| `floorplan_code` | `str` | Yes | `text` |
| `bedrooms` | `Decimal` | Yes | `decimal(4, 1)` |
| `bathrooms` | `Decimal` | Yes | `decimal(4, 1)` |
| `sqft` | `int` | Yes | `int` |
| `finish_package` | `str` | Yes | `text` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `recorded_from` | `datetime.datetime` | No | `timestamptz` |
| `recorded_to` | `datetime.datetime` | Yes | `timestamptz` |

### `UnitExistenceInterval`

Table: `unit_existence_interval` (9 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `interval_id` | `UUID` | No | `uuid` |
| `unit_id` | `UUID` | No | `uuid` |
| `valid_from` | `datetime.date` | No | `date` |
| `valid_to` | `datetime.date` | Yes | `date` |
| `existence_status` | `str` | No | `text` |
| `rentable_flag` | `bool` | No | `boolean` |
| `reason_code` | `str` | Yes | `text` |
| `recorded_from` | `datetime.datetime` | No | `timestamptz` |
| `recorded_to` | `datetime.datetime` | Yes | `timestamptz` |

### `UnitAlias`

Table: `unit_alias` (11 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `alias_id` | `UUID` | No | `uuid` |
| `unit_id` | `UUID` | No | `uuid` |
| `source_system_id` | `UUID` | Yes | `uuid` |
| `alias_key` | `str` | No | `text` |
| `alias_type` | `str` | No | `text` |
| `valid_from` | `datetime.date` | Yes | `date` |
| `valid_to` | `datetime.date` | Yes | `date` |
| `match_method` | `str` | Yes | `text` |
| `match_confidence` | `Decimal` | Yes | `decimal(5, 4)` |
| `reviewer_override` | `bool` | No | `boolean` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `CalendarDay`

Table: `calendar_day` (10 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `day_date` | `datetime.date` | No | `date` |
| `day_of_week` | `int` | No | `smallint` |
| `day_of_month` | `int` | No | `smallint` |
| `day_of_year` | `int` | No | `smallint` |
| `week_of_year` | `int` | No | `smallint` |
| `month` | `int` | No | `smallint` |
| `quarter` | `int` | No | `smallint` |
| `year` | `int` | No | `smallint` |
| `is_weekend` | `bool` | No | `boolean` |
| `is_month_end` | `bool` | No | `boolean` |

### `PropertyAmenity`

Table: `property_amenity` (9 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `amenity_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | Yes | `uuid` |
| `amenity_category` | `str` | No | `text` |
| `amenity_name` | `str` | No | `text` |
| `is_present` | `bool` | Yes | `boolean` |
| `source` | `str` | Yes | `text` |
| `verification` | `str` | Yes | `text` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `UnitAmenity`

Table: `unit_amenity` (9 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `amenity_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | Yes | `uuid` |
| `amenity_category` | `str` | No | `text` |
| `amenity_name` | `str` | No | `text` |
| `is_present` | `bool` | Yes | `boolean` |
| `source` | `str` | Yes | `text` |
| `verification` | `str` | Yes | `text` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `MarketContext`

Table: `market_context` (13 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `context_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | Yes | `uuid` |
| `submarket_name` | `str` | Yes | `text` |
| `submarket_vacancy_pct` | `Decimal` | Yes | `decimal(6, 3)` |
| `submarket_avg_rent_psf` | `Decimal` | Yes | `decimal(10, 2)` |
| `yoy_rent_growth_pct` | `Decimal` | Yes | `decimal(6, 3)` |
| `new_supply_units` | `int` | Yes | `int` |
| `employment_growth_pct` | `Decimal` | Yes | `decimal(6, 3)` |
| `population_growth_pct` | `Decimal` | Yes | `decimal(6, 3)` |
| `median_household_income` | `Decimal` | Yes | `decimal(12, 2)` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

---

## lease

Module: `src/shared/models/lease.py`

### `Resident`

Table: `resident` (10 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `resident_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `resident_name` | `str` | Yes | `text` |
| `household_id` | `UUID` | Yes | `uuid` |
| `contact_email` | `str` | Yes | `text` |
| `contact_phone` | `str` | Yes | `text` |
| `source_system_id` | `UUID` | Yes | `uuid` |
| `source_key` | `str` | Yes | `text` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `Lease`

Table: `lease` (28 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `lease_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `unit_id` | `UUID` | No | `uuid` |
| `resident_id` | `UUID` | Yes | `uuid` |
| `lease_type` | `str` | Yes | `text` |
| `lease_start` | `datetime.date` | No | `date` |
| `lease_end` | `datetime.date` | Yes | `date` |
| `lease_term_months` | `int` | Yes | `int` |
| `execution_date` | `datetime.date` | Yes | `date` |
| `monthly_rent` | `Decimal` | Yes | `decimal(12, 2)` |
| `market_rent` | `Decimal` | Yes | `decimal(12, 2)` |
| `security_deposit` | `Decimal` | Yes | `decimal(12, 2)` |
| `concession_type` | `str` | Yes | `text` |
| `concession_monthly` | `Decimal` | Yes | `decimal(12, 2)` |
| `concession_start` | `datetime.date` | Yes | `date` |
| `concession_end` | `datetime.date` | Yes | `date` |
| `leasing_agent` | `str` | Yes | `text` |
| `move_in_date` | `datetime.date` | Yes | `date` |
| `notice_date` | `datetime.date` | Yes | `date` |
| `expected_move_out` | `datetime.date` | Yes | `date` |
| `actual_move_out` | `datetime.date` | Yes | `date` |
| `move_out_reason` | `str` | Yes | `text` |
| `occupancy_status` | `str` | Yes | `text` |
| `source_ingestion_id` | `UUID` | Yes | `uuid` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `recorded_from` | `datetime.datetime` | No | `timestamptz` |
| `recorded_to` | `datetime.datetime` | Yes | `timestamptz` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `LeaseInterval`

Table: `lease_interval` (11 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `interval_id` | `UUID` | No | `uuid` |
| `lease_id` | `UUID` | No | `uuid` |
| `unit_id` | `UUID` | No | `uuid` |
| `valid_from` | `datetime.date` | No | `date` |
| `valid_to` | `datetime.date` | Yes | `date` |
| `monthly_rent` | `Decimal` | Yes | `decimal(12, 2)` |
| `effective_rent` | `Decimal` | Yes | `decimal(12, 2)` |
| `concession_value` | `Decimal` | Yes | `decimal(12, 2)` |
| `interval_status` | `str` | No | `text` |
| `recorded_from` | `datetime.datetime` | No | `timestamptz` |
| `recorded_to` | `datetime.datetime` | Yes | `timestamptz` |

### `LeaseCharge`

Table: `lease_charge` (9 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `charge_id` | `UUID` | No | `uuid` |
| `lease_id` | `UUID` | No | `uuid` |
| `unit_id` | `UUID` | No | `uuid` |
| `charge_code` | `str` | No | `text` |
| `charge_description` | `str` | Yes | `text` |
| `monthly_amount` | `Decimal` | No | `decimal(12, 2)` |
| `effective_from` | `datetime.date` | Yes | `date` |
| `effective_to` | `datetime.date` | Yes | `date` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `LeaseEvent`

Table: `lease_event` (6 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `event_id` | `UUID` | No | `uuid` |
| `lease_id` | `UUID` | No | `uuid` |
| `event_type` | `str` | No | `text` |
| `event_date` | `datetime.date` | No | `date` |
| `details` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `NoticeEvent`

Table: `notice_event` (8 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `event_id` | `UUID` | No | `uuid` |
| `lease_id` | `UUID` | No | `uuid` |
| `unit_id` | `UUID` | No | `uuid` |
| `notice_date` | `datetime.date` | No | `date` |
| `expected_move_out` | `datetime.date` | Yes | `date` |
| `notice_type` | `str` | Yes | `text` |
| `reason` | `str` | Yes | `text` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `MoveEvent`

Table: `move_event` (11 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `event_id` | `UUID` | No | `uuid` |
| `lease_id` | `UUID` | Yes | `uuid` |
| `unit_id` | `UUID` | No | `uuid` |
| `resident_id` | `UUID` | Yes | `uuid` |
| `event_type` | `str` | No | `text` |
| `event_date` | `datetime.date` | No | `date` |
| `rent_amount` | `Decimal` | Yes | `decimal(12, 2)` |
| `reason` | `str` | Yes | `text` |
| `source_ingestion_id` | `UUID` | Yes | `uuid` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `RenewalOffer`

Table: `renewal_offer` (16 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `offer_id` | `UUID` | No | `uuid` |
| `lease_id` | `UUID` | No | `uuid` |
| `unit_id` | `UUID` | No | `uuid` |
| `resident_id` | `UUID` | Yes | `uuid` |
| `offer_date` | `datetime.date` | No | `date` |
| `current_rent` | `Decimal` | Yes | `decimal(12, 2)` |
| `offered_rent` | `Decimal` | Yes | `decimal(12, 2)` |
| `offered_term` | `str` | Yes | `text` |
| `outcome` | `str` | Yes | `text` |
| `accepted_date` | `datetime.date` | Yes | `date` |
| `incentive_offered` | `str` | Yes | `text` |
| `incentive_value` | `Decimal` | Yes | `decimal(12, 2)` |
| `competitor_offer` | `Decimal` | Yes | `decimal(12, 2)` |
| `resident_sentiment` | `str` | Yes | `text` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `PaymentEvent`

Table: `payment_event` (8 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `event_id` | `UUID` | No | `uuid` |
| `lease_id` | `UUID` | No | `uuid` |
| `unit_id` | `UUID` | No | `uuid` |
| `payment_date` | `datetime.date` | No | `date` |
| `amount` | `Decimal` | No | `decimal(12, 2)` |
| `payment_type` | `str` | No | `text` |
| `payment_method` | `str` | Yes | `text` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `DelinquencySnapshot`

Table: `delinquency_snapshot` (14 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `snapshot_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `unit_id` | `UUID` | No | `uuid` |
| `resident_id` | `UUID` | Yes | `uuid` |
| `snapshot_date` | `datetime.date` | No | `date` |
| `current_balance` | `Decimal` | Yes | `decimal(12, 2)` |
| `bucket_0_30` | `Decimal` | Yes | `decimal(12, 2)` |
| `bucket_31_60` | `Decimal` | Yes | `decimal(12, 2)` |
| `bucket_61_90` | `Decimal` | Yes | `decimal(12, 2)` |
| `bucket_90_plus` | `Decimal` | Yes | `decimal(12, 2)` |
| `last_payment_date` | `datetime.date` | Yes | `date` |
| `collections_status` | `str` | Yes | `text` |
| `eviction_filed` | `bool` | Yes | `boolean` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

---

## operations

Module: `src/shared/models/operations.py`

### `StaffMember`

Table: `staff_member` (9 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `staff_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `staff_name` | `str` | No | `text` |
| `role` | `str` | Yes | `text` |
| `tenure_months` | `int` | Yes | `int` |
| `certifications` | `str` | Yes | `text` |
| `is_active` | `bool` | No | `boolean` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `Vendor`

Table: `vendor` (7 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `vendor_id` | `UUID` | No | `uuid` |
| `tenant_id` | `UUID` | No | `uuid` |
| `vendor_name` | `str` | No | `text` |
| `vendor_type` | `str` | Yes | `text` |
| `contact_info` | `dict[str, Any]` | No | `jsonb` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `WorkOrder`

Table: `work_order` (18 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `work_order_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `unit_id` | `UUID` | Yes | `uuid` |
| `work_order_number` | `str` | Yes | `text` |
| `category` | `str` | No | `text` |
| `sub_category` | `str` | Yes | `text` |
| `description` | `str` | Yes | `text` |
| `priority` | `str` | Yes | `text` |
| `status` | `str` | No | `text` |
| `assigned_to` | `str` | Yes | `text` |
| `vendor_id` | `UUID` | Yes | `uuid` |
| `cost` | `Decimal` | Yes | `decimal(12, 2)` |
| `date_created` | `datetime.date` | No | `date` |
| `date_completed` | `datetime.date` | Yes | `date` |
| `is_make_ready` | `bool` | No | `boolean` |
| `source_ingestion_id` | `UUID` | Yes | `uuid` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `WorkOrderLineItem`

Table: `work_order_line_item` (6 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `line_item_id` | `UUID` | No | `uuid` |
| `work_order_id` | `UUID` | No | `uuid` |
| `cost_category` | `str` | No | `text` |
| `description` | `str` | Yes | `text` |
| `amount` | `Decimal` | No | `decimal(12, 2)` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `WorkOrderStatusEvent`

Table: `work_order_status_event` (6 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `event_id` | `UUID` | No | `uuid` |
| `work_order_id` | `UUID` | No | `uuid` |
| `status` | `str` | No | `text` |
| `event_date` | `datetime.datetime` | No | `timestamptz` |
| `notes` | `str` | Yes | `text` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `MakeReadyCycle`

Table: `make_ready_cycle` (21 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `cycle_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `unit_id` | `UUID` | No | `uuid` |
| `move_out_date` | `datetime.date` | Yes | `date` |
| `notice_date` | `datetime.date` | Yes | `date` |
| `make_ready_start` | `datetime.date` | Yes | `date` |
| `make_ready_complete` | `datetime.date` | Yes | `date` |
| `ready_observed` | `datetime.date` | Yes | `date` |
| `first_listing_date` | `datetime.date` | Yes | `date` |
| `first_tour_date` | `datetime.date` | Yes | `date` |
| `first_showing_date` | `datetime.date` | Yes | `date` |
| `application_date` | `datetime.date` | Yes | `date` |
| `lease_signed_date` | `datetime.date` | Yes | `date` |
| `move_in_date` | `datetime.date` | Yes | `date` |
| `prior_lease_id` | `UUID` | Yes | `uuid` |
| `new_lease_id` | `UUID` | Yes | `uuid` |
| `total_turn_days` | `int` | Yes | `int` |
| `make_ready_scope` | `str` | Yes | `text` |
| `total_cost` | `Decimal` | Yes | `decimal(12, 2)` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `VacancyCycle`

Table: `vacancy_cycle` (12 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `cycle_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `unit_id` | `UUID` | No | `uuid` |
| `vacancy_start` | `datetime.date` | No | `date` |
| `vacancy_end` | `datetime.date` | Yes | `date` |
| `days_vacant` | `int` | Yes | `int` |
| `prior_rent` | `Decimal` | Yes | `decimal(12, 2)` |
| `new_rent` | `Decimal` | Yes | `decimal(12, 2)` |
| `vacancy_cost` | `Decimal` | Yes | `decimal(12, 2)` |
| `make_ready_cycle_id` | `UUID` | Yes | `uuid` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `UnitConditionObservation`

Table: `unit_condition_observation` (27 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `observation_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | No | `uuid` |
| `unit_id` | `UUID` | No | `uuid` |
| `observation_date` | `datetime.date` | No | `date` |
| `observer_id` | `UUID` | Yes | `uuid` |
| `flooring` | `str` | Yes | `text` |
| `walls_paint` | `str` | Yes | `text` |
| `kitchen_cabinets` | `str` | Yes | `text` |
| `kitchen_appliances` | `str` | Yes | `text` |
| `bathroom_fixtures` | `str` | Yes | `text` |
| `windows_blinds` | `str` | Yes | `text` |
| `doors_hardware` | `str` | Yes | `text` |
| `lighting_fixtures` | `str` | Yes | `text` |
| `hvac_in_unit` | `str` | Yes | `text` |
| `overall_cleanliness` | `str` | Yes | `text` |
| `general_finish` | `str` | Yes | `text` |
| `cleanliness_acceptable` | `bool` | Yes | `boolean` |
| `odor_present` | `bool` | Yes | `boolean` |
| `pest_evidence` | `bool` | Yes | `boolean` |
| `water_damage` | `bool` | Yes | `boolean` |
| `appliances_functional` | `bool` | Yes | `boolean` |
| `windows_blinds_intact` | `bool` | Yes | `boolean` |
| `hvac_operational` | `bool` | Yes | `boolean` |
| `ready_to_show` | `bool` | Yes | `boolean` |
| `condition_notes` | `str` | Yes | `text` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `FieldValidation`

Table: `field_validation` (11 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `validation_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | No | `uuid` |
| `entity_type` | `str` | No | `text` |
| `entity_id` | `UUID` | No | `uuid` |
| `field_name` | `str` | No | `text` |
| `pm_value` | `str` | Yes | `text` |
| `field_value` | `str` | Yes | `text` |
| `is_match` | `bool` | Yes | `boolean` |
| `severity` | `str` | Yes | `text` |
| `notes` | `str` | Yes | `text` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `BudgetActualLine`

Table: `budget_actual_line` (11 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `line_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | Yes | `uuid` |
| `line_category` | `str` | No | `text` |
| `line_item` | `str` | No | `text` |
| `period_month` | `datetime.date` | No | `date` |
| `budget_amount` | `Decimal` | Yes | `decimal(14, 2)` |
| `actual_amount` | `Decimal` | Yes | `decimal(14, 2)` |
| `per_unit_amount` | `Decimal` | Yes | `decimal(12, 2)` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `PropertyConditionObservation`

Table: `property_condition_observation` (12 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `observation_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `observation_date` | `datetime.date` | No | `date` |
| `overall_condition` | `str` | Yes | `text` |
| `common_areas` | `str` | Yes | `text` |
| `exterior_presentation` | `str` | Yes | `text` |
| `amenities_condition` | `str` | Yes | `text` |
| `issues_count` | `int` | Yes | `int` |
| `issues_detail` | `str` | Yes | `text` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `CapitalAssetObservation`

Table: `capital_asset_observation` (12 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `observation_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `system_name` | `str` | No | `text` |
| `system_type` | `str` | Yes | `text` |
| `condition_rating` | `str` | Yes | `text` |
| `install_year` | `int` | Yes | `int` |
| `last_service_date` | `datetime.date` | Yes | `date` |
| `age_years` | `int` | Yes | `int` |
| `observation_notes` | `str` | Yes | `text` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `DeferredMaintenanceItem`

Table: `deferred_maintenance_item` (11 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `item_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `location` | `str` | Yes | `text` |
| `description` | `str` | No | `text` |
| `affected_system` | `str` | Yes | `text` |
| `severity` | `str` | Yes | `text` |
| `estimated_cost` | `Decimal` | Yes | `decimal(12, 2)` |
| `is_safety_hazard` | `bool` | No | `boolean` |
| `photo_asset_id` | `UUID` | Yes | `uuid` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `FireSafetyObservation`

Table: `fire_safety_observation` (15 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `observation_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `fire_inspection_current` | `bool` | Yes | `boolean` |
| `last_fire_inspection` | `datetime.date` | Yes | `date` |
| `open_violations` | `bool` | Yes | `boolean` |
| `violation_count` | `int` | Yes | `int` |
| `violation_details` | `str` | Yes | `text` |
| `no_open_code_violations` | `bool` | Yes | `boolean` |
| `ada_compliance_met` | `bool` | Yes | `boolean` |
| `insurance_current` | `bool` | Yes | `boolean` |
| `reac_nspire_score` | `Decimal` | Yes | `decimal(5, 1)` |
| `elevator_inspection_current` | `bool` | Yes | `boolean` |
| `last_elevator_inspection` | `datetime.date` | Yes | `date` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `BackOfHouseObservation`

Table: `back_of_house_observation` (11 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `observation_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `shop_organized` | `bool` | Yes | `boolean` |
| `parts_inventory_labeled` | `bool` | Yes | `boolean` |
| `safety_equipment_present` | `bool` | Yes | `boolean` |
| `fire_extinguisher_current` | `bool` | Yes | `boolean` |
| `chemical_storage_compliant` | `bool` | Yes | `boolean` |
| `vehicle_cart_condition` | `str` | Yes | `text` |
| `cleanliness` | `str` | Yes | `text` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

---

## demand

Module: `src/shared/models/demand.py`

### `Lead`

Table: `lead` (11 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `lead_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `prospect_id` | `str` | Yes | `text` |
| `lead_created_date` | `datetime.date` | Yes | `date` |
| `lead_source_id` | `UUID` | Yes | `uuid` |
| `agent_id` | `UUID` | Yes | `uuid` |
| `unit_type_interest` | `str` | Yes | `text` |
| `status` | `str` | Yes | `text` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `source_ingestion_id` | `UUID` | Yes | `uuid` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `LeadSource`

Table: `lead_source` (6 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `source_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `source_name` | `str` | No | `text` |
| `source_category` | `str` | Yes | `text` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `LeadEvent`

Table: `lead_event` (11 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `event_id` | `UUID` | No | `uuid` |
| `lead_id` | `UUID` | No | `uuid` |
| `event_type` | `str` | No | `text` |
| `event_date` | `datetime.date` | No | `date` |
| `agent_id` | `UUID` | Yes | `uuid` |
| `response_time_min` | `int` | Yes | `int` |
| `outcome` | `str` | Yes | `text` |
| `reason_lost` | `str` | Yes | `text` |
| `notes` | `str` | Yes | `text` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `CommunicationEvent`

Table: `communication_event` (9 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `event_id` | `UUID` | No | `uuid` |
| `lead_id` | `UUID` | Yes | `uuid` |
| `resident_id` | `UUID` | Yes | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `channel` | `str` | No | `text` |
| `direction` | `str` | No | `text` |
| `event_date` | `datetime.datetime` | No | `timestamptz` |
| `notes` | `str` | Yes | `text` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `TourEvent`

Table: `tour_event` (11 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `event_id` | `UUID` | No | `uuid` |
| `lead_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `agent_id` | `UUID` | Yes | `uuid` |
| `tour_date` | `datetime.date` | No | `date` |
| `tour_type` | `str` | Yes | `text` |
| `outcome` | `str` | Yes | `text` |
| `duration_minutes` | `int` | Yes | `int` |
| `units_shown` | `dict[str, Any]` | Yes | `jsonb` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `ApplicationEvent`

Table: `application_event` (10 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `event_id` | `UUID` | No | `uuid` |
| `lead_id` | `UUID` | Yes | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `unit_id` | `UUID` | Yes | `uuid` |
| `application_date` | `datetime.date` | No | `date` |
| `status` | `str` | No | `text` |
| `screening_score` | `str` | Yes | `text` |
| `decision_date` | `datetime.date` | Yes | `date` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `Agent`

Table: `agent` (7 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `agent_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `agent_name` | `str` | No | `text` |
| `agent_type` | `str` | Yes | `text` |
| `is_active` | `bool` | No | `boolean` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `CrmAssignmentInterval`

Table: `crm_assignment_interval` (6 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `interval_id` | `UUID` | No | `uuid` |
| `lead_id` | `UUID` | No | `uuid` |
| `agent_id` | `UUID` | No | `uuid` |
| `assigned_from` | `datetime.date` | No | `date` |
| `assigned_to` | `datetime.date` | Yes | `date` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `ConversionMetricSnapshot`

Table: `conversion_metric_snapshot` (13 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `snapshot_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | Yes | `uuid` |
| `period_label` | `str` | No | `text` |
| `total_leads` | `int` | Yes | `int` |
| `total_tours` | `int` | Yes | `int` |
| `total_no_shows` | `int` | Yes | `int` |
| `total_applications` | `int` | Yes | `int` |
| `total_leases` | `int` | Yes | `int` |
| `avg_days_lead_tour` | `Decimal` | Yes | `decimal(8, 2)` |
| `avg_days_tour_app` | `Decimal` | Yes | `decimal(8, 2)` |
| `avg_days_app_lease` | `Decimal` | Yes | `decimal(8, 2)` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

---

## marketing

Module: `src/shared/models/marketing.py`

### `MarketingChannel`

Table: `marketing_channel` (7 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `channel_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `channel_name` | `str` | No | `text` |
| `channel_type` | `str` | No | `text` |
| `platform_url` | `str` | Yes | `text` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `Campaign`

Table: `campaign` (9 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `campaign_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `channel_id` | `UUID` | Yes | `uuid` |
| `campaign_name` | `str` | No | `text` |
| `start_date` | `datetime.date` | Yes | `date` |
| `end_date` | `datetime.date` | Yes | `date` |
| `budget` | `Decimal` | Yes | `decimal(12, 2)` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `CampaignSpend`

Table: `campaign_spend` (5 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `spend_id` | `UUID` | No | `uuid` |
| `campaign_id` | `UUID` | No | `uuid` |
| `period_month` | `datetime.date` | No | `date` |
| `amount` | `Decimal` | No | `decimal(12, 2)` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `WebsiteObservation`

Table: `website_observation` (17 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `observation_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | Yes | `uuid` |
| `observation_date` | `datetime.date` | No | `date` |
| `website_url` | `str` | Yes | `text` |
| `website_exists` | `bool` | Yes | `boolean` |
| `mobile_responsive` | `bool` | Yes | `boolean` |
| `live_chat` | `bool` | Yes | `boolean` |
| `contact_form` | `bool` | Yes | `boolean` |
| `floor_plans` | `bool` | Yes | `boolean` |
| `photo_gallery` | `bool` | Yes | `boolean` |
| `unit_availability` | `bool` | Yes | `boolean` |
| `virtual_tours` | `bool` | Yes | `boolean` |
| `online_application` | `bool` | Yes | `boolean` |
| `tour_scheduling` | `bool` | Yes | `boolean` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `SocialObservation`

Table: `social_observation` (10 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `observation_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | Yes | `uuid` |
| `platform` | `str` | No | `text` |
| `profile_url` | `str` | Yes | `text` |
| `is_active` | `bool` | Yes | `boolean` |
| `follower_count` | `int` | Yes | `int` |
| `post_frequency` | `str` | Yes | `text` |
| `observation_date` | `datetime.date` | No | `date` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `ReputationObservation`

Table: `reputation_observation` (11 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `observation_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | Yes | `uuid` |
| `platform` | `str` | No | `text` |
| `platform_url` | `str` | Yes | `text` |
| `profile_exists` | `bool` | Yes | `boolean` |
| `review_score` | `Decimal` | Yes | `decimal(3, 1)` |
| `review_count` | `int` | Yes | `int` |
| `reviews_last_90d` | `int` | Yes | `int` |
| `observation_date` | `datetime.date` | No | `date` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `GoogleBusinessObservation`

Table: `google_business_observation` (7 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `observation_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | Yes | `uuid` |
| `gmb_claimed` | `bool` | Yes | `boolean` |
| `gmb_optimized` | `bool` | Yes | `boolean` |
| `observation_date` | `datetime.date` | No | `date` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `Listing`

Table: `listing` (11 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `listing_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `unit_id` | `UUID` | Yes | `uuid` |
| `floor_plan_id` | `UUID` | Yes | `uuid` |
| `channel_id` | `UUID` | Yes | `uuid` |
| `platform` | `str` | No | `text` |
| `listing_url` | `str` | Yes | `text` |
| `first_listed_date` | `datetime.date` | Yes | `date` |
| `delisted_date` | `datetime.date` | Yes | `date` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `ListingObservation`

Table: `listing_observation` (24 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `observation_id` | `UUID` | No | `uuid` |
| `listing_id` | `UUID` | Yes | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `unit_id` | `UUID` | Yes | `uuid` |
| `assessment_id` | `UUID` | Yes | `uuid` |
| `platform` | `str` | No | `text` |
| `observation_date` | `datetime.date` | No | `date` |
| `asking_rent` | `Decimal` | Yes | `decimal(12, 2)` |
| `concession_displayed` | `bool` | Yes | `boolean` |
| `concession_amount` | `Decimal` | Yes | `decimal(12, 2)` |
| `photo_count` | `int` | Yes | `int` |
| `photo_quality` | `Decimal` | Yes | `decimal(4, 1)` |
| `description_quality` | `Decimal` | Yes | `decimal(4, 1)` |
| `description_word_count` | `int` | Yes | `int` |
| `floor_plan_available` | `bool` | Yes | `boolean` |
| `virtual_tour_available` | `bool` | Yes | `boolean` |
| `amenities_listed` | `bool` | Yes | `boolean` |
| `pricing_accurate` | `bool` | Yes | `boolean` |
| `matches_availability` | `bool` | Yes | `boolean` |
| `contact_info_accurate` | `bool` | Yes | `boolean` |
| `listing_url` | `str` | Yes | `text` |
| `notes` | `str` | Yes | `text` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `ListingPhotoAssessment`

Table: `listing_photo_assessment` (21 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `assessment_photo_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | Yes | `uuid` |
| `hero_image_present` | `bool` | Yes | `boolean` |
| `exterior_shots_count` | `int` | Yes | `int` |
| `living_room_shown` | `bool` | Yes | `boolean` |
| `kitchen_shown` | `bool` | Yes | `boolean` |
| `bedrooms_shown` | `bool` | Yes | `boolean` |
| `bathrooms_shown` | `bool` | Yes | `boolean` |
| `features_shown` | `bool` | Yes | `boolean` |
| `pool_photo` | `bool` | Yes | `boolean` |
| `fitness_photo` | `bool` | Yes | `boolean` |
| `clubhouse_photo` | `bool` | Yes | `boolean` |
| `other_amenity_count` | `int` | Yes | `int` |
| `total_amenities` | `int` | Yes | `int` |
| `amenities_photographed` | `int` | Yes | `int` |
| `lifestyle_photos` | `int` | Yes | `int` |
| `professional_photographer` | `bool` | Yes | `boolean` |
| `last_photo_update` | `datetime.date` | Yes | `date` |
| `shows_actual_units` | `str` | Yes | `text` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `ListingContentAssessment`

Table: `listing_content_assessment` (22 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `content_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | Yes | `uuid` |
| `platform_count` | `int` | Yes | `int` |
| `ils_coverage` | `str` | Yes | `text` |
| `posting_method` | `str` | Yes | `text` |
| `syndication_tool` | `str` | Yes | `text` |
| `update_frequency` | `str` | Yes | `text` |
| `usp_mentioned` | `bool` | Yes | `boolean` |
| `neighborhood_context` | `bool` | Yes | `boolean` |
| `call_to_action` | `bool` | Yes | `boolean` |
| `contact_info_clear` | `bool` | Yes | `boolean` |
| `floor_plans_on_listing` | `bool` | Yes | `boolean` |
| `unit_specs_accurate` | `bool` | Yes | `boolean` |
| `amenities_fully_listed` | `bool` | Yes | `boolean` |
| `pet_policy_stated` | `bool` | Yes | `boolean` |
| `lease_terms_mentioned` | `bool` | Yes | `boolean` |
| `pricing_consistent` | `bool` | Yes | `boolean` |
| `availability_accurate` | `bool` | Yes | `boolean` |
| `photos_match_condition` | `bool` | Yes | `boolean` |
| `specials_updated` | `bool` | Yes | `boolean` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `ListingAsset`

Table: `listing_asset` (7 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `asset_id` | `UUID` | No | `uuid` |
| `listing_id` | `UUID` | No | `uuid` |
| `asset_type` | `str` | No | `text` |
| `storage_path` | `str` | Yes | `text` |
| `quality_score` | `Decimal` | Yes | `decimal(4, 1)` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `MarketingObservation`

Table: `marketing_observation` (7 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `observation_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | Yes | `uuid` |
| `observation_date` | `datetime.date` | No | `date` |
| `observation_type` | `str` | No | `text` |
| `data` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

---

## competitive

Module: `src/shared/models/competitive.py`

### `CompetitiveSet`

Table: `competitive_set` (7 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `comp_set_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | Yes | `uuid` |
| `set_name` | `str` | No | `text` |
| `valid_from` | `datetime.date` | Yes | `date` |
| `valid_to` | `datetime.date` | Yes | `date` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `CompetitiveSetMember`

Table: `competitive_set_member` (5 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `member_id` | `UUID` | No | `uuid` |
| `comp_set_id` | `UUID` | No | `uuid` |
| `competitor_property_id` | `UUID` | No | `uuid` |
| `distance_miles` | `Decimal` | Yes | `decimal(6, 2)` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `CompFloorplan`

Table: `comp_floorplan` (8 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `comp_floorplan_id` | `UUID` | No | `uuid` |
| `competitor_property_id` | `UUID` | No | `uuid` |
| `unit_type` | `str` | Yes | `text` |
| `bedrooms` | `Decimal` | Yes | `decimal(4, 1)` |
| `bathrooms` | `Decimal` | Yes | `decimal(4, 1)` |
| `sqft` | `int` | Yes | `int` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `CompListingObservation`

Table: `comp_listing_observation` (20 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `observation_id` | `UUID` | No | `uuid` |
| `competitor_property_id` | `UUID` | No | `uuid` |
| `comp_floorplan_id` | `UUID` | Yes | `uuid` |
| `assessment_id` | `UUID` | Yes | `uuid` |
| `observation_date` | `datetime.date` | No | `date` |
| `bedrooms` | `Decimal` | Yes | `decimal(4, 1)` |
| `bathrooms` | `Decimal` | Yes | `decimal(4, 1)` |
| `unit_type` | `str` | Yes | `text` |
| `sqft` | `int` | Yes | `int` |
| `asking_rent` | `Decimal` | Yes | `decimal(12, 2)` |
| `rent_per_sqft` | `Decimal` | Yes | `decimal(8, 2)` |
| `floor` | `str` | Yes | `text` |
| `is_available` | `bool` | Yes | `boolean` |
| `private_outdoor` | `bool` | Yes | `boolean` |
| `concession_amount` | `Decimal` | Yes | `decimal(12, 2)` |
| `days_listed` | `int` | Yes | `int` |
| `confidence_score` | `Decimal` | Yes | `decimal(5, 4)` |
| `notes` | `str` | Yes | `text` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `CompPropertyObservation`

Table: `comp_property_observation` (7 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `observation_id` | `UUID` | No | `uuid` |
| `competitor_property_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | Yes | `uuid` |
| `observation_date` | `datetime.date` | No | `date` |
| `occupancy_rate_pct` | `Decimal` | Yes | `decimal(6, 3)` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `CompMarketingAssessment`

Table: `comp_marketing_assessment` (11 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `assessment_score_id` | `UUID` | No | `uuid` |
| `competitor_property_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | Yes | `uuid` |
| `platform_coverage` | `Decimal` | Yes | `decimal(4, 1)` |
| `photo_quality` | `Decimal` | Yes | `decimal(4, 1)` |
| `content_quality` | `Decimal` | Yes | `decimal(4, 1)` |
| `listing_accuracy` | `Decimal` | Yes | `decimal(4, 1)` |
| `website_quality` | `Decimal` | Yes | `decimal(4, 1)` |
| `social_marketing` | `Decimal` | Yes | `decimal(4, 1)` |
| `partnership_referral` | `Decimal` | Yes | `decimal(4, 1)` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

---

## field_evidence

Module: `src/shared/models/field_evidence.py`

### `MysteryShop`

Table: `mystery_shop` (75 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `shop_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | No | `uuid` |
| `shop_date` | `datetime.date` | No | `date` |
| `agent_name` | `str` | Yes | `text` |
| `is_subject` | `bool` | No | `boolean` |
| `phone_friendly_greeting` | `bool` | Yes | `boolean` |
| `phone_answered_timely` | `bool` | Yes | `boolean` |
| `phone_enthusiasm` | `bool` | Yes | `boolean` |
| `phone_described_community` | `bool` | Yes | `boolean` |
| `phone_qualifying_questions` | `bool` | Yes | `boolean` |
| `phone_offered_incentives` | `bool` | Yes | `boolean` |
| `phone_matched_needs` | `bool` | Yes | `boolean` |
| `phone_scheduled_tour` | `bool` | Yes | `boolean` |
| `phone_collected_info` | `bool` | Yes | `boolean` |
| `phone_impression` | `Decimal` | Yes | `decimal(4, 1)` |
| `phone_response_time` | `Decimal` | Yes | `decimal(8, 2)` |
| `phone_response_unit` | `str` | Yes | `text` |
| `email_response_time` | `Decimal` | Yes | `decimal(8, 2)` |
| `email_response_unit` | `str` | Yes | `text` |
| `greeting_prompt` | `bool` | Yes | `boolean` |
| `greeting_eye_contact` | `bool` | Yes | `boolean` |
| `greeting_handshake` | `bool` | Yes | `boolean` |
| `greeting_asked_name` | `bool` | Yes | `boolean` |
| `greeting_rapport` | `bool` | Yes | `boolean` |
| `greeting_refreshments` | `bool` | Yes | `boolean` |
| `greeting_impression` | `Decimal` | Yes | `decimal(4, 1)` |
| `needs_move_timeline` | `bool` | Yes | `boolean` |
| `needs_floor_plan` | `bool` | Yes | `boolean` |
| `needs_budget` | `bool` | Yes | `boolean` |
| `needs_lifestyle` | `bool` | Yes | `boolean` |
| `needs_most_important` | `bool` | Yes | `boolean` |
| `needs_active_listening` | `bool` | Yes | `boolean` |
| `needs_impression` | `Decimal` | Yes | `decimal(4, 1)` |
| `wait_time_minutes` | `Decimal` | Yes | `decimal(6, 1)` |
| `tour_duration_minutes` | `Decimal` | Yes | `decimal(6, 1)` |
| `tour_showed_unit` | `bool` | Yes | `boolean` |
| `tour_highlighted_features` | `bool` | Yes | `boolean` |
| `tour_amenities` | `bool` | Yes | `boolean` |
| `tour_tailored` | `bool` | Yes | `boolean` |
| `tour_product_knowledge` | `bool` | Yes | `boolean` |
| `tour_competitive_knowledge` | `bool` | Yes | `boolean` |
| `tour_submarket_knowledge` | `bool` | Yes | `boolean` |
| `tour_lease_terms` | `bool` | Yes | `boolean` |
| `tour_curb_appeal` | `bool` | Yes | `boolean` |
| `tour_fair_housing` | `bool` | Yes | `boolean` |
| `presentation_impression` | `Decimal` | Yes | `decimal(4, 1)` |
| `close_asked_lease` | `bool` | Yes | `boolean` |
| `close_overcame_objections` | `bool` | Yes | `boolean` |
| `close_next_steps` | `bool` | Yes | `boolean` |
| `close_urgency` | `bool` | Yes | `boolean` |
| `close_pricing_info` | `bool` | Yes | `boolean` |
| `closing_impression` | `Decimal` | Yes | `decimal(4, 1)` |
| `followup_received` | `bool` | Yes | `boolean` |
| `followup_personalized` | `bool` | Yes | `boolean` |
| `followup_referenced_visit` | `bool` | Yes | `boolean` |
| `followup_close_attempt` | `bool` | Yes | `boolean` |
| `followup_impression` | `Decimal` | Yes | `decimal(4, 1)` |
| `followup_timing` | `str` | Yes | `text` |
| `followup_method` | `str` | Yes | `text` |
| `fair_housing_no_discrimination` | `bool` | Yes | `boolean` |
| `fair_housing_consistent` | `bool` | Yes | `boolean` |
| `fair_housing_accommodations` | `bool` | Yes | `boolean` |
| `fair_housing_impression` | `Decimal` | Yes | `decimal(4, 1)` |
| `condition_grounds` | `bool` | Yes | `boolean` |
| `condition_office` | `bool` | Yes | `boolean` |
| `condition_show_unit` | `bool` | Yes | `boolean` |
| `condition_common_areas` | `bool` | Yes | `boolean` |
| `condition_signage` | `bool` | Yes | `boolean` |
| `condition_impression` | `Decimal` | Yes | `decimal(4, 1)` |
| `overall_experience` | `Decimal` | Yes | `decimal(4, 1)` |
| `strengths` | `str` | Yes | `text` |
| `gaps` | `str` | Yes | `text` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `VacantUnitAudit`

Table: `vacant_unit_audit` (23 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `audit_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | No | `uuid` |
| `unit_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `observation_date` | `datetime.date` | No | `date` |
| `marketed` | `bool` | Yes | `boolean` |
| `like_kind_listing_date` | `datetime.date` | Yes | `date` |
| `marketed_date` | `datetime.date` | Yes | `date` |
| `listing_platform` | `str` | Yes | `text` |
| `listing_type` | `str` | Yes | `text` |
| `representative_unit` | `bool` | Yes | `boolean` |
| `last_refresh_date` | `datetime.date` | Yes | `date` |
| `leasing_agent` | `str` | Yes | `text` |
| `tours_scheduled` | `int` | Yes | `int` |
| `tours_completed` | `int` | Yes | `int` |
| `applications_received` | `int` | Yes | `int` |
| `showing_method` | `str` | Yes | `text` |
| `why_still_vacant` | `str` | Yes | `text` |
| `concession_type` | `str` | Yes | `text` |
| `concession_proactive` | `bool` | Yes | `boolean` |
| `notes` | `str` | Yes | `text` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `ResidentInterview`

Table: `resident_interview` (10 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `interview_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | No | `uuid` |
| `unit_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `interview_type` | `str` | No | `text` |
| `interview_date` | `datetime.date` | No | `date` |
| `resident_id` | `UUID` | Yes | `uuid` |
| `data` | `dict[str, Any]` | No | `jsonb` |
| `notes` | `str` | Yes | `text` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `TourObservation`

Table: `tour_observation` (7 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `observation_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `observation_date` | `datetime.date` | No | `date` |
| `data` | `dict[str, Any]` | No | `jsonb` |
| `notes` | `str` | Yes | `text` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

---

## intake_snapshot

Module: `src/shared/models/intake_snapshot.py`

### `TechPlatform`

Table: `tech_platform` (9 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `platform_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | Yes | `uuid` |
| `platform_name` | `str` | No | `text` |
| `annual_cost` | `Decimal` | Yes | `decimal(12, 2)` |
| `staff_mobile_access` | `bool` | Yes | `boolean` |
| `functions_handled` | `dict[str, Any]` | No | `jsonb` |
| `capabilities` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `TechSummary`

Table: `tech_summary` (12 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `summary_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | Yes | `uuid` |
| `total_annual_spend` | `Decimal` | Yes | `decimal(12, 2)` |
| `spend_per_unit` | `Decimal` | Yes | `decimal(12, 2)` |
| `active_integrations` | `int` | Yes | `int` |
| `staff_mobile_access` | `bool` | Yes | `boolean` |
| `resident_app` | `bool` | Yes | `boolean` |
| `automation_level` | `str` | Yes | `text` |
| `redundant_systems` | `str` | Yes | `text` |
| `gaps_pain_points` | `str` | Yes | `text` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `StaffingSnapshot`

Table: `staffing_snapshot` (5 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `snapshot_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | Yes | `uuid` |
| `data` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `LeasingModelSnapshot`

Table: `leasing_model_snapshot` (5 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `snapshot_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | Yes | `uuid` |
| `data` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `ResidentEventProgram`

Table: `resident_event_program` (5 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `program_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | Yes | `uuid` |
| `data` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `RenewalRetentionSnapshot`

Table: `renewal_retention_snapshot` (5 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `snapshot_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | Yes | `uuid` |
| `data` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `PartnershipReferralSnapshot`

Table: `partnership_referral_snapshot` (5 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `snapshot_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | Yes | `uuid` |
| `data` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

---

## assessment

Module: `src/shared/models/assessment.py`

### `Assessment`

Table: `assessment` (14 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `assessment_id` | `UUID` | No | `uuid` |
| `tenant_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `client_id` | `UUID` | Yes | `uuid` |
| `assessment_type` | `str` | No | `text` |
| `status` | `str` | No | `text` |
| `date_range_start` | `datetime.date` | Yes | `date` |
| `date_range_end` | `datetime.date` | Yes | `date` |
| `site_visit_date` | `datetime.date` | Yes | `date` |
| `comp_set_id` | `UUID` | Yes | `uuid` |
| `created_by` | `UUID` | Yes | `uuid` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |
| `updated_at` | `datetime.datetime` | No | `timestamptz` |

### `AssessmentDataCoverage`

Table: `assessment_data_coverage` (8 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `coverage_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | No | `uuid` |
| `domain` | `str` | No | `text` |
| `source_system_id` | `UUID` | Yes | `uuid` |
| `coverage_status` | `str` | No | `text` |
| `coverage_pct` | `Decimal` | Yes | `decimal(5, 2)` |
| `notes` | `str` | Yes | `text` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `AnalysisRun`

Table: `analysis_run` (9 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `run_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | No | `uuid` |
| `rule_package_version` | `str` | No | `text` |
| `benchmark_version` | `str` | Yes | `text` |
| `transformation_version` | `str` | Yes | `text` |
| `status` | `str` | No | `text` |
| `started_at` | `datetime.datetime` | Yes | `timestamptz` |
| `completed_at` | `datetime.datetime` | Yes | `timestamptz` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `Scorecard`

Table: `scorecard` (8 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `scorecard_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | No | `uuid` |
| `analysis_run_id` | `UUID` | Yes | `uuid` |
| `scorecard_type` | `str` | No | `text` |
| `overall_score` | `Decimal` | Yes | `decimal(6, 2)` |
| `overall_grade` | `str` | Yes | `text` |
| `version` | `str` | No | `text` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `ScoreResult`

Table: `score_result` (24 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `result_id` | `UUID` | No | `uuid` |
| `scorecard_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | No | `uuid` |
| `analysis_run_id` | `UUID` | Yes | `uuid` |
| `scoring_level` | `str` | No | `text` |
| `area_number` | `int` | Yes | `int` |
| `area_name` | `str` | Yes | `text` |
| `item_name` | `str` | Yes | `text` |
| `sub_item_name` | `str` | Yes | `text` |
| `input_type` | `str` | Yes | `text` |
| `metric_value` | `Decimal` | Yes | `decimal(14, 4)` |
| `normalized_score` | `Decimal` | Yes | `decimal(6, 2)` |
| `weight` | `Decimal` | Yes | `decimal(8, 4)` |
| `weighted_score` | `Decimal` | Yes | `decimal(8, 4)` |
| `benchmark_type` | `str` | Yes | `text` |
| `benchmark_reference` | `str` | Yes | `text` |
| `confidence_score` | `Decimal` | Yes | `decimal(5, 2)` |
| `coverage_score` | `Decimal` | Yes | `decimal(5, 2)` |
| `grade_letter` | `str` | Yes | `text` |
| `scope_status` | `str` | Yes | `text` |
| `evidence_count` | `int` | Yes | `int` |
| `version` | `str` | No | `text` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `Finding`

Table: `finding` (16 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `finding_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | No | `uuid` |
| `analysis_run_id` | `UUID` | Yes | `uuid` |
| `finding_type` | `str` | No | `text` |
| `domain` | `str` | No | `text` |
| `severity` | `str` | No | `text` |
| `title` | `str` | No | `text` |
| `description` | `str` | No | `text` |
| `entity_type` | `str` | Yes | `text` |
| `entity_id` | `UUID` | Yes | `uuid` |
| `evidence_refs` | `dict[str, Any]` | No | `jsonb` |
| `contributing_causes` | `dict[str, Any]` | No | `jsonb` |
| `confidence` | `Decimal` | Yes | `decimal(5, 2)` |
| `rule_package_version` | `str` | Yes | `text` |
| `attributes` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `ImpactEstimate`

Table: `impact_estimate` (16 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `estimate_id` | `UUID` | No | `uuid` |
| `finding_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | No | `uuid` |
| `impact_model` | `str` | No | `text` |
| `impact_family_id` | `UUID` | Yes | `uuid` |
| `primary_driver_share` | `Decimal` | Yes | `decimal(5, 4)` |
| `contributing_share` | `Decimal` | Yes | `decimal(5, 4)` |
| `low_estimate` | `Decimal` | Yes | `decimal(14, 2)` |
| `base_estimate` | `Decimal` | Yes | `decimal(14, 2)` |
| `high_estimate` | `Decimal` | Yes | `decimal(14, 2)` |
| `annualized_amount` | `Decimal` | Yes | `decimal(14, 2)` |
| `per_unit_amount` | `Decimal` | Yes | `decimal(12, 2)` |
| `formula_trace` | `dict[str, Any]` | No | `jsonb` |
| `assumption_trace` | `dict[str, Any]` | No | `jsonb` |
| `confidence` | `Decimal` | Yes | `decimal(5, 2)` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `Contradiction`

Table: `contradiction` (14 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `contradiction_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | No | `uuid` |
| `source_a_type` | `str` | No | `text` |
| `source_a_ref` | `UUID` | Yes | `uuid` |
| `source_b_type` | `str` | No | `text` |
| `source_b_ref` | `UUID` | Yes | `uuid` |
| `matching_rule` | `str` | No | `text` |
| `contradiction_type` | `str` | No | `text` |
| `severity` | `str` | No | `text` |
| `affected_domains` | `dict[str, Any]` | No | `jsonb` |
| `trust_penalty` | `Decimal` | Yes | `decimal(5, 4)` |
| `evidence_links` | `dict[str, Any]` | No | `jsonb` |
| `notes` | `str` | Yes | `text` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `Recommendation`

Table: `recommendation` (16 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `recommendation_id` | `UUID` | No | `uuid` |
| `finding_id` | `UUID` | Yes | `uuid` |
| `assessment_id` | `UUID` | No | `uuid` |
| `domain` | `str` | No | `text` |
| `target_entity_type` | `str` | Yes | `text` |
| `target_entity_id` | `UUID` | Yes | `uuid` |
| `priority` | `str` | No | `text` |
| `title` | `str` | No | `text` |
| `description` | `str` | No | `text` |
| `expected_impact` | `dict[str, Any]` | Yes | `jsonb` |
| `owner` | `str` | Yes | `text` |
| `due_date` | `datetime.date` | Yes | `date` |
| `status` | `str` | No | `text` |
| `verification_evidence` | `dict[str, Any]` | Yes | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |
| `updated_at` | `datetime.datetime` | No | `timestamptz` |

### `Report`

Table: `report` (8 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `report_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | No | `uuid` |
| `template_name` | `str` | No | `text` |
| `report_type` | `str` | No | `text` |
| `status` | `str` | No | `text` |
| `created_by` | `UUID` | Yes | `uuid` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |
| `updated_at` | `datetime.datetime` | No | `timestamptz` |

### `ReportSection`

Table: `report_section` (10 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `section_id` | `UUID` | No | `uuid` |
| `report_id` | `UUID` | No | `uuid` |
| `section_type` | `str` | No | `text` |
| `sort_order` | `int` | No | `int` |
| `title` | `str` | Yes | `text` |
| `content` | `dict[str, Any]` | No | `jsonb` |
| `data_bindings` | `dict[str, Any]` | No | `jsonb` |
| `narrative` | `str` | Yes | `text` |
| `chart_spec` | `dict[str, Any]` | Yes | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `ReportRender`

Table: `report_render` (7 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `render_id` | `UUID` | No | `uuid` |
| `report_id` | `UUID` | No | `uuid` |
| `format` | `str` | No | `text` |
| `storage_path` | `str` | No | `text` |
| `section_manifest` | `dict[str, Any]` | No | `jsonb` |
| `rendered_at` | `datetime.datetime` | No | `timestamptz` |
| `rendered_by` | `UUID` | Yes | `uuid` |

---

## workspace

Module: `src/shared/models/workspace.py`

### `Study`

Table: `study` (7 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `study_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | No | `uuid` |
| `study_name` | `str` | No | `text` |
| `description` | `str` | Yes | `text` |
| `created_by` | `UUID` | Yes | `uuid` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |
| `updated_at` | `datetime.datetime` | No | `timestamptz` |

### `SavedQuery`

Table: `saved_query` (10 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `query_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | Yes | `uuid` |
| `study_id` | `UUID` | Yes | `uuid` |
| `query_name` | `str` | No | `text` |
| `query_definition` | `dict[str, Any]` | No | `jsonb` |
| `parameters` | `dict[str, Any]` | No | `jsonb` |
| `filters` | `dict[str, Any]` | No | `jsonb` |
| `chart_spec` | `dict[str, Any]` | Yes | `jsonb` |
| `created_by` | `UUID` | Yes | `uuid` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `ResultSnapshot`

Table: `result_snapshot` (15 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `snapshot_id` | `UUID` | No | `uuid` |
| `saved_query_id` | `UUID` | Yes | `uuid` |
| `assessment_id` | `UUID` | Yes | `uuid` |
| `study_id` | `UUID` | Yes | `uuid` |
| `source_data_version` | `str` | Yes | `text` |
| `transformation_version` | `str` | Yes | `text` |
| `rule_package_version` | `str` | Yes | `text` |
| `benchmark_version` | `str` | Yes | `text` |
| `result_payload` | `dict[str, Any]` | No | `jsonb` |
| `chart_spec` | `dict[str, Any]` | Yes | `jsonb` |
| `sql_definition` | `str` | Yes | `text` |
| `filters` | `dict[str, Any]` | No | `jsonb` |
| `data_hash` | `str` | Yes | `text` |
| `created_by` | `UUID` | Yes | `uuid` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `StudyItem`

Table: `study_item` (6 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `item_id` | `UUID` | No | `uuid` |
| `study_id` | `UUID` | No | `uuid` |
| `item_type` | `str` | No | `text` |
| `ref_id` | `UUID` | No | `uuid` |
| `sort_order` | `int` | Yes | `int` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `ComparisonBoard`

Table: `comparison_board` (7 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `board_id` | `UUID` | No | `uuid` |
| `study_id` | `UUID` | Yes | `uuid` |
| `assessment_id` | `UUID` | Yes | `uuid` |
| `board_name` | `str` | No | `text` |
| `layout` | `dict[str, Any]` | No | `jsonb` |
| `created_by` | `UUID` | Yes | `uuid` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `Annotation`

Table: `annotation` (7 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `annotation_id` | `UUID` | No | `uuid` |
| `entity_type` | `str` | No | `text` |
| `entity_id` | `UUID` | No | `uuid` |
| `note_text` | `str` | No | `text` |
| `created_by` | `UUID` | Yes | `uuid` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |
| `updated_at` | `datetime.datetime` | No | `timestamptz` |

### `EvidenceBundle`

Table: `evidence_bundle` (6 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `bundle_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | No | `uuid` |
| `bundle_name` | `str` | No | `text` |
| `item_refs` | `dict[str, Any]` | No | `jsonb` |
| `created_by` | `UUID` | Yes | `uuid` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

---

## scoring_config

Module: `src/shared/models/scoring_config.py`

### `ScoringRubricVersion`

Table: `scoring_rubric_version` (5 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `version_id` | `UUID` | No | `uuid` |
| `version_label` | `str` | No | `text` |
| `is_active` | `bool` | No | `boolean` |
| `config` | `dict[str, Any]` | No | `jsonb` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `BenchmarkVersion`

Table: `benchmark_version` (6 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `version_id` | `UUID` | No | `uuid` |
| `version_label` | `str` | No | `text` |
| `benchmark_type` | `str` | No | `text` |
| `data` | `dict[str, Any]` | No | `jsonb` |
| `is_active` | `bool` | No | `boolean` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `MetricRegistry`

Table: `metric_registry` (10 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `metric_id` | `UUID` | No | `uuid` |
| `metric_name` | `str` | No | `text` |
| `domain` | `str` | No | `text` |
| `grain` | `str` | No | `text` |
| `description` | `str` | Yes | `text` |
| `formula` | `str` | Yes | `text` |
| `required_inputs` | `dict[str, Any]` | No | `jsonb` |
| `output_type` | `str` | No | `text` |
| `version` | `str` | No | `text` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `DiagnosticPackage`

Table: `diagnostic_package` (10 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `package_id` | `UUID` | No | `uuid` |
| `package_name` | `str` | No | `text` |
| `domain` | `str` | No | `text` |
| `version` | `str` | No | `text` |
| `required_inputs` | `dict[str, Any]` | No | `jsonb` |
| `optional_inputs` | `dict[str, Any]` | No | `jsonb` |
| `grain` | `str` | Yes | `text` |
| `description` | `str` | Yes | `text` |
| `is_active` | `bool` | No | `boolean` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

### `ImpactModelCatalog`

Table: `impact_model_catalog` (10 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `model_id` | `UUID` | No | `uuid` |
| `model_name` | `str` | No | `text` |
| `formula` | `str` | No | `text` |
| `required_inputs` | `dict[str, Any]` | No | `jsonb` |
| `optional_refinements` | `dict[str, Any]` | No | `jsonb` |
| `low_high_params` | `dict[str, Any]` | No | `jsonb` |
| `double_count_rules` | `dict[str, Any]` | No | `jsonb` |
| `narrative` | `str` | Yes | `text` |
| `version` | `str` | No | `text` |
| `created_at` | `datetime.datetime` | No | `timestamptz` |

---

## clickhouse_facts

Module: `src/shared/models/clickhouse_facts.py`

### `FactUnitDay`

Table: `fact_unit_day` (18 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `property_id` | `UUID` | No | `uuid` |
| `unit_id` | `UUID` | No | `uuid` |
| `day_date` | `datetime.date` | No | `date` |
| `unit_version_id` | `UUID` | No | `uuid` |
| `existence_status` | `str` | No | `lowcardinality(string)` |
| `rentable_flag` | `int` | No | `uint8` |
| `occupancy_state` | `str` | No | `lowcardinality(string)` |
| `readiness_state` | `str` | No | `lowcardinality(string)` |
| `marketing_state` | `str` | No | `lowcardinality(string)` |
| `active_lease_id` | `UUID` | Yes | `nullable(uuid)` |
| `active_listing_id` | `UUID` | Yes | `nullable(uuid)` |
| `days_vacant` | `int` | Yes | `nullable(int32)` |
| `asking_rent` | `Decimal` | Yes | `nullable(decimal(12,2))` |
| `effective_rent` | `Decimal` | Yes | `nullable(decimal(12,2))` |
| `concession_value` | `Decimal` | Yes | `nullable(decimal(12,2))` |
| `condition_score` | `Decimal` | Yes | `nullable(decimal(5,2))` |
| `contradiction_flags` | `str` | No | `string` |
| `evidence_coverage` | `str` | No | `string` |

### `FactLeaseInterval`

Table: `fact_lease_interval` (12 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `property_id` | `UUID` | No | `uuid` |
| `unit_id` | `UUID` | No | `uuid` |
| `lease_id` | `UUID` | No | `uuid` |
| `interval_start` | `datetime.date` | No | `date` |
| `interval_end` | `datetime.date` | Yes | `nullable(date)` |
| `monthly_rent` | `Decimal` | Yes | `nullable(decimal(12,2))` |
| `effective_rent` | `Decimal` | Yes | `nullable(decimal(12,2))` |
| `concession_value` | `Decimal` | Yes | `nullable(decimal(12,2))` |
| `lease_type` | `str` | No | `lowcardinality(string)` |
| `resident_id` | `UUID` | Yes | `nullable(uuid)` |
| `bedrooms` | `Decimal` | Yes | `nullable(decimal(4,1))` |
| `sqft` | `int` | Yes | `nullable(int32)` |

### `FactVacancyCycle`

Table: `fact_vacancy_cycle` (11 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `property_id` | `UUID` | No | `uuid` |
| `unit_id` | `UUID` | No | `uuid` |
| `cycle_id` | `UUID` | No | `uuid` |
| `vacancy_start` | `datetime.date` | No | `date` |
| `vacancy_end` | `datetime.date` | Yes | `nullable(date)` |
| `days_vacant` | `int` | Yes | `nullable(int32)` |
| `prior_rent` | `Decimal` | Yes | `nullable(decimal(12,2))` |
| `new_rent` | `Decimal` | Yes | `nullable(decimal(12,2))` |
| `vacancy_cost` | `Decimal` | Yes | `nullable(decimal(12,2))` |
| `make_ready_days` | `int` | Yes | `nullable(int32)` |
| `make_ready_cost` | `Decimal` | Yes | `nullable(decimal(12,2))` |

### `FactWorkOrder`

Table: `fact_work_order` (10 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `property_id` | `UUID` | No | `uuid` |
| `unit_id` | `UUID` | Yes | `nullable(uuid)` |
| `work_order_id` | `UUID` | No | `uuid` |
| `category` | `str` | No | `lowcardinality(string)` |
| `is_make_ready` | `int` | No | `uint8` |
| `date_created` | `datetime.date` | No | `date` |
| `date_completed` | `datetime.date` | Yes | `nullable(date)` |
| `days_to_complete` | `int` | Yes | `nullable(int32)` |
| `cost` | `Decimal` | Yes | `nullable(decimal(12,2))` |
| `vendor_id` | `UUID` | Yes | `nullable(uuid)` |

### `FactLeadFunnelEvent`

Table: `fact_lead_funnel_event` (8 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `property_id` | `UUID` | No | `uuid` |
| `lead_id` | `UUID` | No | `uuid` |
| `event_type` | `str` | No | `lowcardinality(string)` |
| `event_date` | `datetime.date` | No | `date` |
| `agent_id` | `UUID` | Yes | `nullable(uuid)` |
| `lead_source` | `str` | Yes | `nullable(string)` |
| `response_time_min` | `int` | Yes | `nullable(int32)` |
| `outcome` | `str` | Yes | `nullable(string)` |

### `FactListingObservation`

Table: `fact_listing_observation` (9 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `property_id` | `UUID` | No | `uuid` |
| `unit_id` | `UUID` | Yes | `nullable(uuid)` |
| `observation_id` | `UUID` | No | `uuid` |
| `platform` | `str` | No | `lowcardinality(string)` |
| `observation_date` | `datetime.date` | No | `date` |
| `asking_rent` | `Decimal` | Yes | `nullable(decimal(12,2))` |
| `photo_quality` | `Decimal` | Yes | `nullable(decimal(4,1))` |
| `description_quality` | `Decimal` | Yes | `nullable(decimal(4,1))` |
| `days_on_market` | `int` | Yes | `nullable(int32)` |

### `FactMarketingPresenceDay`

Table: `fact_marketing_presence_day` (6 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `property_id` | `UUID` | No | `uuid` |
| `channel_id` | `UUID` | No | `uuid` |
| `day_date` | `datetime.date` | No | `date` |
| `is_active` | `int` | No | `uint8` |
| `platform` | `str` | No | `lowcardinality(string)` |
| `spend_daily` | `Decimal` | Yes | `nullable(decimal(12,2))` |

### `FactCompListingObservation`

Table: `fact_comp_listing_observation` (9 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `competitor_property_id` | `UUID` | No | `uuid` |
| `observation_id` | `UUID` | No | `uuid` |
| `observation_date` | `datetime.date` | No | `date` |
| `bedrooms` | `Decimal` | Yes | `nullable(decimal(4,1))` |
| `sqft` | `int` | Yes | `nullable(int32)` |
| `asking_rent` | `Decimal` | Yes | `nullable(decimal(12,2))` |
| `rent_per_sqft` | `Decimal` | Yes | `nullable(decimal(8,2))` |
| `is_available` | `int` | Yes | `nullable(uint8)` |
| `concession_amount` | `Decimal` | Yes | `nullable(decimal(12,2))` |

### `FactScoreResult`

Table: `fact_score_result` (12 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `assessment_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `scorecard_id` | `UUID` | No | `uuid` |
| `scoring_level` | `str` | No | `lowcardinality(string)` |
| `area_number` | `int` | Yes | `nullable(int32)` |
| `area_name` | `str` | Yes | `nullable(string)` |
| `item_name` | `str` | Yes | `nullable(string)` |
| `normalized_score` | `Decimal` | Yes | `nullable(decimal(6,2))` |
| `weighted_score` | `Decimal` | Yes | `nullable(decimal(8,4))` |
| `confidence_score` | `Decimal` | Yes | `nullable(decimal(5,2))` |
| `grade_letter` | `str` | Yes | `nullable(string)` |
| `version` | `str` | No | `string` |

### `FactFindingImpact`

Table: `fact_finding_impact` (10 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `assessment_id` | `UUID` | No | `uuid` |
| `property_id` | `UUID` | No | `uuid` |
| `finding_id` | `UUID` | No | `uuid` |
| `finding_type` | `str` | No | `lowcardinality(string)` |
| `domain` | `str` | No | `lowcardinality(string)` |
| `severity` | `str` | No | `lowcardinality(string)` |
| `impact_model` | `str` | Yes | `nullable(string)` |
| `base_estimate` | `Decimal` | Yes | `nullable(decimal(14,2))` |
| `annualized_amount` | `Decimal` | Yes | `nullable(decimal(14,2))` |
| `confidence` | `Decimal` | Yes | `nullable(decimal(5,2))` |

### `FactAssessmentScore`

Table: `fact_assessment_score` (8 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `property_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | No | `uuid` |
| `assessment_date` | `datetime.date` | No | `date` |
| `area_number` | `int` | Yes | `nullable(int32)` |
| `area_name` | `str` | Yes | `nullable(string)` |
| `overall_score` | `Decimal` | Yes | `nullable(decimal(6,2))` |
| `grade_letter` | `str` | Yes | `nullable(string)` |
| `version` | `str` | No | `string` |

### `FactAssessmentFinding`

Table: `fact_assessment_finding` (8 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `property_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | No | `uuid` |
| `assessment_date` | `datetime.date` | No | `date` |
| `finding_id` | `UUID` | No | `uuid` |
| `domain` | `str` | No | `lowcardinality(string)` |
| `severity` | `str` | No | `lowcardinality(string)` |
| `is_recurring` | `int` | No | `uint8` |
| `prior_finding_id` | `UUID` | Yes | `nullable(uuid)` |

### `FactRecommendationStatus`

Table: `fact_recommendation_status` (7 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `property_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | No | `uuid` |
| `recommendation_id` | `UUID` | No | `uuid` |
| `domain` | `str` | No | `lowcardinality(string)` |
| `priority` | `str` | No | `lowcardinality(string)` |
| `status` | `str` | No | `lowcardinality(string)` |
| `status_date` | `datetime.date` | No | `date` |

### `FactPropertyKpiPeriod`

Table: `fact_property_kpi_period` (6 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `property_id` | `UUID` | No | `uuid` |
| `period_start` | `datetime.date` | No | `date` |
| `period_end` | `datetime.date` | No | `date` |
| `kpi_name` | `str` | No | `lowcardinality(string)` |
| `kpi_value` | `Decimal` | Yes | `nullable(decimal(14,4))` |
| `kpi_unit` | `str` | No | `lowcardinality(string)` |

### `FactUnitChronicity`

Table: `fact_unit_chronicity` (7 fields)

| Field | Python Type | Nullable | SQL Type |
|-------|-----------|----------|----------|
| `property_id` | `UUID` | No | `uuid` |
| `unit_id` | `UUID` | No | `uuid` |
| `assessment_id` | `UUID` | No | `uuid` |
| `chronic_type` | `str` | No | `lowcardinality(string)` |
| `duration_days` | `int` | Yes | `nullable(int32)` |
| `cycle_count` | `int` | Yes | `nullable(int32)` |
| `total_cost` | `Decimal` | Yes | `nullable(decimal(14,2))` |

---
