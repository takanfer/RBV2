# Authentication Middleware Specification

Defines the JWT authentication middleware, claims schema, tenant resolution flow, and CORS configuration. Every agent implementing auth-related code must follow these patterns exactly.

**Sources:**
- `ADR-015-authentication.md` — managed auth provider, JWT issuance, role mapping (line 31), provider selection criteria
- `Service_Interface_Contracts.md` §1 — AuthZ / Tenant Policy: `check_access`, `get_tenant_context`, `enforce_row_filter` (lines 36-72)
- `Database_Schema_Specification.md` — `user_account` table (line 187): `user_id`, `tenant_id`, `email`, `role`, `auth_provider_id`
- `phase-0-foundations.mdc` — JWT middleware at `src/api/dependencies/auth.py` (line 51), tenant context via `SET app.current_tenant_id` (line 57)
- `Implementation_Tasks.md` — P0-T14 (FastAPI + JWT middleware), P0-T17 (auth provider integration)

---

## Authentication vs Authorization Boundary

**Authentication** (this spec): Proving who the user is. The managed auth provider handles login, password management, MFA, and JWT issuance. The platform validates the JWT and extracts the user identity.

**Authorization** (Service_Interface_Contracts.md §1): Determining what the user can do. The AuthZ service checks permissions against the user's role, tenant, client, and assessment scope.

The middleware performs authentication. It does not perform authorization. Authorization happens in the service layer via `check_access`.

---

## JWT Claims Schema

The JWT issued by the auth provider must contain these claims:

| Claim | Type | Source | Description |
|-------|------|--------|-------------|
| `sub` | string (UUID) | Auth provider | User ID — maps to `user_account.user_id` via `auth_provider_id` |
| `email` | string | Auth provider | User's email address |
| `iss` | string | Auth provider | Issuer URL (validated against `AUTH_ISSUER_URL` env var) |
| `aud` | string | Auth provider | Audience (validated against `AUTH_AUDIENCE` env var) |
| `exp` | int (Unix timestamp) | Auth provider | Token expiration |
| `iat` | int (Unix timestamp) | Auth provider | Token issued-at |

**Note on custom claims:** The auth provider's `sub` claim contains the provider-side user ID. The middleware resolves this to the platform's `user_account` record via the `auth_provider_id` column (`Database_Schema_Specification.md` line 193). Role and tenant_id are NOT in the JWT — they are looked up from the `user_account` table to prevent stale JWT claims from granting incorrect access.

---

## Middleware Flow

File: `src/api/dependencies/auth.py`

### Step-by-step flow for every authenticated request:

```
1. Extract `Authorization: Bearer <token>` header
2. Decode and validate JWT:
   - Verify signature against JWKS keys from `AUTH_JWKS_URL`
   - Verify `iss` matches `AUTH_ISSUER_URL`
   - Verify `aud` matches `AUTH_AUDIENCE`
   - Verify `exp` is in the future
3. Extract `sub` (provider user ID) from validated claims
4. Look up `user_account` by `auth_provider_id = sub`
   - If no match: return 401 Unauthorized
   - If `is_active = false`: return 403 Forbidden
5. Build `CurrentUser` object:
   - user_id (platform UUID)
   - tenant_id
   - email
   - role
   - display_name
6. Call AuthZ `get_tenant_context(user_id)` to build `TenantContext`:
   - tenant_id
   - accessible client_ids
   - role
   - scope restrictions
7. Set PostgreSQL session variable: `SET app.current_tenant_id = '<tenant_id>'`
   (enables RLS policies — phase-0-foundations.mdc line 57)
```

### FastAPI Dependency Chain

```python
async def get_current_user(
    authorization: str = Header(...),
    db: AsyncSession = Depends(get_db),
) -> CurrentUser:
    """Validates JWT, resolves platform user. Returns CurrentUser or raises 401/403."""

async def get_tenant_context(
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TenantContext:
    """Calls AuthZ get_tenant_context, sets RLS session var. Returns TenantContext."""

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Yields a SQLAlchemy async session from the connection pool."""
```

Every route that requires authentication uses `Depends(get_current_user)` or `Depends(get_tenant_context)`. Routes that need the full tenant scope (most routes) depend on `get_tenant_context` which transitively depends on `get_current_user`.

---

## Data Models

### `CurrentUser`

```python
class CurrentUser(BaseModel):
    user_id: UUID
    tenant_id: UUID
    email: str
    role: str
    display_name: str
```

Source fields: `user_account` table (`Database_Schema_Specification.md` lines 187-198)

### `TenantContext`

```python
class TenantContext(BaseModel):
    tenant_id: UUID
    client_ids: list[UUID]
    role: str
    scopes: list[str]
```

Source: `Database_Schema_Specification.md` line 192 — the DDL column is singular `text not null` (one role per user, not a list). The `tenant_id` and `client_ids` fields come from the tenant/user relationship. The `scopes` field is derived at runtime from the role value (not stored in the database). Note: `Service_Interface_Contracts.md` line 58 uses the plural "roles" in its parenthetical — the DDL (Priority 11) is authoritative.

---

## JWKS Key Caching

The middleware fetches the auth provider's JWKS (JSON Web Key Set) from `AUTH_JWKS_URL` to validate JWT signatures. Keys are cached in memory with a TTL of 1 hour. On signature validation failure, the middleware refreshes the JWKS cache once before returning 401.

---

## Token Expiry and Refresh

The platform does not handle token refresh. The auth provider manages refresh tokens. The client (frontend) is responsible for obtaining a new access token before the current one expires. If a request arrives with an expired JWT, the middleware returns 401 with code `token_expired`. The frontend then refreshes and retries.

---

## CORS Configuration

Source: `ADR-009-frontend-stack.md` — Next.js frontend at `frontend/` (line 51)

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

| Environment | `CORS_ALLOWED_ORIGINS` |
|-------------|----------------------|
| Local dev | `http://localhost:3000` |
| Staging | `https://staging.partners-platform.com` |
| Production | `https://app.partners-platform.com` |

---

## Error Responses from Middleware

| Condition | HTTP Status | Error Code | Message |
|-----------|-------------|------------|---------|
| Missing Authorization header | 401 | `missing_token` | Authorization header required |
| Malformed Bearer token | 401 | `invalid_token` | Invalid authorization header format |
| JWT signature invalid | 401 | `invalid_signature` | Token signature verification failed |
| JWT expired | 401 | `token_expired` | Token has expired |
| Issuer mismatch | 401 | `invalid_issuer` | Token issuer not recognized |
| Audience mismatch | 401 | `invalid_audience` | Token audience mismatch |
| User not found in platform | 401 | `user_not_found` | No platform account for this identity |
| User account deactivated | 403 | `account_deactivated` | User account is not active |

All middleware errors use the same `ErrorResponse` shape defined in `API_Design_Specification.md`.
