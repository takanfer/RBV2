# Deployment Roadmap

## Overview

The platform is built across 5 tables with 25 total columns.

Layer A — Raw Evidence Store

Holds immutable source data.

Layer C — Analytical Facts (ClickHouse)

Provides fast analytical queries.

## Phase Plan

| Phase | Services Built | Timeline |
|-------|---------------|----------|
| 0 | Data Ingestion Service | Week 1-2 |
| 1 | Scoring Engine Service | Week 3-4 |

## Infrastructure

The platform uses FastAPI on AWS with PostgreSQL and ClickHouse.

The `property` table is bitemporal with valid_from/valid_to tracking.

The `source_asset` table has created_at/updated_at audit columns.
