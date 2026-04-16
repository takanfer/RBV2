# Service Interface Contracts

## 1. Data Ingestion Service

**Phase:** 0
**Directory:** `src/services/data_ingestion`

| `Operation` | Input | Output |
|---|---|---|
| `create_ingestion` | IngestionRequest | Ingestion |
| `get_ingestion_status` | uuid | IngestionStatus |
| `list_ingestion_jobs` | ListFilter | list[Ingestion] |

## 2. Scoring Engine Service

**Phase:** 1
**Directory:** `src/services/scoring_engine`

| `Operation` | Input | Output |
|---|---|---|
| `compute_scores` | ScoreRequest | ScoreResult |
| `get_score_snapshot` | uuid | ScoreSnapshot |
| `list_score_history` | HistoryFilter | list[ScoreSnapshot] |
