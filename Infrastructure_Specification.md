# Infrastructure Specification

Defines the environment configuration, container topology, storage layout, and secrets management for the RBv2 platform. Every agent configuring infrastructure must follow these patterns exactly.

**Sources:**
- `ADR-008-local-development.md` — Docker Compose with PG 16, ClickHouse, MinIO, Redis
- `ADR-013-cloud-provider.md` — AWS: RDS, ClickHouse Cloud, S3, ECS Fargate, Secrets Manager, Route 53, CloudWatch
- `ADR-014-task-queue.md` — Celery + Redis, worker at `src/worker.py`, tasks co-located with services
- `Project_Skeleton_Specification.md` — `docker/docker-compose.yml` (line 70), `.env` (line 62), `docker/docker-compose.test.yml` (line 71)
- `Implementation_Tasks.md` — P0-T02 (Docker Compose), P0-T03 (environment config), P0-T06 (S3 wrapper)
- `phase-0-foundations.mdc` — technology constraints (lines 40-50)

---

## Docker Compose (Local Development)

Source: ADR-008, `Project_Skeleton_Specification.md` §5.2 (lines 297-310)

File: `docker/docker-compose.yml`

### Service Definitions

| Service Name | Image | Ports | Purpose |
|-------------|-------|-------|---------|
| `postgres` | `postgres:16` | `5432:5432` | Canonical OLTP store (mirrors AWS RDS) |
| `clickhouse` | `clickhouse/clickhouse-server` | `8123:8123`, `9000:9000` | Analytical warehouse (mirrors ClickHouse Cloud) |
| `minio` | `minio/minio` | `9090:9000`, `9091:9001` | S3-compatible object storage (mirrors AWS S3) |
| `redis` | `redis:7` | `6379:6379` | Celery broker and result backend (mirrors ElastiCache) |

Python services run on the host, not in containers, for fast iteration (ADR-008 line 31).

### Test Stack

File: `docker/docker-compose.test.yml`

Provides isolated database instances for CI integration tests. Same images, different ports, ephemeral volumes.

---

## Environment Variables

Source: `phase-0-foundations.mdc` line 48, Implementation_Tasks P0-T03

All configuration is via environment variables loaded through Pydantic Settings (`src/shared/config/settings.py`). The `.env` file is used for local development only and is not committed to git.

### Required Variables

| Variable | Type | Default (local) | Description |
|----------|------|-----------------|-------------|
| `DATABASE_URL` | str | `postgresql://postgres:postgres@localhost:5432/partners` | PostgreSQL connection string |
| `DATABASE_POOL_SIZE` | int | `5` | SQLAlchemy connection pool size |
| `DATABASE_MAX_OVERFLOW` | int | `10` | SQLAlchemy max overflow connections |
| `CLICKHOUSE_HOST` | str | `localhost` | ClickHouse server host |
| `CLICKHOUSE_PORT` | int | `8123` | ClickHouse HTTP port |
| `CLICKHOUSE_DATABASE` | str | `partners` | ClickHouse database name |
| `CLICKHOUSE_USER` | str | `default` | ClickHouse user |
| `CLICKHOUSE_PASSWORD` | str | `` | ClickHouse password (empty for local) |
| `S3_ENDPOINT_URL` | str | `http://localhost:9090` | S3/MinIO endpoint URL |
| `S3_ACCESS_KEY` | str | `minioadmin` | S3/MinIO access key |
| `S3_SECRET_KEY` | str | `minioadmin` | S3/MinIO secret key |
| `S3_BUCKET_EVIDENCE` | str | `partners-evidence` | Bucket for raw evidence and frozen snapshots |
| `S3_BUCKET_REPORTS` | str | `partners-reports` | Bucket for rendered reports |
| `REDIS_URL` | str | `redis://localhost:6379/0` | Redis connection for Celery broker |
| `CELERY_RESULT_BACKEND` | str | `redis://localhost:6379/1` | Redis DB for Celery results |
| `AUTH_ISSUER_URL` | str | *(none)* | Auth provider JWT issuer URL |
| `AUTH_AUDIENCE` | str | *(none)* | Auth provider JWT audience |
| `AUTH_JWKS_URL` | str | *(none)* | Auth provider JWKS endpoint for key retrieval |
| `LOG_LEVEL` | str | `INFO` | Structured logging level |
| `LOG_FORMAT` | str | `json` | Log output format (`json` for production, `console` for local dev) |
| `ENVIRONMENT` | str | `development` | `development`, `staging`, or `production` |
| `CORS_ALLOWED_ORIGINS` | str | `http://localhost:3000` | Comma-separated list of allowed CORS origins |

