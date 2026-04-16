# Authorization Model Specification

Defines the authorization model for the RBv2 platform: the `check_access` function, role-based access control (RBAC) with hierarchical resource scoping, role definitions, and the `AccessDecision` type.

This document covers **authorization** (what can this user do?). For **authentication** (who is this user?), see `Authentication_Middleware_Specification.md`.

---

## Sources

- `Service_Interface_Contracts.md` lines 36–71 — AuthZ / Tenant Policy contract (`check_access`, `get_tenant_context`, `enforce_row_filter`)
- `Authentication_Middleware_Specification.md` — JWT middleware flow, `CurrentUser`, `TenantContext` types
- `Database_Schema_Specification.md` line 187–198 — `user_account` table (role enum: admin, consultant, analyst, client_viewer)
- `UI_UX_Specification.md` lines 16–22 — Role definitions and access scopes
- `spec_1` §16.1 (lines 1227–1233) — Tenant and data security: scopes, role-based permissions, row-level access, restricted marts
- `phase-0-foundations.mdc` lines 60–62 — RLS policies, tenant context via session variable

---

## 1. Resource Hierarchy

All platform resources exist within a strict containment hierarchy. Access granted at a higher level implies access to all resources below it.

```
Tenant (consultant organization)
  └── Client (property owner)
        └── Portfolio (group of properties)
              └── Property (single property)
                    └── Assessment (single assessment)
```

Source: `Service_Interface_Contracts.md` lines 63–69 (Security model scope levels).

**Hierarchy rules:**
- A Tenant contains one or more Clients.
- A Client contains zero or more Portfolios.
- A Portfolio contains one or more Properties. A Property may belong to exactly one Client (and optionally one Portfolio).
- An Assessment belongs to exactly one Property.
- A user belongs to exactly one Tenant.

---

## 2. Roles

Four roles are defined in the `user_account.role` column (DDL line 192):

| Role | Access Level | Portal | Description |
|------|-------------|--------|-------------|
| `admin` | Full platform administration | Consultant workspace | Tenant management, user management, all data within tenant |
| `consultant` | Full workspace access | Consultant workspace | All data within tenant/client scope, create assessments, run diagnostics, generate reports |
| `analyst` | Workspace access, potentially scoped | Consultant workspace | May be scoped to specific clients or assessments by admin assignment |
| `client_viewer` | Read-only, approved outputs only | Client portal | Can only see published/approved outputs for their client's properties |

Source: `UI_UX_Specification.md` lines 16–22, `Database_Schema_Specification.md` line 192.

**Role assignment:** Each user has exactly one role (the DDL column is `text not null`, singular). Role is stored in `user_account.role`, not in the JWT. The middleware looks up the role from the database on every request to prevent stale claims.

Source: `Authentication_Middleware_Specification.md` line 37.

---

## 3. Actions

Operations are grouped into standard action types:

| Action | Description |
|--------|-------------|
| `read` | View/retrieve a resource |
| `write` | Create or update a resource |
| `delete` | Remove a resource |
| `execute` | Trigger a computation (scoring run, report render, import) |
| `approve` | Publish/approve outputs for client visibility |
| `admin` | Administrative operations (user management, tenant config) |

---

## 4. Permission Matrix

| Action | `admin` | `consultant` | `analyst` | `client_viewer` |
|--------|---------|-------------|-----------|-----------------|
| `read` (any tenant resource) | Yes | Yes | Scoped | Client-only, approved |
| `write` (assessments, findings) | Yes | Yes | Scoped | No |
| `delete` (assessments, data) | Yes | Yes | No | No |
| `execute` (scoring, imports, reports) | Yes | Yes | Scoped | No |
| `approve` (publish to client portal) | Yes | Yes | No | No |
| `admin` (users, tenant config) | Yes | No | No | No |

**"Scoped" means:** the analyst's access is restricted to specific clients or assessments assigned by an admin. The scope is determined by the `TenantContext.client_ids` and `TenantContext.scopes` fields returned by `get_tenant_context`.

