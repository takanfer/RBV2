# REST API Design Specification

Defines the HTTP API surface conventions for all FastAPI endpoints. Every agent implementing API routes must follow these patterns exactly to prevent drift across sessions and phases.

**Sources:**
- `ADR-002-api-framework.md` — FastAPI decision, Pydantic-native schemas, auto-generated OpenAPI
- `Service_Interface_Contracts.md` — 15 services, 85 operations, cross-cutting error categories (lines 490-501)
- `Project_Skeleton_Specification.md` — route files in `src/api/routes/` (line 114), one module per domain
- `ADR-015-authentication.md` — JWT validation, role mapping
- `phase-0-foundations.mdc` — FastAPI at `src/api/main.py` (line 47)

---

## URL Structure

### Base Path

All API routes are served under `/api/`. No version prefix in the URL path. Versioning is deferred until the Client Portal (Phase 5) creates an external-facing API surface.

### Resource Naming

- **Plural nouns** for collection endpoints: `/api/assessments`, `/api/properties`, `/api/ingestions`
- **Kebab-case** for multi-word resources: `/api/review-items`, `/api/data-coverage`, `/api/score-results`
- **Nested resources** only when the child is meaningless without the parent:
  - `/api/assessments/{assessment_id}/scores` — scores belong to an assessment
  - `/api/assessments/{assessment_id}/findings` — findings belong to an assessment
  - `/api/ingestions/{ingestion_id}/review-items` — review items belong to an ingestion
- **Flat resources** when the entity has its own identity:
  - `/api/properties/{property_id}` — not nested under `/api/tenants/{tenant_id}/properties` (tenant is inferred from JWT)
  - `/api/source-systems/{source_system_id}` — not nested under ingestion

### HTTP Methods

| Method | Semantics | Response Code |
|--------|-----------|---------------|
| `GET` | Read a single resource or list | 200 |
| `POST` | Create a new resource | 201 |
| `PUT` | Full replacement of a resource | 200 |
| `PATCH` | Partial update | 200 |
| `DELETE` | Remove a resource | 204 (no body) |

### Action Endpoints

Operations that don't map to CRUD (e.g., `apply_mappings`, `resolve_unit_aliases`, `compute_scores`) use `POST` on a verb sub-resource:

- `POST /api/ingestions/{ingestion_id}/apply-mappings`
- `POST /api/assessments/{assessment_id}/compute-scores`
- `POST /api/assessments/{assessment_id}/trigger-run`

---

## Request and Response Shapes

### Request Bodies

All request bodies are Pydantic models from `src/shared/models/` or API-specific input schemas defined in the route module. No raw dicts.

### Response Bodies

Single resources return the Pydantic model directly (no envelope):

```json
{
  "assessment_id": "uuid",
  "property_id": "uuid",
  "assessment_type": "FULL_ENGAGEMENT",
  "status": "draft",
  "created_at": "2026-04-14T00:00:00Z"
}
```

### List Responses

All list endpoints return a paginated envelope:

```json
{
  "items": [...],
  "total": 142,
  "page_size": 50,
  "cursor": "eyJpZCI6IjEyMyJ9"
}
```

The envelope Pydantic model:

```python
class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page_size: int
    cursor: str | None = None
```

### Pagination

Cursor-based pagination using an opaque cursor token (base64-encoded JSON of the last item's sort key). Query parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page_size` | int | 50 | Items per page (max 200) |
| `cursor` | string | None | Opaque cursor from previous response |

Offset-based pagination is not used. Cursor-based prevents duplicate/skip issues on concurrent inserts.

### Filtering and Sorting

Standard query parameters for list endpoints:

| Parameter | Example | Description |
|-----------|---------|-------------|
| `sort_by` | `sort_by=created_at` | Column to sort on (must be a declared sortable field) |
| `sort_dir` | `sort_dir=desc` | `asc` or `desc` (default: `desc` for timestamps, `asc` for names) |
| `status` | `status=draft` | Filter by enum field value |
| `property_id` | `property_id=uuid` | Filter by FK relationship |
| `q` | `q=search+term` | Free-text search (where supported) |
| `created_after` | `created_after=2026-01-01` | Timestamp range filter |
| `created_before` | `created_before=2026-12-31` | Timestamp range filter |

Each route explicitly declares which filter parameters it supports via FastAPI `Query()` parameters. Undeclared parameters are ignored (not silently accepted).

---

## Error Responses

All errors return a consistent JSON shape:

```json
{
  "error": {
    "code": "assessment_not_found",
    "message": "Assessment with ID abc-123 not found",
    "detail": {}
  }
}
```

The error Pydantic model:

```python
class ErrorDetail(BaseModel):
    code: str
    message: str
    detail: dict[str, Any] = {}

class ErrorResponse(BaseModel):
    error: ErrorDetail
```

### Error Code to HTTP Status Mapping

Source: `Service_Interface_Contracts.md` lines 490-501

| Error Category | HTTP Status | Example Codes |
|---------------|-------------|---------------|
| Not Found | 404 | `assessment_not_found`, `property_not_found`, `unit_not_found` |
| Permission | 403 | `permission_denied`, `tenant_mismatch` |
| Validation | 400 | `schema_validation_error`, `invalid_query`, `invalid_resolution` |
| State | 409 | `invalid_status_transition`, `unresolved_review_items` |
| Upstream | 422 | `metrics_not_computed`, `no_findings`, `insufficient_data` |
| Infrastructure | 500 | `storage_error`, `render_error`, `execution_error` |

### Error Code Format

- Lowercase snake_case
- Pattern: `{entity}_{condition}` or `{category}_{condition}`
- Examples: `assessment_not_found`, `invalid_status_transition`, `duplicate_hash`

---

## Authentication

### Header

All authenticated endpoints require:

```
Authorization: Bearer <jwt>
```

### Unauthenticated Endpoints

Only these endpoints are accessible without a JWT:

- `GET /api/health` — health check
- `GET /docs` — OpenAPI documentation (development only)
- `GET /openapi.json` — OpenAPI schema (development only)

### Tenant Scoping

The tenant is never in the URL. It is always derived from the authenticated user's JWT claims via the AuthZ service's `get_tenant_context` operation (Service_Interface_Contracts.md §1, line 58).

---

## Content Type

- Request: `application/json` for all endpoints except file uploads
- File uploads: `multipart/form-data`
- Response: `application/json` for all endpoints

---

## OpenAPI Documentation

FastAPI auto-generates OpenAPI at `/docs` (Swagger UI) and `/openapi.json`. Source: ADR-002 line 15.

All route functions must include:
- `response_model` parameter pointing to the output Pydantic model
- `status_code` parameter for the success status code
- `summary` parameter with a one-line description

Tags are set once on `APIRouter(tags=["engagements"])`, not repeated on individual routes (see `Code_Patterns_Specification.md` §1).

```python
@router.get(
    "/assessments/{assessment_id}",
    response_model=Assessment,
    status_code=200,
    summary="Get assessment by ID",
)
```
