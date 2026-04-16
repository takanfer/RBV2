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


class Building(BaseModel):
    """Building entity."""

    building_id: UUID
    property_id: UUID
    parent_building_id: UUID | None = None
    building_label: str
    building_type: str | None = None
    stories: int | None = None
    unit_count: int | None = None
    has_elevator: bool | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class FloorPlan(BaseModel):
    """FloorPlan entity."""

    floor_plan_id: UUID
    property_id: UUID
    plan_code: str
    plan_name: str | None = None
    bedrooms: Decimal
    bathrooms: Decimal
    sqft: int | None = None
    base_market_rent: Decimal | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


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


class UnitExistenceInterval(BaseModel):
    """UnitExistenceInterval entity."""

    interval_id: UUID
    unit_id: UUID
    valid_from: datetime.date
    valid_to: datetime.date | None = None
    existence_status: str
    rentable_flag: bool
    reason_code: str | None = None
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


class CalendarDay(BaseModel):
    """CalendarDay entity."""

    day_date: datetime.date
    day_of_week: int
    day_of_month: int
    day_of_year: int
    week_of_year: int
    month: int
    quarter: int
    year: int
    is_weekend: bool
    is_month_end: bool


class PropertyAmenity(BaseModel):
    """PropertyAmenity entity."""

    amenity_id: UUID
    property_id: UUID
    assessment_id: UUID | None = None
    amenity_category: str
    amenity_name: str
    is_present: bool | None = None
    source: str | None = None
    verification: str | None = None
    created_at: datetime.datetime


class UnitAmenity(BaseModel):
    """UnitAmenity entity."""

    amenity_id: UUID
    property_id: UUID
    assessment_id: UUID | None = None
    amenity_category: str
    amenity_name: str
    is_present: bool | None = None
    source: str | None = None
    verification: str | None = None
    created_at: datetime.datetime


class MarketContext(BaseModel):
    """MarketContext entity."""

    context_id: UUID
    property_id: UUID
    assessment_id: UUID | None = None
    submarket_name: str | None = None
    submarket_vacancy_pct: Decimal | None = None
    submarket_avg_rent_psf: Decimal | None = None
    yoy_rent_growth_pct: Decimal | None = None
    new_supply_units: int | None = None
    employment_growth_pct: Decimal | None = None
    population_growth_pct: Decimal | None = None
    median_household_income: Decimal | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime
