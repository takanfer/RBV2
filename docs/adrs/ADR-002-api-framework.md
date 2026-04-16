# ADR-002: FastAPI

**Status:** Accepted  
**Date:** 2026-04-04  
**Decides:** API framework for all application services

## Decision

FastAPI is the API framework for all HTTP-exposed application services.

## Rationale

- Async-native — handles concurrent requests to analytical warehouse without blocking
- Pydantic-native — shared type definitions (Pydantic models) work directly as request/response schemas with zero conversion
- Auto-generated OpenAPI documentation — every endpoint is documented automatically, enabling frontend development against a live spec
- High performance — ASGI-based, comparable to Node.js throughput
- Dependency injection system — clean separation of auth, database sessions, and tenant context

## Implications

- Internal service-to-service calls within the monorepo may use direct Python imports rather than HTTP when running in the same process
- All API routes live in `src/api/routes/` and use FastAPI routers
- Request/response models are Pydantic classes from `src/shared/models/`
