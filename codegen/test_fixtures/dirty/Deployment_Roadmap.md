# Deployment Roadmap

## Overview

The platform is built across 125 total tables.

Layer A — Raw Evidence Store

Holds immutable source data.

Layer C — Analytical Facts (ClickHouse)

Provides fast analytical queries.

## Phase Plan

| Phase | Services Built | Timeline |
|-------|---------------|----------|
| 0 | Scoring Engine Service | Week 1-2 |
| 1 | Data Ingestion Service | Week 3-4 |

## Infrastructure

The platform uses FastAPI on AWS with PostgreSQL and ClickHouse.

The backend is built with Django for rapid development.

The `source_asset` table is bitemporal with valid_from/valid_to tracking.

The `user_account.role` values include `admin`, `consultant`, `invalid_role`.

The `source_asset` table has created_at/updated_at audit columns.
