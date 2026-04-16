# ADR-009: Next.js + TypeScript + Tailwind + shadcn/ui

**Status:** Accepted  
**Date:** 2026-04-04  
**Decides:** Frontend framework and component architecture

## Decision

| Layer | Technology |
|-------|-----------|
| Framework | Next.js (App Router) |
| Language | TypeScript (strict mode) |
| Styling | Tailwind CSS |
| Components | shadcn/ui |
| Data Tables | TanStack Table |
| Charts | Recharts (standard) / D3 (custom visualizations) |
| Data Fetching | TanStack Query |
| Forms | React Hook Form + Zod |

## Rationale

### Next.js
- Server-side rendering for client portal performance and SEO
- App Router for modern React Server Components
- API routes for BFF (backend-for-frontend) patterns when needed
- File-based routing for predictable URL structure

### TypeScript
- Non-negotiable at this complexity level — the platform has 12 scoring areas, 65 items, 315 sub-items, 1,100+ data fields across all sources. Type safety prevents drift between frontend and backend data shapes.

### Tailwind CSS + shadcn/ui
- Tailwind provides a consistent design system via utility classes
- shadcn/ui components are copied into the project (not a node_modules dependency) — fully customizable, no version lock-in

### TanStack Table + Recharts/D3
- The platform is data-dense: unit-day facts, lease intervals, scorecard drilldowns, comparison boards, finding graphs
- TanStack Table is the most capable React table library for sorting, filtering, pagination, and column management on large datasets
- Recharts handles standard scorecard visualizations; D3 handles custom visualizations like vacancy timelines and cohort distributions

### TanStack Query
- Caching and background refresh against FastAPI endpoints
- Optimistic updates for interactive workspace features
- Automatic refetching when assessment data changes

### React Hook Form + Zod
- Zod validation schemas mirror Pydantic models on the backend — same validation rules, both ends
- React Hook Form is performant for large forms (field capture, financial intake, audit workbook)

## Implications

- Frontend code lives in `frontend/` at repo root
- TypeScript types generated from FastAPI OpenAPI spec (or shared manually) to stay in sync with backend Pydantic models
- shadcn/ui components live in `frontend/src/components/ui/`
- No Material UI, no Ant Design, no Bootstrap
