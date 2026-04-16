# Shared Type Definitions

**Total models:** 5
**Total fields:** 30

## evidence

### SourceAsset

- source_asset_id: UUID
- tenant_id: UUID
- file_name: str
- mime_type: str | None
- created_at: datetime
- updated_at: datetime

## tenancy

### Property

- property_id: UUID
- tenant_id: UUID
- name: str
- address: str | None
- unit_count: int | None
- valid_from: datetime
- valid_to: datetime
- created_at: datetime
- updated_at: datetime

### UserAccount

- user_account_id: UUID
- tenant_id: UUID
- email: str
- role: str
- created_at: datetime
- updated_at: datetime

## analytics

### FactUnitDay

- property_id: str
- unit_id: str
- day: date
- status: str
- rent: float | None

### FactScoreSnapshot

- property_id: str
- snapshot_date: date
- area_id: int
- score: float
