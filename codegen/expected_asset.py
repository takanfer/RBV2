"""Asset domain models — generated from Database_Schema_Specification.md DDL."""

from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class Property(BaseModel):
    """Property entity."""

    property_id: UUID
    tenant_id: UUID
    client_id: UUID | None = None
    portfolio_id: UUID | None = None
    property_name: str
    street_address: str
    city: str
    state: str
    zip_code: str
    total_units: int | None = None
    year_built: int | None = None
    property_class: str | None = None
    building_type: str | None = None
    buildings_count: int | None = None
    stories: int | None = None
    total_sqft: int | None = None
    lot_size: str | None = None
    parking_spaces: int | None = None
    parking_type: str | None = None
    is_subject: bool = True
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime
    updated_at: datetime.datetime


class Unit(BaseModel):
    """Unit entity."""

    unit_id: UUID
    property_id: UUID
    unit_natural_key: str
    created_at: datetime.datetime
    retired_at: datetime.datetime | None = None


class UnitVersion(BaseModel):
    """UnitVersion entity."""

    unit_version_id: UUID
    unit_id: UUID
    valid_from: datetime.date
    valid_to: datetime.date | None = None
    building_id: UUID | None = None
    floor_plan_id: UUID | None = None
    floor_label: str | None = None
    unit_label: str
    floorplan_code: str | None = None
    bedrooms: Decimal | None = None
    bathrooms: Decimal | None = None
    sqft: int | None = None
    finish_package: str | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    recorded_from: datetime.datetime
    recorded_to: datetime.datetime | None = None


class UnitAlias(BaseModel):
    """UnitAlias entity."""

    alias_id: UUID
    unit_id: UUID
    source_system_id: UUID | None = None
    alias_key: str
    alias_type: str
    valid_from: datetime.date | None = None
    valid_to: datetime.date | None = None
    match_method: str | None = None
    match_confidence: Decimal | None = None
    reviewer_override: bool = False
    created_at: datetime.datetime
