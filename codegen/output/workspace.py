"""Workspace domain models — generated from Database_Schema_Specification.md DDL."""

from __future__ import annotations

import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class Study(BaseModel):
    """Study entity."""

    study_id: UUID
    assessment_id: UUID
    study_name: str
    description: str | None = None
    created_by: UUID | None = None
    created_at: datetime.datetime
    updated_at: datetime.datetime


class SavedQuery(BaseModel):
    """SavedQuery entity."""

    query_id: UUID
    assessment_id: UUID | None = None
    study_id: UUID | None = None
    query_name: str
    query_definition: dict[str, Any]
    parameters: dict[str, Any] = Field(default_factory=dict)
    filters: dict[str, Any] = Field(default_factory=dict)
    chart_spec: dict[str, Any] | None = None
    created_by: UUID | None = None
    created_at: datetime.datetime


class ResultSnapshot(BaseModel):
    """ResultSnapshot entity."""

    snapshot_id: UUID
    saved_query_id: UUID | None = None
    assessment_id: UUID | None = None
    study_id: UUID | None = None
    source_data_version: str | None = None
    transformation_version: str | None = None
    rule_package_version: str | None = None
    benchmark_version: str | None = None
    result_payload: dict[str, Any]
    chart_spec: dict[str, Any] | None = None
    sql_definition: str | None = None
    filters: dict[str, Any] = Field(default_factory=dict)
    data_hash: str | None = None
    created_by: UUID | None = None
    created_at: datetime.datetime


class StudyItem(BaseModel):
    """StudyItem entity."""

    item_id: UUID
    study_id: UUID
    item_type: str
    ref_id: UUID
    sort_order: int | None = None
    created_at: datetime.datetime


class ComparisonBoard(BaseModel):
    """ComparisonBoard entity."""

    board_id: UUID
    study_id: UUID | None = None
    assessment_id: UUID | None = None
    board_name: str
    layout: dict[str, Any] = Field(default_factory=dict)
    created_by: UUID | None = None
    created_at: datetime.datetime


class Annotation(BaseModel):
    """Annotation entity."""

    annotation_id: UUID
    entity_type: str
    entity_id: UUID
    note_text: str
    created_by: UUID | None = None
    created_at: datetime.datetime
    updated_at: datetime.datetime


class EvidenceBundle(BaseModel):
    """EvidenceBundle entity."""

    bundle_id: UUID
    assessment_id: UUID
    bundle_name: str
    item_refs: dict[str, Any] = Field(default_factory=dict)
    created_by: UUID | None = None
    created_at: datetime.datetime