### `.env.example` Template

The `.env.example` file at repo root contains all variables with local-dev defaults. Developers copy it to `.env`. Production values come from AWS Secrets Manager injected as environment variables into ECS task definitions.

---

## Secrets Management

### Boundary: What Goes Where

| Secret Type | Local Dev | Production |
|-------------|-----------|-----------|
| Database passwords | `.env` file | AWS Secrets Manager → ECS env vars |
| S3 credentials | `.env` file (MinIO defaults) | IAM roles (no explicit keys) |
| Auth provider config | `.env` file | AWS Secrets Manager → ECS env vars |
| Redis password | None (local Redis has no auth) | AWS Secrets Manager → ECS env vars |
| API keys (future) | `.env` file | AWS Secrets Manager → ECS env vars |

### Rules

- Never commit `.env` to git. `.env` is in `.gitignore`.
- Never hardcode secrets in source code.
- Production secrets are retrieved from AWS Secrets Manager at deployment time and injected as environment variables into ECS task definitions.
- All environment variables have local-dev defaults in the Pydantic Settings class so the app starts with `docker compose up` and no `.env` file (see `Code_Patterns_Specification.md` §9). Auth variables (`AUTH_ISSUER_URL`, `AUTH_AUDIENCE`, `AUTH_JWKS_URL`) have empty-string defaults and are validated at middleware initialization, not at settings load.

---

## S3 Bucket Structure

Source: `phase-0-foundations.mdc` line 42 (S3 for raw evidence), Implementation_Tasks P0-T06

### Buckets

| Bucket | Purpose |
|--------|---------|
| `partners-evidence` | Raw evidence files, frozen snapshots, source assets |
| `partners-reports` | Rendered report artifacts (PDF, HTML, PPTX) |

### Key Structure

```
partners-evidence/
  tenants/{tenant_id}/
    ingestions/{ingestion_id}/
      assets/{asset_id}/{original_filename}
    snapshots/{snapshot_id}/
      {artifact_name}

partners-reports/
  tenants/{tenant_id}/
    reports/{report_id}/
      renders/{render_id}.{format}
```

### Rules

- All keys are prefixed with `tenants/{tenant_id}/` for tenant isolation.
- Raw evidence files are immutable. Once uploaded, they are never modified or deleted (phase-1-canonical-core.mdc lines 47-49).
- Each `source_asset` record stores the S3 key and SHA-256 hash. Duplicate uploads (same hash) are rejected idempotently (Service_Interface_Contracts.md line 137).
- Content-addressable deduplication is at the hash level, not the key level.

---

## Production Topology

Source: ADR-013

### AWS Services

| Platform Component | AWS Service | Notes |
|-------------------|-------------|-------|
| PostgreSQL | RDS for PostgreSQL (or Aurora PostgreSQL) | Multi-AZ, automated backups |
| ClickHouse | ClickHouse Cloud on AWS | Managed, same region as RDS |
| Object storage | S3 | Standard tier, lifecycle policies for older evidence |
| Container orchestration | ECS (Fargate) | Serverless containers, no EC2 management |
| Secrets | Secrets Manager | Rotatable, injected into ECS tasks |
| DNS / CDN | Route 53 / CloudFront | Frontend served via CloudFront |
| Monitoring | CloudWatch | Logs, metrics, alarms |
| Redis | ElastiCache (Redis) | Celery broker, same VPC as ECS |

### ECS Service Definitions

| ECS Service | Container | Scaling |
|-------------|-----------|---------|
| `api` | FastAPI application (`src/api/main.py`) | Horizontal (min 2, scale on CPU/request count) |
| `worker` | Celery worker (`src/worker.py`) | Horizontal (scale on queue depth) |
| `frontend` | Next.js application (`frontend/`) | Horizontal (min 2, scale on request count) |

### IaC Approach

Infrastructure-as-code tool selection is deferred to Phase 0 implementation and will be recorded as a new ADR at that time. The specification above defines WHAT is deployed; the IaC tool defines HOW it is provisioned.
