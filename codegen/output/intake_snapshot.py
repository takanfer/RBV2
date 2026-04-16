"""Intake Snapshot domain models — generated from Database_Schema_Specification.md DDL."""

from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class TechPlatform(BaseModel):
    """TechPlatform entity."""

    platform_id: UUID
    property_id: UUID
    assessment_id: UUID | None = None
    platform_name: str
    annual_cost: Decimal | None = None
    staff_mobile_access: bool | None = None
    functions_handled: dict[str, Any] = Field(default_factory=dict)
    capabilities: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class TechSummary(BaseModel):
    """TechSummary entity."""

    summary_id: UUID
    property_id: UUID
    assessment_id: UUID | None = None
    total_annual_spend: Decimal | None = None
    spend_per_unit: Decimal | None = None
    active_integrations: int | None = None
    staff_mobile_access: bool | None = None
    resident_app: bool | None = None
    automation_level: str | None = None
    redundant_systems: str | None = None
    gaps_pain_points: str | None = None
    created_at: datetime.datetime


class StaffingSnapshot(BaseModel):
    """StaffingSnapshot entity."""

    snapshot_id: UUID
    property_id: UUID
    assessment_id: UUID | None = None
    data: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class LeasingModelSnapshot(BaseModel):
    """LeasingModelSnapshot entity."""

    snapshot_id: UUID
    property_id: UUID
    assessment_id: UUID | None = None
    data: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class ResidentEventProgram(BaseModel):
    """ResidentEventProgram entity."""

    program_id: UUID
    property_id: UUID
    assessment_id: UUID | None = None
    data: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class RenewalRetentionSnapshot(BaseModel):
    """RenewalRetentionSnapshot entity."""

    snapshot_id: UUID
    property_id: UUID
    assessment_id: UUID | None = None
    data: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class PartnershipReferralSnapshot(BaseModel):
    """PartnershipReferralSnapshot entity."""

    snapshot_id: UUID
    property_id: UUID
    assessment_id: UUID | None = None
    data: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime
