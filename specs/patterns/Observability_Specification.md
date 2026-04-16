# Observability Specification

Defines the structured logging format, correlation ID propagation, health check contract, and monitoring patterns. Every agent implementing logging, health checks, or monitoring must follow these patterns exactly.

**Sources:**
- `ADR-013-cloud-provider.md` — CloudWatch for monitoring (line 21)
- `Service_Interface_Contracts.md` — audit logging cross-cutting (line 505), error categories (lines 490-501)
- `Database_Schema_Specification.md` — `audit_log` table (lines 207-220)
- `Implementation_Tasks.md` — P0-T02 (health checks, line 58), P0-T18 (audit logging, lines 165-170)
- `Project_Skeleton_Specification.md` — CI pipeline (lines 339-347)

---

## Structured Logging

### Format

All application logs are structured JSON. One JSON object per log line.

### Required Fields

Every log entry must contain these fields:

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | string (ISO 8601) | UTC timestamp with milliseconds: `2026-04-14T12:34:56.789Z` |
| `level` | string | `DEBUG`, `INFO`, `WARN`, `ERROR` |
| `service` | string | Service name: `api`, `worker`, `authz`, `engagement`, etc. |
| `correlation_id` | string (UUID) | Request-scoped unique ID for tracing across service calls |
| `message` | string | Human-readable description |

### Optional Fields (included when available)

| Field | Type | When Present |
|-------|------|-------------|
| `tenant_id` | string (UUID) | After authentication resolves tenant |
| `user_id` | string (UUID) | After authentication resolves user |
| `method` | string | HTTP method (`GET`, `POST`, etc.) — API requests only |
| `path` | string | HTTP path — API requests only |
| `status_code` | int | HTTP response status — API responses only |
| `duration_ms` | int | Request processing time in milliseconds — API responses only |
| `error_code` | string | Error code from `ErrorResponse` — error logs only |
| `task_id` | string | Celery task ID — worker logs only |
| `exc_info` | string | Exception traceback — ERROR level only |

### Example Log Lines

Request start:
```json
{"timestamp": "2026-04-14T12:34:56.789Z", "level": "INFO", "service": "api", "correlation_id": "abc-123", "tenant_id": "t-456", "user_id": "u-789", "method": "POST", "path": "/api/assessments", "message": "Request started"}
```

Request complete:
```json
{"timestamp": "2026-04-14T12:34:56.890Z", "level": "INFO", "service": "api", "correlation_id": "abc-123", "tenant_id": "t-456", "user_id": "u-789", "method": "POST", "path": "/api/assessments", "status_code": 201, "duration_ms": 101, "message": "Request completed"}
```

Error:
```json
{"timestamp": "2026-04-14T12:34:56.890Z", "level": "ERROR", "service": "api", "correlation_id": "abc-123", "tenant_id": "t-456", "user_id": "u-789", "error_code": "storage_error", "message": "Failed to upload to S3", "exc_info": "Traceback (most recent call last):\n..."}
```

### Local Development Override

When `LOG_FORMAT=console` (see `Infrastructure_Specification.md`), logs are human-readable instead of JSON:

```
2026-04-14 12:34:56 INFO  [abc-123] POST /api/assessments — Request started
```

---

## Log Levels

| Level | When to Use | Examples |
|-------|------------|---------|
| `ERROR` | Unhandled exceptions, infrastructure failures, data corruption | S3 unreachable, migration failure, unexpected None |
| `WARN` | Expected failures, validation rejections, degraded state | JWT expired, invalid input, rate limited, retry triggered |
| `INFO` | State transitions, request lifecycle, business events | Assessment created, ingestion finalized, scoring run started, report rendered |
| `DEBUG` | Query details, intermediate state, diagnostic data | SQL statements, Pydantic validation details, cache hit/miss |

### Rules

- `ERROR` must always include `exc_info` (full traceback).
- `INFO` is the default production level. All state transitions must be logged at `INFO`.
- `DEBUG` is never enabled in production. It may contain PII (query parameters, row data).
- Never log secrets, passwords, or full JWT tokens at any level.
- Tenant PII (email, names) may appear in `DEBUG` only. `INFO` and above use IDs only.

---

## Correlation ID Propagation

### Flow