---

## 5. `check_access` Function

### Signature

```python
async def check_access(
    user_id: UUID,
    resource_type: str,
    resource_id: UUID,
    action: str,
) -> AccessDecision:
    """
    Determines whether the given user can perform the given action on the given resource.
    
    Args:
        user_id: The platform user ID (from user_account.user_id)
        resource_type: One of "tenant", "client", "portfolio", "property", "assessment"
        resource_id: The UUID of the specific resource
        action: One of "read", "write", "delete", "execute", "approve", "admin"
    
    Returns:
        AccessDecision with allow/deny and applicable scopes
    
    Raises:
        PermissionDenied: User does not have permission for this action on this resource
        TenantMismatch: Resource belongs to a different tenant than the user
    """
```

Source: `Service_Interface_Contracts.md` line 57.

### Decision Logic

```
FUNCTION check_access(user_id, resource_type, resource_id, action) -> AccessDecision:
    
    # 1. Load user and tenant context
    user = get_user_account(user_id)
    IF user IS NULL OR user.is_active == FALSE:
        RAISE PermissionDenied("User not found or inactive")
    
    # 2. Resolve the resource's tenant
    resource_tenant_id = resolve_tenant_for_resource(resource_type, resource_id)
    
    # 3. Tenant isolation check (FIRST — always enforced)
    IF user.tenant_id != resource_tenant_id:
        RAISE TenantMismatch("Resource belongs to a different tenant")
    
    # 4. Role-based permission check
    role = user.role
    
    IF role == "admin":
        # Admin can do everything within their tenant
        RETURN AccessDecision(allowed=TRUE, scopes=["*"])
    
    IF role == "consultant":
        # Consultant can do everything except admin actions
        IF action == "admin":
            RAISE PermissionDenied("Admin action requires admin role")
        RETURN AccessDecision(allowed=TRUE, scopes=["*"])
    
    IF role == "analyst":
        # Analyst cannot delete, approve, or admin
        IF action IN ("delete", "approve", "admin"):
            RAISE PermissionDenied(f"Analyst cannot perform {action}")
        
        # Analyst may be scoped to specific clients/assessments
        tenant_context = get_tenant_context(user_id)
        IF tenant_context.scopes:
            # Check if the resource is within the analyst's allowed scope
            IF NOT resource_within_scope(resource_type, resource_id, tenant_context):
                RAISE PermissionDenied("Resource outside analyst scope")
        
        RETURN AccessDecision(allowed=TRUE, scopes=tenant_context.client_ids)
    
    IF role == "client_viewer":
        # Client viewer can only read approved/published outputs
        IF action != "read":
            RAISE PermissionDenied("Client viewer can only read")
        
        # Must be for their client's properties
        tenant_context = get_tenant_context(user_id)
        IF NOT resource_within_scope(resource_type, resource_id, tenant_context):
            RAISE PermissionDenied("Resource not accessible to this client")
        
        # Additional filter: only approved outputs
        RETURN AccessDecision(allowed=TRUE, scopes=tenant_context.client_ids, filter="approved_only")
    
    RAISE PermissionDenied("Unknown role")
```

### Resource Scope Resolution

```
FUNCTION resource_within_scope(resource_type, resource_id, tenant_context) -> BOOL:
    # Walk up the hierarchy to find the client_id for this resource
    client_id = resolve_client_for_resource(resource_type, resource_id)
    
    IF client_id IS NULL:
        RETURN FALSE
    
    RETURN client_id IN tenant_context.client_ids
```

---

## 6. `AccessDecision` Type

```python
class AccessDecision(BaseModel):
    allowed: bool
    scopes: list[UUID]        # List of client_ids the user can access
    filter: str | None = None  # Optional filter flag (e.g., "approved_only" for client_viewer)
```

Source: `Service_Interface_Contracts.md` line 57 — `AccessDecision (allow/deny + scopes)`.

