# Implementation Tasks

## Phase 0: Data Ingestion

The platform has 15 services across all phases.

### Task 1: Build Ingestion Pipeline

Implement the data ingestion pipeline per `Service_Interface_Contracts.md`.

Operations: `create_ingestion`, `get_ingestion_status`, `list_ingestion_jobs`.

Key tables: `source_asset.tenant_id`, `source_asset.file_name`, `fake_table.column_a`.

The `user_account.role` field supports roles: `admin`, `consultant`, `analyst`, `client_viewer`, `client_user`, `super_admin`.

See `Database_Schema_Specification.md` line 9999 for schema overview.

File: `src/services/data_ingestion/nonexistent_file.py`

References spec_1 §1.1 for data collection requirements.

See also spec_1 §99.9 for advanced analytics.

## Phase 1: Scoring Engine

### Task 2: Build Scoring

Implement scoring per spec_1 §2.1 and `Nonexistent_Document.md`.

Operations: `compute_scores`, `get_score_snapshot`, `list_score_history`.

ClickHouse table `fact_unit_day` stores daily unit snapshots.

ClickHouse table `property` stores canonical property data.

See [Data Onramp](Data_Onramp_Specification.md) and [Ghost Doc](Ghost_Document.md) for ingestion details.

Intake channels include `file_import` and `api_pull` ingestion types.

Resolution options: `accept`, `flag`, `reject`, `override`.

The `Data_Onramp_Specification.md` line 3 defines `zebra_protocol` for data transfer.
