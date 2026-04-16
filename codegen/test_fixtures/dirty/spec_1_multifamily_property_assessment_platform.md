# Multifamily Property Assessment Platform

## §1 Platform Overview

This document defines requirements for the multifamily property assessment platform.

### §1.1 Data Collection

**M1.** The platform shall ingest data from property management systems.

**M2.** The platform shall support multiple data formats.

### §1.2 Core Domain

**M3.** The platform shall maintain a canonical property model.

## §2 Analytical Engine

### §2.1 Scoring

**S1.** The scoring engine shall compute weighted area scores.

**S2.** The scoring engine shall handle missing data gracefully.

## §3 Deployment

### §3.1 Infrastructure

The platform deploys on AWS using FastAPI and PostgreSQL.
