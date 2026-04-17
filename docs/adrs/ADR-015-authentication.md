# ADR-015: AWS Cognito Authentication

**Status:** Accepted  
**Date:** 2026-04-16 (updated from 2026-04-12)  
**Decides:** User authentication mechanism (how users prove their identity)

## Decision

AWS Cognito handles user login, registration, password management, MFA, and JWT issuance. The platform's AuthZ service consumes the authenticated identity (JWT) and enforces authorization (who can access what).

## What This Solves

The AuthZ / Tenant Policy service (Service_Interface_Contracts.md §1) defines *authorization* — checking what an authenticated user is allowed to do. But it requires a verified user identity as input. This ADR fills the gap: how does the user prove who they are before AuthZ can check their permissions?

## Architecture

```
User → AWS Cognito (login/MFA) → JWT issued → API receives JWT →
  FastAPI middleware validates JWT → extracts user_id →
  AuthZ service checks permissions for that user_id
```

## Provider Selection

AWS Cognito was selected based on the following evaluation:

| Criterion | Requirement | Cognito |
|-----------|-------------|---------|
| JWT issuance | Must issue standard JWTs with `sub` (user ID), `email`, custom claims | Yes — Cognito ID tokens contain `sub`, `email`, and support custom attributes |
| Multi-tenant support | Must support organization/tenant scoping | Yes — custom attributes or groups per User Pool |
| Role mapping | Must allow custom roles matching `user_account.role` enum (`admin`, `consultant`, `analyst`, `client_viewer`) | Yes — Cognito groups map to roles |
| MFA | Must support TOTP or similar second factor | Yes — TOTP and SMS MFA built-in |
| Social/SSO | Should support Google, Microsoft for enterprise clients | Yes — federation with external IdPs |
| Self-service | Must provide password reset, email verification | Yes — hosted UI or custom UI with Cognito APIs |

**Rationale for Cognito over alternatives (Auth0, Clerk, Supabase Auth):**
- All infrastructure is AWS (ADR-013). Cognito keeps the vendor footprint minimal — one cloud provider for everything.
- Native IAM integration for backend service-to-service auth if needed in the future.
- No additional vendor contract or billing relationship.
- Cognito pricing scales with usage (first 50,000 MAU free tier).

## Key Patterns

- The `user_account` table in PostgreSQL stores the platform-side user profile (role, tenant_id, scope). Cognito stores credentials (password hash, MFA keys).
- The `user_account.auth_provider_id` field links the local record to the Cognito `sub` (user ID in the User Pool).
- FastAPI middleware validates the Cognito-issued JWT on every request, extracts the user identity, and passes it to the AuthZ service's `get_tenant_context` operation.
- No passwords or credentials are stored in the platform's database.
- JWKS URL follows the Cognito format: `https://cognito-idp.{region}.amazonaws.com/{userPoolId}/.well-known/jwks.json`

## Implications

- `pyproject.toml` adds `boto3` (Cognito admin operations) and `python-jose[cryptography]` (JWT validation with JWKS)
- FastAPI dependency (`src/api/dependencies/auth.py`) validates Cognito JWTs and extracts user identity
- `user_account` table needs an `auth_provider_id` column (verify against DDL during implementation)
- Environment variables: `COGNITO_USER_POOL_ID`, `COGNITO_REGION`, `COGNITO_APP_CLIENT_ID`
- No login/registration endpoints in the platform API — Cognito hosted UI or client-side SDK handles those
- Client portal and consultant workspace both authenticate through the same Cognito User Pool, distinguished by role (Cognito groups)
