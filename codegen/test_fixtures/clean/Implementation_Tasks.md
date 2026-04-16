# Implementation Tasks

## Phase 0: Data Ingestion

### Task 1: Build Ingestion Pipeline

Implement the data ingestion pipeline per `Service_Interface_Contracts.md`.

Operations: `create_ingestion`, `get_ingestion_status`, `list_ingestion_jobs`.

Key tables: `source_asset.tenant_id`, `source_asset.file_name`.

The `user_account.role` field supports roles: `admin`, `consultant`, `analyst`, `client_viewer`, `client_user`, `viewer`.

See `Database_Schema_Specification.md` line 1 for schema overview.

File: `src/services/data_ingestion/router.py`

API route: `src/api/routes/ingestion.py`

References spec_1 §1.1 for data collection requirements.

## Phase 1: Scoring Engine

### Task 2: Build Scoring

Implement scoring per spec_1 §2.1 and `Scoring_Model_Specification.md`.

Operations: `compute_scores`, `get_score_snapshot`, `list_score_history`.

ClickHouse table `fact_unit_day` stores daily unit snapshots.

PostgreSQL table `property` stores canonical property data.

See [Data Onramp](Data_Onramp_Specification.md) for ingestion details.

Intake channels include `file_import` and `api_pull` ingestion types.

Resolution options: `accept`, `flag`, `reject`, `defer`.