---

## 7. `get_tenant_context` Function

Returns the full authorization context for a user. Called by the auth middleware on every request.

```python
async def get_tenant_context(user_id: UUID) -> TenantContext:
    """
    Builds the tenant context for the given user.
    
    Returns:
        TenantContext with tenant_id, accessible client_ids, role, scopes
    
    Raises:
        UserNotFound: No user_account record for this user_id
        TenantSuspended: The user's tenant is suspended
    """
```

Source: `Service_Interface_Contracts.md` line 58.

### Construction Logic

```
FUNCTION get_tenant_context(user_id) -> TenantContext:
    user = get_user_account(user_id)
    IF user IS NULL:
        RAISE UserNotFound
    
    tenant = get_tenant(user.tenant_id)
    IF tenant.is_suspended:
        RAISE TenantSuspended
    
    # Determine accessible client_ids based on role
    IF user.role IN ("admin", "consultant"):
        # Full access to all clients within tenant
        client_ids = get_all_client_ids_for_tenant(user.tenant_id)
    ELIF user.role == "analyst":
        # Scoped to assigned clients (via user_client_assignment or similar)
        client_ids = get_assigned_client_ids(user.user_id)
    ELIF user.role == "client_viewer":
        # Scoped to their own client
        client_ids = get_client_ids_for_viewer(user.user_id)
    
    RETURN TenantContext(
        tenant_id=user.tenant_id,
        client_ids=client_ids,
        role=user.role,
        scopes=derive_scopes_from_role(user.role)
    )
```

---

## 8. `enforce_row_filter` Function

Generates a SQL filter clause for row-level security enforcement at the application layer.

```python
async def enforce_row_filter(
    tenant_context: TenantContext,
    table_name: str,
) -> str:
    """
    Returns a SQL WHERE clause fragment for tenant isolation.
    
    For most tables: WHERE tenant_id = :tenant_id
    For client_viewer: adds additional approval status filters
    
    Raises:
        InvalidScope: table_name not recognized or not tenant-scoped
    """
```

Source: `Service_Interface_Contracts.md` line 59.

**Note:** This is the application-layer complement to PostgreSQL RLS policies. Both exist: RLS provides defense-in-depth at the database level (via `SET app.current_tenant_id`), while `enforce_row_filter` provides the application-layer equivalent for ClickHouse queries (which does not support RLS).

---

## 9. Client Portal Access Rules

For `client_viewer` role, additional restrictions apply beyond RBAC:

1. **Approved outputs only.** The client portal only shows outputs where `status = 'published'` or equivalent approval flag.
2. **No draft data.** Consultant working notes, draft hypotheses, and unapproved scores are never visible.
3. **No PII exposure.** PII masking is applied per tenant policy on all portal responses.
4. **Limited explore.** Only pre-approved filters and comparisons — no raw SQL, no unrestricted pivots.

Source: `spec_1` §16.1 lines 1227–1233 (restricted marts for client access), `UI_UX_Specification.md` line 22 ("Read-only access to approved outputs only").

---

## 10. Service Account / Admin Bypass

For system-level operations (migrations, background tasks, scheduled jobs), a service account pattern is used:

- Service accounts do not go through the JWT middleware.
- Service accounts set the PostgreSQL session variable for tenant context explicitly for each operation (via `SET app.current_tenant_id`).
- Service accounts are identified by a shared secret or internal token, not a user JWT.
- RLS bypass for service accounts: use a PostgreSQL role that has `BYPASSRLS` or set a session variable that RLS policies recognize as a service context.

---

## Authoritative Sources

- `Service_Interface_Contracts.md` — AuthZ contract (lines 36–71)
- `Authentication_Middleware_Specification.md` — Middleware flow and data types
- `Database_Schema_Specification.md` — `user_account` DDL (lines 187–198)
- `UI_UX_Specification.md` — Role definitions (lines 16–22)
- `spec_1` §16.1 — Security model (lines 1227–1233)
