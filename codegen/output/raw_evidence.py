"""Raw Evidence domain models — generated from Database_Schema_Specification.md DDL."""

from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class SourceSystem(BaseModel):
    """SourceSystem entity."""

    source_system_id: UUID
    tenant_id: UUID
    system_name: str
    system_type: str
    vendor_name: str | None = None
    api_base_url: str | None = None
    adapter_type: str
    configuration: dict[str, Any] = Field(default_factory=dict)
    is_active: bool = True
    created_at: datetime.datetime
    updated_at: datetime.datetime


class SourceIngestion(BaseModel):
    """SourceIngestion entity."""

    ingestion_id: UUID
    source_system_id: UUID
    assessment_id: UUID | None = None
    ingestion_type: str
    status: str
    file_count: int
    record_count: int | None = None
    idempotency_key: str | None = None
    started_at: datetime.datetime | None = None
    completed_at: datetime.datetime | None = None
    error_detail: dict[str, Any] | None = None
    created_at: datetime.datetime
    created_by: UUID | None = None


class SourceAsset(BaseModel):
    """SourceAsset entity."""

    asset_id: UUID
    ingestion_id: UUID
    asset_type: str
    original_filename: str | None = None
    mime_type: str | None = None
    file_size_bytes: int | None = None
    content_hash: str
    storage_path: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class SourceRecordRaw(BaseModel):
    """SourceRecordRaw entity."""

    record_id: UUID
    asset_id: UUID
    ingestion_id: UUID
    record_type: str
    source_row_number: int | None = None
    raw_data: dict[str, Any]
    mapping_status: str
    mapping_confidence: Decimal | None = None
    canonical_entity: str | None = None
    canonical_id: UUID | None = None
    created_at: datetime.datetime


class MappingRule(BaseModel):
    """MappingRule entity."""

    rule_id: UUID
    source_system_id: UUID
    source_record_type: str
    source_column: str
    target_table: str
    target_column: str
    transform_expr: str | None = None
    is_active: bool = True
    created_at: datetime.datetime
    created_by: UUID | None = None


class MappingReviewQueue(BaseModel):
    """MappingReviewQueue entity."""

    review_id: UUID
    ingestion_id: UUID
    record_id: UUID | None = None
    review_type: str
    description: str
    suggested_mapping: dict[str, Any] | None = None
    resolution: str | None = None
    resolved_by: UUID | None = None
    resolved_at: datetime.datetime | None = None
    created_at: datetime.datetime
