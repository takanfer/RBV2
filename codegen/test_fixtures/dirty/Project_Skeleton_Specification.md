# Project Skeleton Specification

## 1. Overview

Monorepo structure for the RBv2 platform.

## 2. Repository Structure

```
/
├── src/
│   ├── api/
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── ...                  # One module per domain
│   ├── services/
│   │   ├── data_ingestion/
│   │   │   ├── __init__.py
│   │   │   └── router.py
│   │   └── scoring_engine/
│   │       ├── __init__.py
│   │       └── router.py
│   └── shared/
│       └── models/
│           └── __init__.py
├── tests/
│   └── conftest.py
├── docker/
│   └── docker-compose.yml
└── docs/
    └── adrs/
```

## 3. Services

| # | Service | Directory |
|---|---------|-----------|
| 1 | Data Ingestion Service | `src/services/data_ingestion` |
| 2 | Scoring Engine Service | `src/services/scoring_engine` |
