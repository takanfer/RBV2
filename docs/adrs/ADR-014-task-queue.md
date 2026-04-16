# ADR-014: Celery + Redis for Task Queue / Workflow Orchestration

**Status:** Accepted  
**Date:** 2026-04-12  
**Decides:** Background task execution and multi-step pipeline orchestration

## Decision

Celery with Redis as the message broker handles asynchronous task execution and multi-step pipeline orchestration.

## What This Solves

The assessment pipeline (import → entity resolution → temporal spine → metrics → scoring → findings → impact) is a multi-step chain where steps can take significant time, may fail, and need retry capability. A task queue decouples step execution from API request/response cycles.

## Components

| Component | Role |
|-----------|------|
| **Celery** | Task definition, execution, retry, chaining, result tracking |
| **Redis** | Message broker (queues) and result backend |

## Local Development

Redis is added to the Docker Compose stack alongside PostgreSQL, ClickHouse, and MinIO.

## Key Patterns

- Each service operation that is long-running (import processing, temporal spine build, full scoring run, report rendering) is exposed as a Celery task.
- Celery chains link multi-step pipelines (e.g., import → entity resolution → temporal refresh).
- Celery workers run in separate processes from the FastAPI application.
- Short-lived operations (check_access, get_assessment) remain synchronous FastAPI endpoints.
- Task status is queryable via the Engagement service's `get_run_status` operation.

## Rationale

- **Why not direct in-process calls:** Long-running operations (file import, full temporal spine rebuild, report rendering) would block API responses and cannot be retried on failure.
- **Why not Temporal/Dramatiq:** Celery is the most widely adopted Python task queue with the largest ecosystem. The pipeline's complexity (linear chains with occasional fan-out) does not require Temporal's workflow-as-code model.
- **Why Redis over RabbitMQ:** Redis serves double duty as broker and result backend. Simpler infrastructure. AWS ElastiCache provides managed Redis in production.

## Implications

- `docker/docker-compose.yml` adds a Redis container
- `pyproject.toml` adds `celery` and `redis` dependencies
- Worker entry point at `src/worker.py`
- Task definitions co-located with their service (e.g., `src/services/import_mapping/tasks.py`)
- CI runs a Redis container for integration tests
- Production deployment requires a Redis instance (AWS ElastiCache)