1. **API middleware** generates a UUID v4 `correlation_id` for each incoming request (or reads it from the `X-Correlation-ID` request header if present).
2. The correlation ID is stored in a context variable (Python `contextvars.ContextVar`).
3. All log statements within that request automatically include the correlation ID.
4. If the request triggers a Celery task, the correlation ID is passed as a task header.
5. The Celery worker reads the correlation ID from the task header and sets it in its own context.
6. The API response includes the correlation ID as the `X-Correlation-ID` response header.

### Implementation

```python
import contextvars

correlation_id_var: contextvars.ContextVar[str] = contextvars.ContextVar(
    "correlation_id", default=""
)
```

The FastAPI middleware sets the context variable before the route handler runs and clears it after.

---

## Health Check

### Endpoint

`GET /api/health` — unauthenticated, always available.

### Response Shape

```json
{
  "status": "ok",
  "version": "0.1.0",
  "environment": "production",
  "checks": {
    "postgres": "ok",
    "clickhouse": "ok",
    "redis": "ok",
    "s3": "ok"
  }
}
```

### Check Behavior

| Check | What It Does | Timeout |
|-------|-------------|---------|
| `postgres` | Executes `SELECT 1` against the connection pool | 3 seconds |
| `clickhouse` | Executes `SELECT 1` via clickhouse-connect | 3 seconds |
| `redis` | Calls `PING` on the Redis connection | 2 seconds |
| `s3` | Calls `head_bucket` on the evidence bucket | 3 seconds |

### Status Codes

- All checks pass: `200 OK`, `"status": "ok"`
- One or more checks fail: `503 Service Unavailable`, `"status": "degraded"`, failed checks show `"error"` with a brief message

### Usage

- ECS health checks poll this endpoint to determine container readiness.
- CloudWatch synthetic monitoring polls this endpoint for uptime tracking.
- Load balancers use this endpoint for target group health.

---

## Audit Logging (Business Events)

Source: `Service_Interface_Contracts.md` line 505, `Database_Schema_Specification.md` lines 207-220

Audit logging is distinct from structured logging. Audit logs are business records stored in the `audit_log` PostgreSQL table. Structured logs are operational records sent to CloudWatch.

### What Gets Audited

All write operations on tenant-scoped data (Service_Interface_Contracts.md line 505):

| Action Category | Examples |
|----------------|---------|
| Create | Assessment created, ingestion started, report generated |
| Update | Assessment status changed, mapping resolved, score overridden |
| Delete | Assessment deleted, ingestion cancelled |
| Override | Manual score override, entity merge, review resolution |

### Audit Log Record

Source: `audit_log` DDL (lines 207-218)

| Column | Type | Description |
|--------|------|-------------|
| `log_id` | UUID | Primary key |
| `tenant_id` | UUID | Tenant scope |
| `user_id` | UUID (nullable) | Acting user (null for system actions) |
| `action` | text | Action name: `create_assessment`, `update_status`, `resolve_review_item` |
| `entity_type` | text | Entity: `assessment`, `source_ingestion`, `mapping_review_queue` |
| `entity_id` | UUID | ID of the affected entity |
| `before_value` | JSONB (nullable) | Entity state before the change |
| `after_value` | JSONB (nullable) | Entity state after the change |
| `reason` | text (nullable) | User-provided reason for manual overrides |
| `created_at` | timestamptz | Timestamp of the action |

### Rules

- Audit logging is performed by the service layer, not the route layer.
- Every service function that mutates data must call the audit logger before returning.
- `before_value` and `after_value` are Pydantic model `.model_dump()` snapshots.
- System-triggered actions (e.g., scheduled scoring) set `user_id = null`.

---

## Production Monitoring

Source: ADR-013 line 21 (CloudWatch)

### Metrics to Collect

| Metric | Source | Alert Threshold |
|--------|--------|-----------------|
| API request latency (p50, p95, p99) | Access logs | p99 > 2s |
| API error rate (5xx) | Access logs | > 1% over 5 minutes |
| API error rate (4xx) | Access logs | Informational (no alert) |
| Celery queue depth | Redis `LLEN` | > 100 tasks pending for > 5 minutes |
| Celery task failure rate | Worker logs | > 5% over 15 minutes |
| PostgreSQL connection pool usage | SQLAlchemy metrics | > 80% of pool size |
| ClickHouse query latency | Application logs | p95 > 5s |
| S3 operation failures | Application logs | Any failure |
| Health check status | `/api/health` | Any `503` response |
