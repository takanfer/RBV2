# ADR-015: Managed Authentication Provider

**Status:** Accepted  
**Date:** 2026-04-12  
**Decides:** User authentication mechanism (how users prove their identity)

## Decision

A managed authentication provider handles user login, registration, password management, and token issuance. The platform's AuthZ service consumes the authenticated identity (JWT) and enforces authorization (who can access what).

## What This Solves

The AuthZ / Tenant Policy service (Service_Interface_Contracts.md §1) defines *authorization* — checking what an authenticated user is allowed to do. But it requires a verified user identity as input. This ADR fills the gap: how does the user prove who they are before AuthZ can check their permissions?

## Architecture

```
User → Auth Provider (login/MFA) → JWT issued → API receives JWT →
  FastAPI middleware validates JWT → extracts user_id →
  AuthZ service checks permissions for that user_id
```

## Provider Selection

The specific provider (Auth0, Clerk, AWS Cognito, Supabase Auth, or equivalent) will be selected during Phase 0 implementation based on:

| Criterion | Requirement |
|-----------|-------------|
| JWT issuance | Must issue standard JWTs with `sub` (user ID), `email`, custom claims |
| Multi-tenant support | Must support organization/tenant scoping |
| Role mapping | Must allow custom roles matching `user_account.role` enum (`admin`, `consultant`, `analyst`, `client_viewer`) |
| MFA | Must support TOTP or similar second factor |
| Social/SSO | Should support Google, Microsoft for enterprise clients |
| Self-service | Must provide password reset, email verification |

## Key Patterns

- The `user_account` table in PostgreSQL stores the platform-side user profile (role, tenant_id, scope). The auth provider stores credentials (password hash, MFA keys).
- The `user_account.auth_provider_id` field links the local record to the provider's user ID.
- FastAPI middleware validates the JWT on every request, extracts the user identity, and passes it to the AuthZ service's `get_tenant_context` operation.
- No passwords or credentials are stored in the platform's database.

## Rationale

- **Why not self-hosted auth:** Authentication is security-critical (password hashing, brute-force protection, token rotation, MFA). Building it correctly is substantial work unrelated to the platform's core value. Managed providers handle this at scale.
- **Why deferred provider selection:** Auth0, Clerk, and Cognito all meet the requirements. The exact choice depends on pricing at scale and integration experience during Phase 0. The JWT interface is the same regardless.

## Implications

- `pyproject.toml` adds `python-jose` or `pyjwt` for JWT validation
- FastAPI dependency (`src/api/dependencies/auth.py`) validates JWTs and extracts user identity
- `user_account` table needs an `auth_provider_id` column (verify against DDL during implementation)
- `.env` includes auth provider configuration (issuer URL, audience, client ID)
- No login/registration endpoints in the platform API — the auth provider handles those
- Client portal and consultant workspace both authenticate through the same provider, distinguished by role
