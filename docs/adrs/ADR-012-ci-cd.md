# ADR-012: GitHub Actions

**Status:** Accepted  
**Date:** 2026-04-04  
**Decides:** CI/CD platform

## Decision

GitHub Actions handles all continuous integration and deployment.

## Rationale

- Tightly integrated with GitHub (where the monorepo is hosted)
- Matrix builds for testing against multiple Python versions
- Docker layer caching for fast CI runs
- Marketplace actions for AWS deployment (ECS, S3, RDS migrations)
- Free tier sufficient for early development

## Implications

- Workflow files in `.github/workflows/`
- `ci.yml` — runs ruff, pytest (unit + integration) on every push
- `deploy.yml` — builds Docker images, runs migrations, deploys to ECS on merge to main
- Branch protection requires CI pass before merge
