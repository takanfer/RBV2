# ADR-010: PWA for Mobile Field Capture

**Status:** Accepted  
**Date:** 2026-04-04  
**Decides:** Mobile strategy for field auditors

## Decision

Mobile field capture (mystery shops, unit walks, site observations) uses a Progressive Web App (PWA) built from the same Next.js application with offline-capable service workers.

## Rationale

- One codebase serves consultant laptop and auditor mobile device
- Service workers enable offline data capture — field observations are stored locally and synced when connectivity returns
- Installable on iOS and Android home screens without app store distribution
- No separate React Native codebase to maintain
- Field capture forms use the same React Hook Form + Zod validation as the desktop workspace

## Future Option

If native mobile capabilities are needed later (camera hardware access, background GPS, push notifications beyond PWA scope), React Native shares the same TypeScript/React component patterns and can be added without rewriting.
