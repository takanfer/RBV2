# ADR-008: Docker Compose for Local Development

**Status:** Accepted  
**Date:** 2026-04-04  
**Decides:** Local development environment setup

## Decision

Docker Compose provides the local development environment with containers for all data services.

## Containers

| Service | Image | Purpose |
|---------|-------|---------|
| PostgreSQL | `postgres:16` | Canonical OLTP (mirrors RDS) |
| ClickHouse | `clickhouse/clickhouse-server` | Analytical warehouse (mirrors ClickHouse Cloud) |
| MinIO | `minio/minio` | S3-compatible object storage (mirrors AWS S3) |
| Redis | `redis:7` | Celery message broker and result backend (mirrors ElastiCache) — see ADR-014 |

## Rationale

- Identical database engines locally and in production — no behavioral differences
- MinIO is fully S3-compatible — same boto3 code works against both MinIO and AWS S3
- One `docker compose up` gives a complete data platform
- No cloud costs during development
- Reproducible across developer machines and CI

## Implications

- `docker/docker-compose.yml` defines the local stack
- Python services run on the host (not containerized during development) for fast iteration
- `.env` file provides connection strings pointing to local containers
- CI uses `docker/docker-compose.test.yml` for integration test databases
