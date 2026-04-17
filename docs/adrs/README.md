# Architecture Decision Records

This directory contains all locked technology and architecture decisions for the Multifamily Property Assessment Platform. Once an ADR is recorded, agents and developers must conform to it. ADRs are not modified after acceptance — if a decision is reversed, a new ADR supersedes the old one.

## Index

| ADR | Decision | Status |
|-----|----------|--------|
| [ADR-001](ADR-001-python-version.md) | Python 3.11+ | Accepted |
| [ADR-002](ADR-002-api-framework.md) | FastAPI | Accepted |
| [ADR-003](ADR-003-database-access.md) | SQLAlchemy Core + clickhouse-connect | Accepted |
| [ADR-004](ADR-004-schema-migrations.md) | Alembic | Accepted |
| [ADR-005](ADR-005-package-manager.md) | uv | Accepted |
| [ADR-006](ADR-006-testing.md) | pytest | Accepted |
| [ADR-007](ADR-007-linting-formatting.md) | ruff | Accepted |
| [ADR-008](ADR-008-local-development.md) | Docker Compose | Accepted |
| [ADR-009](ADR-009-frontend-stack.md) | Next.js + TypeScript + Tailwind + shadcn/ui | Accepted |
| [ADR-010](ADR-010-mobile-field-capture.md) | PWA | Accepted |
| [ADR-011](ADR-011-repository-structure.md) | Monorepo | Accepted |
| [ADR-012](ADR-012-ci-cd.md) | GitHub Actions | Accepted |
| [ADR-013](ADR-013-cloud-provider.md) | AWS (RDS, S3, ClickHouse Cloud, ECS) | Accepted |
| [ADR-014](ADR-014-task-queue.md) | Celery + Redis | Accepted |
| [ADR-015](ADR-015-authentication.md) | AWS Cognito (JWT) | Accepted |
| [ADR-016](ADR-016-report-rendering.md) | WeasyPrint + python-pptx | Accepted |
